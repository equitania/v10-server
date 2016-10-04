# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api


class ExportExports(models.Model):
    _name = 'export.exports'
    _order = 'name'

    name = fields.Char('Name', default='New')
    state = fields.Selection([('draft', 'Draft'), ('created', 'Created')], invisible=1)
    date_range = fields.Char('Export Date Range')
    file = fields.Binary('Export File')
    file_name = fields.Char('Export Filename', size=256)
    note = fields.Text('Note')
    company_id = fields.Many2one('res.company', string='Company',\
        required=True, default=lambda self: self.env['res.company'].\
        _company_default_get('export.exports'))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].\
                next_by_code('st.export.sequence')
            vals['file_name'] = vals['name'] + '.csv'
        return super(ExportExports, self).create(vals)

    @api.multi
    def _reset_datev_move(self, move):
        export_moves = self.env['export.move'].search([('export_export', '=', move)])
        export_moves.write({'state': 'created'})

    @api.multi
    def unlink(self):
        for export in self:
            self._reset_datev_move(export.id)
        return super(ExportExports, self).unlink()
