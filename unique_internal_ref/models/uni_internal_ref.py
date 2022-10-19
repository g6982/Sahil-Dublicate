from odoo import api, fields, models


class UniqueInternalRef(models.Model):
    _inherit = "product.product"

    _sql_constraints = [
        ('default_code_uniq', 'unique(default_code)', "A Internal Reference can only be assigned to one product !"),
    ]
