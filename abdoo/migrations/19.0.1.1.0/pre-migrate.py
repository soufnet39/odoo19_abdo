def migrate(cr, version):
    """Drop the old Many2one column so Odoo can create the Many2many relation table."""
    cr.execute("""
        ALTER TABLE product_template
        DROP COLUMN IF EXISTS maison
    """)
