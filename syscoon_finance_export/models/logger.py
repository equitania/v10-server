# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields


class AccountMoveExportLogger(models.Model):
    _name = 'export.logger'
    _description = 'Error Logging for Move Creation'

    name = fields.Char('Name')
    logging = fields.Text('Logging')
    moves = fields.Integer('Created Moves')
    errors = fields.Integer('Errors')
