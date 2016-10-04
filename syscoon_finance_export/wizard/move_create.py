from openerp import models, api, _
from openerp.exceptions import UserError

class ExportMoveCreate(models.TransientModel):
    _name = 'export.move.create'
    _description = 'Creates Datev Moves'

    @api.multi
    def create_export_move(self):
        context = dict(self._context or {})
        moves = self.env['account.move'].browse(context.get('active_ids'))
        move_to_datev = self.env['account.move']
        for move in moves:
            if move.state == 'posted':
                move_to_datev += move
        if not move_to_datev:
            raise UserError(_('There is no posted move item to create a Datev-Move.'))
        move_to_datev.action_export_move_create()
        return {'type': 'ir.actions.act_window_close'}

