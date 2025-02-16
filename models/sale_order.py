from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'  # Inherit from the  sale.order model

    batch_id = fields.Many2one('custom.batch', string='Batch')  
    #  Many2one field to link to  custom.batch model

    @api.model  
    def create(self, vals):
        """Override create method to automatically add the sale order to a batch."""
        sale_order = super(SaleOrder, self).create(vals)  
        if sale_order.partner_id:  #  if the sale order have a customer 
            batch = self.env['custom.batch'].search([('customer_id', '=', sale_order.partner_id.id)])  
            # Search for a batch with the same customer
            if not batch:  # If no batch  found  the customer
                batch = self.env['custom.batch'].create_batch_for_customer(sale_order.partner_id.id) 
                # Create a new batch for the customer
            sale_order.batch_id = batch.id  
        return sale_order  

    def write(self, vals):
        """Override write method to update the batch if the customer changes."""
        if 'partner_id' in vals:  # Check if the customer  changed in the write operation
            for order in self:  # Loop through the sale orders being updated 
                batch = self.env['custom.batch'].search([('customer_id', '=', vals['partner_id'])]) 
                # Search for a batch for the new customer
                if not batch:  # If a batch for the new customer doesn't exist
                    batch = self.env['custom.batch'].create_batch_for_customer(vals['partner_id'])  
                    # Create a new batch for the new customer
                order.batch_id = batch.id  
                # Update the sale order's batch_id to  created batch
        return super(SaleOrder, self).write(vals)  

    def action_view_batch(self):
        self.ensure_one() 
        return {
            'type': 'ir.actions.act_window', # action type
            'name': 'Batch', # window name
            'res_model': 'custom.batch', #model of  record that  opened
            'res_id': self.batch_id.id, # id of  record  will be opened
            'view_mode': 'form', # view type
            'target': 'current', #where the view will be opened
        }