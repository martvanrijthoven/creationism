import logging
from typing import Optional, List
import os
import pathlib
from datetime import datetime
from typing import Optional

_logger_names = []
_log_path = None


def _get_log_path() -> str:
    global _log_path
    if _log_path is None:
        raise ValueError("log_path not set")
    return _log_path


def reset_logging(log_path: str, time_stamped=True) -> Optional[str]:
    global _logger_names
    for name in _logger_names:
        logger = logging.getLogger(name)
        if isinstance(logger, logging.Logger):
            logger.setLevel(logging.NOTSET)
            logger.propagate = True
            logger.disabled = False
            logger.filters.clear()
            handlers = logger.handlers.copy()
            for handler in handlers:
                # Copied from `logging.shutdown`.
                try:
                    handler.acquire()
                    handler.flush()
                    handler.close()
                except (OSError, ValueError):
                    pass
                finally:
                    handler.release()
                logger.removeHandler(handler)

    _logger_names = []

    global _log_path
    _log_path = _get_formatted_log_path(log_path, time_stamped)
    return _log_path


def set_logger(
    name: str, sub_path=None, return_logger=False
) -> Optional[logging.Logger]:

    log_path = _get_log_path()

    if sub_path:
        log_path = os.path.join(log_path, sub_path)
        pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)

    global _logger_names
    if name in _logger_names:
        return logging.getLogger(name)

    _logger_names.append(name)

    logger2 = logging.getLogger(name)
    logger2.setLevel(logging.DEBUG)
    ch = _get_handler(log_path, name)
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger2.addHandler(ch)
    if return_logger:
        return logger2


def _get_formatted_log_path(log_path: str, time_stamped: bool):
    if log_path is None:
        return
    
    if time_stamped:
        logtime = datetime.timestamp(datetime.now())
        log_path = os.path.join(
            str(log_path),
            "run-" + str(logtime).replace(".", ""),
        )

    pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)
    return log_path


def _get_handler(log_path: str, name: str):
    if log_path:
        # create handler and set level to debug
        log_filename = os.path.join(log_path, name) + ".log"
        return logging.FileHandler(log_filename, mode="w")
    return logging.StreamHandler()
