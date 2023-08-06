"""Provides utility functions."""

import asyncio
from typing import Any, Coroutine, List, Union
from rmlab_errors import MultipleError


async def run_async_tasks(
    tasks: List[Coroutine], return_results: bool = False, discard_none: bool = False
) -> Union[List[Any], None]:
    """Runs multiple asynchronous tasks concurrently capturing exceptions.

    Args:
        tasks (List[Coroutine]): List of tasks to run concurrently.
        return_results (bool, optional): Whether to return results of tasks. Defaults to False.
        discard_none (bool, optional): If returning results, whether to discard the tasks returning ``None``. Defaults to False.

    Raises:
        MultipleError: If more than one task raised an exception.
        Exception: If a single task raised an exception.

    Returns:
        Union[List[Any], NoneType]: If ``return_results`` is ``True``, None otherwise.
    """

    results = await asyncio.gather(*tasks, return_exceptions=True)

    errors = [res for res in results if isinstance(res, Exception)]
    if len(errors) > 1:
        raise MultipleError(*errors)
    elif len(errors) == 1:
        raise errors[0]

    if return_results:
        if discard_none:
            return [r for r in results if r is not None]
        else:
            return list(results)
