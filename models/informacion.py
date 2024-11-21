# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Módulo básico para practicar cosas'

    name = fields.Char(required=True, size=20, string = "Nombre:")
    descripcion = fields.Text(string="A descripcion")
    alto_en_cms = fields.Integer(string="Alto en cm")
    ancho_en_cms = fields.Integer(string="Ancho en cm")
    longo_en_cms = fields.Integer(string="Longo en cm")
    peso = fields.Float(digits=(6,2), default=2.7,string="Peso en KG:")
    autorizado = fields.Boolean(string="¿Autorizado?", default=True)
    sexo_traducido = fields.Selection([("Hombre", "Home"),("Mujer", "Muller"),("Otros", "Outros")], string="Sexo:")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

