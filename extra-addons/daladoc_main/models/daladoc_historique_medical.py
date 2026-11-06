from odoo import models, fields, api    




class HistoriqueMedical(models.Model):
    _name = 'daladoc.historique.medical'
    _description = 'Historique Medical'

    patient_id = fields.Many2one('res.partner', string='Patient', required=True, domain="[('is_patient', '=', True)]")

    # Info
    date = fields.Date(string='Date', required=True)

    # Maladie, Traitements et Metrics
    maladie_id = fields.Many2one('daladoc.maladie', string='Maladie')

    # Traitements with domain based on the selected maladie 
    allowed_treatment_ids = fields.Many2many(
        'daladoc.treatments',
        compute='_compute_allowed_treatment_ids',
        string='Allowed treatments',
    )

    treatments_ids = fields.Many2many(
    'daladoc.treatments',
    string='Traitements',
    domain="[('id', 'in', allowed_treatment_ids)]",
    )

    @api.depends('maladie_id', 'maladie_id.treatments_ids')
    def _compute_allowed_treatment_ids(self):
        for rec in self:
            rec.allowed_treatment_ids = rec.maladie_id.treatments_ids

    @api.onchange('maladie_id')
    def _onchange_maladie_id(self):
        self.treatments_ids = self.treatments_ids & self.maladie_id.treatments_ids

    # Metrics Historique
    metrics_ids = fields.One2many('daladoc.metrics.historique', 'historique_medical_id', string='Metrics Historique')

   
