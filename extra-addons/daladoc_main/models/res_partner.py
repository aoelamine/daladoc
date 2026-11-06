from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_doctor = fields.Boolean(string='Is a Doctor', default=False)
    is_patient = fields.Boolean(string='Is a Patient', default=False)
    is_assistant = fields.Boolean(string='Is an Assistant', default=False)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', required=True)

    assurance = fields.Selection([
        ('cnas', 'CNAS'),
        ('casnos', 'CASNOS'),
        ('non_assure', 'Non Assuré'),
    ], string='Assurance', required=True, default='non_assure')

    is_enceinte = fields.Boolean(string='Enceinte ?', default=False)

    historique_medical_ids = fields.One2many('daladoc.historique.medical', 'patient_id', string='Historique Medical')

    