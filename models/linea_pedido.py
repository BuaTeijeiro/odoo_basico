# -*- coding: utf-8 -*-
from unittest.mock import sentinel

from odoo import models, fields, api
from odoo.api import ondelete
from odoo.exceptions import ValidationError
from reportlab.lib.pdfencrypt import computeO


class lineapedido(models.Model):
    _name = 'odoo_basico.lineapedido'
    _description = 'Registros de lineas de pedidos'

    nome = fields.Char(string="Nombre de la línea")
    descripcion = fields.Char(string="Comentarios:")
    unidades = fields.Integer(string="cantidad")
    pedido_id = fields.Many2one('odoo_basico.pedido', ondelete="cascade", required=True)
    informacion_ids = fields.Many2many("odoo_basico.informacion",
                                       string="Rexistro de Información",
                                       relation="odoo_basico_lineapedido_informacion",
                                       column1="lineapedido_id", column2="informacion_id")

    @api.constrains('unidades')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_unidades(self):  # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.unidades < 1:
                raise ValidationError('As unidades de %s ten que ser maior que 0' % rexistro.nome)