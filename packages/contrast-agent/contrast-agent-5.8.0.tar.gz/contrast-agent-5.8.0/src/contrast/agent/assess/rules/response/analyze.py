# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from html.parser import HTMLParser

from contrast.agent.settings import Settings
from contrast.reporting import teamserver_messages
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


def analyze_response_rules(context, reporting_client):
    settings = Settings()

    response_rules = settings.enabled_response_rules()
    response = context.response
    body = response.body.decode("utf-8") or ""

    if not response_rules or not body:
        return

    content_type = response.headers.get("content-type", "")

    status_code = response.status_code
    valid_response_rules = [
        rule for rule in response_rules if rule.is_valid(status_code, content_type)
    ]

    if not valid_response_rules:
        return

    class FormHtmlParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "form":

                for rule in valid_response_rules[:]:
                    violated = rule.is_violated(attrs)
                    if violated:
                        # no longer need to analyze the same rule within this
                        # request if it has already been violated
                        # and sent a finding
                        valid_response_rules.remove(rule)

                        self.send_finding(rule)

        def send_finding(self, rule):
            full_tag = self.get_starttag_text()

            original_start = self.rawdata.index(full_tag)
            original_end = original_start + len(full_tag)

            html = self.body_to_report(original_start, original_end)

            redacted_start = html.index(full_tag)
            redacted_end = redacted_start + len(full_tag)

            finding = rule.create_finding(html, redacted_start, redacted_end)
            context.activity.findings.extend([finding])
            msg = teamserver_messages.Preflight(context.activity)

            reporting_client.add_message(msg)

        def body_to_report(self, form_start, form_end):
            # 50chars before + full tag + 50 chars after

            if form_start - 50 < 0:
                start = 0
            else:
                start = form_start - 50

            if form_end + 50 > len(self.rawdata):
                end = len(self.rawdata)
            else:
                end = form_end + 50  # -1 ?

            return self.rawdata[start:end]

    parser = FormHtmlParser()
    parser.feed(body)
