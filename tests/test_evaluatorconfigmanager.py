#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tempfile import tempdir
import pytest

from gear.evaluator.evaluatorconfigmanager import EvaluatorConfigManager


class TestEvaluatorConfigManager:
    """
    tests for EvaluatorConfigManager
    """

    def test_000_create_config(self, tmp_path):
        """
        do a test
        """
        ecm = EvaluatorConfigManager(tmp_path)
        fn = ecm.create_config(
            name="name",
            description="my description",
            author="author <author@example.com>"
        )
        print(fn)
