from collections import defaultdict

from .parsers.patient_data import parse_visit_info, parse_patient_info
from .parsers.health_history import parse_health_history, clean_patient_history
from .parsers.measurements import parse_measurements
from .parsers.triage import parse_triage


class JSONPreprocessor:

    def __init__(self, **kwargs):
        self.doctor_notes = kwargs['doctor_notes']
        self.symptom_data = kwargs.get('symptom_data', {})
        self.physical_exam = []
        self.treatments_selected_formatted = None
        self.media = kwargs.get('media', [])
        self._parse_doctor_notes()

    def _parse_doctor_notes(self):
        self.visit_details = parse_visit_info(self.doctor_notes.get('visitInformation', {}))
        self.patient_details, self.contact_information = parse_patient_info(
            self.doctor_notes.get('patientInformation', {}))

        self.measurements, additional_media = parse_measurements(self.doctor_notes.get('measurements', {}))
        self.media.extend(additional_media)

        self.patient_history = parse_health_history(self.doctor_notes.get('patientHealthHistory', {}))
        # BAK-2127: Use the History object and then look for the symptom when not is found.
        if len(self.patient_history.get('allergies', [])) == 0:
            for s in self.doctor_notes.get('triage', []):
                if s['symptomId'] == 'SYMPT0000044':
                    self.patient_history['allergies'] = [v[0] for v in s['values'] if v[0]]
                    break

        self.symptoms, self.symptoms_with_icds, self.measurements_taken, self.ros_symptoms = parse_triage(
            triage=self.doctor_notes.get('triage', []),
            patient_history=self.patient_history,
            patient_gender=self.patient_details['gender'].lower(),
            symptom_data=self.symptom_data,
        )

        # Diagnostic Engine
        self.illnesses_selected = []
        icd_illnesses_not_displayed = []
        if self.doctor_notes.get('diagnosticEngine'):
            for item in self.doctor_notes['diagnosticEngine']:
                start_dict = {'icd_cd': str(item.get('icd10', '')), 'icd_desc': str(item.get('icdName', '')),
                              'is_primary': item.get('isPrimary', False)}
                contrib = []
                min_value = 0.010
                if item.get('isSelected'):
                    for contributor in item.get('contributors', []):
                        # this means values whose contribution is 0 is not displayed.  This is intended.
                        contrib_value = float(contributor.get('contribution', 0))
                        if contrib_value > min_value or contrib_value < - min_value:
                            contrib.append([str(contributor.get('symptomName')), contrib_value * 100.0])
                    start_dict['contributors'] = contrib
                    self.illnesses_selected.append(start_dict)

        self.illnesses_selected.sort(key=lambda v: v['icd_cd'])

        for illness in self.illnesses_selected:
            test_dict = defaultdict(int)
            for key, value in illness.get('contributors'):
                if key in self.symptoms['not_presenting']:
                    test_dict[key + ' - Not Presenting'] += value
                else:
                    test_dict[key] += value
            # the 90 is because there is a threshold of 90 that is set by the DE.  Want to keep that threshold
            # this is pretty arbitrary
            for key, value in test_dict.items():
                if value > 90:
                    test_dict[key] = 90
                if value < -90:
                    test_dict[key] = -90
            confidence = sorted(test_dict.items(), key=lambda v: abs(v[1]), reverse=True)
            confidence = [[k, "{0:.1f}".format(v) + '%'] for (k, v) in confidence]
            illness['contributors'] = confidence

        self.patient_history = clean_patient_history(self.patient_history)

        # Treatment Engine
        treatments_selected = []
        # these treatments should not be printed out as they are the defaults
        TREATMENT_BLACKLIST = ['INCOMPLETE', 'Not Needed', 'Normal Diet', 'No Restrictions', 'None Needed',
                               'Immediately', 'Return as needed']

        if self.doctor_notes.get('treatmentEngine'):
            for item in self.doctor_notes['treatmentEngine']:
                if item.get('icdCode', '') not in icd_illnesses_not_displayed:
                    for treatment in item.get('treatments', []):
                        for detail in treatment.get('details', []):
                            start_dict = {}
                            if detail.get('name', '') not in TREATMENT_BLACKLIST and detail.get('isSelected'):
                                start_dict['type'] = treatment.get('type', '')
                                start_dict['name'] = detail.get('name', '')
                                start_dict['illness'] = item.get('icdDesc', '')
                                treatments_selected.append(start_dict)

        treatments_selected_formatted_unordered = []
        for i in set([i.get('type', '') for i in treatments_selected]):
            start_dict = {'type': i, 'names': []}
            for j in set([j.get('name', '') for j in treatments_selected if j.get('type', '') == i]):
                next_dict = {'name': str(j), 'illnesses': []}
                if start_dict.get('type', '') in ['Prescription Drugs', 'OTC Drugs']:
                    if self.doctor_notes.get('drugInformation'):
                        for d in self.doctor_notes['drugInformation']:
                            if d['drugName'] == next_dict.get('name', ''):
                                next_dict['route'] = str(d.get('route', None))
                                next_dict['unit'] = str(d.get('unit', None))
                                next_dict['strength'] = str(d.get('strength', None))
                                next_dict['quantity'] = str(d.get('quantity', None))
                                next_dict['directionsString'] = str(d.get('directionsString', None))

                for k in set([k.get('illness', '') for k in treatments_selected if k.get('name', '') == j]):
                    next_dict['illnesses'].append(k)
                start_dict['names'].append(next_dict)
            treatments_selected_formatted_unordered.append(start_dict)

        treatment_order = {
            'Prescription Drugs': 1,
            'OTC Drugs': 2,
            'Labs': 3,
            'Imaging': 4,
            'Procedures': 5,
            'Diet': 6,
            'Activity': 7,
            'Physical Therapy': 8,
            'Counseling': 9,
            'Wound Care': 10,
            'Physical Exam': 11,
            'Return to Work/School Status': 12,
            'Discharge Disposition': 13
        }

        treatments_selected_formatted_unordered_types = [
            x for x in treatments_selected_formatted_unordered
            if isinstance(x.get('type'), str) and 'names' in x]

        self.treatments_selected_formatted = sorted(treatments_selected_formatted_unordered_types,
                                                    key=lambda x: treatment_order.get(x.get('type', ''), 1))

        additional_info_source = self.doctor_notes.get('additionalInformation', {})
        self.additional_info = {
            'notes': additional_info_source.get('additionalDoctorNotes'),
            'treatments': additional_info_source.get('treatmentDoctorNotes'),
            'diagnostics': additional_info_source.get('diagnosticDoctorNotes'),
            'medication_instructions': additional_info_source.get('medicationInstructions')
        }
        self.physical_exam = additional_info_source.get('physicalExam', [])

        if self.measurements.get('systolic'):
            systolic_value = self.measurements.get('systolic', {}).get('value', '0')
        else:
            systolic_value = None

        if self.measurements.get('diastolic'):
            diastolic_value = self.measurements.get('diastolic', {}).get('value', '0')
        else:
            diastolic_value = None

        if systolic_value is not None and diastolic_value is not None:
            self.measurements['blood_pressure'] = str(systolic_value) + '/' + str(diastolic_value) + ' mmHg'
        else:
            self.measurements['blood_pressure'] = 'Not Measured'

        if self.measurements.get('weight'):
            wgt = round(self.measurements.get('weight').get('value', '0'), 1)
            self.measurements['weight'] = str(wgt) + ' lbs'
        else:
            self.measurements['weight'] = 'Not Measured'

        if self.measurements.get('pulse'):
            self.measurements['pulse'] = str(self.measurements.get('pulse', {}).get('value', '0')) + ' bpm'
        else:
            self.measurements['pulse'] = 'Not Measured'

        if self.measurements.get('temperature'):
            temp = round(self.measurements.get('temperature', {}).get('value', '0'), 1)
            self.measurements['temperature'] = str(temp) + ' °F'
        else:
            self.measurements['temperature'] = 'Not Measured'

        if self.measurements.get('mean_arterial_pressure'):
            map_value = self.measurements.get('mean_arterial_pressure', {}).get('value', '0')
            self.measurements['mean_arterial_pressure'] = str(int(float(map_value)))
        else:
            self.measurements['mean_arterial_pressure'] = 'Not Measured'

        if self.measurements.get('blood_oxygen'):
            map_value = self.measurements.get('blood_oxygen', {}).get('value', '0')
            self.measurements['blood_oxygen'] = str(int(float(map_value))) + ' %'
        else:
            self.measurements['blood_oxygen'] = 'Not Measured'

        if self.measurements.get('height'):
            map_value = self.measurements.get('height', {}).get('value', '0')
            self.measurements['height'] = str(map_value) + ' inch'
        else:
            self.measurements['height'] = 'Not Measured'

        if self.measurements.get('respiratory_rate'):
            self.measurements['respiratory_rate'] = str(self.measurements['respiratory_rate'].get('value', 0))
        else:
            self.measurements['respiratory_rate'] = 'Not Measured'

    def get_notes_parsing_result(self):
        def _clean_symptoms(symptoms):
            return [[item[0], item[1]] for item in symptoms]

        def _clean_illness(illness):
            return {
                'icd_cd': illness.get('icd_cd'),
                'icd_desc': illness.get('icd_desc'),
                'contributors': [item[0] for item in illness.get('contributors', [])]
            }

        presenting_symptoms = _clean_symptoms(self.symptoms.get('presenting', []))
        not_presenting_symptoms = self.symptoms.get('not_presenting', [])
        selected_illnesses = [_clean_illness(illness) for illness in self.illnesses_selected] + [
            {
                'icd_cd': symptom[1],
                'icd_desc': symptom[2],
                'contributors': []
            } for symptom in self.symptoms_with_icds]
        allowed_measurements = {
            'blood_pressure',
            'weight',
            'pulse',
            'mean_arterial_pressure',
            'blood_oxygen',
            'temperature'
        }
        vitals = {key: value for key, value in self.measurements.items() if key in allowed_measurements}
        return {
            'visitDetails': self.visit_details,
            'patientDetails': self.patient_details,
            'contactInformation': self.contact_information,
            'vitals': vitals,
            'patientHistory': self.patient_history,
            'physicalExam': self.physical_exam,
            'presentingSymptoms': presenting_symptoms,
            'notPresentingSymptoms': not_presenting_symptoms,
            'illnessesSelected': selected_illnesses,
            'treatmentsSelected': self.treatments_selected_formatted,
            'potentialMeasurements': self.measurements_taken,
            'additionalInformation': self.additional_info
        }

    def has_diagnoses_and_treatments(self):
        return self.illnesses_selected and self.treatments_selected_formatted

    @staticmethod
    def _has_measurement(key, parsed_measurements):
        return key in parsed_measurements and parsed_measurements[key].get("value", 0) > 0

    def has_vitals_for_pdf(self):
        measurements = parse_measurements(self.doctor_notes.get('measurements', {}))[0]
        vitals_keys = ["pulse", "blood_oxygen", "mean_arterial_pressure",
                       "weight", "temperature", "height", "respiratory_rate"]
        has_blood_pressure = all(self._has_measurement(value, measurements) for value in ["systolic", "diastolic"])
        has_other_measurements = any(self._has_measurement(key, measurements) for key in vitals_keys)
        return has_blood_pressure or has_other_measurements
