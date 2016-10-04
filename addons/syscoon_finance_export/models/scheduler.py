# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, api
import logging

_logger = logging.getLogger(__name__)


class ExportMoveScheduler(models.TransientModel):
    _name = 'syscoon.export.move.scheduler'
    _description = 'Scheduler for Creates Datev Moves'

    @api.model
    def export_move_scheduler(self):
        export_config = self.env['export.configuration'].search([])
        move_to_datev = self.env['account.move']
        _logger.info('Export Move Scheduler started')
        for config in export_config:
            if not config.scheduler_journals:
                _logger.warning('No Journals defined for the Scheduler in company!')
                return
            else:
                if config.scheduler_limit:
                    moves = self.env['account.move'].search([
                        ('company_id', '=', config.company_id.id),
                        ('journal_id', 'in', config.scheduler_journals.ids),
                        ('state', '=', 'posted')
                    ], order='id asc', limit=config.scheduler_limit)
                else:
                    moves = self.env['account.move'].search([
                        ('company_id', '=', config.company_id.id),
                        ('journal_id', 'in', config.scheduler_journals.ids),
                        ('state', '=', 'posted')
                    ], order='id asc')
            move_to_datev += moves
            if not move_to_datev:
                _logger.warning('There is no posted move item to create a Datev-Move.')
            move_to_datev.action_export_move_create()
