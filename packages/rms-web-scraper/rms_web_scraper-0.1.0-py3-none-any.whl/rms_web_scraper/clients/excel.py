import io
import os
from typing import Dict, Tuple

import pandas as pd
from bs4 import BeautifulSoup
from httpx import Cookies

from .base import BaseClient
from ..exceptions import UnconfiguredReport
from ..telerik import telerik_excel_report_form


class ExcelClient(BaseClient):

    """
    Async client for downloading excel report data from RMS

    Reports must be custom reports, stock RMS reports are not
    supported

    Parameters
        - company_id (int): RMS company id for login
        - username (str): RMS username for login
        - password (str): RMS password for login

    """

    async def get_report(self, report_name: str) -> pd.DataFrame:
        """
        Get report from web and convert directly into a
        DataFrame. The download file is not saved to disk.

        Parameters
            - report_name (str): The report name spelled exactly
            how it appears in RMS
        """

        report_params = await self._get_excel_report_params(report_name)
        report = await self._client.request(
            'POST',
            report_params[0],
            data=report_params[1],
            params=report_params[2],
            cookies=report_params[3],
            follow_redirects=True
        )
        file_stream = io.BytesIO(report.content)
        return pd.read_excel(file_stream)

    async def download_report(self, report_name: str) -> None:
        """
        Get report and save excel file to disk

        Parameters
            - report_name (str): The report name spelled exactly
            how it appears in RMS
        """
        report_params = await self._get_excel_report_params(report_name)
        
        filepath = os.path.join(self._config.report_dir, f"{report_name}.xlsx")
        with open(filepath, 'wb') as download:
            async with self._client.stream(
                'POST',
                report_params[0],
                data=report_params[1],
                params=report_params[2],
                cookies=report_params[3],
                follow_redirects=True
            ) as report:
                async for chunk in report.aiter_bytes():
                    download.write(chunk)

    async def _get_excel_report_params(
        self,
        report_name: str
    ) -> Tuple[str, Dict[str, str], Dict[str, str], Cookies]:

        # client blocks until session cookie is obtained
        session_cookies = await self._get_session()
        # check for cached form inputs, saves from having to
        # make request to load viewstates. Cached forms are
        # good with the original cookie from the session
        # that generated the viewstates
        try:
            cached = self._cache[repr(session_cookies)]
            return (*cached, session_cookies)
        except KeyError:
            pass
        report_configs = self._config.reports
        report_id = None
        # get report id from config file
        for report_config in report_configs:
            if report_config['name'] == report_name:
                report_id = report_config['id']
                break
        if not report_id:
            raise UnconfiguredReport(
                f"Cannot get report ID, {report_name} not in config"
            )
        report_url = self._config.urls.report_url
        params = {
            'ID': report_id,
            'Report': report_name
        }
        # first request is to main report page, cant go directly
        # to the POST request because the Telerik viewstates are
        # unknown at this point
        response = await self._client.get(report_url, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        event_target = self._config.telerik.excel.event_target
        event_argument = self._config.telerik.excel.event_argument
        form_data = telerik_excel_report_form(
            soup,
            event_target=event_target,
            event_argument=event_argument
        )
        try:
            self._cache[repr(session_cookies)] = (report_url, form_data, params)
        except ValueError:
            pass
        return report_url, form_data, params, session_cookies