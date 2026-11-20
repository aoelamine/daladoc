from odoo import models, fields, api

class DaladocPrescription(models.Model):
    _name = 'daladoc.prescription'
    _description = 'Daladoc Prescription'

    name = fields.Char(string='Prescription Name', required=True)
    visit_id = fields.Many2one('daladoc.visit', string='Visit', ondelete='cascade')
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    doctor_id = fields.Many2one('res.partner', string='Doctor', required=True)
    date_prescribed = fields.Datetime(string='Date Prescribed', default=fields.Datetime.now, required=True)
    medication_ids = fields.One2many('daladoc.prescription.line', 'prescription_id', string='Medications')
    notes = fields.Text(string='Notes')



class DaladocPrescriptionLine(models.Model):
    _name = 'daladoc.prescription.line'
    _description = 'Daladoc Prescription Line'


    prescription_id = fields.Many2one('daladoc.prescription', string='Prescription')
    medication_id = fields.Many2one('daladoc.meds', string='Medication', required=True)
    dosage = fields.Char(string='Dosage', required=True)
