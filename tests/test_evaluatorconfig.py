#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tempfile import tempdir
import pytest

from gear.evaluator.base.evaluatorconfig.evaluatorconfig import EvaluatorConfig

config_content = """---
name: Example Configuration
description: This is an example description.
author: John Doe <johndoe@example.com>
"""

@pytest.fixture()
def config_file(tmpdir):
    print(tmpdir)
    fn = tmpdir / "test.yaml"
    fn.write(config_content)

    return fn


class TestEvaluatorConfig:
    """
    tests for EvaluatorConfig
    """

    def test_000_load_config(self, tmp_path, config_file):
        """
        do a test
        """
        print(config_file)
        ec = EvaluatorConfig(config_file)
        ec.load()
        print(ec)
        print(ec.dict)
        ec.save()
