# -*- coding: utf-8 -*-
from unittest.mock import sentinel

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from reportlab.lib.pdfencrypt import computeO


class pedido(models.Model):
    _name = 'odoo_basico.pedido'
    _description = 'Registros de pedidos'

    fecha = fields.Date(string="Fecha de pedido")
    name = fields.Char(string="codigo de pedido")
    cliente = fields.Many2one('res.partner', required=True)
    lineapedido_ids = fields.One2many('odoo_basico.lineapedido', 'pedido_id')


