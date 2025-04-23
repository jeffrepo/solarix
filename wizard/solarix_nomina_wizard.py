# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64
import io
import xlsxwriter


class solarix_nomina_wizard(models.TransientModel):
    _name = 'solarix.nomina_wizard'

    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    workcenter_ids = fields.Many2many("mrp.workcenter", string="Centros de trabajo")

    def print_report(self):
        datas = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        datas['form'] = res
        return self.env.ref('solarix.action_solarix_report').report_action([], data=datas)