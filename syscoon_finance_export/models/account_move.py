# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api, _
from openerp.exceptions import UserError
from openerp.tools.float_utils import float_is_zero

from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class AccountMove2ExportMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(
        selection_add=[('export_move', 'Datev Move Created')])

    def st_compute_debit_credit(self, move, lines):
        debit = 0.0
        debit_accounts = []
        credit = 0.0
        credit_accounts = []
        invoice = self.env['account.invoice'].search([('move_id', '=', move.id)])
        for line in lines:
            if line.debit:
                debit += line.debit
                debit_accounts.append(line.account_id.code)
            if line.credit:
                credit += line.credit
                credit_accounts.append(line.account_id.code)
        if invoice and invoice.type in ['out_invoice', 'in_refund']:
            debit_accounts = []
            if not invoice.account_id.code in debit_accounts:
                debit_accounts.append(invoice.account_id.code)
        if invoice and invoice.type in ['out_refund', 'in_invoice']:
            credit_accounts = []
            if not invoice.account_id.code in debit_accounts:
                credit_accounts.append(invoice.account_id.code)
        for da in debit_accounts:
            account = self.env['account.account'].search([('code', '=', da)])
            if account.user_type_id.type in ('receivable', 'payable'):
                debit_accounts =[]
                debit_accounts.append(account.code)
        for ca in credit_accounts:
            account = self.env['account.account'].search([('code', '=', ca)])
            if account.user_type_id.type in ('receivable', 'payable'):
                credit_accounts = []
                credit_accounts.append(account.code)
        totals = {
            'debit': debit,
            'debit_accounts': sorted(set(debit_accounts)),
            'credit': credit,
            'credit_accounts': sorted(set(credit_accounts))
        }
        return totals

    def st_create_tax_additions(self, line):
        tax_bkey, tax_pc, tax_account, tax_account_refund = '', 0.0, '', ''
        if line.tax_ids and len(line.tax_ids) == 1:
            tax = self.env['export.key'].search(
                [('vat_code', '=', line.tax_ids.id)], limit=1)
            tax_bkey = tax.export_key
            tax_pc = tax.vat_code.amount
            tax_account = tax.vat_code.account_id.code
            tax_account_refund = tax.vat_code.refund_account_id.code
        return tax_bkey, tax_pc, tax_account, tax_account_refund

    def st_check_account(self, line):
        auto_account_id = self.env['export.auto.account'].search(
            [('account_id', '=', line.account_id.id)])
        tax_bkey, tax_pc, tax_account, tax_account_refund =\
            self.st_create_tax_additions(line)
        if auto_account_id:
            if float_is_zero(tax_pc, precision_rounding=2):
                tax_pc = auto_account_id.vat_code.amount
        return bool(auto_account_id), tax_bkey, tax_pc, tax_account, tax_account_refund

    def st_calculate_amount(self, move, line, tax_pc):
        #todo: gross if company-settings are gross
        amount = 0.0
        if line.debit:
            amount += line.debit
        if line.credit:
            amount += line.credit
        if tax_pc:
            gross_amount = amount * (1 + (tax_pc / 100))
            tax = gross_amount - amount
            amount += tax
        amount = move.currency_id.round(amount)
        return amount

    def st_build_line(self, account, move, res, line):
        auto_account, tax_bkey, tax_pc, tax_account, tax_account_refund =\
            self.st_check_account(line)
        res['name'] = 'New'
        res['date'] = move.date
        res['currency'] = move.currency_id.name
        res['dc_sign'] = account['sign']
