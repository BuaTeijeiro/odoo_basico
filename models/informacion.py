# -*- coding: utf-8 -*-
from unittest.mock import sentinel

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Módulo básico para practicar cosas'

    name = fields.Char(required=True, size=20, string = "Nombre:")
    descripcion = fields.Text(string="A descripcion")
    alto_en_cms = fields.Integer(string="Alto en cm")
    ancho_en_cms = fields.Integer(string="Ancho en cm")
    longo_en_cms = fields.Integer(string="Longo en cm")
    peso = fields.Float(digits=(6,2), default=2.7,string="Peso en KG:")
    volume = fields.Float(digits=(6, 7), compute="_volume", store=True, string="Volume m3")
    densidade = fields.Float(digits=(6,7), compute = "_densidade", store=True, string="Densidade kg/m3")#store=True para que se almacene en la base de datos
    autorizado = fields.Boolean(string="¿Autorizado?", default=True)
    sexo_traducido = fields.Selection([("Hombre", "Home"),("Mujer", "Muller"),("Otros", "Outros")], string="Sexo:")
    literal = fields.Char(store=False)

    foto = fields.Binary(string='Foto')
    adxunto_nome = fields.Char(string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo adxunto")

    # Os campos Many2one crean un campo na BD
    moeda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")
    moeda_euro_id = fields.Many2one('res.currency', default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")], limit=1))
    # con domain, filtramos os valores mostrados. Pode ser mediante unha constante (vai entre comillas) ou unha variable
    gasto_en_euros = fields.Monetary(string="Gasto en euros", currency_field="moeda_euro_id")
    moeda_dolar_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', "USD")], limit=1))
    gasto_en_dolares = fields.Monetary(string="Gasto en dolares", currency_field="moeda_dolar_id")
    moeda_koruna_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', "CZK")], limit=1))
    gasto_en_koruny = fields.Monetary(string="Gasto en korunas", currency_field="moeda_koruna_id")

    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]
    _order = "volume asc"

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms) / 1000000

    @api.depends('peso','volume')
    def _densidade(self):
        for rexistro in self:
            if rexistro.volume != 0:
                rexistro.densidade = float(rexistro.peso) / float(rexistro.volume)
            else:
                rexistro.densidade = 0


    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for rexistro in self:
            if rexistro.alto_en_cms > 7:
                rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_en_cms
            else:
                rexistro.literal = ""

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):  # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)