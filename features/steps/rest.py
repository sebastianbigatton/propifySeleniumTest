import requests
from behave import given, when, then


@when(u'GET request is performed to "{url}"')
def get_request(context, url):
    response = requests.get(url)
    context.response = _parse_json(response)


@then('Response matches with')
def verify_response(context):
    fail_msg = 'Response is not the expected! Expected: {}, Obtained: {}'
    fail_msg = fail_msg.format(context.text, context.response)
    assert context.response == context.text, fail_msg


def _parse_json(response):
    try:
        return response.json()
    except ValueError:
        return None