#        res['amount'] = str(self.st_calculate_amount(move, line, tax_pc)).replace('.', ',')
        res['amount'] = self.st_calculate_amount(move, line, tax_pc)
        if auto_account:
            res['bkey'] = ''
        else:
            res['bkey'] = tax_bkey
        res['account_offset'] = line.account_id.code
        res['slip1'] = move.name.replace('/', '')
        if line.date_maturity:
            res['slip2'] = fields.Date.from_string(line.date_maturity).strftime('%d%m%y')
        else:
            res['slip2'] = ''
        res['booking_date'] = fields.Date.from_string(move.date).strftime('%d%m')
        res['account'] = account['account']
        res['cost1'] = ''
        res['cost2'] = ''
        res['cost_quant'] = ''
        res['discount'] = ''
        res['bookingtext'] = line.name
        res['vat_id'] = ''
        res['eu_tax'] = ''
        res['base_cur_amount'] = ''
        res['base_cur_code'] = ''
        res['exchange_rate'] = ''
        res['company_id'] = move.company_id.id
        res['account_move'] = move.id
        res['move_date'] = move.date
        return res

    def st_generate_account(self, move, lines):
        totals = self.st_compute_debit_credit(move, lines)
        account = False
        sign = False
        for line in lines:
            if len(totals['debit_accounts']) == 1 and not line.tax_ids:
                account = totals['debit_accounts'][0]
                sign = 's'
            if len(totals['credit_accounts']) == 1 and not line.tax_ids:
                account = totals['credit_accounts'][0]
                sign = 'h'
        return {
            'account': account,
            'sign': sign
        }

    def st_generate_hash(self, res):
        return "%s-%s-%s-%s-%s-%s" % (
            res['dc_sign'],
            res.get('bkey', 'False'),
            res['account'], 
            res['account_offset'],
            res.get('cost1', 'False'),
            res.get('cost2', 'False')
        )

    def st_create_group(self, booking):
        line2 = {}
        for b in booking:
            tmp = self.st_generate_hash(b)
            if tmp in line2:
                am = line2[tmp]['amount'] + b['amount']
                bt = line2[tmp]['bookingtext'] + ' ' + b['bookingtext']
                line2[tmp]['amount'] = am
                line2[tmp]['bookingtext'] = bt
            else:
                line2[tmp] = b
        booking = []
        for key, val in line2.items():
            booking.append(val.copy())
        return booking

    def st_generate_line(self, move, tax_accounts, export_logger, export_errors, export_moves):
        booking = []
        res = {}
        if move.amount:
            move_lines = move.line_ids
            account = self.st_generate_account(move, move_lines)
            if account['account'] == False:
                export_logger.append(_('%s has no / to many different accounts in debit / credit and can not exported') % move.name)
                export_errors += 1
                return export_errors, export_moves, export_logger
            export_moves += 1
            for line in move_lines:
                if account['sign'] == 's' and line.debit:
                    account['sign'] = 'h'
                if account['sign'] == 'h' and line.credit:
                    account['sign'] = 's'
                res = self.st_build_line(account, move, res, line)
                if res['account_offset'] != res['account']:
                    if res['account_offset'] in tax_accounts:
                        continue
                    elif res['account'] in tax_accounts:
                        continue
                    else:
                        booking.append(res.copy())
            grouped_lines = self.st_create_group(booking)
            for gl in grouped_lines:
                self.env['export.move'].create(gl)
                self.write({'state': 'export_move'})
            return export_errors, export_moves, export_logger


    def st_check_tax_lines(self):
        tax_accounts = []
        for txid in self.env['account.tax'].search([]):
            if txid.account_id and txid.account_id.code not in tax_accounts:
                tax_accounts.append(txid.account_id.code)
            if txid.refund_account_id and txid.refund_account_id.code not in tax_accounts:
                tax_accounts.append(txid.refund_account_id.code)
        return tax_accounts

    @api.multi
    def action_export_move_create(self):
        export_logger = []
        export_errors = 0
        export_moves = 0
        tax_accounts = self.st_check_tax_lines()
        company = self.env['res.company']._company_default_get('account.move')
        # export_config will be used in a later version
        export_config = self.env['export.configuration'].search([('company_id', '=', company.id)])
        for move in self:
            if not move.amount:
                export_logger.append(_('%s has amount 0,00 and can not exported') % move.name)
                export_errors += 1
            else:
                em = self.st_generate_line(move, tax_accounts, export_logger, export_errors, export_moves)
                export_moves = em[1]
                export_errors = em[0]
                export_logger = em[2]
                _logger.info('Move %s created.', move.name)
        if not export_errors:
            export_logger.append(_('No Errors, %d moves correctly created') % export_moves)
        self.env['export.logger'].create({
            'name': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'errors': export_errors,
            'moves': export_moves,
            'logging': '\n'.join(export_logger)
        })

    @api.multi
    def button_cancel(self):
        for move in self:
            if move.state == 'export_move':
                raise UserError(_('Forbidden to Cancel! You can not delete a Move which is exported! Please delete the Datev-Export first'))
        return super(AccountMove2ExportMove, self).button_cancel()
