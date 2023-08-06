import inspect
from typing import Any, Awaitable, Callable, Optional, TypeVar, Union, cast

from deprecation import deprecated

from jetpack import _utils
from jetpack.config import _symbols
from jetpack.core._errors import NotAsyncError
from jetpack.core._jetpack_function import JetpackFunction
from jetpack.core._jetpack_function_with_client import schedule as schedule

T = TypeVar("T")
__pdoc__ = {}
__pdoc__["jet"] = "Alias for function"
__pdoc__["jetroutine"] = "Alias for function"


# @function is our general remote work decorator. It does not specify how the
# work will be done (RPC, job, queue, etc) and instead leaves that as an
# implementation detail.
def jetroutine_decorator(
    # The stararg forces the arguments after that to be specified with the keyword
    #
    # > Parameters after “*” [...] are keyword-only parameters and may only be passed by keyword arguments
    # https://docs.python.org/3/reference/compound_stmts.html#function-definitions
    fn: Optional[Callable[..., T]] = None,
    *,
    with_checkpointing: bool = False,
) -> Union[
    Callable[..., Awaitable[T]],
    Callable[[Callable[..., T]], Callable[..., Awaitable[T]]],
]:
    """Decorator that wraps any async Python function, and returns a Jetroutine

    Async python functions decorated with @function (or @jet or @jetroutine) will
    be wrapped as JetpackFunctions, and registered with the runtime. Calling these
    functions will run them as remote Jetroutines, instead of running them locally

    Returns:
        `jetpack._task.jetpack_function.JetpackFunction[T]`

    """

    def wrapper(fn: Callable[..., T]) -> Callable[..., Awaitable[T]]:
        # Use asyncio.iscoroutine() instead?
        if not inspect.iscoroutinefunction(fn):
            raise NotAsyncError(
                f"Jetpack functions must be async. {_utils.qualified_func_name(fn)} is not async."
            )
        _symbols.get_symbol_table().register(fn)
        task: JetpackFunction[T] = JetpackFunction(fn, with_checkpointing)
        return task

    return wrapper(fn) if fn else wrapper


@deprecated(details="Use jetroutine instead.")
def function(
    fn: Optional[Callable[..., T]] = None, *, with_checkpointing: bool = False
) -> Union[
    Callable[..., Awaitable[T]],
    Callable[[Callable[..., T]], Callable[..., Awaitable[T]]],
]:
    # can enable this print to be more aggressive, since smarthop and other
    # customers may not have python's dev-mode on to see the @deprecated decorator's
    # warning message:
    #
    # print("WARNING: @function is deprecated. Use @jetroutine instead.")

    return jetroutine_decorator(fn, with_checkpointing=with_checkpointing)


@deprecated(details="Use jetroutine instead.")
def jet(
    fn: Optional[Callable[..., T]] = None, *, with_checkpointing: bool = False
) -> Union[
    Callable[..., Awaitable[T]],
    Callable[[Callable[..., T]], Callable[..., Awaitable[T]]],
]:
    return jetroutine_decorator(fn, with_checkpointing=with_checkpointing)


jetroutine = jetroutine_decorator


def workflow(
    fn: Optional[Callable[..., T]] = None
) -> Union[
    Callable[..., Awaitable[T]],
    Callable[[Callable[..., T]], Callable[..., Awaitable[T]]],
]:
    return jetroutine_decorator(fn, with_checkpointing=True)
