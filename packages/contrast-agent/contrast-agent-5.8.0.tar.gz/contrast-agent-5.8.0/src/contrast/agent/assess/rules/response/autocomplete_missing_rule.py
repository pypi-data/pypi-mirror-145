# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.response.base_response_rule import BaseResponseRule
from contrast.api import Finding


class AutocompleteMissingRule(BaseResponseRule):
    EXCLUDED_RESPONSE_CODES = [301, 302, 307, 404, 410, 500]
    EXCLUDED_CONTENT_TYPES = ["json", "xml"]

    @property
    def name(self):
        return "autocomplete-missing"

    def is_valid(self, status_code, content_type):
        """
        Rule is valid for analysis if response has matching content-type and status-code
        :return: bool
        """
        return not (
            status_code in self.EXCLUDED_RESPONSE_CODES
            or any(
                [
                    c_type
                    for c_type in self.EXCLUDED_CONTENT_TYPES
                    if c_type in content_type
                ]
            )
        )

    def is_violated(self, attrs):
        """
        Rule is violated if the provided attrs (of the form tag) do not contain
        the "autocomplete" attribute or if it is assigned to anything other than "off"
        :param attrs: list of tuples
        :return: bool
        """
        # if autocomplete is not present at all or it's assigned to
        # anything other than "off", build_finding
        for attr_name, attr_value in attrs:
            if attr_name.lower() == "autocomplete" and attr_value.lower() == "off":
                return False
        return True

    def create_finding(self, html, start_idx: int, end_idx: int):
        properties = dict(
            html=html,
            start=str(start_idx),
            end=str(end_idx),
        )

        return Finding(self, properties)
