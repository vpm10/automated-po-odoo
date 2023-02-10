from odoo import fields, models
from odoo.exceptions import ValidationError


class OrderTransientModel(models.TransientModel):
    _name = 'po.wizard'
    _description = 'PO wizard'

    quantity = fields.Integer(default=1, string='Quantity')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self:
                                 self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self:
                                  self.env.user.company_id.currency_id.id)
    price = fields.Monetary(string='Price')
    product_name_id = fields.Many2one('product.template', string='Product')
    product_product_id = fields.Many2one('product.product',
                                         string='Choose the variant',
                                         domain="[('product_tmpl_id', '=', "
                                                "product_name_id)]")

    def action_to_confirm(self):
        if len(self.product_name_id.seller_ids.partner_id) == 0:
            raise ValidationError('Please add a vendor')
        purchase_order = self.env['purchase.order'].search(
            [('partner_id.id', '=', self.product_name_id.seller_ids.partner_id[
                0].id)])

        if purchase_order.partner_id.id == \
                self.product_name_id.seller_ids.partner_id[0].id:
            purchase_order[-1].write({
                    'order_line': [[0, 0, {
                        'product_id': self.product_product_id.id,
                        'product_qty': self.quantity
                    }]]
                })
        else:
            self.env['purchase.order'].create({
                'partner_id': self.product_name_id.seller_ids.partner_id[0].id,
                'order_line': [[0, 0, {
                    'product_id': self.product_product_id.id,
                    'product_qty': self.quantity
                }]],
            })
