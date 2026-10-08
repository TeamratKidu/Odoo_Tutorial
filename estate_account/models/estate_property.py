
from typing import override

from odoo import Command, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = "estate.property"

    @override
    def action_sold(self):
        # Keep the original checks and state change before creating invoices.
        res = super().action_sold()

        for property_record in self:
            # Each Command.create adds a new line to the invoice being created.
            self.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": property_record.buyer_id.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": f"Commission for {property_record.name}",
                                "quantity": 1,
                                "price_unit": property_record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": f"Administrative fees for {property_record.name}",
                                "quantity": 1,
                                "price_unit": 100.00,
                            }
                        ),
                    ],
                }
            )

        return res

    