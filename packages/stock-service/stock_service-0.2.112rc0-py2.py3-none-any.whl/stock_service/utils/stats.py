from typing import Optional

from stock_service.config import Config

config = Config()

NAMESPACES = (
    "consumers",
    "database.stock",
    "database.take2",
    "external",
    "health",
    "internal",
    "managers",
    "other",
    "producers",
    "rest_endpoints",
    "s4f_endpoints",
)


def profile_with_stats(
    namespace: str,
    stat_name: Optional[str] = None,
    count_exceptions=True,
    count_success=True,
    exceptions_to_catch=(),
):
    """
    decorator to profile function and count the errors and success
    decorator to catch exception as increment statsd reporting

    :param stats: Stats client singleton instance
    :param count_exceptions: increment {func_name}.failure
    :param count_success: increment {func_name}.success
    :param exceptions_to_catch: list of exceptions that will be handled and logged as logger.exception
    """

    if namespace not in NAMESPACES:
        raise ValueError(f"namespace must be one of {NAMESPACES}")

    stats = config.get_stats_client()

    def inner(func):
        def handler(*args, **kwargs):
            prefix = stat_name or func.__name__
            config.logger.debug(stats)
            timer = stats.timer(f"{namespace}.{prefix}.timer")
            timer.start()
            try:
                results = func(*args, **kwargs)
            except Exception as e:
                if count_exceptions:
                    config.stats_client.incr(
                        f"{namespace}.{prefix}.fail.{e.__class__.__name__}"
                    )
                if isinstance(e, exceptions_to_catch):
                    config.logger.exception(e)
                    return None
                else:
                    raise
            else:
                if count_success:
                    config.stats_client.incr(f"{namespace}.{prefix}.success")
                return results
            finally:
                timer.stop()

        return handler

    return inner
