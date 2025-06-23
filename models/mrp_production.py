from odoo import fields, models, api
import logging

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Cuenta analítica')

    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        res = super(MrpProduction, self)._get_move_raw_values(product_id, product_uom_qty, product_uom, operation_id, bom_line)
        if res:
            if ('location_id' and 'product_id') in res and (bom_line and bom_line.location_src_id):
                res['location_id'] = bom_line.location_src_id.id if (bom_line and bom_line.location_src_id) else False,
        return res

    def button_mark_done(self):
        res = super().button_mark_done()
        if self.analytic_account_id:
            amount = 0
            for line in self.workorder_ids:
                amount += line.cost_production
                
            account_analytic_line_id = self.env["account.analytic.line"].create({
                "name": self.name,
                "account_id": self.analytic_account_id.id,
                "company_id": self.company_id.id,
                "amount": amount * -1,
                "unit_amount": 1,
            })
        return res

class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    cost_production = fields.Float("Costo producción",compute='_compute_cost_production', store=True)
    production_order_name = fields.Char(string="Production order name", related="production_id.name", store=True)

    @api.depends('workcenter_id','qty_remaining','operation_id', 'production_id')
    def _compute_cost_production(self):
        for record in self:
            record.cost_production = record.operation_id.x_studio_costo_mob * record.production_id.product_qty
