from os import getenv
from neo4jrestclient.client import GraphDatabase
from pandas import DataFrame

from pdf_generator.utils import time_convert

SYMPTOM_BLACKLIST = [
    None,
    'SYMPT0000001',
    'SYMPT0000002',
    'SYMPT0000004',
    'SYMPT0000005',
    'SYMPT0000006',
    'SYMPT0000007',
    'SYMPT0000008',
    'SYMPT0000009',
    'SYMPT0000010',
    'SYMPT0000097',
    'SYMPT0000234',
    'SYMPT0000998',
    'SYMPT0001218',
    'SYMPT0001301',
    'SYMPT0009999',
]

POTENTIAL_MEASUREMENTS = [
    'SYMPT0001328',
    'SYMPT0001981',
    'SYMPT0001982',
    'SYMPT0001983',
    'SYMPT0002001',
    'SYMPT0002007',
    'SYMPT0002008',
]

# need to manually change some values for BP and diabetes:
bp_name_map = {
    'type_1': 'Type 1',
    'type_2': 'Type 2',
    'hyper_stage_1': 'Hypertension Stage 1',
    'hyper_stage_2': 'Hypertension Stage 2',
    'hyper_crisis': 'Hypertensive Crises',
    'hyper_crises': 'Hypertensive Crises',

}


GDB_Q_GET_SYMPTOM_ICDS = """Match(s:SymptomTemplate) where length(s.ICDRCode) > 1 with s optional 
                            Match (i: Illnesss{icd10Code : s.ICDRCode})  return s.code, s.name, s.ICDRCode, i.name"""


def connect_to_gdb():
    GDB_URL = getenv('GDB_URL')
    GDB_USER = getenv('GDB_USERNAME')
    GDB_PASS = getenv('GDB_PASSWORD')

    return GraphDatabase(GDB_URL, username=GDB_USER, password=GDB_PASS)


def get_symptom_icds():
    graph_db = connect_to_gdb()
    symptomICDLU_query = graph_db.query(q=GDB_Q_GET_SYMPTOM_ICDS)
    symptomICDLU = DataFrame(
        [i for i in symptomICDLU_query], columns=['symptomCode', 'symptomName', 'icdCode', 'icdName']
    )
    symptomICDLU.set_index('symptomCode', inplace=True, drop=True)

    return symptomICDLU


def parse_symptoms(symptoms):
    symptom_icds = get_symptom_icds()

    symptoms_with_icds = []

    presenting_symptoms = []
    non_presenting_symptoms = []

    symptom_group_order_template = ['General', 'Behaviour', 'behavior' 'Neurological', 'Measurements', 'Physical']
    symptom_keys = symptoms.keys()

    # Place existing symptoms first in list following order above
    symptom_group_order = [i for i in symptom_group_order_template if i in symptom_keys]
    # Add remaining present groups
    symptom_group_order.extend([i for i in symptoms.keys() if i not in symptom_group_order])

    for group in symptom_group_order:
        for symptom in symptoms.get(group, []):
            symptom_id, response, value, name, _ = symptom
            if not response:
                non_presenting_symptoms.append(name)
            else:
                # Capture symptoms with ICD codes
                if symptom_id in list(symptom_icds.index):
                    # Initial '' to keep same format as icds
                    symptoms_with_icds.append(
                        ['', symptom_icds.at[symptom_id, 'icdCode'], symptom_icds.at[symptom_id, 'symptomName']]
                    )

                presenting_symptoms.append([name, value, 'sub-heading'])

    return_symptoms = {
        'presenting': presenting_symptoms,
        'not_presenting': list(dict.fromkeys(non_presenting_symptoms)),
    }

    return return_symptoms, symptoms_with_icds


def is_skip_symptom(symptom_id, response, gender):
    # Even though response should be str, it comes in as bool all too often
    if response == 'skip':
        return True

    if symptom_id in SYMPTOM_BLACKLIST:
        return True

    # SYMPT0000213 = pregnancy
    if symptom_id == 'SYMPT0000213' and gender == 'male':
        return True


