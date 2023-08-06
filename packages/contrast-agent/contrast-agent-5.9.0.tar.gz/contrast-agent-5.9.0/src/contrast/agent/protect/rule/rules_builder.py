# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import OrderedDict

from contrast.agent.protect.rule.cmdi_rule import CmdInjection
from contrast.agent.protect.rule.deserialization_rule import Deserialization
from contrast.agent.protect.rule.http_method_tampering import MethodTampering
from contrast.agent.protect.rule.malformed_header import MalformedHeader
from contrast.agent.protect.rule.nosqli_rule import NoSqlInjection
from contrast.agent.protect.rule.path_traversal_rule import PathTraversal
from contrast.agent.protect.rule.sqli_rule import SqlInjection
from contrast.agent.protect.rule.ssrf_rule import Ssrf
from contrast.agent.protect.rule.unsafe_file_upload_rule import UnsafeFileUpload
from contrast.agent.protect.rule.xss_rule import Xss
from contrast.agent.protect.rule.xxe_rule import Xxe


def build_protect_rules():
    """
    Build a dict with rules with prefilter rules first.
    We want prefilter rules first so they get evaluated / trigger first.

    :return: an ordered dict of protect rules
    """
    rules = OrderedDict(
        {
            UnsafeFileUpload.NAME: UnsafeFileUpload(),
            CmdInjection.NAME: CmdInjection(),
            Deserialization.NAME: Deserialization(),
            # Turned off until TS can handle rule information
            MalformedHeader.NAME: MalformedHeader(),
            MethodTampering.NAME: MethodTampering(),
            NoSqlInjection.NAME: NoSqlInjection(),
            # Padding Oracle rule is currently disabled - CONTRAST-35352
            # PaddingOracle.NAME: PaddingOracle(),
            PathTraversal.NAME: PathTraversal(),
            SqlInjection.NAME: SqlInjection(),
            Ssrf.NAME: Ssrf(),
            Xss.NAME: Xss(),
            Xxe.NAME: Xxe(),
        }
    )

    return rules
