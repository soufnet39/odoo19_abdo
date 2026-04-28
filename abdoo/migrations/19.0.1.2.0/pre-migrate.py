def migrate(cr, version):
    """Delete the orphan header-button view so view validation passes during upgrade."""
    cr.execute("""
        DELETE FROM ir_ui_view
        WHERE name = 'product.template.view.list.abdoo.print'
    """)