def parse_triage(triage, patient_history, patient_gender, symptom_data):
    measurements_taken = []
    symptom_ids = {'General': []}

    for item in triage:
        symptom_id = item.get('symptomId', '')

        response = str(item.get('response', '')).lower()
        # Negative response should be boolean to facilitate logic
        if response in ['false', '']:
            response = False

        if is_skip_symptom(symptom_id, response, patient_gender):
            continue

        values = item.get('values', [])

        symptom_name = item.get('symptomName', '')
        if symptom_name in bp_name_map.keys():
            symptom_name = bp_name_map[symptom_name]

        symptom_group = item.get('symptomGroup', '')

        if symptom_id in POTENTIAL_MEASUREMENTS:
            measurements_taken.append(symptom_name)

        # Parse health history categories
        lookup_category = '_'.join(item.get('categoryName', '').split(' ')).lower()
        if lookup_category in patient_history.keys() and response == 'true':
            if not any(symptom_name.lower() in s.lower() for s in patient_history[lookup_category]):
                patient_history[lookup_category].append(symptom_name)

        # Initialize group list if it does not exist.
        if symptom_group not in symptom_ids.keys():
            symptom_ids[symptom_group] = []

        normalized_symptom = [symptom_id, response, '', symptom_name,
                              symptom_data.get(symptom_id, {}).get('logicalGroupNames', [])  # ROS Group
                              ]
        # number = ''
        # descriptor = ''

        # TODO: Figure out if this comes from triage at all.
        # SYMPT0000009 = time since last drink, parse and continue
        if symptom_id == 'SYMPT0000009' and response:
            time = time_convert(values[0])
            normalized_symptom[2] = '{}{}'.format(time[0], time[1])
            if normalized_symptom not in symptom_ids[symptom_group]:
                symptom_ids[symptom_group].append(normalized_symptom)
        else:
            # values are an array of arrays because of legacy reasons, they have
            # been unpacked at this point so every symptom will have only one
            # array acting as a descriptor.
            # Labs will have descriptor in position 0, may be displayed with a
            # response of 'false' and must be displayed descriptor - value
            # while the rest of the symptoms are the opposite and false responses
            # are not described, only the name is displayed.
            if values and values[0]:
                for i, val in enumerate(values[0]):
                    if not isinstance(val, str):
                        values[0][i] = '' if val is None else str(val)
                lab_desc, number, descriptor = values[0]
                if symptom_group == 'Labs':
                    if not response:
                        normalized_symptom[1] = 'false'
                    measurement = '' if item.get('measurement') is None else str(item.get('measurement'))
                    if measurement and lab_desc and measurement != lab_desc:
                        normalized_symptom[2] = '{} - {}'.format(lab_desc, measurement)
                    else:
                        normalized_symptom[2] = lab_desc if lab_desc else measurement
                elif response:
                    if number and descriptor:
                        normalized_symptom[2] = '{} - {}'.format(number, descriptor)
                    else:
                        normalized_symptom[2] = descriptor if descriptor else number

        if normalized_symptom not in symptom_ids[symptom_group]:
            symptom_ids[symptom_group].append(normalized_symptom)

    # Removes labs before regular symptom parsing.
    lab_symptoms = symptom_ids.pop('Labs', [])

    symptoms, symptoms_with_icds = parse_symptoms(symptom_ids)

    symptoms['labs'] = lab_symptoms

    return symptoms, symptoms_with_icds, measurements_taken, _compose_ros_symptoms(symptom_ids, symptom_data, triage)


def _compose_ros_symptoms(symptom_ids, symptom_data, triage):
    """
    :param symptom_ids:
    :param symptom_data:
    :type symptom_data: dict
    :return:
    """
    ros_symptoms = {}

    def __add_to_ros_group(_group, _symptom, remove_basic=False):
        if remove_basic:
            _symptom[3] = _symptom[3].replace("Basic ", "")
        if _group in ros_symptoms.keys():
            ros_symptoms[_group].append(_symptom)
        else:
            ros_symptoms[_group] = [_symptom]

    # Get all symptoms as a list
    symptom_ids_list = []
    for g in symptom_ids:
        symptom_ids_list += symptom_ids[g]

    for symptom in symptom_ids_list:
        for g in symptom[4]:
            if str(g).startswith('ROS-'):
                __add_to_ros_group(g[4:], symptom)

        # BAK-2669
        symptom_id = symptom[0]
        _symptom_detail = symptom_data.get(symptom_id, {})
        symptom_name = _symptom_detail.get('symptomName', '')
        if symptom_name.startswith('Basic '):
            if _symptom_detail.get("symptomGroup") == "Pain/Swelling":
                if "pain" in symptom_name.lower():
                    # Get Pain Location symptom
                    for _id, s in symptom_data.items():
                        if s.get('categoryName') == _symptom_detail.get('categoryName') and \
                                'location' in s.get('symptomName', '').lower():
                            if _id in [ss.get('symptomId') for ss in triage]:
                                loc_symptom = [ss for ss in triage if ss.get('symptomId') == _id][0]
                                if loc_symptom['response'] and loc_symptom['values'] and loc_symptom['values'][0][0]:
                                    symptom[3] = symptom[3] + ", " + loc_symptom['values'][0][0]
                                    __add_to_ros_group('MusculoSkeletal', symptom, remove_basic=True)
                elif 'swelling' in symptom_name.lower():
                    __add_to_ros_group('MusculoSkeletal', symptom, remove_basic=True)
                else:
                    pass

        if "itch" in symptom_name:
            __add_to_ros_group('MusculoSkeletal', symptom, remove_basic=True)

    return ros_symptoms
