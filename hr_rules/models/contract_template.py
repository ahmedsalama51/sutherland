# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

    name = fields.Char(string='Allowance Type', track_visibility='onchange')
    value = fields.Float(string='Value', track_visibility='onchange')


class DeductionHr(models.Model):
    _name = 'deduction.hr'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HR Contract Template Deductions"
    
    name = fields.Char(string='Deduction Type', track_visibility='onchange')
    value = fields.Float(string='Value', track_visibility='onchange')
    
    
class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    contract_template_id = fields.Many2one('contract.template', string='Contract Template',
                                           track_visibility='onchange')
