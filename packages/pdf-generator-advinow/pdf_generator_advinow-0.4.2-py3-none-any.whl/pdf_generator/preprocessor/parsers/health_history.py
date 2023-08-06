from collections import defaultdict
from datetime import datetime

from pdf_generator.preprocessor.parsers.triage import connect_to_gdb

CATEGORY_MAP = {
    'Medications': 'medications',
    'Allergies': 'allergies',
    'Medication Allergies': 'medication_allergies',
    'Immunizations': 'immunizations',
    'Surgical History': 'surgical_history',
    'Packs Per Day': 'packsPerDay',
    'Drinks Per Day': 'drinksPerDay',
    'Caffeine Drinks Per Day': 'caffeinePerDay',
    'Caffeine User': 'caffeineUser',
    'Alcohol User': 'alcoholUser'
}


SOCIAL_VALUES = ['Packs Per Day', 'Drinks Per Day', 'Caffeine Drinks Per Day', 'Caffeine User', 'Alcohol User']


GDB_Q_GET_ILLNESSNAME_BY_ICDS = """MATCH(ill:MITA_Illness) where ill.icd10Code in {} with ill 
                                    return ill.name, ill.icd10Code"""


def get_illness_name_by_icd_codes(icd_codes):
    graph_db = connect_to_gdb()
    illnesses = graph_db.query(q=GDB_Q_GET_ILLNESSNAME_BY_ICDS.format(icd_codes))
    return [ill[0] for ill in illnesses]


def get_correct_noun_form(noun, ending, number):
    return noun if str(number) == '1' else noun + ending


def parse_social_history(health_history):
    alcohol_desc = 'Patient did not report a last alcoholic drink.'
    tobacco_desc = 'Patient is not and has never been a smoker.'
    caffeine_desc = 'Patient does not report consuming caffeine.'

    alc_per_day = health_history.get('drinksPerDay', '')
    alcohol_noun = get_correct_noun_form('drink', 's', alc_per_day)
    last_drink = health_history.get('lastDrinkDate', '')
    drinking_end = health_history.get('drinkingEndDate', '')
    drinking_start = health_history.get('drinkingStartDate', '')
    packs_per_day = health_history.get('packsPerDay', '')
    smoking_noun = get_correct_noun_form('pack', 's', packs_per_day)
    smoking_start = health_history.get('smokingStartDate', '')
    smoking_end = health_history.get('smokingEndDate', '')
    caff_per_day = health_history.get('caffeinePerDay', '')

    if last_drink and not drinking_end:
        alcohol_desc = (
            'Patient\'s last alcoholic drink was {}. '
            'Patient reports drinking {} {} per day.'.format(
                last_drink, alc_per_day, alcohol_noun))
    elif drinking_start and drinking_end:
        alcohol_desc = (
            'Patient started drinking on {} and stopped drinking on {}. '
            'Patient reports drinking {} {} per day.'.format(
                drinking_start, drinking_end, alc_per_day, alcohol_noun))

    if smoking_start and smoking_end:
        tobacco_desc = (
            'Patient started smoking on {} and stopped smoking on {}. '
            'Patient reports smoking {} {} per day.'.format(
                smoking_start, smoking_end, packs_per_day, smoking_noun))
    elif smoking_start and not smoking_end:
        tobacco_desc = (
            'Patient has been a smoker since {}. '
            'Patient reports smoking {} {} per day.'.format(
                smoking_start, packs_per_day, smoking_noun))

    if caff_per_day:
        noun = get_correct_noun_form('drink', 's', caff_per_day)
        caffeine_desc = (
            'Patient reports drinking {} caffeine {} per day.'.format(
                caff_per_day, noun))

    return {
        'alcohol': alcohol_desc,
        'tobacco': tobacco_desc,
        'caffeine': caffeine_desc,
    }


def parse_health_history(health_history):
    parsed_health_history = defaultdict(list)
    parsed_health_history.update({
        'medications': [],
        'allergies': [],
        'medication_allergies': [],
        'immunizations': [],
    })
    history_items = health_history.pop('historyItem', [])

    previous_history_codes = []

    for item in history_items:
        category = item['historyType']
        history_key = CATEGORY_MAP.get(category)
        raw_value = item.get('historyItem', '')

        if category in SOCIAL_VALUES:
            health_history[history_key] = raw_value

        else:
            parsed_value = None

            if item['itemType'] == 'family':
                history_key = 'family_history'
                parsed_value = '{} - {}'.format(category, item['familyRelationship'].title())

            elif not history_key:
                history_key = 'personal_history'
                if item['symptomID'] == 'SYMPT0002070':     # <= BAK-2653
                    # Use the ones in the current year only.
                    if datetime.today().year == datetime.strptime(item['dateDetected'], '%Y-%m-%d').year:
                        previous_history_codes.append(raw_value)
                    continue

                parsed_value = category
                if raw_value:
                    parsed_value = '{} - {}'.format(parsed_value, raw_value)

            parsed_health_history[history_key].append(parsed_value or raw_value)

    illness_data = get_illness_name_by_icd_codes(previous_history_codes)
    for illness in illness_data:
        parsed_health_history['personal_history'].append('Previous Visit History - {}'.format(illness))

    parsed_health_history.update(**parse_social_history(health_history))

    return parsed_health_history


def clean_patient_history(patient_history):
    for key, value in patient_history.items():
        if not value:
            patient_history[key] = ['No {} Reported'.format(' '.join([v.capitalize() for v in key.split('_')]))]
        else:
            # Symptoms can be in both the triage and history sections leading to a duplication.
            # Doing a type check to not affect alcohol, tobacco, and caffeine data.
            if isinstance(value, list):
                new_values = []
                for v in value:
                    if isinstance(v, str):
                        if not any(v.lower() in s.lower() for s in new_values if isinstance(s, str)):
                            new_values.append(v)
                    elif v not in new_values:
                        new_values.append(v)
                patient_history[key] = new_values

    return patient_history
