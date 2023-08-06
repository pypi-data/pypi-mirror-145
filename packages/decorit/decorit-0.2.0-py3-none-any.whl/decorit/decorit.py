"""Definition of decorators.

BSD 3-Clause License
Copyright (c) 2021, Daniel Nagel
All rights reserved.

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import functools
import time as pytime
import types
import warnings

from beartype import beartype
from beartype.typing import Any, Callable, Optional


@beartype
def copy_doc(source: Callable) -> Callable:
    """Copy docstring from source.

    Parameters
    ----------
    source : Callable
        Function to take doc string from.

    Examples
    --------
    >>> import decorit
    >>> # define function from which we copy the docstring
    >>> def func_to_copy_from(args):
    ...     \"\"\"Docstring of func_to_copy_from.\"\"\"
    >>> @decorit.copy_doc(func_to_copy_from)
    ... def func(args):
    ...     pass  # function goes here
    >>> func.__doc__
    'Docstring of func_to_copy_from.'

    """
    @beartype
    def wrapper_copy_doc(func: Callable) -> Callable:
        if source.__doc__:
            func.__doc__ = source.__doc__  # noqa: WPS125
        return func
    return wrapper_copy_doc


@beartype
def copy_doc_params(source: Callable) -> Callable:
    """Copy parameters from docstring source.

    The docstring needs to be formatted according to numpy styleguide.

    .. todo:: Catch if after parameters is further docstring

    Parameters
    ----------
    source : Callable
        Function to take doc string from.

    Examples
    --------
    >>> import decorit
    >>> # define function from which the Parameters section is copied
    >>> func_to_copy_from = decorit.copy_doc_params
    >>> @decorit.copy_doc_params(func_to_copy_from)
    ... def func(args):
    ...     pass  # function goes here
    >>> # Function uses parameters of given func

    """
    @beartype
    def wrapper_copy_doc(func: Callable) -> Callable:
        PARAMS_STRING = 'Parameters'
        doc_source = source.__doc__
        doc_func = func.__doc__
        if doc_source and doc_func and doc_source.find(PARAMS_STRING) != -1:
            # find last \n before keyphrase
            idx = doc_source[:doc_source.find(PARAMS_STRING)].rfind('\n')
            doc_params = doc_source[idx:]

            doc_params = doc_source[doc_source.find(PARAMS_STRING):]
            func.__doc__ = '{0}\n\n{1}'.format(  # noqa: WPS125
                doc_func.rstrip(),  # ensure that doc_func ends on empty line
                doc_params,
            )
        return func
    return wrapper_copy_doc


@beartype
def deprecated(
    msg: Optional[str] = None,
    since: Optional[str] = None,
    remove: Optional[str] = None,
) -> Callable:
    """Add deprecated warning.

    Parameters
    ----------
    msg : str
        Message of deprecated warning.

    since : str
        Version since deprecated, e.g. '1.0.2'

    remove : str
        Version this function will be removed, e.g. '0.14.2'

    Returns
    -------
    f : Callable
        Return decorated function.

    Examples
    --------
    >>> import decorit
    >>> @decorit.deprecated(msg='Use func_new instead.', remove='1.0.0')
    ... def func(args):
    ...     pass  # function goes here
    >>> # If function is called, you will get now a deprecation warning
    >>> # DeorecationWarning: Calling deprecated function func. Use func_new
    >>> # instead. -- Function will be removed starting from 1.0.0

    """
    @beartype
    def deprecated_msg(
        func: Callable,
    ) -> str:
        warn_msg = 'Calling deprecated function {0}.'.format(func.__name__)
        if msg:
            warn_msg += ' {0}'.format(msg)
        if since:
            warn_msg += ' -- Deprecated since version {v}'.format(v=since)
        if remove:
            warn_msg += (
                ' -- Function will be removed starting from ' +
                '{v}'.format(v=remove)
            )
        return warn_msg

    @beartype
    def decorator_deprecated(func: Callable) -> Callable:
        @beartype
        @functools.wraps(func)
        def wrapper_deprecated(*args: Any, **kwargs: Any) -> Callable:
            warnings.warn(
                deprecated_msg(func),
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)  # pragma: no cover

        return wrapper_deprecated

    return decorator_deprecated


@beartype
def alias(name: str) -> Callable:
    """Add alternative identity to function.

    This decorator supports only functions and no class members!

    Parameters
    ----------
    name : str
        Alternative function name.

    Returns
    -------
    f : function
        Return decorated function.

    Examples
    --------
    >>> import decorit
    >>> @decorit.alias('tau')
    ... def lagtime(args):
    ...     pass  # function goes here
    >>> tau(...)  # Function can now be called via alias.

    """
    @beartype
    def copy_func(func: Callable) -> Callable:
        """Return deep copy of a function."""
        func_copy = types.FunctionType(
            func.__code__,  # noqa: WPS609
            func.__globals__,  # noqa: WPS609
            name=name,
            argdefs=func.__defaults__,  # noqa: WPS609
            closure=func.__closure__,  # noqa: WPS609
        )
        # Copy attributes of function
        func_copy.__kwdefaults__ = func.__kwdefaults__  # noqa: WPS609
        return func_copy

    @beartype
    def decorated_doc(func: Callable) -> str:
        return (
            'This function is an alias of `{0}`.'.format(func.__name__) +
            'See its docstring for further help.'
        )

    @beartype
    def decorator_alias(func: Callable) -> Callable:
        # register function
        func_copy = copy_func(func)
        func_copy.__globals__[name] = func_copy  # noqa: WPS609
        func_copy.__doc__ = decorated_doc(func)  # noqa: WPS609, WPS125
        return func

    return decorator_alias


@beartype
def logging(func):
    """Print each call with arguments.

    Returns
    -------
    f : function
        Return decorated function.

    Examples
    --------
    >>> import decorit
    >>> @decorit.logging
    ... def func(*args):
    ...     return args  # function goes here
    >>> # Function prints now logging when called
    >>> var = func('a', 5)
    Calling func('a', 5)
    'func' -> ('a', 5)

    """
    @beartype
    @functools.wraps(func)
    def wrapper_logging(*args: Any, **kwargs: Any) -> Callable:
        args_repr = ['{0!r}'.format(arg) for arg in args]
        kwargs_repr = [
            '{0}={1!r}'.format(key, itm) for key, itm in kwargs.items()
        ]
        print('Calling {0}({1})'.format(  # noqa: WPS421
            func.__name__, ', '.join(args_repr + kwargs_repr),
        ))

        return_val = func(*args, **kwargs)

        print('{0!r} -> {1!r}'.format(  # noqa: WPS421
            func.__name__, return_val,
        ))
        return return_val
    return wrapper_logging


@beartype
def _time_txt(seconds: float) -> str:
    """Get string to format time."""
    if seconds < 1e-3:
        txt = '{name!r}: {mus:.0f}µs elapsed'
    elif seconds < 1:
        txt = '{name!r}: {ms:.3f}ms elapsed'
    elif seconds < 300:
        txt = '{name!r}: {s:.3f}s elapsed'
    elif seconds < 3600:
        txt = '{name!r}: {min:.3f}min elapsed'
    else:
        txt = '{name!r}: {h:.3f}h elapsed'
    return txt


@beartype
def time(func):
    """Print time needed for execution.

    Returns
    -------
    f : function
        Return decorated function.

    Examples
    --------
    >>> import decorit
    >>> @decorit.time
    ... def func(*args):
    ...     return args  # function goes here
    >>> # Function prints now logging when called
    >>> var = func('a', 5)
    'func': 1µs elapsed

    """

    @beartype
    @functools.wraps(func)
    def wrapper_time(*args: Any, **kwargs: Any) -> Callable:
        start = pytime.perf_counter()
        return_val = func(*args, **kwargs)
        elapsed_time = pytime.perf_counter() - start

        attributes = {
            'name': func.__name__,
            'mus': elapsed_time * 1e6,
            'ms': elapsed_time * 1e3,
            's': elapsed_time,
            'min': elapsed_time / 60,
            'h': elapsed_time / 3600,
        }
        print(_time_txt(elapsed_time).format(**attributes))  # noqa: WPS421

        return return_val
    return wrapper_time


@beartype
def run_once(func):
    """Run function only once, irrespectively of the arguments.

    This decorator adds a attribute has_run to the function with which it
    can be checked if the function was executed yet.

    Attributes
    ----------
    has_run : bool
        Bool displays if function has run.

    Returns
    -------
    f : function
        Return decorated function.

    Examples
    --------
    >>> import decorit
    >>> @decorit.run_once
    ... def func(*args):
    ...     pass  # function goes here
    >>> # Function is now only called on first run
    >>> func(...) # run once the first time
    >>> func.has_run
    True
    >>> # Running the function once a second time can be achived by:
    >>> func.has_run = False
    >>> func(...) # run once the second time

    """

    @beartype
    @functools.wraps(func)
    def wrapper_run_once(*args: Any, **kwargs: Any) -> Callable:
        if not wrapper_run_once.has_run:
            wrapper_run_once.has_run = True
            return func(*args, **kwargs)
    wrapper_run_once.has_run = False
    return wrapper_run_once
