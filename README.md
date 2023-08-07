# TODO:
- [ ] Add the usage section
- [ ] Add the screenshots
- [ ] Add Docker setup section


# Django ICU translator

Django ICU Translator is a straightforward Django application designed for translating ICU format messages and GraphQL enums with ease.

## History

### Automatic text translation
During the development of a React.js project with react-intl for internationalization purposes, we encountered challenges with translating the application to different languages. The traditional approach of using free translation tools like Google Translate often resulted in inaccuracies, and we had to manually correct the translations which is very time consuming task and we couldn't afford it.

### Graphql enums translation
Our backend server utilizes GraphQL enums, which presented another translation challenge. Enum values needed to be mapped to properly translated strings in the frontend. However, some enum items were repeated across different enums, and changing the translation for one enum could inadvertently affect the translation for other usages. For example, translating BIRTH_DAY to Birth day in the CompareSourceEnum should be different from translating it to On birth day in the EvaluationBaseEnum. Managing these duplications became cumbersome, necessitating a tool to identify potential conflicts in enum translations. Additionally, the auto-translation challenge persisted for other languages.

```
enum CompareSourceEnum {
    BIRTH_DAY
    BIRTH_MONTH
    BIRTH_YEAR
}

enum EvaluationBaseEnum {
    BIRTH_DAY
    MONTH_FOLLOWING_BIRTHDAY
    SOME_OTHER_OPTIONS
}
```

## Solution
To address these issues, I developed an app that provides the following solutions:

1. **Automatic Text Translation**: The app automatically extracts all internationalization strings used in your application (for `react-intl`) using cron jobs. It adds them to the database and then automatically runs Google Translate to translate any unconfirmed strings into the defined languages. The app won't overwrite items with confirmed, approved translations.

2. **Graphql Enums Translation**: The app extracts and translates the enums used in the server. It accomplishes this by using a GraphQL query to fetch all the enums defined in the server and then stores them in the database. The same automatic translation process is applied to these enums for your defined languages.

> Additionally, the app offers a feature to create a pull request on your Bitbucket repository with the changes to your ICU files (detailed in the [Usage section](#usage)).


## Requirements

Before installing the app, ensure that your frontend repository is compatible with it. The app executes the following command to extract intl strings from your frontend repository (assuming you use `react-intl`):
```bash
npx --yes @formatjs/cli extract 'src/**/*.(js|jsx|ts|tsx)' --ignore='**/*.d.ts' --out-file extractLang/en.json --id-interpolation-pattern '[sha512:contenthash:base64:6]'
```
Make sure npm and npx are installed on your host machine.


The app also requires a bash script named `compileLang.sh` in your repository root directory, responsible for compiling the extracted intl strings to the ICU format. For example:
```bash
#!/bin/bash

npx --yes @formatjs/cli compile downloadLang/en-US.json --ast --out-file src/compiled-lang/en.json --format simple
npx --yes @formatjs/cli compile downloadLang/fr-CA.json --ast --out-file src/compiled-lang/fr.json --format simple
npx --yes @formatjs/cli compile downloadLang/fa-IR.json --ast --out-file src/compiled-lang/fa.json --format simple
npx --yes @formatjs/cli compile downloadLang/he-IL.json --ast --out-file src/compiled-lang/he.json --format simple

npx --yes @formatjs/cli compile downloadLang/enums/en-US.json --ast --out-file src/compiled-lang/enums/en.json --format simple
npx --yes @formatjs/cli compile downloadLang/enums/fr-CA.json --ast --out-file src/compiled-lang/enums/fr.json --format simple
npx --yes @formatjs/cli compile downloadLang/enums/fa-IR.json --ast --out-file src/compiled-lang/enums/fa.json --format simple
npx --yes @formatjs/cli compile downloadLang/enums/he-IL.json --ast --out-file src/compiled-lang/enums/he.json --format simple

```

Remember to provide the files in the src/compiled-lang directory to the react-intl provider in your application.

Now that you've ensured compatibility, proceed with the installation process.


## Installation

### 1. Install the package
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 2. Setup the environment variables
```
cp .env.example .env
```
Don't forget to change the values in `.env` file.

### 3. Run the migrations
```
python manage.py migrate
```

### 4. Create a super user
```
python manage.py createsuperuser
```

### 5. Create the cron jobs
```
python manage.py crontab remove
python manage.py crontab add
```

### 6. Run the server
```
python manage.py runserver
```

## Usage