from odoo import models, fields, api, _    
from odoo.exceptions import ValidationError


class MetricsHistorique(models.Model):
    _name = 'daladoc.metrics.historique'
    _description = 'Metrics Historique'

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.metric_id.name} - {rec.value}"  
    

    historique_medical_id = fields.Many2one('daladoc.historique.medical', string='Historique Medical', required=True)
    
    allowed_metric_ids = fields.Many2many(
        'daladoc.metrics',
        compute='_compute_allowed_metric_ids',
        string='Allowed metrics',
    )

    metric_id = fields.Many2one(
        'daladoc.metrics',
        string='Metric',
        required=True,
        domain="[('id', 'in', allowed_metric_ids)]",
    )

    value = fields.Float(string='Value', required=True)

    @api.depends('historique_medical_id.maladie_id.metrics_ids')
    def _compute_allowed_metric_ids(self):
        for rec in self:
            rec.allowed_metric_ids = rec.historique_medical_id.maladie_id.metrics_ids

    @api.constrains('metric_id', 'historique_medical_id')
    def _check_metric_allowed(self):
        for rec in self:
            allowed = rec.historique_medical_id.maladie_id.metrics_ids
            if rec.metric_id not in allowed:
                raise ValidationError(
                    _("The metric '%s' is not defined for the selected maladie.", rec.metric_id.display_name))