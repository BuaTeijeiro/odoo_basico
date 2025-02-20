# -*- coding: utf-8 -*-
import os
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import pytz
import locale
import platform

from . import miñasUtilidades


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
    # con domain, filtramos os valores mostrados. Pode ser mediante unha constante (vai entre comillas) ou unha variable
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label", string="Moeda en formato texto")
    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login", string="Usuario creador da moeda", store=True)

    moeda_euro_id = fields.Many2one('res.currency', default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")], limit=1))
    gasto_en_euros = fields.Monetary(string="Gasto en euros", currency_field="moeda_euro_id")
    moeda_dolar_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', "USD")], limit=1))
    gasto_en_dolares = fields.Monetary(string="Gasto en dolares", currency_field="moeda_dolar_id")
    moeda_koruna_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', "CZK")], limit=1))
    gasto_en_koruny = fields.Monetary(string="Gasto en korunas", currency_field="moeda_koruna_id", compute = "_koruna")
    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
    hora_utc = fields.Char(compute="_actualiza_hora_utc", string="Hora UTC", size=15, store=True)
    hora_timezone_usuario = fields.Char(compute="actualiza_hora_timezone_usuario", string="Hora Timezone do Usuario", size=15, store=True)
    mes_castelan = fields.Char(compute="_mes_castelan", string="Mes Castellano", store=True)
    mes_galego = fields.Char(compute="_mes_galego", string="Mes Galego", store=True)
    mes_checo = fields.Char(compute="_mes_checo", string="Mes Checo", store=True)
    mes_chino = fields.Char(compute="_mes_chino", string="Mes Chino", store=True)
    mes_coreano = fields.Char(compute="_mes_coreano", string="Mes Coreano", store=True)
    mes_xapones = fields.Char(compute="_mes_xapones", string="Mes Xaponés", store=True)
    mes_rumano= fields.Char(compute="_mes_rumano", string="Mes Rumano", store=True)
    mes_hungaro = fields.Char(compute="_mes_hungaro", string="Mes Hungaro", store=True)

    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]
    _order = "volume asc"

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms) / 1000000

    @api.depends('gasto_en_euros')
    def _koruna(self):
        for rexistro in self:
            rexistro.gasto_en_koruny = float(rexistro.gasto_en_euros) * 25

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

    def envio_email(self):
        meu_usuario = self.env.user
        # mail_de     Odoo pon o email que configuramos en gmail para facer o envio
        mail_reply_to = meu_usuario.partner_id.email  # o enderezo email que ten asociado o noso usuario
        mail_para = 'david.buho.tijeras@gmail.com'
        mail_valores = {
            'subject': 'Aquí iría o asunto do email ',
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Aquí iría o corpo do email cos datos por exemplo de "%s" ' % self.descripcion,
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True

    def ver_contexto(self):  # Este método é chamado dende un botón de informacion.xml
            for rexistro in self:
                # Ao usar warning temos que importar a libreria mediante from odoo.exceptions import Warning
                # Importamos tamén a libreria os mediante import os
                # raise Warning(
                #     'Contexto: %s Ruta: %s Contido %s' % (rexistro.env.context, os.getcwd(), os.listdir(os.getcwd())))

                raise ValidationError('Contexto: %s Ruta: %s Contido %s' % (rexistro.env.context, os.getcwd(), os.listdir(os.getcwd())))
                # env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
            return True

    @api.depends('data_hora')
    def _actualiza_hora_utc(self):
        for rexistro in self:  # A hora se almacena na BD en horario UTC (2 horas menos no verán, 1 hora menos no inverno)
            rexistro.hora_utc = rexistro.data_hora.strftime("%H:%M:%S")

    @api.depends('data_hora')
    def actualiza_hora_timezone_usuario(
            self):  # Non pode ser un metodo privado porque da erro ao ser chamado dende o boton na vista xml        # "_actualiza_hora_timezone_usuario en odoo_basico.informacion es privado y no se puede activar con un botón"
        for rexistro in self:
            rexistro.chamado_dende_pedido_e_dende_apidepends(rexistro)

    def chamado_dende_pedido_e_dende_apidepends(self,
                                                parametro_cos_datos_a_actualizar):  # Ten 2 parametros xa que polo segundo recibe os rexistros que queremos actualizar dende pedido
        # TypeError: informacion.actualiza_hora_timezone_usuario() takes 1 positional argument but 2 were given
        #     parametro_cos_datos_a_actualizar.hora_timezone_usuario = self.convirte_data_hora_de_utc_a_timezone_do_usuario(parametro_cos_datos_a_actualizar.data_hora).strftime("%H:%M:%S")  # Convertimos a hora de UTC a hora do timezone do usuario
        for rexistro in parametro_cos_datos_a_actualizar:
            rexistro.hora_timezone_usuario = rexistro.convirte_data_hora_de_utc_a_timezone_do_usuario(
                rexistro.data_hora).strftime("%H:%M:%S")  # Convertimos a hora de UTC a hora do timezone do usuario

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self,
                                                        data_hora_utc_object):  # recibe a data hora en formato object
        usuario_timezone = pytz.timezone(
            self.env.user.tz or 'UTC')  # obter a zona horaria do usuario. Ollo!!! nas preferencias do usuario ten que estar ben configurada a zona horaria
        return pytz.UTC.localize(data_hora_utc_object).astimezone(
            usuario_timezone)  # hora co horario do usuario en formato object
        # para usar  pytz temos que facer  import pytz


    @api.depends('data')
    def _mes_castelan(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))
        for rexistro in self:
            rexistro.mes_castelan = rexistro.data.strftime("%B")  # strftime https://strftime.org/

    @api.depends('data')
    def _mes_galego(self):
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Galician_Spain.1252', 'gl_ES.utf8'))
        for rexistro in self:
            rexistro.mes_galego = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))

    @api.depends('data')
    def _mes_checo(self):
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Czech_Czech Republic.1250', 'cs_CZ.UTF-8'))
        for rexistro in self:
            rexistro.mes_checo = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))

    @api.depends('data')
    def _mes_chino(self):
        locale.setlocale(locale.LC_TIME,
                         miñasUtilidades.cadeaTextoSegunPlataforma('Chinese_China.936', 'zh_CN.UTF-8'))
        for rexistro in self:
            rexistro.mes_chino = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))


    @api.depends('data')
    def _mes_coreano(self):
        locale.setlocale(locale.LC_TIME,
                         miñasUtilidades.cadeaTextoSegunPlataforma('Korean_Korea.949', 'ko_KR.UTF-8'))
        for rexistro in self:
            rexistro.mes_coreano = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))

    @api.depends('data')
    def _mes_xapones(self):
        locale.setlocale(locale.LC_TIME,
                         miñasUtilidades.cadeaTextoSegunPlataforma('Japanese_Japan.932', 'ja_JP.UTF-8'))
        for rexistro in self:
            rexistro.mes_xapones = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))

    @api.depends('data')
    def _mes_rumano(self):
        locale.setlocale(locale.LC_TIME,
                         miñasUtilidades.cadeaTextoSegunPlataforma('Romanian_Romania.1250', 'ro_RO.UTF-8'))
        for rexistro in self:
            rexistro.mes_rumano = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))

    @api.depends('data')
    def _mes_hungaro(self):
        locale.setlocale(locale.LC_TIME,
                         miñasUtilidades.cadeaTextoSegunPlataforma('Hungarian_Hungary.1250', 'hu_HU.UTF-8'))
        for rexistro in self:
            rexistro.mes_hungaro = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))