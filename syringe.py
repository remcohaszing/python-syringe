# -*- encoding: utf-8 -*-

"""
A simple dependency injection library.

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
    'Injector',
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
        init = cls.__init__

        def __init__(self, *args, **kwargs):
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
        name: The lookup name.

    Returns:
        The provided instance.

    """
    if name not in _PROVIDERS:
        raise NoCandidateError('No provider found for [{}]'.format(name))
    return _PROVIDERS[name]



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
        return get(self.name)


def inject(name):
    """
    Returns:
        an :cls:`Injector` with the specified name.

    """
    return Injector(name)


def mock(name, cls=None):
    """
    Provide a mock overriding any namespace conflicts.

    Args:
        name: The name of the mock to provide.
        cls: The optional mock class to provice.

    """
    if cls is None:
        cls = type(str(name), (mock_module.Mock,), {})
    instance = cls()
    _PROVIDERS[name] = instance
    return instance


def clear():
    """
    Clears all current providers.

    This may be useful for testing.

    """
    _PROVIDERS.clear()
