
import requests
import sys
import json
from django.conf import settings
from ..models import GraphqlEnum, GraphqlEnumValue, GraphqlEnumValueTranslation, Language

BASE_URL = settings.BACKEND_BASE_URL
AUTHORIZATION = settings.BACKEND_AUTHORIZATION
USERNAME = settings.BACKEND_USERNAME
PASSWORD = settings.BACKEND_PASSWORD


def get_access_token():
    try:
        # authenticate url
        url = BASE_URL + '/auth/local'

        # authenticate headers
        headers = {
            'Authorization': f'Basic {AUTHORIZATION}',
            'Origin': 'https://webapp.orangedigitalcloud.com',
            'Referer': 'https://webapp.orangedigitalcloud.com/'
        }

        # authenticate data
        data = {
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD,
            'auth': 'basic'
        }

        response = requests.post(url, headers=headers, json=data)

        # extract access token
        access_token = response.json()["access_token"]
        return access_token
    except Exception as e:
        raise e


def read_enums_in_server():
    try:
        # Define the GraphQL endpoint
        url = BASE_URL + "/graphql"
        headers = {"Authorization": "Bearer " + get_access_token()}

        # Define the introspection query
        query = """
        query IntrospectionQuery {
            __schema {
            types {
                kind
                name
                enumValues {
                name
                }
            }
            }
        }
        """

        # Send the introspection query to the GraphQL server
        response = requests.post(url, json={'query': query}, headers=headers)

        # Extract the enums from the introspection query response
        enums = dict()
        for t in json.loads(response.text)["data"]["__schema"]["types"]:
            if t["kind"] == "ENUM" and not t['name'].startswith("_"):
                enums[t["name"]] = list()
                for enumValue in t["enumValues"]:
                    enums[t["name"]].append(enumValue["name"])

        # Now we have list of all the enums in the system in a dictionary with this structure:
        """
        {
            'EnumName': ['EnumValue1', 'EnumValue2', ...],
            ...
        }
        """

        
        return enums
    except Exception as e:
        print("Error getting enums", file=sys.stderr)
        raise e

def normalizer(text):
    # split the string into words using underscores as separators
    words = text.split('_')

    # capitalize the first letter of each word and convert the rest to lowercase
    output_str = ' '.join([word.capitalize() for word in words])

    return output_str


def update_enums_in_db():
    try:
        enums = read_enums_in_server()
        for enum_name, enum_values in enums.items():
            # Get the GraphqlEnum object with the matching name, or create a new one if it doesn't exist
            graphql_enum, created = GraphqlEnum.objects.get_or_create(name=enum_name)

            # Remove any GraphqlEnumValue objects that are not in the JSON file
            graphql_enum.values.exclude(name__in=enum_values).delete()

            # Add any new GraphqlEnumValue objects that are in the JSON file
            for enum_value_name in enum_values:
                enum_value, created = GraphqlEnumValue.objects.get_or_create(name=enum_value_name)
                graphql_enum.values.add(enum_value)

                for language in Language.objects.all():
                    # Get the GraphqlEnumValueTranslation object with the matching enum_value and language, or create a new one if it doesn't exist
                    graphql_enum_value_translation, created = GraphqlEnumValueTranslation.objects.get_or_create(enum_value=enum_value, language=language)

                    if created and language.code == 'en-US':
                        # Set the string of the GraphqlEnumValueTranslation object to the enum_value_name
                        graphql_enum_value_translation.string = normalizer(enum_value_name)

                        graphql_enum_value_translation.save()


            # Save the GraphqlEnum object
            graphql_enum.save()


    except Exception as e:
        print("Error updating enums in db", file=sys.stderr)
        raise e