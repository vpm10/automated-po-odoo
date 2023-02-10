from odoo import fields, models


class AutoPurchaseOrder(models.Model):
    _inherit = 'product.template'

    product_variant_id = fields.Many2one('product.product',
                                         string='Product variant')

    def action_to_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'po.wizard',
            'target': 'new',
            'context': {
                'default_price': self.list_price,
                'default_product_name_id': self.id,
                'default_product_product_id': self.product_variant_id.id
            }

        }
