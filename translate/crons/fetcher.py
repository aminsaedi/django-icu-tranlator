import shutil
import os
from git import Repo
from django.conf import settings
from django.db.models import Count
from django.db.models.functions import Lower
import subprocess
import json
from ..models import (
    Language,
    ApplicationString,
    ApplicationStringsTranslation,
    DuplicateString,
)
from ..apps import TranslateConfig

BASE_DIR = str(settings.BASE_DIR)
APP_NAME = TranslateConfig.name


def update_translation_strings():
    try:
        shutil.rmtree(BASE_DIR + f"/{APP_NAME}/temp/frontendFetch")
    except FileNotFoundError:
        pass
    Repo.clone_from(settings.GIT_URL, BASE_DIR + f"/{APP_NAME}/temp/frontendFetch")

    result = subprocess.run(
        ["./extract.sh"],
        cwd=f"{BASE_DIR}/{APP_NAME}/temp/frontendFetch",
        stdout=subprocess.PIPE,
    )
    """
        Check if the command was successful
    """
    if result.returncode != 0:
        raise Exception("Error while extracting translation strings")
    """
        Read the extracted translation strings
    """
    with open(
        f"{BASE_DIR}/{APP_NAME}/temp/frontendFetch/extractLang/en.json", "r"
    ) as f:
        data = json.load(f)
    try:
        shutil.rmtree(BASE_DIR + f"/{APP_NAME}/temp/frontendFetch")
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
            ApplicationString.objects.get(formatjs_id=formatjs_id)
        except ApplicationString.DoesNotExist:
            translation_string = ApplicationString(
                formatjs_id=formatjs_id,
                default_message=translation_string.get("defaultMessage") or "ERROR",
                description=translation_string.get("description"),
                is_special_char=translation_string.get("defaultMessage").count("{") > 0,
            )
            translation_string.save()

            ApplicationStringsTranslation(
                translation_string=translation_string,
                language=Language.objects.get(code="en-US"),
                string=translation_string.default_message,
                is_approved=False,
            ).save()

            for other_language in Language.objects.exclude(code="en-US"):
                ApplicationStringsTranslation(
                    translation_string=translation_string,
                    language=other_language,
                    string="",
                    is_approved=False,
                ).save()

    for application_string in ApplicationString.objects.all():
        if application_string.formatjs_id not in data.keys():
            print(application_string.formatjs_id + " deleted")
            application_string.delete()

    DuplicateString.objects.all().delete()

    duplicates = (
        ApplicationString.objects.annotate(message_lower=Lower("default_message"))
        .values("message_lower")
        .annotate(count=Count("message_lower"))
    )

    for duplicate in duplicates:
        if duplicate["count"] > 1:
            duplicate_string = DuplicateString(
                default_message=duplicate["message_lower"], count=duplicate["count"]
            )
            duplicate_string.save()
