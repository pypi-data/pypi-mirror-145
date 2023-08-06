#!/usr/bin/env python

from unittest import TestCase

from camillademo.main import hello_world


class HelloWordTestCase(TestCase):

    def test_hello_world(self):
        self.assertEqual('Camilla Python Demo!', hello_world())
