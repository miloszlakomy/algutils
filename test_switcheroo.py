import unittest

import collections
import itertools
import random
import traceback

import contexttimer

from algutils import switcheroo


class Switcherooling(switcheroo.Switcheroo):
    def load_switch_to(self, _unused_attribute_name):
        return ["q", "w", "e"]


class SwitcherooTestCase(unittest.TestCase):
    def test_switcheroo(self) -> None:
        s = switcheroo.Switcheroo([123, 234, 345])
        self.assertIsInstance(s, switcheroo.Switcheroo)
        item = s[1]
        self.assertNotIsInstance(s, switcheroo.Switcheroo)
        self.assertIsInstance(s, list)
        self.assertEqual(item, 234)
        self.assertEqual(s, [123, 234, 345])

    def test_attribute_access(self) -> None:
        NT = collections.namedtuple("NT", ["attr"])
        nt = NT(attr=321)
        s = switcheroo.Switcheroo(nt)
        self.assertIsInstance(s, switcheroo.Switcheroo)
        attr = s.attr
        self.assertNotIsInstance(s, switcheroo.Switcheroo)
        self.assertIsInstance(s, NT)
        self.assertEqual(attr, 321)
        self.assertEqual(s, nt)

    def test_subtraction(self) -> None:
        self.assertEqual(switcheroo.Switcheroo(1) - 1, 0)

    def test_getitem_and_subtraction(self) -> None:
        self.assertEqual(switcheroo.Switcheroo([1])[0] - 1, 0)

    def test_load_switch_to(self) -> None:
        s = Switcherooling()
        self.assertIsInstance(s, switcheroo.Switcheroo)
        item = s[1]
        self.assertNotIsInstance(s, switcheroo.Switcheroo)
        self.assertIsInstance(s, list)
        self.assertEqual(s, ["q", "w", "e"])

    def test_switcheroo_without_switch_to(self) -> None:
        s = switcheroo.Switcheroo()
        self.assertIsInstance(s, switcheroo.Switcheroo)
        with self.assertRaises(switcheroo.SwitchToUnsetException):
            _ = s.attr
        self.assertIsInstance(s, switcheroo.Switcheroo)
        with self.assertRaises(switcheroo.SwitchToUnsetException):
            _ = s[1]
        self.assertIsInstance(s, switcheroo.Switcheroo)

    def test_switch_variable_name(self) -> None:
        s1 = s2 = switcheroo.Switcheroo([123, 234, 345], switch_variable_name="s1")
        self.assertIsInstance(s1, switcheroo.Switcheroo)
        self.assertIsInstance(s2, switcheroo.Switcheroo)
        item1 = s1[1]
        item2 = s2[1]
        self.assertNotIsInstance(s1, switcheroo.Switcheroo)
        self.assertIsInstance(s1, list)
        self.assertIsInstance(s2, switcheroo.Switcheroo)
        self.assertEqual(item1, 234)
        self.assertEqual(item2, 234)
        self.assertEqual(s1, [123, 234, 345])
