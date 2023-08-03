import datetime
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import ApplicationStringsTranslation, Language, ManualPushRequest, GraphqlEnumValue, GraphqlEnum, GraphqlEnumValueTranslation, ManualTranslateRequest, CustomKey, CustomKeyTranslation
from .crons.updator import create_pull_request_for_strings, create_pull_request_for_enums
from .crons.translator import translate_all_enums,  translate_all_strings


@receiver(post_save, sender=Language)
def add_tranlsation_key_for_new_language(sender, instance, created, **kwargs):
    if created:
        all_strings = ApplicationStringsTranslation.objects.filter(
            language__code='en-US')

        ApplicationStringsTranslation.objects.bulk_create([
            ApplicationStringsTranslation(
                translation_string=string.translation_string,
                language=instance,
                string='',
                is_approved=False
            ) for string in all_strings
        ])

        all_enum_translations = GraphqlEnumValueTranslation.objects.filter(
            language__code='en-US')

        GraphqlEnumValueTranslation.objects.bulk_create([
            GraphqlEnumValueTranslation(
                enum_value=enum.enum_value,
                language=instance,
                string='',
                is_approved=False
            ) for enum in all_enum_translations
        ])


@receiver(post_save, sender=ManualPushRequest)
def run_push_request(sender, instance, created, **kwargs):
    if created:
        instance.description = 'Started pushing to frontend'
        instance.save()
        try:
            if instance.target_type == ManualPushRequest.TARGET_TYPE_CHOICES[0][0]:
                create_pull_request_for_strings()
            else:
                create_pull_request_for_enums()
        except Exception as e:
            instance.description = str(e)
            instance.is_success = False
            instance.save()
            return
        instance.end_time = datetime.datetime.now()
        instance.description = 'Pushed to frontend'
        instance.is_success = True
        instance.save()


@receiver(pre_delete, sender=GraphqlEnum)
def delete_enum(sender, instance, **kwargs):
    GraphqlEnumValue.objects.filter(graphqlenum=instance).delete()


@receiver(post_save, sender=ManualTranslateRequest)
def run_translate_request(sender, instance, created, **kwargs):
    if created:
        instance.description = 'Started translating'
        instance.save()
        try:
            if instance.target_type == ManualTranslateRequest.TARGET_TYPE_CHOICES[0][0]:
                translate_all_strings()
            else:
                translate_all_enums()
        except Exception as e:
            instance.description = str(e)
            instance.is_success = False
            instance.save()
            return
        instance.end_time = datetime.datetime.now()
        instance.description = 'Translated'
        instance.is_success = True
        instance.save()

@receiver(post_save, sender=CustomKey)
def add_tranlsation_key_for_new_custom_key(sender, instance, created, **kwargs):
    if created:
        all_languages = Language.objects.all()

        CustomKeyTranslation.objects.bulk_create([
            CustomKeyTranslation(
                custom_key=instance,
                language=lang,
                string='',
            ) for lang in all_languages
        ])