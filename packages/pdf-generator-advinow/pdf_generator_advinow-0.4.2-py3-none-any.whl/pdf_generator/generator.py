import copy
import warnings

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, ListFlowable, ListItem, PageBreak, \
    TableStyle
from reportlab.platypus.flowables import HRFlowable, KeepTogether, Image
from PIL import Image as PILImage

from .preprocessor import JSONPreprocessor
from .styles import getStyleSheet, getTableStyles
from .utils import stretch_image_size


class PDFGenerator(JSONPreprocessor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buffer = BytesIO()
        self.buffer_discharge = BytesIO()
        self.stylesheet = getStyleSheet()
        self.tablestylesheet = getTableStyles()
        self._create_pdf()

    def get_buffer(self):
        return self.buffer

    def get_buffer_discharge(self):
        return self.buffer_discharge

    def _create_pdf(self):
        """
        The minus 6 below is because when the frame is applied to the doc,
        there is a padding that cannot be modified without creating an entire
        new class.  The hack is to offset it by 6, so now everything in the
        frame will be at the 1" margin.
        """
        bottom_margin = top_margin = left_margin = right_margin = 1.0 * inch - 6
        pdf_title = '{} {}'.format(self.patient_details.get('full_name'), self.visit_details.get('formatted_date'))
        pdf_args = {'pagesize': letter, 'rightMargin': right_margin, 'leftMargin': left_margin,
                    'topMargin': top_margin, 'bottomMargin': bottom_margin, 'showBoundary': 0,
                    'title': pdf_title}
        doc = SimpleDocTemplate(self.buffer, **pdf_args)
        doc_discharge = SimpleDocTemplate(self.buffer_discharge, **pdf_args)

        # this is for the doctors notes
        self.Elements = []
        # discharge
        self.Elements_discharge = []

        # precomputed self.Elements
        self.basic_horz_line = HRFlowable(color=colors.darkgrey, thickness=1)
        self.width_between_columns = Spacer(20, 1)

        ptext = 'Patient Visit Summary'
        self.Elements.append(Paragraph(ptext, self.stylesheet['title']))
        self.Elements.append(Spacer(1, 12))
        self.Elements_discharge.append(Paragraph(ptext, self.stylesheet['title']))
        self.Elements_discharge.append(Spacer(1, 12))

        visit_table_data = [
            [Paragraph('Doctor Name:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.visit_details['doctor_name'], self.stylesheet['default'])],
            [Paragraph('Facility:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.visit_details['location'], self.stylesheet['default'])],
            [Paragraph('Arrival Date:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.visit_details['formatted_date'], self.stylesheet['default'])],
            [Paragraph('Arrival Time:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.visit_details['formatted_time'], self.stylesheet['default'])],
            [self.Elements.append(Spacer(1, 12))],
            [Paragraph('Patient Name:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.patient_details['full_name'], self.stylesheet['default'])],
            [Paragraph('Gender:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.patient_details['gender'], self.stylesheet['default'])],
            [Paragraph('Ethnicity:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.patient_details['ethnicity'], self.stylesheet['default'])],
            [Paragraph('Birth Date:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.patient_details['birth_date'], self.stylesheet['default'])],
            [Paragraph('Age:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.patient_details['age_years'], self.stylesheet['default'])],
            [self.Elements.append(Spacer(1, 12))],
            [Paragraph('Visit Reason:', self.stylesheet['table_header']),
             self.width_between_columns,
             Paragraph(self.visit_details['visit_reason'], self.stylesheet['default'])]
        ]

        visit_table = Table(
            data=visit_table_data, colWidths=self._get_max_width(visit_table_data),
            hAlign='LEFT', style=self.tablestylesheet['left'])

        self.Elements.append(visit_table)
        self.Elements.extend([Spacer(1, 12), self.basic_horz_line])

        self.Elements_discharge.append(visit_table)
        self.Elements_discharge.extend([Spacer(1, 12), self.basic_horz_line])

        patient_vital_group = []
        ptext = 'Patient Vitals'
        patient_vital_group.append(Paragraph(ptext, self.stylesheet['title']))
        patient_vital_group.append(Spacer(1, 12))
        if self.has_vitals_for_pdf():
            self._vitals_creation(patient_vital_group)
        else:
            patient_vital_group.append(Paragraph('No Vitals for this visit', self.stylesheet['default']))
        patient_vital_group.extend([Spacer(1, 12), self.basic_horz_line])
        self.Elements.append(KeepTogether(patient_vital_group))

        personal_medical_history = []
        ptext = 'Patient History'
        personal_medical_history.append(Paragraph(ptext, self.stylesheet['title']))
        personal_medical_history.append(Spacer(1, 12))

        ptext = '<u>Personal Medical History</u>'
        personal_medical_history.append(Paragraph(ptext, self.stylesheet['header']))

        personal_medical_history_data = []

        if len(self.patient_history.get('personal_history', [])) > 0 and \
                self.patient_history.get('personal_history') != ['']:
            for i in sorted(self.patient_history['personal_history']):
                personal_medical_history_data.append([Paragraph(i, self.stylesheet['table_header'])])
        else:
            personal_medical_history_data.append(
                [Paragraph('No Reported Personal Medical History', self.stylesheet['default'])]
            )

        personal_medical_history_table = Table(data=personal_medical_history_data,
                                               colWidths=self._get_max_width(personal_medical_history_data),
                                               hAlign='LEFT', style=self.tablestylesheet['top_align'])
        personal_medical_history.append(personal_medical_history_table)
        personal_medical_history.extend([Spacer(1, 12)])

        self.Elements.append(KeepTogether(personal_medical_history))

        surgical_history = []
        ptext = '<u>Past Surgical History</u>'
        surgical_history.append(Paragraph(ptext, self.stylesheet['header']))

        surgical_history_data = []

        surgical_history_items = sorted(self.patient_history.get('surgical_history', []))
        if len(surgical_history_items) > 0 and surgical_history_items != ['']:
            for i in surgical_history_items:
                surgical_history_data.append([Paragraph(i, self.stylesheet['table_header'])])
        else:
            surgical_history_data.append([Paragraph('No Reported Past Surgical History', self.stylesheet['default'])])

        surgical_history_table = Table(data=surgical_history_data, colWidths=self._get_max_width(surgical_history_data),
                                       hAlign='LEFT', style=self.tablestylesheet['top_align'])
        surgical_history.append(surgical_history_table)
        surgical_history.extend([Spacer(1, 12)])

        self.Elements.append(KeepTogether(surgical_history))

        family_history_group = []
        ptext = '<u>Family Medical History</u>'
        family_history_group.append(Paragraph(ptext, self.stylesheet['header']))

        family_history_data = []

        if self.patient_history.get('family_history', []):
            for i in sorted(self.patient_history['family_history']):
                family_history_data.append([Paragraph(i, self.stylesheet['table_header'])])
        else:
            family_history_data.append([Paragraph('No Reported Family Medical History', self.stylesheet['default'])])

        family_history_table = Table(data=family_history_data, colWidths=self._get_max_width(family_history_data),
                                     hAlign='LEFT', style=self.tablestylesheet['top_align'])

        family_history_group.append(family_history_table)
        family_history_group.extend([Spacer(1, 12), self.basic_horz_line])
        self.Elements.append(KeepTogether(family_history_group))

        patient_history_group = []
        patient_history_top_data = [[Paragraph('Medications', self.stylesheet['header_center']),
                                     Paragraph('Immunizations', self.stylesheet['header_center'])]]

        bullet_list = []
        for key in ['medications', 'immunizations']:

            end_list = []
            for item in self.patient_history[key]:
                end_list.append(ListItem(Paragraph(item, self.stylesheet['default_list'])))

            bullet_list.append(ListFlowable(end_list, bulletType='bullet', start=u'\u2022', leftIndent=8))

        patient_history_top_data.append(bullet_list)

        patient_history_top_table = Table(
            data=patient_history_top_data, colWidths=[doc.width / 2] * 2,
            style=self.tablestylesheet['top_align']
        )

        patient_history_group.append(patient_history_top_table)
        patient_history_group.append(Spacer(1, 12))

        patient_history_top_data = [[Paragraph('Medication Allergies', self.stylesheet['header_center']),
                                     Paragraph('Other Allergies', self.stylesheet['header_center'])]]

        bullet_list = []
        for key in ['medication_allergies', 'allergies']:

            end_list = []
            for item in sorted(self.patient_history[key]):
                end_list.append(ListItem(Paragraph(item, self.stylesheet['default_list'])))

            bullet_list.append(ListFlowable(end_list, bulletType='bullet', start=u'\u2022', leftIndent=8))

        patient_history_top_data.append(bullet_list)

        patient_history_top_table = Table(
            data=patient_history_top_data, colWidths=[doc.width / 2] * 2,
            style=self.tablestylesheet['top_align']
        )

        patient_history_group.append(patient_history_top_table)
        patient_history_group.append(Spacer(1, 12))
        self.Elements.append(KeepTogether(patient_history_group))

        social_history_group = []
        ptext = '<u>Social History</u>'
        social_history_group.append(Paragraph(ptext, self.stylesheet['header']))

        social_data = [[Paragraph('Smoking Status: ', self.stylesheet['table_header']),
                        self.width_between_columns,
                        Paragraph(self.patient_history['tobacco'], self.stylesheet['default'])],
                       [Paragraph('Alcohol Status: ', self.stylesheet['table_header']),
                        self.width_between_columns,
                        Paragraph(self.patient_history['alcohol'], self.stylesheet['default'])],
                       [Paragraph('Caffeine Status: ', self.stylesheet['table_header']),
                        self.width_between_columns,
                        Paragraph(self.patient_history['caffeine'], self.stylesheet['default'])]]

        social_table = Table(data=social_data, colWidths=self._get_max_width(social_data), hAlign='LEFT',
                             style=self.tablestylesheet['left'])

        social_history_group.append(social_table)
        social_history_group.append(Spacer(1, 12))
        self.Elements.append(KeepTogether(social_history_group))

        physical_exam_group = []
        ptext = 'Physical Exam'
        physical_exam_group.append(Paragraph(ptext, self.stylesheet['title']))
        physical_exam_group.append(Spacer(1, 12))

        if self.physical_exam:
            exam_data = [
                [Paragraph('{}: '.format(item['examName']), self.stylesheet['table_header']),
                 self.width_between_columns,
                 Paragraph(item['examResults'], self.stylesheet['default'])] for item in self.physical_exam
            ]
            exam_table = Table(data=exam_data, colWidths=self._get_max_width(exam_data), hAlign='LEFT',
                               style=self.tablestylesheet['exam_table'])
            physical_exam_group.append(exam_table)
        else:
            physical_exam_group.append(Paragraph('Physical Exam not conducted', self.stylesheet['default']))

        physical_exam_group.append(Spacer(1, 12))
        self.Elements.append(KeepTogether(physical_exam_group))

        self._symptoms_creation(self.Elements)

        self._add_ros_symptoms()

        # to align all the table columns, we will use a standard colwidths
        self.std_ill_col_widths = [(doc.width - 160) / 2, 80, (doc.width - 160) / 2, 80]
        self.std_trt_col_widths = [90, doc.width - 90]

        lab_group = self._lab_creation()
        self.Elements.append(KeepTogether(lab_group))

        # if no illnesses are selected (pdf generated during doctor using the app)
        # dont display any illness/treatment info.
        if len(self.illnesses_selected) > 0:
            self.symptoms_with_icds = list(map(list, set(map(tuple, self.symptoms_with_icds))))
            self._illness_creation(dta=self.illnesses_selected, ttl='Illnesses Diagnosed',
                                   element_target=self.Elements, symp_data=self.symptoms_with_icds, is_selected=True)
            if self.treatments_selected_formatted:
                self._treatment_creation(self.treatments_selected_formatted, 'Treatments', element_target=self.Elements,
                                         is_selected=True)

            # for the discharge, we dont want all the contributors and we can combine the illnesses and symptoms.
            # Must be run after the notes

            for i in self.illnesses_selected:
                ill_list = ['', i['icd_cd'], i['icd_desc']]
                self.symptoms_with_icds.insert(0, ill_list)

            self._illness_creation(ttl='Illnesses Diagnosed', element_target=self.Elements_discharge,
                                   symp_data=self.symptoms_with_icds)
            if self.treatments_selected_formatted:
                self._treatment_creation(
                    self.treatments_selected_formatted, 'Treatments',
                    element_target=self.Elements_discharge
                )

        add_doctors_notes = self.create_additional_notes('notes', 'Summary Doctor\'s Notes', [])
        self.Elements.append(KeepTogether(add_doctors_notes))

        if self.media:
            self.Elements.append(PageBreak())
            ptext = 'Supplemental Information'
            self.Elements.append(Paragraph(ptext, self.stylesheet['title']))
            self.Elements.append(Spacer(1, 12))
            self.Elements.append(self.basic_horz_line)
            self.Elements.append(Spacer(1, 12))
            if self.media:
                self._measurement_images(self.media, self.Elements)
        doc.build(self.Elements, onFirstPage=self._footer, onLaterPages=self._footer)
        doc_discharge.build(self.Elements_discharge, onFirstPage=self._footer, onLaterPages=self._footer)

    def _vitals_creation(self, target_elements):
        vital_table_data = [
            [Paragraph('Blood Pressure:', self.stylesheet['table_header']),
             Paragraph(self.measurements['blood_pressure'], self.stylesheet['default'])],
            [Paragraph('Pulse:', self.stylesheet['table_header']),
             Paragraph(self.measurements['pulse'], self.stylesheet['default'])],
            [Paragraph('Oxygen Saturation:', self.stylesheet['table_header']),
             Paragraph(self.measurements['blood_oxygen'], self.stylesheet['default'])],
            [Paragraph('Mean Arterial Pressure:', self.stylesheet['table_header']),
             Paragraph(self.measurements['mean_arterial_pressure'], self.stylesheet['default'])],
            [Paragraph('Weight:', self.stylesheet['table_header']),
             Paragraph(self.measurements['weight'], self.stylesheet['default'])],
            [Paragraph('Temperature:', self.stylesheet['table_header']),
             Paragraph(self.measurements['temperature'], self.stylesheet['default'])],
            [Paragraph('Height:', self.stylesheet['table_header']),
             Paragraph(self.measurements['height'], self.stylesheet['default'])],
            [Paragraph('Respiratory Rate:', self.stylesheet['table_header']),
             Paragraph(self.measurements['respiratory_rate'], self.stylesheet['default'])],
        ]

        vital_table = Table(data=self._table_splitter(vital_table_data), hAlign='LEFT',
                            style=self.tablestylesheet['left'])
        target_elements.append(vital_table)

    def _symptoms_creation(self, target_elements):
        symptom_group = []
        ptext = 'History of Present Illness'
        symptom_group.append(Spacer(1, 12))
        symptom_group.append(Paragraph(ptext, self.stylesheet['title']))
        symptom_group.append(Paragraph(self.doctor_notes.get('summaryHPI', ""), self.stylesheet['default']))
        symptom_group.append(Spacer(1, 12))

        presenting_symptoms = sorted(self.symptoms['presenting'])
        not_presenting_symptoms = sorted(self.symptoms['not_presenting'])

        if presenting_symptoms or not_presenting_symptoms:
            ptext = '<u>Symptoms Presenting</u>'
            symptom_group.append(Paragraph(ptext, self.stylesheet['header']))
            presenting_symptoms_data = []
            for i in presenting_symptoms:
                if len(i) == 1:
                    presenting_symptoms_data.append([Paragraph(i[0], self.stylesheet['table_header'])])
                else:
                    presenting_symptoms_data.append([Paragraph(i[0], self.stylesheet['sub_table_header']),
                                                     self.width_between_columns,
                                                     Paragraph(i[1], self.stylesheet['default'])])

            if len(presenting_symptoms_data) > 0:
                presenting_symptoms_table = Table(data=presenting_symptoms_data,
                                                  colWidths=self._get_max_width(presenting_symptoms_data),
                                                  hAlign='LEFT', style=self.tablestylesheet['symptoms'])
                symptom_group.append(presenting_symptoms_table)
            else:
                symptom_group.append(Paragraph('No Presenting Symptoms Reported', self.stylesheet['default']))

            symptom_group.append(Spacer(1, 12))
            target_elements.append(KeepTogether(symptom_group))

            non_presenting_symptom_group = []
            ptext = '<u>Symptoms Not Presenting</u>'
            non_presenting_symptom_group.append(Paragraph(ptext, self.stylesheet['header']))
            if not_presenting_symptoms:
                not_presenting_symptoms_data = ListFlowable([Paragraph(i, self.stylesheet['default_list'])
                                                             for i in not_presenting_symptoms],
                                                            bulletType='bullet', start=u'\u2022', leftIndent=10)
                non_presenting_symptom_group.append(not_presenting_symptoms_data)
            else:
                non_presenting_symptom_group.append(Paragraph('No Non Presenting Symptoms Reported',
                                                    self.stylesheet['default']))
            non_presenting_symptom_group.extend([Spacer(1, 12)])
            target_elements.append(KeepTogether(non_presenting_symptom_group))
        else:
            symptom_group.append(Paragraph('No symptoms collected for this visit', self.stylesheet['default']))
            target_elements.append(KeepTogether(symptom_group))

    def _lab_creation(self):
        lab_group = [Spacer(1, 12), Paragraph('Labs', self.stylesheet['title']), Spacer(1, 12)]

        lab_data = []
        for lab in self.symptoms['labs']:
            lab_data.append([Paragraph(lab[3], self.stylesheet['sub_table_header']),
                            self.width_between_columns,
                            Paragraph(lab[2], self.stylesheet['default'])])

        if not lab_data:
            lab_group.append(Paragraph('No labs for this visit', self.stylesheet['default']))
        else:
            lab_table = Table(data=lab_data, colWidths=self._get_max_width(lab_data), hAlign='LEFT',
                              style=self.tablestylesheet['symptoms'])
            lab_group.append(lab_table)
        lab_group.append(Spacer(1, 12))

        return lab_group

    def _medication_instructions_creation(self, ttl, element_target):
        self.create_additional_notes(
            'medication_instructions',
            ttl,
            element_target
        )
        element_target.append(Spacer(1, 12))

    def _illness_creation(self, ttl, element_target, dta=None, symp_data=None, is_selected=False):
        illnesses_diagnosed = [Spacer(1, 12), Paragraph(ttl, self.stylesheet['title'])]
        if is_selected:
            illnesses_diagnosed = self.create_additional_notes('diagnostics', 'Diagnostic Notes', illnesses_diagnosed)
            # Add primary illness
            if dta:
                primary_illnesses = [i for i in dta if i['is_primary']]
                other_illnesses = copy.deepcopy(dta)
                if primary_illnesses:
                    p = primary_illnesses[0]
                    combined = [[Paragraph('Primary Diagnosis  -  ' + p['icd_cd'] + "  -  " + p['icd_desc'],
                                           self.stylesheet['bold'])]]
                    illnesses_diagnosed.append(Table(data=combined, colWidths=[480], hAlign='LEFT'))
                    illnesses_diagnosed.append(Spacer(1, 12))
                    other_illnesses.remove(p)

                if other_illnesses:
                    illnesses_diagnosed.append(Table(data=[[Paragraph("Other Diagnosis", self.stylesheet['bold'])]],
                                                     colWidths=[480], hAlign='LEFT'))
                    for d in other_illnesses:
                        illnesses_diagnosed.append(Table(data=[[Paragraph(d['icd_cd'] + '  -  ' + d['icd_desc'],
                                                                          self.stylesheet['default'])]],
                                                         colWidths=[480], hAlign='LEFT'))

        illnesses_diagnosed.append(Spacer(1, 12))

        if symp_data:
            for i in symp_data:
                combined = [[Paragraph(i[1] + ':    ' + i[2], self.stylesheet['default'])]]
                illnesses_diagnosed.append(Table(data=combined, colWidths=[480], hAlign='LEFT'))
            if not dta:
                illnesses_diagnosed.append(Spacer(1, 12))

        illnesses_diagnosed.append(Spacer(1, 18))

        if dta:
            for n, i in enumerate(dta):
                current_ill = []
                combined = [[Paragraph("{}     {}".format(i['icd_cd'], i['icd_desc']),
                                       self.stylesheet['bold'])]]
                current_ill.append(Table(data=combined, colWidths=[480], hAlign='LEFT'))
                current_ill.append(Paragraph('Contributors', self.stylesheet['header_center']))
                current_ill.append(Spacer(1, 12))
                contrib_data = []
                if len(i['contributors']) == 0:
                        non_contrib = Paragraph('Contributors not available for doctor added illnesses.',
                                                self.stylesheet['default_center'])
                        current_ill.append(non_contrib)
                        illnesses_diagnosed.append(KeepTogether(current_ill))
                else:
                    for j in i['contributors']:
                        if ' - Not Presenting' in j[0]:
                            contrib_data.append([Paragraph(j[0], self.stylesheet['italic']),
                                                 Paragraph(j[1], self.stylesheet['default_number_list'])])
                        else:
                            contrib_data.append([Paragraph(j[0], self.stylesheet['default']),
                                                 Paragraph(j[1], self.stylesheet['default_number_list'])])
                    contrib_split = self._table_splitter(contrib_data)
                    current_ill.append(Table(
                        data=contrib_split, colWidths=self.std_ill_col_widths,
                        hAlign='LEFT', style=self.tablestylesheet['left']
                    ))
                    illnesses_diagnosed.append(KeepTogether(current_ill))

                illnesses_diagnosed.append(Spacer(1, 12))
                illnesses_diagnosed.append(Spacer(1, 12))

        illnesses_diagnosed.append(self.basic_horz_line)
        element_target.extend(illnesses_diagnosed)

    def _treatment_creation(self, dta, ttl, element_target, is_selected=False):
        for n, i in enumerate(dta):
            treatments_assigned = []
            if n == 0:
                ptext = ttl
                treatments_assigned.append(Paragraph(ptext, self.stylesheet['title']))
                if is_selected:
                    notes_title = 'Treatments Notes'
                    treatments_assigned = self.create_additional_notes('treatments', notes_title, treatments_assigned)
                treatments_assigned.append(Spacer(1, 12))
                self._medication_instructions_creation('Medication Instructions', treatments_assigned)
            ptext = '<u>' + i['type'] + '</u>'
            treatments_assigned.append(Paragraph(ptext, self.stylesheet['header']))

            for j in i['names']:
                if i['type'] in ['Prescription Drugs', 'OTC Drugs']:

                    name_data = [[
                        Paragraph(j['name'], self.stylesheet['header_center']),
                        Paragraph('', self.stylesheet['default'])
                    ]]
                    if 'quantity' in j and j['quantity'] is not None:
                        name_data.append([
                            Paragraph('Quantity', self.stylesheet['sub_table_header']),
                            Paragraph(str(j['quantity']), self.stylesheet['default'])
                        ])
                    if 'strength' in j and j['strength'] is not None:
                        name_data.append([
                            Paragraph('Strength', self.stylesheet['sub_table_header']),
                            Paragraph(j['strength'], self.stylesheet['default'])
                        ])
                    if 'directionsString' in j and j['directionsString'] is not None:
                        name_data.append([
                            Paragraph('Directions', self.stylesheet['sub_table_header']),
                            Paragraph(j['directionsString'], self.stylesheet['default'])
                        ])
                    name_data.append([
                        Paragraph('Used to Treat', self.stylesheet['sub_table_header']),
                        Paragraph(', '.join(j['illnesses']), self.stylesheet['default'])
                    ])
                else:
                    name_data = [
                        [
                            Paragraph(j['name'], self.stylesheet['header_center']),
                            Paragraph('', self.stylesheet['default'])
                        ], [
                            Paragraph('Used to Treat', self.stylesheet['sub_table_header']),
                            Paragraph(', '.join(j['illnesses']), self.stylesheet['default'])
                        ]
                    ]

                treatments_assigned.append(Table(data=name_data, colWidths=self.std_trt_col_widths,
                                                 hAlign='LEFT', style=self.tablestylesheet['treatment_table']))

                treatments_assigned.append(Spacer(1, 12))
            treatments_assigned.append(Spacer(1, 12))
            element_target.append(KeepTogether(treatments_assigned))

    @staticmethod
    def _footer(canvas, doc):
        foot_font = 'Roboto'
        foot_font_size = 10
        foot_text = "Page %d" % doc.page

        foot_line_height = doc.bottomMargin * 0.5 + foot_font_size
        canvas.saveState()
        canvas.setFont(foot_font, foot_font_size)
        canvas.drawString(doc.width + doc.leftMargin - canvas.stringWidth(foot_text, foot_font, foot_font_size),
                          doc.bottomMargin * 0.5, foot_text)
        canvas.line(doc.leftMargin, foot_line_height, doc.width + doc.leftMargin, foot_line_height)
        canvas.restoreState()

    @staticmethod
    def _table_splitter(chart):
        num_rows = len(chart)
        num_cols = len(chart[0])
        left_side = int(num_rows / 2) + (num_rows % 2 > 0)
        new_chart = []
        for i in range(left_side):
            new_row = []
            for j in range(num_cols):
                new_row.append(chart[i][j])
            if i + left_side < num_rows:
                for k in range(num_cols):
                    new_row.append(chart[i + left_side][k])
            new_chart.append(new_row)
        return new_chart

    @staticmethod
    def _get_max_width(table):
        # update if doc width changed
        docwidth = 480
        table_width = len(table[0])
        max_values = [0] * table_width
        curr_val = 0
        for i in range(len(table)):
            for j in range(len(table[i])):
                if isinstance(table[i][j], Paragraph):

                    if len(table[i][j].frags) > 0:
                        additional_indent = table[i][j].style.leftIndent + table[i][j].style.rightIndent
                        curr_val = (stringWidth(table[i][j].text, table[i][j].frags[0].fontName,
                                                table[i][j].frags[0].fontSize) +
                                    additional_indent)

                if isinstance(table[i][j], Spacer):
                    curr_val = table[i][j].width
                if curr_val > max_values[j]:
                    max_values[j] = curr_val

        if sum(max_values) > docwidth:
            max_vl = max(max_values)
            max_vl_i = max_values.index(max_vl)
            max_values_dupe = list(max_values)
            max_values_dupe.remove(max_vl)
            new_val = docwidth - sum(max_values_dupe)
            max_values[max_vl_i] = new_val
        return max_values

    def _measurement_images(self, media_objects, target_list):
        for media in media_objects:
            image = self._generate_image(media['media'], 4 * inch, 4 * inch)
            if image:
                image_container = [
                    Paragraph(media['title'], self.stylesheet['title']),
                    image
                ]
                target_list.append(KeepTogether(image_container))
                target_list.append(Spacer(1, 24))
            else:
                warnings.warn("Invalid image type for {}".format(media['title']))

    @staticmethod
    def _generate_image(bytes_stream, max_width, max_height):
        try:
            image = PILImage.open(bytes_stream)
        except IOError:
            return None
        else:
            bytes_stream.seek(0)
            image_stretch = stretch_image_size(image.width, image.height, max_width, max_height)
            return Image(bytes_stream, image_stretch['width'], image_stretch['height'])

    def create_additional_notes(self, notes_type, text, target):
        notes = self.additional_info.get(notes_type, "")
        if notes is not None:
            notes = notes.replace("\n", "<br/>\n")
            text = '<u>{}</u>'.format(text)
            target.append(Paragraph(text, self.stylesheet['header']))
            target.append(Paragraph(notes, self.stylesheet['default']))
        return target

    def _add_ros_symptoms(self):
        # Display Review of Symptoms
        ros_group = [
            Spacer(1, 12),
            Paragraph("Review of Symptoms", self.stylesheet['title']),
            Spacer(1, 6),
        ]
        if self.ros_symptoms:
            ros_table_data = []
            for group in sorted(self.ros_symptoms.keys()):
                content = sorted(['(A) {}'.format(s[3]) for s in self.ros_symptoms[group] if s[1]])
                content += sorted(['(D) {}'.format(s[3]) for s in self.ros_symptoms[group] if not s[1]])
                ros_table_data.append(
                    [Paragraph('{}: '.format(group), self.stylesheet['table_header']),
                     self.width_between_columns,
                     Paragraph(', '.join(content), self.stylesheet['default'])],
                )

            ros_table = Table(
                data=ros_table_data, colWidths=self._get_max_width(ros_table_data),
                hAlign='LEFT', vAlign='TOP', style=self.tablestylesheet['left'])
            ros_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            ros_group.append(ros_table)
            ros_group.append(Spacer(1, 6))
        else:
            ros_group.append(Paragraph('No symptoms for this visit', self.stylesheet['default']))

        ros_group.append(Spacer(1, 12))
        self.Elements.append(KeepTogether(ros_group))
