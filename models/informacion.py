# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Módulo básico para practicar cosas'

    name = fields.Char(required=True, size=20, string = "Nombre:")
    descripcion = fields.Text(string="A descripcion")
    alto_en_cm = fields.Integer(string="Alto en cm")
    ancho_en_cm = fields.Integer(string="Ancho en cm")
    longo_en_cm = fields.Integer(string="Longo en cm")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

