# -*- encoding: utf-8 -*-
"""
Tests for :mod:`syringe`.

"""
import unittest

import syringe


class TestProvides(unittest.TestCase):
    """
    Tests :func:`syringe.provides`.

    """
    def setUp(self):
        """
        Reset the :obj:`syringe._PROVIDERS` dict.

        """
        syringe._PROVIDERS.clear()

    def test_provide_one(self):
        """
        Test that the decorated class is added to the providers.

        """
        @syringe.provides('mock')
        class CLS(object):
            pass

        instance = CLS()
        self.assertIs(instance, syringe._PROVIDERS['mock'])

    def test_provide_duplicate(self):
        """
        Test that a duplicate instance of a class raises a
        :exc:`syringe.DuplicateProviderError`.

        """
        @syringe.provides('mock')
        class CLS(object):
            pass

        CLS()
        with self.assertRaises(syringe.DuplicateProviderError) as e:
            CLS()
        self.assertEqual('A provider for [mock] already exists',
                         e.exception.args[0])

    def test_provide_duplicate_other_class(self):
        """
        Test that a duplicate instance of different classes providing
        the same name raises a :exc:`syringe.DuplicateProviderError`.

        """
        @syringe.provides('mock')
        class AMock(object):
            pass

        @syringe.provides('mock')
        class BMock(object):
            pass

        AMock()
        with self.assertRaises(syringe.DuplicateProviderError) as e:
            BMock()
        self.assertEqual('A provider for [mock] already exists',
                         e.exception.args[0])


class TestGet(unittest.TestCase):
    """
    Tests :func:`syringe.get`.

    """
    def setUp(self):
        """
        Reset the :obj:`syringe._PROVIDERS` dict.

        """
        syringe._PROVIDERS.clear()

    def test_get(self):
        """
        Test simply getting a provided instance.

        """
        @syringe.provides('mock')
        class CLS(object):
            pass

        instance = CLS()
        self.assertIs(instance, syringe.get('mock'))

    def test_no_candidate(self):
        """
        Test that a :exc:`syringe.NoCandidateError` is raised when no
        candidate exists.

        """
        with self.assertRaises(syringe.NoCandidateError) as e:
            syringe.get('mock')
        self.assertEqual('No provider found for [mock]', e.exception.args[0])


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
        syringe._PROVIDERS.clear()

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


class TestMock(unittest.TestCase):
    """
    Test that mocks may be subclassed for easy mocking using syringe.

    """
    injected = syringe.inject('mock')

    def setUp(self):
        syringe._PROVIDERS.clear()

    def test_same_instance(self):
        """
        Test that the injected mock is the actual mock instance.

        """
        m = syringe.mock('mock')
        self.assertIs(m, self.injected)

    def test_call_mock(self):
        """
        Test that the actual mock is called when calling the injected mock.

        """
        m = syringe.mock('mock')
        m.ask.return_value = 42
        answer = self.injected.ask(
            'what is the answer to life the universe and everything?')
        m.ask.assert_called_once_with(
            'what is the answer to life the universe and everything?')
        self.assertEqual(42, answer)

    def test_mock_override(self):
        """
        Test that a mock overrides any other provided instance.

        """
        syringe.mock('mock')
        m = syringe.mock('mock')
        self.assertIs(m, self.injected)

    def test_custom_mock(self):
        """
        Test that a custom object can be used as a mock.

        """
        class MyMock(object):
            pass

        m = MyMock()
        copy = syringe.mock('mymock', m)
        self.assertIs(m, copy)
        self.assertIs(m, syringe.get('mymock'))


class TestClear(unittest.TestCase):
    """
    Tests :func:`syringe.clear`.

    """
    def test_same_instance(self):
        """
        Test that the providers dict is still the same instance.

        """
        providers = syringe._PROVIDERS
        syringe.clear()
        self.assertIs(providers, syringe._PROVIDERS)

    def test_empty(self):
        """
        Test that the providers dict is empty after clearing.

        """
        @syringe.provides('mock')
        class CLS(object):
            pass

        CLS()
        self.assertIn('mock', syringe._PROVIDERS)
        syringe.clear()
        self.assertDictEqual({}, syringe._PROVIDERS)
