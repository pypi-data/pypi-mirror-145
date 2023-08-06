from typing import Dict, List

from bs4 import BeautifulSoup

from .exceptions import FormNotFound, NoInputs


def get_form_inputs(soup: BeautifulSoup) -> Dict[str, str]:

    """
    Pull all input tags from an HTML form

    Raises:
        FormNotFound: No form found on HTML page
        NoInputs: No input tags found in HTML form

    Returns:
        form_inputs: A dictionary with the input ID and
        input value for key and value pair respectively
    """

    form = soup.form
    if form is None:
        raise FormNotFound
    form_inputs = {}
    for inp in soup.find_all('input'):
        try:
            form_inputs[inp.attrs['id']] = inp.attrs['value']
        except KeyError:
            # input field is not ID'd dont include
            pass
    if not form_inputs:
        raise NoInputs
    return form_inputs

def build_form_data(
    form_inputs: Dict[str, str],
    excluded_inputs: List[str] = [],
    included_inputs: Dict[str, str] = {}
) -> Dict[str, str]:
    """
    Take all form inputs and generate final form to submit.
    The final form can be tweaked by providing inputs
    manually and/or excluding certain inputs
    """

    filtered_form = {
        key: val for key, val in form_inputs.items() if key not in excluded_inputs
    }
    filtered_form.update(included_inputs)
    return filtered_form


