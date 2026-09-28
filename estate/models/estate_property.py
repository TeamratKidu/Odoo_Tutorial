

from odoo import fields, models


class estate_property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property" # what if it was an underscore instead of a dot? What is the difference between underscore and dot in this context?

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postcode", index=True)
    date_availability = fields.Date(string="Date Available", default=fields.Date.today)
    expected_price = fields.Float(string="Expected Price", required=True) # not nullable how and why is this field required? What is the difference between required and nullable?
    selling_price = fields.Float(string="Selling Price", readonly=True)
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
