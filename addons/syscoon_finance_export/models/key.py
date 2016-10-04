# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api


class ExportKey(models.Model):
    _name = 'export.key'
    _order = 'name'

    name = fields.Char('Name', default='')
    active = fields.Boolean('Active', default=True)
    vat_code = fields.Many2one('account.tax', string='VAT Code')
    export_key = fields.Char('Export Key')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env['res.company']._company_default_get('export.key'))

    _sql_constraints = [
        ('vat_code_unique', 'unique (vat_code, company_id)',
            'The VAT-Code must be unique per Company!')
    ]

    @api.onchange('vat_code')
    def _onchange_vat_code(self):
        self.name = self.vat_code.description
        self.company_id = self.vat_code.company_id