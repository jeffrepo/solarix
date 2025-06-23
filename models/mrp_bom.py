# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    location_src_id = fields.Many2one('stock.location','Ubicación origen')