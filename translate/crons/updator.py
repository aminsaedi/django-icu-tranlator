import shutil
from git import Repo
import requests
import datetime
import json
import subprocess
from django.conf import settings
from ..apps import TranslateConfig
from ..models import ApplicationStringsTranslation, AutoPushLog, Language, GraphqlEnumValueTranslation, CustomKeyTranslation

BASE_DIR = str(settings.BASE_DIR)
APP_NAME = TranslateConfig.name

BITBUCKET_URL, BITBUCKET_USERNAME, BITBUCKET_PASSWORD = settings.BITBUCKET_URL, settings.BITBUCKET_USERNAME, settings.BITBUCKET_PASSWORD


def generate_json_for_language(lang_code: str) -> str:
    """
    Generate a json file for the language
    :param lang_code: language code
    :return: None
    """

    lang = Language.objects.get(code=lang_code)
    strings = ApplicationStringsTranslation.objects.filter(language=lang)

    json_dict = {}

    for string in strings:
        json_dict[string.translation_string.formatjs_id] = string.string if string.string else ''

    return json.dumps(json_dict, ensure_ascii=False, indent=4)


def create_pull_request(source_branch: str, title: str) -> bool:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {'title': title, 'description': '-', 'source': {
        'branch': {'name': source_branch}}, 'destination': {'branch': {'name': 'master'}}}
    response = requests.post(BITBUCKET_URL, headers=headers, json=data, auth=(
        BITBUCKET_USERNAME, BITBUCKET_PASSWORD))
    if response.status_code != 201:
        raise Exception('Error while creating pull request' +
                        str(response.text) + str(response.status_code))


def create_pull_request_for_strings():
    log = AutoPushLog.objects.create(
        start_time=datetime.datetime.now(),
    )
    log.save()
    try:
        try:
            shutil.rmtree(BASE_DIR + f'/{APP_NAME}/temp/frontendUpdate')
        except:
            pass

        Repo.clone_from(settings.GIT_URL, BASE_DIR +
                        f'/{APP_NAME}/temp/frontendUpdate')

        for lang in Language.objects.all():
            with open(f'{BASE_DIR}/{APP_NAME}/temp/frontendUpdate/downloadLang/{lang.code}.json', 'w') as f:
                f.write(generate_json_for_language(lang.code))

        # run ./compileLang.sh inside the frontendUpdate folder
        result = subprocess.run(['./compileLang.sh'],
                                cwd=f'{BASE_DIR}/{APP_NAME}/temp/frontendUpdate')
        if result.returncode != 0:
            raise Exception(
                'Error while compiling translation strings' + str(result.stdout))

        repo = Repo(f'{BASE_DIR}/{APP_NAME}/temp/frontendUpdate')

        # if number of files in git status is 0, then there are no changes
        result = [item.a_path for item in repo.index.diff(None)]
        if len(result) == 0:
            log.is_success = True
            log.end_time = datetime.datetime.now()
            log.description = 'No changes in translation strings'
            log.save()
            print('No changes in translation strings')
            return
        # create a new branch in this format update-lang/YYYY-MM-DD-HH-MM-SS

        branch_name = f'update-lang/{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'

        repo.create_head(branch_name)

        # checkout to the new branch
        repo.git.checkout(branch_name)

        # add all files
        repo.git.add('--all')

        # commit
        repo.git.commit('-m', 'Automatic strings update on ' +
                        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

        # set upstream and push
        result = repo.git.push('--set-upstream', 'origin', branch_name)

        # create a pull request
        create_pull_request(branch_name, 'Automatic strings update on ' +
                            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

        try:
            shutil.rmtree(BASE_DIR + f'/{APP_NAME}/temp/frontendUpdate')
        except:
            pass

        log.is_success = True
        log.end_time = datetime.datetime.now()
        log.description = 'Translation strings updated successfully'
        log.save()
    except Exception as e:
        log.is_success = False
        log.end_time = datetime.datetime.now()
        log.description = str(e)
        log.save()
        print(e)


def create_pull_request_for_enums():
    log = AutoPushLog.objects.create(
        start_time=datetime.datetime.now(),
        target_type=AutoPushLog.TARGET_TYPE_CHOICES[1][0]
    )
    log.save()

    try:

        try:
            shutil.rmtree(BASE_DIR + f'/{APP_NAME}/temp/frontendEnum')
        except:
            pass

        Repo.clone_from(settings.GIT_URL, BASE_DIR +
                        f'/{APP_NAME}/temp/frontendEnum')

        #  DO THE REST HERE
        for lang in Language.objects.all():
            all_enums = GraphqlEnumValueTranslation.objects.filter(
                language=lang)
            json_dict = {}
            for enum in all_enums:
                json_dict[enum.enum_value.name] = enum.string if enum.string else ''

            # all custom keys
            all_customs = CustomKeyTranslation.objects.filter(language=lang)
            for custom in all_customs:
                json_dict[custom.custom_key.formatjs_id] = custom.string if custom.string else ''

            # also the language it self should be in the enums list
            json_dict[lang.code] = lang.name
            with open(f'{BASE_DIR}/{APP_NAME}/temp/frontendEnum/downloadLang/enums/{lang.code}.json', 'w') as f:
                f.write(json.dumps(json_dict, ensure_ascii=False, indent=4))

        # run ./compileLang.sh inside the frontendUpdate folder
        result = subprocess.run(
            ['./compileLang.sh'], cwd=f'{BASE_DIR}/{APP_NAME}/temp/frontendEnum')

        if result.returncode != 0:
            raise Exception(
                'Error while compiling translation strings' + str(result.stdout))

        repo = Repo(f'{BASE_DIR}/{APP_NAME}/temp/frontendEnum')

        # if number of files in git status is 0, then there are no changes
        result = [item.a_path for item in repo.index.diff(None)]
        if len(result) == 0:
            log.is_success = True
            log.end_time = datetime.datetime.now()
            log.description = 'No changes in translation strings'
            log.save()
            print('No changes in translation strings')
            return
        # create a new branch in this format update-lang/YYYY-MM-DD-HH-MM-SS

        branch_name = f'update-enum/{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'

        repo.create_head(branch_name)

        # checkout to the new branch
        repo.git.checkout(branch_name)

        # add all files
        repo.git.add('--all')

        # commit
        repo.git.commit('-m', 'Automatic enums update on ' +
                        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

        # set upstream and push
        result = repo.git.push('--set-upstream', 'origin', branch_name)

        # create a pull request
        create_pull_request(branch_name, 'Automatic enums update on ' +
                            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

        try:
            shutil.rmtree(BASE_DIR + f'/{APP_NAME}/temp/frontendEnum')
        except:
            pass

        log.is_success = True
        log.end_time = datetime.datetime.now()
        log.description = 'Translation strings updated successfully'
        log.save()
    except Exception as e:
        log.is_success = False
        log.end_time = datetime.datetime.now()
        log.description = str(e)[:200]
        log.save()
        raise e
