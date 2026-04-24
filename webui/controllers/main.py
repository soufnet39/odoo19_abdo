# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.fields import Domain
from odoo.http import request

_logger = logging.getLogger(__name__)

# Custom filter URL parameter names
_CUSTOM_FILTER_PARAMS = [
    'filter_type',
    'age',
    'carburant',
    'maison',
    'moteur',
    'moteur_type',
    'filter_marque',
]

# Fields whose values are integers (Many2one record IDs)
_M2O_PARAMS = {'maison', 'moteur', 'moteur_type', 'filter_marque'}


class WebsiteSaleWebUI(WebsiteSale):

    def _webui_get_filter_params(self):
        """Parse custom filter values from the current request."""
        args = request.httprequest.args
        result = {}
        for param in _CUSTOM_FILTER_PARAMS:
            raw = args.getlist(param)
            if param in _M2O_PARAMS:
                result[param] = [int(v) for v in raw if v.isdigit()]
            else:
                result[param] = raw
        return result

    def _webui_build_domain(self, filter_params):
        """Return an ORM Domain if any custom filters are active, else None."""
        domains = []
        for param in _CUSTOM_FILTER_PARAMS:
            values = filter_params.get(param)
            if values:
                domains.append(Domain(param, 'in', values))
        return Domain.AND(domains) if domains else None

    def _shop_lookup_products(self, options, post, search, website):
        """Apply custom abdoo filters on top of the standard product search."""
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(
            options, post, search, website
        )
        try:
            filter_params = self._webui_get_filter_params()
            extra_domain = self._webui_build_domain(filter_params)
            if extra_domain is not None:
                search_result = search_result.filtered_domain(list(extra_domain))
                product_count = len(search_result)
        except Exception:
            _logger.exception("webui: error applying custom filters")
        return fuzzy_search_term, product_count, search_result

    def _shop_get_query_url_kwargs(self, search, min_price, max_price, order=None, tags=None, **kwargs):
        result = super()._shop_get_query_url_kwargs(
            search, min_price, max_price, order=order, tags=tags, **kwargs
        )
        try:
            filter_params = self._webui_get_filter_params()
            for param in _CUSTOM_FILTER_PARAMS:
                values = filter_params.get(param)
                if values:
                    result[param] = values
        except Exception:
            _logger.exception("webui: error building query URL kwargs")
        return result

    def _get_additional_shop_values(self, values, **kwargs):
        result = super()._get_additional_shop_values(values, **kwargs)
        try:
            env = request.env
            filter_params = self._webui_get_filter_params()
            keep = values['keep']

            def toggle_url(param, value):
                current = list(filter_params.get(param, []))
                if param in _M2O_PARAMS:
                    value = int(value)
                if value in current:
                    current.remove(value)
                else:
                    current.append(value)
                return keep(**{param: current or 0})

            clear_kwargs = {p: 0 for p in _CUSTOM_FILTER_PARAMS}
            webui_clear_url = keep(**clear_kwargs) if any(filter_params.values()) else None

            # Use the public fields_get API — safer than accessing ._fields directly
            pt = env['product.template'].sudo()
            selection_fields = pt.fields_get(['filter_type', 'age', 'carburant'])

            result.update({
                'webui_filter_params': filter_params,
                'webui_toggle_url': toggle_url,
                'webui_clear_url': webui_clear_url,
                'webui_filter_type_options': selection_fields.get('filter_type', {}).get('selection', []),
                'webui_age_options': selection_fields.get('age', {}).get('selection', []),
                'webui_carburant_options': selection_fields.get('carburant', {}).get('selection', []),
                'webui_maison_options': env['maison.marques'].sudo().search([]),
                'webui_moteur_options': env['motors'].sudo().search([]),
                'webui_moteur_type_options': env['motor.types'].sudo().search([]),
                'webui_filter_marque_options': env['filter.marques'].sudo().search([]),
            })
        except Exception:
            _logger.exception("webui: error building shop filter values")
        return result

    @http.route('/shop/cart/order-request', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def cart_order_request(self, name='', phone='', email='', notes='', **kwargs):
        """Receive the Order Now form, send an email with cart contents, redirect."""
        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        notes = notes.strip()

        if not name or not phone:
            return request.redirect('/shop/cart?order_error=1')

        order = request.cart
        if not order or not order.website_order_line:
            return request.redirect('/shop/cart')

        # Build HTML list of cart items (no prices — consistent with site policy)
        lines_html = ''.join(
            f'<li>{line.product_id.display_name} &times; {int(line.product_uom_qty)}</li>'
            for line in order.website_order_line
        )

        body_html = f"""
            <p><strong>Nom :</strong> {name}</p>
            <p><strong>Téléphone :</strong> {phone}</p>
            {'<p><strong>Email :</strong> ' + email + '</p>' if email else ''}
            <h4 style="margin-top:16px;">Produits demandés :</h4>
            <ul>{lines_html}</ul>
            {'<p><strong>Notes :</strong> ' + notes + '</p>' if notes else ''}
        """

        company = request.env.company
        recipient = company.email
        if not recipient:
            _logger.warning("webui order-request: company has no email configured")
            return request.redirect('/shop/cart?order_sent=1')

        request.env['mail.mail'].sudo().create({
            'subject': f'Nouvelle demande de commande — {name}',
            'email_from': company.email,
            'reply_to': email or company.email,
            'email_to': recipient,
            'body_html': body_html,
        }).send()

        return request.redirect('/shop/cart?order_sent=1')
