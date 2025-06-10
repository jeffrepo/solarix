
# -*- encoding: utf-8 -*-

from odoo import api, models, fields
import time
import datetime
from datetime import date
from datetime import datetime, date, time, timedelta
from odoo.fields import Date, Datetime
import logging

class ReportSolarixNomina(models.AbstractModel):
    _name = 'report.solarix.nomina'

    def _get_op(self, date_start, date_end, workcenter_ids):
        logging.warning(date_start)
        logging.warning(date_end)
        date_s = date_start
        date_e = date_end
        order_ids = self.env["mrp.workorder"].sudo().search([("workcenter_id","in",workcenter_ids),("date_start","!=", False),("date_start",">=",date_s),("date_finished","<=", date_e),("state","=","done")], order = "production_order_name asc")
        orders = {}
        if order_ids:
            for order in order_ids:
                workcenter = order.workcenter_id.name
                if workcenter not in orders:
                    orders[workcenter] = {'name': workcenter, 'workcenter_orders': {}, 'total': 0}

                logging.warning(order.date_start)
                order_date = (order.date_start - timedelta(hours=6)).date()
                logging.warning(order_date)
                if str(order_date) not in orders[workcenter]['workcenter_orders']:
                    orders[workcenter]['workcenter_orders'][str(order_date)] = {"date": str(order_date), "orders_data": []}
                    #orders[str(order_date)] = {"date": order_date, "orders_data": []}
                total = order.operation_id.x_studio_costo_mob * order.production_id.product_qty
                order_dic = {
                    "op": order.production_id.x_studio_op,
                    "reference": order.production_id.name,
                    "product": order.product_id.name,
                    "operation": order.name,
                    "quantity": order.production_id.product_qty,
                    "unit_price": round(order.operation_id.x_studio_costo_mob,2),
                    "total": round(total,2)
                }
                
                orders[workcenter]['workcenter_orders'][str(order_date)]["orders_data"].append(order_dic)
                orders[workcenter]['total'] += total
        return orders
    
    def _get_today(self):
        today = datetime.now()
        date = datetime.now().date()
        hour = fields.Datetime.to_string(fields.Datetime.context_timestamp(self.with_context(tz=self.env.user.tz), fields.Datetime.from_string(today)))
        return [date,hour]
        
    @api.model
    def _get_report_values(self, docids, data=None):
        data = data if data is not None else {}
        model = 'solarix.nomina'
        docs = data.get('ids', data.get('active_ids'))
        logging.warning("repor values data")
        logging.warning(data)
        fecha_inicio = data.get('form', {}).get('fecha_inicio', False)
        fecha_fin = data.get('form', {}).get('fecha_fin', False)
        workcenter_ids = data.get('form', {}).get('workcenter_ids', False)
        logging.warning(workcenter_ids)
        company_id = self.env.user.company_id
        logging.warning(company_id)
        date_s = datetime.fromisoformat(fecha_inicio) - timedelta(hours=6)
        date_e = datetime.fromisoformat(fecha_inicio) - timedelta(hours=6)
        #folio_inicial = data.get('form', {}).get('folio_inicial', False)
        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            '_get_info': self._get_op,
            'fecha_inicio': date_s,
            'fecha_inicio2': fecha_inicio,
            'fecha_fin2': fecha_fin,
            'fecha_fin': date_e,
            '_get_today': self._get_today,
            'workcenter_ids': workcenter_ids,
            'company_id': company_id,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
