# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.config import (
    FlaskHttpOnlyRule,
    FlaskSecureFlagRule,
    FlaskSessionAgeRule,
)
from contrast.agent.middlewares.route_coverage.common import (
    create_routes,
    build_route,
    get_view_func_for_request,
)
from contrast.wsgi.middleware import WSGIMiddleware
from contrast.utils.decorators import fail_safely


class FlaskMiddleware(WSGIMiddleware):
    def __init__(self, app):
        self.app = app

        self.config_rules = [
            FlaskSessionAgeRule(),
            FlaskSecureFlagRule(),
            FlaskHttpOnlyRule(),
        ]

        super().__init__(app.wsgi_app, app_name=app.name)

    @fail_safely("Unable to get route coverage", return_value={})
    def get_route_coverage(self):
        return create_routes(self.app)

    @fail_safely("Unable to get Flask view func")
    def get_view_func(self, request):
        return get_view_func_for_request(request, self.app)

    @fail_safely("Unable to build route", return_value="")
    def build_route(self, view_func, url):
        return build_route(view_func.__name__, view_func)

    @fail_safely("Failed to run config scanning rules")
    def scan_configs(self):
        for rule in self.config_rules:
            rule.apply(self.app)
