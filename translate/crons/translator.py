from deep_translator import GoogleTranslator
from datetime import datetime
from django.db.models import Q
from ..models import ApplicationStringsTranslation, AutoTranslationLog, GraphqlEnumValueTranslation


def get_target_lang(full_lang_code):
    """
    Get the source language from the full language code
    :param full_lang_code: full language code
    :return: source language
    """

    if full_lang_code == 'he-IL':
        return 'hebrew'

    return full_lang_code.split('-')[0]


def translate_all_strings():
    log = AutoTranslationLog(
        start_time=datetime.now(),
        total_translated=0
    )
    log.save()

    total = 0
    for string in ApplicationStringsTranslation.objects.filter(translation_string__is_special_char=False, is_approved=False, string='').exclude(language__code='en-US'):
        string.string = GoogleTranslator(source='en', target=get_target_lang(
            string.language.code)).translate(string.translation_string.default_message)
        string.save()
        total += 1
        log.total_translated = total
        log.save()

    for string in ApplicationStringsTranslation.objects.filter(translation_string__is_special_char=True, is_approved=False).exclude(language__code='en-US'):
        string.string = ApplicationStringsTranslation.objects.get(
            translation_string=string.translation_string, language__code='en-US').string
        string.save()

    log.end_time = datetime.now()
    log.total_translated = total
    log.save()


def translate_all_enums():
    log = AutoTranslationLog(
        start_time=datetime.now(),
        total_translated=0,
        target_type=AutoTranslationLog.TARGET_TYPE_CHOICES[1][0]
    )
    log.save()

    total = 0
    for enum in GraphqlEnumValueTranslation.objects.filter(is_approved=False, string='').exclude(language__code='en-US'):
        english_translation = GraphqlEnumValueTranslation.objects.get(
            enum_value=enum.enum_value, language__code='en-US')
        enum.string = GoogleTranslator(source='en', target=get_target_lang(
            enum.language.code)).translate(english_translation.string)
        enum.save()
        total += 1
        log.total_translated = total
        log.save()

    log.end_time = datetime.now()
    log.total_translated = total
    log.save()
