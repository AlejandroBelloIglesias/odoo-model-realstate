# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Owner(models.Model):

    _name = 'realestate.owner'
    _inherits = {'res.partner': 'partner_id'}   
    _description = 'Real Estate Owner'

    # One partner is only one owner
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
   
    # One owner can own many properties
    property_ids = fields.One2many('realestate.property', 'owner_id', string='Properties')
    
    
