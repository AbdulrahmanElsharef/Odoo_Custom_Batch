from odoo import models, fields, api

class CustomBatch(models.Model):
    _name = 'custom.batch'  # The name of the model 
    _description = 'Custom Batch'  #  description of the model
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit from mail features 
    _rec_name = "seq"  # used to display the record's name in view
    _order = 'total_amount'  #  sorting order for record

    seq = fields.Char(string='Batch Number', readonly=True, default=lambda self: self._generate_reference())  
    # Batch number, read-only, generated automatically
    sale_order_ids = fields.One2many('sale.order', 'batch_id', string='Sales Orders')  
    # One2many relationship to sale.order model
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)  
    # Computed and stored total amount
    total_lines_amount = fields.Float(string='Total Lines Amount', compute='_compute_total_lines_amount', store=True)
    # Computed and stored total lines amount
    customer_id = fields.Many2one('res.partner', string='Customer', required=True) 
    # Many2one relationship to res.partner  required

    @api.model  
    def _generate_sequence(self):
        """Generate a unique sequence for the batch number."""
        return self.env['ir.sequence'].next_by_code('custom.batch') or 'New'  
    # Get the next sequence number or 'New' if none

    @api.depends('sale_order_ids.amount_total') 
    def _compute_total_amount(self):
        for batch in self:  # Loop through each  record in the model
            batch.total_amount = sum(order.amount_total for order in batch.sale_order_ids)  
            # Calculate the sum of amount_total from sale order model

    @api.depends('sale_order_ids.order_line.price_subtotal')  
    def _compute_total_lines_amount(self):
        for batch in self:  
            total = 0.0  # Initialize the total
            for sale_order in batch.sale_order_ids:  # Loop through the related sale orders
                total += sum(sale_order.order_line.mapped('price_subtotal'))  
                # Sum the price subtotals for every line of order before tax
            batch.total_lines_amount = total  # Assign the calculated total to the batch

    @api.model  
    def create_batch_for_customer(self, customer_id):
        """Create a new batch for a specific customer."""
        batch = self.create({  # Create a new batch record
            'customer_id': customer_id,  # Set the customer
        })
        return batch  

    def add_sale_order_to_batch(self, sale_order):
        """Add a sale order to the correct batch for its customer."""
        self.ensure_one()  # Ensure that the method is called on a single batch record
        batch = self.search([('customer_id', '=', sale_order.partner_id.id)])  
        # Search for a batch with the same customer
        if not batch:  # If no batch is found
            batch = self.create_batch_for_customer(sale_order.partner_id.id)  
            # Create a new batch for the customer
        sale_order.batch_id = batch.id  # Assign the batch to the sale order