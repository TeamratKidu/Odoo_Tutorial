
from typing import override

from odoo import models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = "estate.property"

    @override
    def action_sold(self):
        res = super().action_sold()
        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.name,
                'quantity': 1,
                'price_unit': self.selling_price,
            })],
        })

        print(f"Invoice created for property {self.name} sold to {self.buyer_id.name} with selling price {self.selling_price}.")
        return res

    