# -*- encoding: utf-8 -*-
"""
A simple dependency injection library.

Usage
=====

First decorate a class with ``@provides('a lookup name')``.

>>> import syringe
>>>
>>> @syringe.provides('cure')
... class Syrup:
...     def drink(self, person):
...         print('Nom nom')
...         person.health = 100
...

Instantiate it. Note that it is not possible to instanciate another instance of
a class decorated with the name ``cure``.

>>> syrup = Syrup()

Next inject it in another class using ``inject('a lookup name')``.

>>> class Person:
...     cure = syringe.inject('cure')
...
...     def drink_medicine(self):
...         self.cure.drink(self)
...

When an instance of the ``Person`` class is created, the value of the injecte name
is the instance of the provided and instantiated class.

>>> person = Person()
>>> person.health = 20
>>> assert person.cure == syrup
>>> person.drink_medicine()
Nom nom
>>> assert person.health == 100


Mocking
-------

A mock instance can be inserted using ``syringe.mock('a lookup name')``

>>> try:
...     from unittest import mock
... except:
...     import mock
...
>>> m = syringe.mock('cure')
>>> person.drink_medicine()
>>> m.drink.assert_called_once_with(person)

"""
import functools

try:
    from unittest import mock as mock_module
except ImportError:
    try:
        import mock as mock_module
    except ImportError:
        mock_module = None


__all__ = [
    'clear',
    'DuplicateProviderError',
    'get',
    'inject',
    'mock',
    'provides',
    'NoCandidateError'
]


_PROVIDERS = {}


class DuplicateProviderError(ValueError):
    """
    Raised when two providers for the same name have been instantiated.

    """


class NoCandidateError(KeyError):
    """
    Raised when no candidate has been registered for the requested name.

    """


def provides(name):
    """
    Provides the decorated class as an injectable object.

    The class ``__init__`` method is monkey patched so a
    :exc:`DuplicateProviderError` is raised when another instance is
    created for this name.

    Args:
        name (str): The name under which the provided class will be accessible.

    """
    def inner(cls):
        cls.__provides = name
        init = cls.__init__

        def __init__(self, *args, **kwargs):
            name = type(self).__provides
            if name in _PROVIDERS:
                raise DuplicateProviderError(
                    'A provider for [{}] already exists'.format(name))
            init(self, *args, **kwargs)
            _PROVIDERS[name] = self

        try:
            __init__ = functools.wraps(init)(__init__)
        except AttributeError:
            # For python 2 compatibility
            __init__ = functools.wraps(init, ('__doc__', '__name__'))(__init__)
        cls.__init__ = __init__
        return cls
    return inner


def get(name):
    """
    Returns the provided instance.

    Args:
        name (str): The lookup name.

    Returns:
        The provided instance.

    """
    if name not in _PROVIDERS:
        raise NoCandidateError('No provider found for [{}]'.format(name))
    return _PROVIDERS[name]


class inject(object):
    """
    Injects the instance of a provided class to the current context.

    """
    def __init__(self, name):
        """
        Args:
            name (str): The lookup name.

        """
        self.name = name

    def __get__(self, obj, value):
        """
        Returns:
            The provided instance.

        """
        if obj is None:
            return self
        return get(self.name)


def mock(name, m=None):
    """
    Provide a mock overriding any namespace conflicts.

    If a second argument is passed, it is provided using the specified
    name. Otherwise a new :class:`unittest.mock.Mock` instance is
    provided.

    Args:
        name (str): The name of the mock to provide.
        m: The optional object to provide as a mock.

    """
    if m is None:
        m = mock_module.Mock()
    _PROVIDERS[name] = m
    return m


def clear():
    """
    Clears all current providers.

    This may be useful for testing.

    """
    _PROVIDERS.clear()
