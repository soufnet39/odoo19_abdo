# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestProductNameSearch(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.marque = cls.env['filter.marques'].create({'name': 'FilterBrand'})
        cls.moteur = cls.env['motors'].create({'name': 'V8Engine'})
        cls.moteur_type = cls.env['motor.types'].create({'name': 'TurboType'})

        cls.product = cls.env['product.template'].create({
            'name': 'HuileFilter',
            'filter_marque': cls.marque.id,
            'filter_type': 'huile',
            'age': 'N',
            'carburant': 'D',
            'moteur': cls.moteur.id,
            'moteur_type': cls.moteur_type.id,
        })

    def _search_tmpl(self, term):
        ids = {r[0] for r in self.env['product.template'].name_search(term, operator='ilike')}
        return self.env['product.template'].browse(list(ids))

    def _search_prod(self, term):
        ids = {r[0] for r in self.env['product.product'].name_search(term, operator='ilike')}
        return self.env['product.product'].browse(list(ids))

    # --- product.template tests ---

    def test_tmpl_search_by_name(self):
        self.assertIn(self.product, self._search_tmpl('HuileFilter'))

    def test_tmpl_search_by_filter_marque(self):
        self.assertIn(self.product, self._search_tmpl('FilterBrand'))

    def test_tmpl_search_by_filter_type_label(self):
        self.assertIn(self.product, self._search_tmpl('huile'))

    def test_tmpl_search_by_age_label(self):
        self.assertIn(self.product, self._search_tmpl('Nouveau'))

    def test_tmpl_search_by_carburant_label(self):
        self.assertIn(self.product, self._search_tmpl('Diesel'))

    def test_tmpl_search_by_moteur(self):
        self.assertIn(self.product, self._search_tmpl('V8Engine'))

    def test_tmpl_search_by_moteur_type(self):
        self.assertIn(self.product, self._search_tmpl('TurboType'))

    def test_tmpl_no_match(self):
        self.assertNotIn(self.product, self._search_tmpl('ZZZNOMATCH'))

    # --- product.product tests ---

    def test_prod_search_by_name(self):
        variant = self.product.product_variant_ids[:1]
        self.assertIn(variant, self._search_prod('HuileFilter'))

    def test_prod_search_by_filter_marque(self):
        variant = self.product.product_variant_ids[:1]
        self.assertIn(variant, self._search_prod('FilterBrand'))

    def test_prod_search_by_age_label(self):
        variant = self.product.product_variant_ids[:1]
        self.assertIn(variant, self._search_prod('Nouveau'))

    def test_prod_search_by_carburant_label(self):
        variant = self.product.product_variant_ids[:1]
        self.assertIn(variant, self._search_prod('Diesel'))

    def test_prod_search_by_moteur(self):
        variant = self.product.product_variant_ids[:1]
        self.assertIn(variant, self._search_prod('V8Engine'))

    def test_prod_search_by_moteur_type(self):
        variant = self.product.product_variant_ids[:1]
        self.assertIn(variant, self._search_prod('TurboType'))

    def test_prod_no_match(self):
        variant = self.product.product_variant_ids[:1]
        self.assertNotIn(variant, self._search_prod('ZZZNOMATCH'))
