# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning


class ContractTemplate(models.Model):
    _name = 'contract.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HR Contract Template"

    name = fields.Char(string='Template Name', track_visibility='onchange')
    allowance_ids = fields.Many2many('allowance.hr', 'contract_template_allowance_rel',
                                     'template_id', 'allowance_id', string='Allowances', track_visibility='onchange')
    deduction_ids = fields.Many2many('deduction.hr', 'contract_template_deduction_rel',
                                     'template_id', 'deduction_id', string='Deductions', track_visibility='onchange')


class AllowanceHr(models.Model):
    _name = 'allowance.hr'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HR Contract Template Allowance"

    name = fields.Char(string='Allowance Type', track_visibility='onchange', require=True)
    value = fields.Float(string='Value', track_visibility='onchange', require=True)
    code = fields.Char("Code", require=True, copy=False)
    
    @api.constrains('code')
    def _unique_code(self):
        for rec in self:
            if rec.code and isinstance(rec.id, int):
                other_ids = self.env['allowance.hr'].search([('code', '=', rec.code), ('id', '!=', rec.id)])
                if other_ids:
                    raise Warning(_("You can't have 2 allowance with same code"))


class DeductionHr(models.Model):
    _name = 'deduction.hr'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HR Contract Template Deductions"
    
    name = fields.Char(string='Deduction Type', track_visibility='onchange', require=True)
    value = fields.Float(string='Value', track_visibility='onchange', require=True)
    code = fields.Char("Code", require=True, copy=False)

    @api.constrains('code')
    def _unique_code(self):
        for rec in self:
            if rec.code and isinstance(rec.id, int):
                other_ids = self.env['allowance.hr'].search([('code', '=', rec.code), ('id', '!=', rec.id)])
                if other_ids:
                    raise Warning(_("You can't have 2 allowance with same code"))
    
    
class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    contract_template_id = fields.Many2one('contract.template', string='Contract Template',
                                           track_visibility='onchange')
    
    def load_template_details(self):
        """
        Load lines of contract template allowance and deduction
        """
        for contract in self:
            if contract.contract_template_id:
                if contract.contract_template_id.allowance_ids:
                    contract.allowance_ids = [(6, 0, contract.contract_template_id.allowance_ids.ids)]
                else:
                    contract.allowance_ids = [[5]]
                if contract.contract_template_id.deduction_ids:
                    contract.deduction_ids = [(6, 0, contract.contract_template_id.deduction_ids.ids)]
                else:
                    contract.allowance_ids = [[5]]

    allowance_ids = fields.Many2many('allowance.hr', 'contract_allowance_rel',
                                     'contract_id', 'allowance_id', string='Allowances', track_visibility='onchange')
    deduction_ids = fields.Many2many('deduction.hr', 'contract_deduction_rel',
                                     'contract_id', 'deduction_id', string='Deductions', track_visibility='onchange')