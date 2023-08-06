from typing import Dict
from bs4 import BeautifulSoup

from .util import build_form_data, get_form_inputs


"""
The Telerik forms are not an exact science. It is a
bit of guess and check to determine the required form
inputs to get the desired result. Chrome dev tools can
show the form inputs used by the browser
"""

def telerik_login_form(
    soup: BeautifulSoup,
    company_id: str,
    username: str,
    password: str
) -> Dict[str, str]:
    """
    Generate login form
    """

    excluded_inputs = [
        'MessageWindow_C_CloseButton'
    ]

    included_inputs = {
        'txtDashId': company_id,
        'txtUserName': username,
        'txtPassword': password
    }

    form_inputs = get_form_inputs(soup)
    return build_form_data(
        form_inputs,
        excluded_inputs=excluded_inputs,
        included_inputs=included_inputs
    )

def telerik_excel_report_form(
    soup: BeautifulSoup,
    event_target: str,
    event_argument: str
) -> Dict[str, str]:
    """
    Generate form to download excel report
    """

    excluded_inputs = [
        'btnBackToHomepage',
        'grdHome_ctl00_ctl02_ctl00_RefreshButton',
        'grdHome_ctl00_ctl02_ctl00_ExportToExcelButton',
        'grdHome_ctl00_ctl03_ctl01_PageSizeComboBox_Input',
    ]

    included_inputs = {
        '__EVENTTARGET': event_target,
        '__EVENTARGUMENT': event_argument
    }
    form_inputs = get_form_inputs(soup)
    return build_form_data(
        form_inputs,
        excluded_inputs=excluded_inputs,
        included_inputs=included_inputs
    )