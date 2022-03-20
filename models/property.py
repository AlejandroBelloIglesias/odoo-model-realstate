# -*- coding: utf-8 -*-
from xml.dom import ValidationErr
from odoo import api, fields, models


class Property(models.Model):

    _name = 'realestate.property'
    _description = 'Real Estate Property'

    # Fields
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    # Multiple properties can be owned by one owner
    owner_id = fields.Many2one('realestate.owner', string='Owner', required=True)
        
    # Property
    type = fields.Selection([
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('land', 'Land'),
        ('other', 'Other'),
    ], string='Type', required=True)
    area = fields.Float(string='Area m2', required=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented')
    ], string='Status', required=True)

    available_for_sale = fields.Boolean(string='Available for Sale')
    new_owner_id = fields.Many2one('realestate.owner', string='New Owner')
    
    available_for_rent = fields.Boolean(string='Available for Rent')
    renter_ids = fields.One2many('realestate.renter', 'property_id', string='Renters')

    # Address (Encapsulable)
    street = fields.Char(string='Street', required=True)
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City', required=True)
    state_id = fields.Char(string='Estate / Province', required=True)
    zip = fields.Char(string='Zip', required=True)
    country_id = fields.Char(string='Country', required=True)

    # ==== RENT ====
    # Rent the owner agreed
    rent_owner = fields.Float(string='Rent agreed with owner')
    # Total ammount of monthly rent paid by the renters (Calculated)
    rent_renters = fields.Float(string='Total rent paid by renters', compute='_compute_rent_renters')

    # ==== SALE ====
    # Sale owner ask
    sale_owner = fields.Float(string='Sale price asked by owner')
    # Sale new owner bid
    sale_new_owner = fields.Float(string='Sale price offered by new owner')

    # ==== CALCULATED ====
    # Total rent paid by renters
    @api.depends('renter_ids')
    def _compute_rent_renters(self):
        for record in self:
            record.rent_renters = sum(record.renter_ids.mapped('rent'))

    # ==== VALIDATIONS ====

    # If the property is sold: 
    # available_for_sale must be True and owner_id, new_owner_id, sale_owner, sale_new_owner must be set
    @api.constrains('status', 'available_for_sale', 'owner_id', 'new_owner_id', 'sale_owner', 'sale_new_owner')
    def _check_sold_status(self):
        for record in self:
            if record.status == 'sold':
                if record.available_for_sale is False or record.owner_id is None or record.new_owner_id is None or record.sale_owner is None or record.sale_new_owner is None:
                    record.status = 'available'
                    raise ValidationErr('If the property is sold, available_for_sale, owner_id, new_owner_id, sale_owner, sale_new_owner must be set')

    # If the property is rented: 
    # available_for_rent must be True and owner_id, renter_ids, rent_owner, rent_renters must be set
    @api.constrains('status', 'available_for_rent', 'owner_id', 'renter_ids', 'rent_owner', 'rent_renters')
    def _check_rented_status(self):
        for record in self:
            if record.status == 'rented':
                if record.available_for_rent is False or record.owner_id is None or record.renter_ids is None or record.rent_owner is None or record.rent_renters is None:
                    record.status = 'available'
                    raise ValidationErr('If the property is rented, available_for_rent, owner_id, renter_ids, rent_owner, rent_renters must be set')

    # All prices must be positive
    @api.constrains('rent_owner', 'sale_owner', 'sale_new_owner')
    def _check_prices(self):
        for record in self:
            if record.rent_owner < 0:
                record.rent_owner = 0
                raise ValidationErr('Rent asked by owner must be positive')
            if record.sale_owner < 0:
                record.sale_owner = 0
                raise ValidationErr('Sale price asked by owner must be positive')
            if record.sale_new_owner < 0:
                record.sale_new_owner = 0
                raise ValidationErr('Sale price paid by new owner must be positive')



    
        
