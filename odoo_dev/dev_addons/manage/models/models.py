# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _
import datetime
import logging

logger = logging.getLogger(__name__)


class developer(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    code = fields.Char(compute="_get_code")
    #is_dev = fields.Boolean()

    def _get_code(self):
        for c in self:
            c.code = str(c.id)



class cliente(models.Model):
    _name = 'manage.cliente'
    _description = 'manage.cliente'
    
    code = fields.Char(compute="_get_code")
    nif = fields.Char(string="DNI", readonly=False, required=True, help="Introduzca el DNI")
    name = fields.Char(string="Nombre", readonly=False, required=True, help="Introduzca el nombre")
    foto = fields.Image(max_width=200, max_height=200)
    dieta = fields.One2many(string="Dietas", comodel_name="manage.dieta", inverse_name='code')
    motivo = fields.Text()
    revision = fields.One2many(string="Revisiones", comodel_name="manage.revision", inverse_name='cliente')
    especialista = fields.Many2one('manage.dietista', related='dieta.especialista', readonly=True)


    def _get_code(self):
        for c in self:
            c.code = str(c.name) + "_" + str(c.id)

    

class nutricionista(models.Model):
    _name = 'manage.nutricionista'
    _description = 'manage.nutricionista'
    
    nif = fields.Char(string="DNI", readonly=False, required=True, help="Introduzca el DNI")
    name = fields.Char(string="Nombre", readonly=False, required=True, help="Introduzca el nombre")
    foto = fields.Image(max_width=200, max_height=200)
    especialidad = fields.Char()
    


class dietista(models.Model):
    _name = 'manage.dietista'
    _description = 'manage.dietista'
    
    nif = fields.Char(string="DNI", readonly=False, required=True, help="Introduzca el DNI")
    name = fields.Char(string="Nombre", readonly=False, required=True, help="Introduzca el nombre")
    foto = fields.Image(max_width=200, max_height=200)
    especialidad = fields.Char()
    taller = fields.One2many(string="Talleres", comodel_name="manage.taller", inverse_name='especialista')
    dieta = fields.One2many(string="Dietas", comodel_name="manage.dieta", inverse_name='especialista')



class dieta(models.Model):
    _name = 'manage.dieta'
    _description = 'manage.dieta'
    
    code = fields.Char(compute="_get_code")
    cliente = fields.Many2one("manage.cliente", ondelete="cascade", required=True)
    especialista = fields.Many2one("manage.dietista", ondelete="cascade", required=True)
    

    def _get_today_day(self):
        return datetime.datetime.now()

    start_date = fields.Datetime(default=_get_today_day)
    duracion = fields.Integer(default = 10)
    end_date = fields.Datetime(compute="_get_end_date", store=True)

    @api.depends('start_date','duracion')
    def _get_end_date(self):
        
        for x in self:
            try:
                if isinstance(x.start_date, datetime.datetime) and x.duracion >0:
                    x.end_date = x.start_date + datetime.timedelta(days=x.duracion)
                else:
                    x.end_date = x.start_date
                #_logger.debug("Código generado: "+x.code)
            except:
                raise ValidationError(_("Ha habido un problema al calcular la fecha de fin"))
        
    def _get_code(self):
        for c in self:
            c.code = ""+str(c.id)



class taller(models.Model):
    _name = 'manage.taller'
    _description = 'manage.taller'
    
    nombre = fields.Char()
    especialista = fields.Many2one("manage.dietista", ondelete="cascade")
    horario = fields.Datetime()#####
    link = fields.Char()

    
class revision(models.Model):
    _name = 'manage.revision'
    _description = 'manage.revision'

    horario = fields.Datetime()
    cliente = fields.Many2one("manage.cliente")
    dieta = fields.Many2one("manage.dieta", compute="_get_dieta_code")

    @api.depends('cliente')
    def _get_dieta_code(self):
        for r in self:
            try:
                dieta = self.env['manage.dieta'].search([('cliente', '=', r.cliente.id)], limit=1)
                r.dieta = dieta.id if dieta else False
            except:
                raise ValidationError(_("Ha habido un problema al encontrar la dieta"))
