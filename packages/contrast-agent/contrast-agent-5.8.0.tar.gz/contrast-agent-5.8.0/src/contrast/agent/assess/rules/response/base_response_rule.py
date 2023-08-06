# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.base_rule import BaseRule


class BaseResponseRule(BaseRule):
    @property
    def name(self):
        raise NotImplementedError

    def is_valid(self):
        raise NotImplementedError

    def is_violated(self):
        raise NotImplementedError

    def add_events_to_finding(self, finding, **kwargs):
        # Response rules do not have events to add to a finding
        pass

    def update_preflight_hash(self, hasher, **kwargs):
        # Response rules do not update the hash
        pass
