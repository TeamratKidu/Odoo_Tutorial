
from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"


    property_ids = fields.One2many("estate.property", "salesperson_id", string="Properties", domain = [("state", "in", ["new", "offer_received"])])

    @api.model
    def create(self, vals):
        user = super().create(vals)
        if user.has_group("estate.group_estate_manager"):
            user.partner_id.is_company = True
        return user