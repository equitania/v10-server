from openerp import models, api, _
from openerp.exceptions import UserError

class ExportMoveUnlink(models.TransientModel):
    _name = 'export.move.unlink'
    _description = 'Unlinks ExportMoves'

    @api.multi
    def unlink_export_move(self):
        context = dict(self._context or {})
        moves = self.env['export.move'].browse(context.get('active_ids'))
        moves_2_delete = self.env['export.move']
        for move in moves:
            if not move.export_export:
                moves_2_delete += move
        if not moves_2_delete:
            raise UserError(_('Pleas delet the Export first, before you can delete a move.'))
        moves_2_delete.action_datev_move_unlink()
        return {'type': 'ir.actions.act_window_close'}