import time
from behave import given, when, then
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

TIMEOUT = 10


@given(u'I open a "{browser_name}" browser')
def open_browser(context, browser_name):
    if browser_name == "chrome":
        context.driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        raise NotImplementedError('Only chrome is supported')


@given(u'I navigate to "{url}"')
def navigate_to(context, url):
    context.driver.get(url)
    context.driver.maximize_window()


@when(u'I fill in "{field}" with "{text}"')
def fill_in_field(context, field, text):
    element = _get_element_by_xpath(context, 'write', text, field)
    element.send_keys(text)


@when(u'I click on "{name}"')
def click_on(context, name):
    element = _get_element_by_xpath(context, 'click', name)
    element.click()


@when(u'I press key "{key}"')
def press_key(context, key):
    active_element = context.driver.switch_to.active_element
    if isinstance(active_element, dict):
        active_element = active_element['value']
    special_key = getattr(Keys, key.upper(), None)
    active_element.send_keys(special_key)


@then(u'I verify "{text}" link text is displayed')
def verify_link_text_displayed(context, text):
    _get_element_by_xpath(context, 'verification', text)


@then(u'I close the browser')
def close_browser(context):
    context.driver.quit()


def _get_element_definition_by_xpath(action, text_arg, field_arg=None):
    if action == "write":
        try:
            definitions = {
                'Search': '//input[(@title="Buscar" or @title="Search")]'
            }
            xpath_string = definitions[field_arg]
        except:
            xpath_string = '//input'
    elif action == "click":
        xpath_string = f'//input[@value="{text_arg}"]'
    elif action == "verification":
        xpath_string = f'//h3[normalize-space(text())="{text_arg}"]'
    else:
        raise NotImplementedError(f'{action} not supported supported')
    return xpath_string


def _get_element_by_xpath(context, action, text_arg, field_arg=None):
    xpath = _get_element_definition_by_xpath(action, text_arg, field_arg)
    element = None
    last_exception = Exception(f'{xpath} was not found')
    start_time = time.time()
    while (time.time() - start_time) <= TIMEOUT:
        try:
            element = context.driver.find_element_by_xpath(xpath)
            break
        except Exception as ex:
            last_exception = ex
        time.sleep(1)
    else:
        raise last_exception
    return element
