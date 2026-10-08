
from typing import override

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"  # What is the difference between underscore and dot?

    name = fields.Char(string="Property Name", required=True, default="Unknown")
    description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postcode", index=True)
    date_availability = fields.Date(
        string="Date Available",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)  # Why required vs nullable?
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)  # What does copy do?
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        help="Orientation of the garden. This field is optional.",
    )  # Should selection values be capitalized?
    active = fields.Boolean(string="Active", default=True)
    last_seen = fields.Datetime(string="Last Seen", default=fields.Datetime.now, copy=False)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="new",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )


    # sql constraints

    _check_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)",
        "Expected price must be a positive number."
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "Selling price must be a positive number."
    )



    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0


    @api.onchange("garden")
    def _onchange_garden(self):
        # Onchange in estate.property form view
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_method(self):
        for record in self:
            if float_compare(record.selling_price, 0, precision_digits=2) > 0 and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise UserError("Selling price cannot be lower than 90% of the expected price.")
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_sold(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError("Only new or cancelled properties can be deleted.")

    # @override
    # def action_sold(self):
    #     setted = super().action_sold();
    #     for record in self:
    #         if record.state == "offer_accepted":
    #             record.status = "refused"
    #     return setted
        