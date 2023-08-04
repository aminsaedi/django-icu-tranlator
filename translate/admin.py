from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from admin_auto_filters.filters import AutocompleteFilter
from django.utils.html import format_html_join
from django import forms


from .models import *


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name')


class ApplicationStringsTranslationsForm(forms.ModelForm):
    class Meta:
        model = ApplicationStringsTranslation
        fields = '__all__'
        widgets = {
            # Use TextInput widget for the TextField
            'string': forms.TextInput(attrs={'size': '100'}),
        }


class ApplicationStringsTranslationsAdmin(NestedStackedInline):
    model = ApplicationStringsTranslation
    form = ApplicationStringsTranslationsForm
    fk_name = 'translation_string'
    extra = 0
    fields = ('language', 'string', 'is_approved')
    readonly_fields = ('language', )

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


class ApplicationStringAdmin(NestedModelAdmin):
    model = ApplicationString
    inlines = [ApplicationStringsTranslationsAdmin]
    list_display = ('default_message', 'get_en_translation',
                    'get_fr_translation', 'description', 'is_special_char')
    search_fields = ('default_message', 'formatjs_id',
                     'applicationstringstranslation__string')
    list_filter = ('is_special_char',)
    readonly_fields = ('formatjs_id', 'default_message',
                       'description', 'is_special_char')


admin.site.register(ApplicationString, ApplicationStringAdmin)


@admin.register(ApplicationStringsTranslation)
class ApplicationStringsTranslationAdmin(admin.ModelAdmin):
    list_display = ('translation_string', 'language', 'string', 'is_approved')
    list_filter = ('language', 'is_approved')
    search_fields = ('translation_string__default_message', 'string')


@admin.register(AutoTranslationLog)
class AutoTranslationLogAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time',
                    'target_type', 'total_translated')

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(AutoPushLog)
class AutoPushLogAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'is_success',
                    'target_type', 'description')
    list_filter = ('is_success', 'target_type')
    search_fields = ('description',)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@admin.register(ManualTranslateRequest)
class ManualTranslateRequestAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'target_type',
                    'is_success', 'description')
    list_filter = ('is_success', 'target_type')
    search_fields = ('description',)
    readonly_fields = ('end_time', 'is_success', 'description')

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


@admin.register(ManualPushRequest)
class ManualPushRequestAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'target_type',
                    'is_success', 'description')
    list_filter = ('is_success', 'target_type')
    search_fields = ('description',)
    readonly_fields = ('end_time', 'is_success', 'description')

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


class GraphqlEnumValuesFilter(AutocompleteFilter):
    title = 'values'
    field_name = 'values'


@admin.register(GraphqlEnum)
class GraphqlEnumAdmin(admin.ModelAdmin):
    list_display = ('name', 'values_display')
    search_fields = ('name',)
    autocomplete_fields = ('values',)
    list_filter = (GraphqlEnumValuesFilter,)

    def values_display(self, obj: GraphqlEnum) -> str:
        return format_html_join(
            ' ',
            '<a href="{}">{}, </a>',
            ((value.get_absolute_url(), value.graphqlenumvaluetranslation_set.get(language__code="en-US").string)
             for value in obj.values.all())
        )

    def has_change_permission(self, request=None, obj=None) -> bool:
        return False

    def has_delete_permission(self, request=None, obj=None) -> bool:
        return False


@admin.register(GraphqlEnumValueTranslation)
class GraphqlEnumValueTranslationAdmin(admin.ModelAdmin):
    list_display = ('enum_value', 'language', 'string', 'is_approved')
    list_filter = ('language', 'is_approved')
    autocomplete_fields = ('enum_value',)
    search_fields = ('enum_value__name', 'string')


class GraphqlEnumValueTranslationNestedInline(NestedStackedInline):
    model = GraphqlEnumValueTranslation
    fk_name = 'enum_value'
    extra = 0
    fields = ('language', 'string', 'is_approved')
    readonly_fields = ('language', )

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


class GraphqlEnumValueInline(admin.TabularInline):
    model = GraphqlEnumValue.graphqlenum_set.through
    extra = 0

    readonly_fields = ('graphqlenum',)

    can_add = False
    can_delete = False


class GraphqlEnumSetFilter(admin.SimpleListFilter):
    title = 'enum'
    parameter_name = 'enum'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> list[tuple[str, str]]:
        return [(enum.id, enum.name) for enum in GraphqlEnum.objects.all()]

    def queryset(self, request: HttpRequest, queryset):
        if self.value():
            return queryset.filter(graphqlenum__id=self.value())


class GraphqlEnumValueAdmin(NestedModelAdmin):
    list_display = ('name', 'enum', 'english_translation',
                    'french_translation')
    search_fields = ('name', 'graphqlenumvaluetranslation__string')
    list_filter = (GraphqlEnumSetFilter,)
    readonly_fields = ('name',)

    inlines = [GraphqlEnumValueInline, GraphqlEnumValueTranslationNestedInline]

    def enum(self, obj: GraphqlEnumValue) -> str:
        return ', '.join([enum.name for enum in obj.graphqlenum_set.all()])
    enum.short_description = 'Used in'

    def english_translation(self, obj: GraphqlEnumValue) -> str:
        return obj.graphqlenumvaluetranslation_set.filter(language__code='en-US').get().string

    def french_translation(self, obj: GraphqlEnumValue) -> str:
        return obj.graphqlenumvaluetranslation_set.filter(language__code='fr-CA').get().string


admin.site.register(GraphqlEnumValue, GraphqlEnumValueAdmin)


@admin.register(CustomKeyTranslation)
class CustomKeyTranslationAdmin(admin.ModelAdmin):
    list_display = ('custom_key', 'language', 'string')
    list_filter = ('language', )
    autocomplete_fields = ('custom_key',)


class CustomKeyTranslationNestedInline(NestedStackedInline):
    model = CustomKeyTranslation
    fk_name = 'custom_key'
    extra = 0
    fields = ('language', 'string', 'is_approved')
    # readonly_fields = ('language', )

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


class CustomKeysAdmin(NestedModelAdmin):
    model = CustomKey
    inlines = [CustomKeyTranslationNestedInline]

    list_display = ('formatjs_id', 'english_translation', 'french_translation')
    search_fields = ('formatjs_id',)

    def english_translation(self, obj: CustomKey) -> str:
        return obj.customkeytranslation_set.filter(language__code='en-US').get().string

    def french_translation(self, obj: CustomKey) -> str:
        return obj.customkeytranslation_set.filter(language__code='fr-CA').get().string


admin.site.register(CustomKey, CustomKeysAdmin)
