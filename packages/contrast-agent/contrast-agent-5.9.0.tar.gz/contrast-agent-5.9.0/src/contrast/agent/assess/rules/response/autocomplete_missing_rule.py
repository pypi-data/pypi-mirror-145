# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.response.base_response_rule import BaseResponseRule


class AutocompleteMissingRule(BaseResponseRule):
    @property
    def name(self):
        return "autocomplete-missing"

    def is_violated(self, _, body, form_tags, meta_tags):
        body_violated, body_properties = self.is_body_violated(body, form_tags)
        return body_violated, body_properties

    def is_body_violated(self, body, form_tags):
        """
        Rule is violated if:
        1. none of the attrs of the list of form tags have an "autocomplete" attr
        2. at least one attr is "autocomplete" but it is is assigned to anything other than "off"
        :param body: response body
        :param form_tags: list of Tag namedtuple
        :return: bool, properties dict
        """
        if not form_tags:
            return False, {}

        for tag in form_tags:
            for attr_name, attr_value in tag.attrs:
                if attr_name.lower() == "autocomplete" and attr_value.lower() == "off":
                    return False, {}

        # If no autocomplete attr in any form tag, report the first form tag since
        # they are all in violation.
        properties = self.build_properties(form_tags[0].tag, body)
        return True, properties

    def build_properties(self, full_tag, body):
        original_start = body.index(full_tag)
        original_end = original_start + len(full_tag)

        html = self.body_to_report(original_start, original_end, body)

        redacted_start = html.index(full_tag)
        redacted_end = redacted_start + len(full_tag)

        return dict(
            html=html,
            start=str(redacted_start),
            end=str(redacted_end),
        )

    def body_to_report(self, form_start, form_end, body):
        # 50chars before + full tag + 50 chars after

        if form_start - 50 < 0:
            start = 0
        else:
            start = form_start - 50

        if form_end + 50 > len(body):
            end = len(body)
        else:
            end = form_end + 50

        return body[start:end]
