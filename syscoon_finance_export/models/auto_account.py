# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api


class ExportAutoAccount(models.Model):
    _name = 'export.auto.account'
    _order = 'name'

    name = fields.Char('Name', default='')
    account_id = fields.Many2one(comodel_name='account.account',
        string='Account')
    vat_code = fields.Many2one(comodel_name='account.tax',
        string='Auto-Tax')
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
        required=True,
        default=lambda self: self.env['res.company'].\
        _company_default_get('auto.account'))

    _sql_constraints = [
        ('vat_code_unique', 'unique (account_id, company_id)',
            'The VAT-Code must be unique per Company')
    ]

    @api.onchange('account_id')
    def _onchange_vat_code(self):
        self.name = '%s %s' % (self.account_id.code or '',
            self.account_id.name or '')