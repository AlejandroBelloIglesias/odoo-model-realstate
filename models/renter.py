# -*- coding: utf-8 -*-
from xml.dom import ValidationErr
from odoo import api, fields, models

class Renter(models.Model):
    
    _name = 'realestate.renter'
    _inherits = {'res.partner': 'partner_id'}

    # One partner is only one renter
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
    
    # Many renters can live in one property
    property_id = fields.Many2one('realestate.property', string='Property', required=True)

    # Rent paid by the renter
    rent = fields.Float(string='Rent', required=True)

    # Rent must be more than 0
    @api.constrains('rent')
    def _check_rent(self):
        for record in self:
            if record.rent <= 0:
                raise ValidationErr('Rent must be more than 0')