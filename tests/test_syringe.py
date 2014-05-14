# -*- encoding: utf-8 -*-

"""
Tests for :mod:`syringe`.

"""
import unittest

try:
    from unittest import mock
except:
    import mock

import syringe


class TestProvides(unittest.TestCase):
    """
    Tests :func:`syringe.provides`.

    """
    def setUp(self):
        """
        Reset the :obj:`syringe._PROVIDERS` dict.

        """
        syringe._PROVIDERS = {}

    def test_provide_one(self):
        """
        Test that the decorated class is added to the providers.

        """
        cls = mock.Mock
        syringe.provides('mock')(cls)
        instance = cls()
        self.assertIs(instance, syringe._PROVIDERS['mock'])

    def test_provide_duplicate(self):
        """
        Test that a duplicate instance of a class raises a
        :exc:`syringe.DuplicateProviderError`.

        """
        cls = mock.Mock
        syringe.provides('mock')(cls)
        instance = cls()
        with self.assertRaises(syringe.DuplicateProviderError) as e:
            cls()
        self.assertEqual('A provider for [mock] already exists',
                         e.exception.args[0])

    def test_provide_duplicate_other_class(self):
        """
        Test that a duplicate instance of different classes providing
        the same name raises a :exc:`syringe.DuplicateProviderError`.

        """
        class AMock(mock.Mock):
            pass

        class BMock(mock.Mock):
            pass

        AMock()
        with self.assertRaises(syringe.DuplicateProviderError) as e:
            BMock()
        self.assertEqual('A provider for [mock] already exists',
                         e.exception.args[0])


class TestInject(unittest.TestCase):
    """
    Tests :func:`syringe.inject`.

    """
    class Dependant(object):
        dependency = syringe.inject('mock')

    def setUp(self):
        """
        Reset the :obj:`syringe._PROVIDERS` dict.

        """
        syringe._PROVIDERS = {}

    def test_no_candidate(self):
        """
        Test that a :exc:`syringe.NoCandidateError` is raised when no
        candidate exists.

        """
        depentant = self.Dependant()
        with self.assertRaises(syringe.NoCandidateError) as e:
            depentant.dependency
        self.assertEqual('No provider found for [mock]', e.exception.args[0])

    def test_inject(self):
        """
        Test that the injected value is the provided value.

        """
        @syringe.provides('mock')
        class Foo(object):
            pass

        foo = Foo()
        dependant = self.Dependant()
        self.assertIs(foo, dependant.dependency)
