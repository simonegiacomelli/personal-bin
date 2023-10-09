#!/usr/bin/env python3

import unittest

from jetbrainslib import Status, status, activate, _option, comment, remove, _marker


class TestJetbrainsFix(unittest.TestCase):

    def test_missing(self):
        self.assertEqual(Status.MISSING, status(''))

    def test_active(self):
        self.assertEqual(Status.ACTIVE, status('\n\n-Dsun.java2d.uiScale=\n\n'))
        self.assertEqual(Status.ACTIVE, status('\n\n-Dsun.java2d.uiScale=2\n\n'))

    def test_commented(self):
        self.assertEqual(Status.COMMENTED, status('\n\n#-Dsun.java2d.uiScale=\n\n'))
        self.assertEqual(Status.COMMENTED, status('\n\n# -Dsun.java2d.uiScale=\n\n'))

    def test_activate(self):
        actual = activate('')
        self.assertEqual(Status.ACTIVE, status(actual))

    def test_double_activate(self):
        actual = activate('')
        actual = activate(actual)
        self.assertEqual(Status.ACTIVE, status(actual))
        _assert_no_duplicates(actual)

    def test_commented_activate(self):
        actual = activate('\nfoo=bar\n#' + _option + '\none=1')
        self.assertEqual('\nfoo=bar\n' + _option + '\none=1', actual)
        _assert_no_duplicates(actual)

    def test_comment(self):
        actual = comment('\nfoo=bar\n' + _option + '\none=1')
        self.assertEqual('\nfoo=bar\n#' + _option + '\none=1', actual)
        _assert_no_duplicates(actual)

    def test_remove(self):
        actual = remove('\nfoo=bar\n' + _option + '\none=1')
        self.assertEqual('\nfoo=bar\none=1', actual)
        _assert_no_duplicates(actual)

    def test_activate_no_previous(self):
        actual = activate('\nfoo=bar\none=1')
        self.assertEqual('\nfoo=bar\none=1\n' + _option, actual)
        _assert_no_duplicates(actual)

    def test_duplicates(self):
        try:
            _assert_no_duplicates(_option + '\n' + _option)
        except:
            return 'ok'
        self.fail('the helper function does not work correctly')


def _assert_no_duplicates(actual):
    parts = actual.split(_marker)
    unittest.TestCase().assertLessEqual(len(parts), 2)

