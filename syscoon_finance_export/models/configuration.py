# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields


class ExportConfiguration(models.Model):
    _name = 'export.configuration'
    _description = 'Configuration of the Export'

    name = fields.Char(comodel_name='res.company', related='company_id.name', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env['res.company']._company_default_get('export.configuration'))
    advisor_number = fields.Char('Advisor Number', size=20)
    auto_export_header = fields.Boolean('Automated Export Header')
    client_number = fields.Char('Client Number', size=20)
    export_method = fields.Selection([('gross', 'gross'), ('net', 'net')], required=True)
    scheduler_journals = fields.Many2many('account.journal')
    scheduler_limit = fields.Integer('Limit Moves', default=0)

    _sql_constraints = [
        ('company_unique', 'unique (company_id)',
            'The Company must be unique in Settings!')
    ]