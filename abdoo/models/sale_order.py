# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            for line in order.order_line:
                product = line.product_id
                if product.is_storable:
                    available = product.qty_available
                    needed = line.product_uom_qty
                    if available < needed:
                        raise UserError(
                            f"Stock insuffisant pour '{product.display_name}' : "
                            f"disponible {available:.2f}, requis {needed:.2f}."
                        )
        return super().action_confirm()
