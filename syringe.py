# -*- encoding: utf-8 -*-

"""
A simple dependency injection library.

"""
import functools
import logging

try:
    from unittest import mock
except ImportError:
    try:
        import mock
    except ImportError:
        mock = None


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
        init = cls.__init__

        def __init__(self, *args, **kwargs):
            if mock and isinstance(self, mock.Mock):
                init(self, *args, **kwargs)
                if name not in _PROVIDERS:
                    _PROVIDERS[name] = self
                    logging.info('Mocked [{}]: {}'.format(name, self))
                return
            if name in _PROVIDERS:
                raise DuplicateProviderError(
                    'A provider for [{}] already exists'.format(name))
            init(self, *args, **kwargs)
            _PROVIDERS[name] = self
            logging.info('Injected [{}]: {}'.format(name, self))

        try:
            __init__ = functools.wraps(init)(__init__)
        except AttributeError:
            # For python 2 compatibility
            __init__ = functools.wraps(init, ('__doc__', '__name__'))(__init__)
        cls.__init__ = __init__
        return cls
    return inner


class Injector(object):
    """
    Not to be used directly. Call :func:`inject` instead.

    Injects the instance of a provided class to the current context.

    """
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, value):
        if obj is None:
            return self
        if self.name not in _PROVIDERS:
            raise NoCandidateError(
                'No provider found for [{}]'.format(self.name))
        return _PROVIDERS[self.name]


def inject(name):
    """
    Returns:
        an :cls:`Injector` with the specified name.

    """
    return Injector(name)


def clear():
    """
    Clears all current providers.

    This may be useful for testing.

    """
    _PROVIDERS.clear()
