import shutil
import os
from git import Repo
from django.conf import settings
from django.db.models import Q
import subprocess
import json
from ..models import Language, ApplicationString, ApplicationStringsTranslation
from ..apps import TranslateConfig

BASE_DIR = str(settings.BASE_DIR)
APP_NAME = TranslateConfig.name

def update_translation_strings():
    try:
        shutil.rmtree(BASE_DIR + f'/{APP_NAME}/temp/frontendFetch')
        shutil.rmtree(BASE_DIR + f'/{APP_NAME}/temp/extractLang')
        os.mkdir(BASE_DIR + f'/{APP_NAME}/temp/extractLang')
    except FileNotFoundError:
        pass
    Repo.clone_from(settings.GIT_URL, BASE_DIR + f'/{APP_NAME}/temp/frontendFetch')
    """
        Run this command to get the latest translation strings from the frontend repo
        npx --yes @formatjs/cli extract 'src/**/*.(js|jsx|ts|tsx)' --ignore='**/*.d.ts' --out-file extractLang/en.json --id-interpolation-pattern '[sha512:contenthash:base64:6]
    """
    result = subprocess.run(['npx', '--yes', '@formatjs/cli', 'extract', f'{BASE_DIR}/{APP_NAME}/tmp/frontendFetch/src/**/*.(js|jsx|ts|tsx)', '--ignore=\'**/*.d.ts\'', '--out-file', f'{BASE_DIR}/{APP_NAME}/temp/extractLang/en.json', '--id-interpolation-pattern', '[sha512:contenthash:base64:6]'])
    """
        Check if the command was successful
    """
    if result.returncode != 0:
        raise Exception('Error while extracting translation strings')
    """
        Read the extracted translation strings
    """
    with open(f'{BASE_DIR}/{APP_NAME}/temp/frontendFetch/extractLang/en.json', 'r') as f:
        data = json.load(f)
    try:
        shutil.rmtree(BASE_DIR + f'/{APP_NAME}/temp/frontendFetch')
        shutil.rmtree(BASE_DIR + f'/{APP_NAME}/temp/extractLang')
    except FileNotFoundError:
        pass
    """
        Data structure:
        {
            "formatJsId": {
                "defaultMessage": "Default message",
                "description": "Description"
            }
        }

    """

    for formatjs_id, translation_string in data.items():
        try:
            translation_string = ApplicationString.objects.get(formatjs_id=formatjs_id)
        except ApplicationString.DoesNotExist:
            translation_string = ApplicationString(
                formatjs_id=formatjs_id,
                default_message=translation_string.get('defaultMessage') or 'ERROR',
                description=translation_string.get('description'),
            )
            translation_string.save()

            ApplicationStringsTranslation(
                translation_string=translation_string,
                language=Language.objects.get(code='en-US'),
                string=translation_string.default_message,
                is_approved=False
            ).save()

            for other_language in Language.objects.exclude(code='en-US'):
                ApplicationStringsTranslation(
                    translation_string=translation_string,
                    language=other_language,
                    string='',
                    is_approved=False
                ).save()
    
    for application_string in ApplicationString.objects.all():
        if application_string.formatjs_id not in data.keys():
            application_string.delete()
