

from odoo import fields, models
from dateutil.relativedelta import relativedelta




class estate_property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property" # what if it was an underscore instead of a dot? What is the difference between underscore and dot in this context?

    name = fields.Char(string="Property Name", required=True, default="Unknown")
    description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postcode", index=True)
    date_availability = fields.Date(string="Date Available", default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True) # not nullable how and why is this field required? What is the difference between required and nullable?
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False) # what is the difference between readonly and copy? What does copy do?
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        help="Orientation of the garden. This field is optional and can be left empty if the property does not have a garden."
    ) # why is there a case sensitivity issue with the selection values? Should they be capitalized or not?
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
