from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer Price must be greater than 0."
    )


    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - date).days

    def action_accept(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True


    
    @api.model
    def create(self, vals):
        if "price" in vals and "property_id" in vals:
            property = self.env["estate.property"].browse(vals["property_id"])
            if vals["price"] <= property.best_price:
                raise UserError("Offer price must be higher than the current best offer.")
        offers = super().create(vals)
        offers.property_id.state = "offer_received"
        return offers

