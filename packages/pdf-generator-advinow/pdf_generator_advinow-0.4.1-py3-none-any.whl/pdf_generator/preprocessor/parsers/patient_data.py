from datetime import datetime

from dateutil.parser import parse


def parse_visit_info(visit_information):
    parsed_info = {
        'doctor_name': visit_information.get('doctorName', ''),
        'location': visit_information.get('locationName', ''),
        'visit_reason': visit_information.get('detailVisitReason', ''),
        'formatted_date': '',
        'formatted_time': '',
    }

    kiosk_start = visit_information.get('kioskStartTime', '')
    if kiosk_start:
        kiosk_start_obj = parse(kiosk_start)
        parsed_info['formatted_date'] = datetime.strftime(kiosk_start_obj, '%Y-%m-%d')
        parsed_info['formatted_time'] = datetime.strftime(kiosk_start_obj, '%H:%M')

    return parsed_info


def parse_patient_info(patient_information):
    parsed_info = {
        'first_name': patient_information.get('firstName', '').capitalize(),
        'last_name': patient_information.get('lastName', '').capitalize(),
        'middle_name': patient_information.get('middleName', '').capitalize(),
        'gender': patient_information.get('gender', '').capitalize(),
        'birth_date': '',
        'ethnicity': '',
    }

    ethnicities = patient_information.get('ethnicity', '')
    if isinstance(ethnicities, list):
        ethnicities = ', '.join(ethnicities)
    parsed_info['ethnicity'] = str(ethnicities)

    birth_date = patient_information.get('birthDate')
    if birth_date:
        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
        diff = datetime.today() - birth_date_obj
        parsed_info['age_years'] = str(int(diff.days / 365.25))
        parsed_info['birth_date'] = datetime.strftime(birth_date_obj, '%Y-%m-%d')

    name_list = [parsed_info['first_name'], parsed_info['last_name']]

    middle_name = parsed_info.get('middle_name', '')
    if middle_name:
        name_list.insert(1, '%s.' % middle_name[0].capitalize())

    parsed_info['full_name'] = ' '.join(name_list)

    return parsed_info, patient_information.get('contactInformation', {})
