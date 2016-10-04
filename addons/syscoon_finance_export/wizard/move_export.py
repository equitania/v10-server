from openerp import models, api, _
from openerp.exceptions import UserError

class ExportMoveExport(models.TransientModel):
    _name = 'export.move.export'
    _description = 'Export Moves'

    @api.multi
    def create_export_file(self):
        context = dict(self._context or {})
        moves = self.env['export.move'].browse(context.get('active_ids'))
        export_to_create = self.env['export.move']
        for move in moves:
            if move.state == 'created':
                export_to_create += move
        if not export_to_create:
            raise UserError(_('There is no posted move item to create a Export-File.'))
        export_to_create.action_create_export_file()
        return {'type': 'ir.actions.act_window_close'}

