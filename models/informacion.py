# -*- coding: utf-8 -*-

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