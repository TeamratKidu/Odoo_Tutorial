from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    sequence = fields.Integer(string="Sequence", default=10)
    name = fields.Char(string="Name", required=True)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Number of Offers", compute="_compute_offer_count")


    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    
