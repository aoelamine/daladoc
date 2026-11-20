from odoo import fields, models, api


class DaladocVisit(models.Model):

    _name = "daladoc.visit"
    _description = "Medical Visit main database table"
    _order = "visit_date desc"


    # Table columns (fields)
    name = fields.Char(string="Visit Reference", required=True, copy=False, readonly=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('daladoc.visit') or 'New')

    # State
    state = fields.Selection([
                            ('check_in','Check-in & Vitals'),
                            ('chief_complaint','Anamnesis & Chief Complaint'),
                            ('examination','Clinical Examination & Assessment'),
                            ('referrals','Prescriptions & Referrals'),
                            ('summary','Summary, Validation & Billing'),   
                            ], default='check_in', required=True, tracking=True, string="Stage")

    # Visit key fields
    visit_date = fields.Datetime(string="Arrival Time", default=fields.Datetime.now, required=True)


    # State 1: Check-in & Vitals

    # Basic fields
    patient_id = fields.Many2one("res.partner", 
                                string="Patient", 
                                required=True, 
                                domain=[('is_patient','=',True)])

    doctor_id = fields.Many2one("res.partner", 
                                string="Doctor", 
                                required=True, 
                                domain=[('is_doctor','=',True)])


    # Vitals fields
    vitals_weight = fields.Float(string="Weight (kg)")
    vitals_height = fields.Float(string="Height (cm)")
    vitals_bp = fields.Char(string="Blood Pressure", placeholder="e.g., 120/80 mmHg")
    vitals_temp = fields.Float(string="Temperature (°C)")
    vitals_heart_rate = fields.Integer(string="Heart Rate (bpm)")


    # State 2: Anamnesis & Chief Complaint

    chief_complaint = fields.Text(string="Chief Complaint", help="Primary reason for the visit in patient's words.")
    history_of_present_illness = fields.Html(string="History of Present Illness (HPI)")
    #symptom_tag_ids = fields.Many2many('daladoc.medic.symptom.tag', string="Symptoms Tags")
    lifestyle_notes = fields.Text(string="Relevant Habits / Context")


    # State 3: Clinical Examination & Assessment

    physical_exam_notes = fields.Html(string="Physical Examination Findings")
    diagnosis_description = fields.Html(string="Clinical Assessment & Diagnosis")


    # State 4: Prescriptions & Referrals

    #procedure_performed_ids = fields.Many2many('medic.procedure', string="Clinical Procedures Performed On-Site")
    #prescription_line_ids = fields.One2many('medic.prescription.line', 'visit_id', string="Prescriptions")
    
    # Sick leave
    requires_sick_leave = fields.Boolean(string="Sick Leave Required?")
    sick_leave_days = fields.Integer(string="Sick Leave Duration (Days)")
    
    # Referrals
    referral_notes = fields.Text(string="Specialist Referral / Orientation Notes")

    # Linked records
    prescription_ids = fields.One2many('daladoc.prescription', 'visit_id', string="Prescriptions")
    lab_test_ids = fields.One2many('daladoc.lab.test', 'visit_id', string="Lab Tests")
    referral_ids = fields.One2many('daladoc.referrals', 'visit_id', string="Referrals")

    prescription_count = fields.Integer(string="Prescriptions Count", compute="_compute_prescription_count")
    lab_test_count = fields.Integer(string="Lab Tests Count", compute="_compute_lab_test_count")
    referral_count = fields.Integer(string="Referrals Count", compute="_compute_referral_count")

    # Followup
    next_followup_date = fields.Date(string="Recommended Follow-Up Date")


    # State 5: Summary, Validation & Billing

    consultation_summary = fields.Html(string="Visit Summary / Medical Report", compute="_compute_summary", store=True)
    payment_status = fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid'), ('exempt', 'Exempt')], string="Payment Status", default='unpaid', tracking=True)
    closed_date = fields.Datetime(string="Closure Timestamp", readonly=True)


    # ==========================================
    # Computed / Display
    # ==========================================

    #@api.depends('patient_id', 'visit_date')
    #def _compute_display_name(self):
    #    for rec in self:
    #        patient_name = rec.patient_id.name or "New Visit"
    #        date_str = rec.visit_date.strftime('%Y-%m-%d %H:%M') if rec.visit_date else ''
    #        rec.display_name = f"{patient_name} – {date_str}" if date_str else patient_name

    @api.depends('state')
    def _compute_summary(self):
        for rec in self:
            if rec.state == 'summary':
                parts = []
                if rec.chief_complaint:
                    parts.append(f"<p><strong>Chief Complaint:</strong> {rec.chief_complaint}</p>")
                if rec.diagnosis_description:
                    parts.append(f"<p><strong>Assessment:</strong> {rec.diagnosis_description}</p>")
                if rec.physical_exam_notes:
                    parts.append(f"<p><strong>Examination:</strong> {rec.physical_exam_notes}</p>")
                rec.consultation_summary = ''.join(parts) if parts else False
            else:
                if not rec.consultation_summary:
                    rec.consultation_summary = False

    # ==========================================
    # Workflow Actions
    # ==========================================

    def action_start_checkin(self):
        self.write({'state': 'check_in'})

    def action_start_complaint(self):
        self.write({'state': 'chief_complaint'})

    def action_start_examination(self):
        self.write({'state': 'examination'})

    def action_start_referrals(self):
        self.write({'state': 'referrals'})

    def action_start_summary(self):
        self.write({'state': 'summary'})

    def action_close_visit(self):
        self.write({
            'state': 'summary',
            'closed_date': fields.Datetime.now(),
        })

    # ==========================================
    # Computed counts
    # ==========================================

    @api.depends('prescription_ids')
    def _compute_prescription_count(self):
        for rec in self:
            rec.prescription_count = len(rec.prescription_ids)

    @api.depends('lab_test_ids')
    def _compute_lab_test_count(self):
        for rec in self:
            rec.lab_test_count = len(rec.lab_test_ids)

    @api.depends('referral_ids')
    def _compute_referral_count(self):
        for rec in self:
            rec.referral_count = len(rec.referral_ids)

    # ==========================================
    # Actions – open linked record forms
    # ==========================================

    def action_create_prescription(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Prescription',
            'res_model': 'daladoc.prescription',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_visit_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }

    def action_view_prescriptions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prescriptions',
            'res_model': 'daladoc.prescription',
            'view_mode': 'list,form',
            'domain': [('visit_id', '=', self.id)],
            'context': {
                'default_visit_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }

    def action_create_lab_test(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Lab Test',
            'res_model': 'daladoc.lab.test',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_visit_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }

    def action_view_lab_tests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lab Tests',
            'res_model': 'daladoc.lab.test',
            'view_mode': 'list,form',
            'domain': [('visit_id', '=', self.id)],
            'context': {
                'default_visit_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }

    def action_create_referral(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Referral',
            'res_model': 'daladoc.referrals',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_visit_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }

    def action_view_referrals(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Referrals',
            'res_model': 'daladoc.referrals',
            'view_mode': 'list,form',
            'domain': [('visit_id', '=', self.id)],
            'context': {
                'default_visit_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }