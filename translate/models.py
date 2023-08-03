from django.db import models
from .apps import TranslateConfig

APP_NAME = TranslateConfig.name

TARGET_TYPE_CHOICES = [
        ('application_string', 'Application String'),
        ('graphql_enum_value', 'Graphql Enum Value')
]

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Language(TimeStampMixin):

    CODE_CHOICES = [
        ('en-US', 'English'),
        ('fr-CA', 'French (Canada)'),
        ('fa-IR', 'Persian (Iran)'),
        ('he-IL', 'Hebrew'),
        ('pt-BR', 'Portuguese (Brazil)'),

    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, choices=CODE_CHOICES, unique=True)

    def __str__(self):
        return self.name

    
class GraphqlEnumValue(TimeStampMixin):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return  f'/{APP_NAME}/graphqlenumvalue/{self.id}/change'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'enum item'
        verbose_name_plural = '2. Enum Items'


class GraphqlEnum(TimeStampMixin):
    name = models.CharField(max_length=100)
    values = models.ManyToManyField(GraphqlEnumValue)

    def __str__(self):
        return self.name
    

class GraphqlEnumValueTranslation(TimeStampMixin):
    enum_value = models.ForeignKey(GraphqlEnumValue, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    string = models.CharField(max_length=255, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.string or "Not translated: " + self.enum_value.name



class ApplicationString(TimeStampMixin):
    formatjs_id = models.CharField(max_length=100, unique=True)
    # default_message = models.CharField(max_length=255)
    default_message = models.TextField()
    # description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_special_char = models.BooleanField(default=False)

    get_en_translation = lambda self: ApplicationStringsTranslation.objects.get(translation_string=self, language__code='en-US')
    get_en_translation.short_description = 'English translation'
    get_en_translation.admin_order_field = 'applicationstringstranslation__string'

    get_fr_translation = lambda self: ApplicationStringsTranslation.objects.get(translation_string=self, language__code='fr-CA')
    get_fr_translation.short_description = 'French translation'
    get_fr_translation.admin_order_field = 'applicationstringstranslation__string'

    def __str__(self):
        return self.default_message + ' (' + self.formatjs_id + ')'

    class  Meta:
        verbose_name = 'application String'
        verbose_name_plural = '1. Application Strings'

class ApplicationStringsTranslation(TimeStampMixin):
    translation_string = models.ForeignKey(ApplicationString, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    # string = models.CharField(max_length=255, blank=True, default='')
    string = models.TextField(blank=True, default='')
    is_approved = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['translation_string', 'language'], name='unique_translation_string_language')
        ]
        ordering = ['translation_string__formatjs_id', 'language__code']


    def __str__(self):
        return self.string


class AutoTranslationLog(TimeStampMixin):
    TARGET_TYPE_CHOICES = TARGET_TYPE_CHOICES
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    total_translated = models.IntegerField(default=0)
    target_type = models.CharField(max_length=100, choices=TARGET_TYPE_CHOICES, default=TARGET_TYPE_CHOICES[0][0])



    def __str__(self):
        return f'{self.total_translated} strings translated from {self.start_time} to {self.end_time}'


class AutoPushLog(TimeStampMixin):
    TARGET_TYPE_CHOICES = TARGET_TYPE_CHOICES
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_success = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    target_type = models.CharField(max_length=100, choices=TARGET_TYPE_CHOICES, default=TARGET_TYPE_CHOICES[0][0])


class ManualPushRequest(TimeStampMixin):
    TARGET_TYPE_CHOICES = TARGET_TYPE_CHOICES
    start_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_success = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    target_type = models.CharField(max_length=100, choices=TARGET_TYPE_CHOICES, default=TARGET_TYPE_CHOICES[0][0])


    class Meta:
        verbose_name = 'Manually create pull request'
        verbose_name_plural = 'Manually create pull request'

class ManualTranslateRequest(TimeStampMixin):
    TARGET_TYPE_CHOICES = TARGET_TYPE_CHOICES
    start_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_success = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    target_type = models.CharField(max_length=100, choices=TARGET_TYPE_CHOICES, default=TARGET_TYPE_CHOICES[0][0])


    class Meta:
        verbose_name = 'Manually run auto translate'
        verbose_name_plural = 'Manually run auto translate'

class CustomKey(TimeStampMixin):
    formatjs_id = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.formatjs_id
    

class CustomKeyTranslation(TimeStampMixin):
    custom_key = models.ForeignKey(CustomKey, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    string = models.CharField(max_length=255, blank=True, default='')


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['custom_key', 'language'], name='unique_custom_key_language')
        ]


    def __str__(self):
        return self.string




