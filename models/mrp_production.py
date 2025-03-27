from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Cuenta analítica')

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
    _inherit = 'mrp.work.order'

    cost_production = fields.Float("Costo producción")