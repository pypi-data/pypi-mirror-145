import sys
import logging
import logging.handlers
from typing import List, Union
from pathlib import Path


log_format = logging.Formatter(
    "[%(asctime)s] %(filename)s/%(lineno)s/%(funcName)s/%(levelname)s: %(message)s"
)

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.INFO)

logger = logging.getLogger("DengUtils")
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


def clean_handler():
    for handler in logger.handlers:
        logger.removeHandler(handler)


def configure_logger(
    level: int,
    handlers: List[logging.Handler] = None,
    log_file: Union[Path, str] = None,
    append: bool = True,
):
    """配置日志处理器
    :param level: int, 指定日志级别
    :param handlers: List[Handler], 日志处理器列表
    :param log_file: 日志文件存储路径
    :param append: 是否为追加模式。当为覆盖模式时会清空已有的handler再添加新的
    """
    # 设置日志级别
    if level in (
        logging.NOTSET,
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.FATAL,
    ):
        logger.setLevel(level)
    else:
        raise ValueError(f"level参数非法：{level}")
    for handler in logger.handlers:
        handler.setLevel(level)

    # 非追加模式时，先清空所有已有的handler
    # 必须放置在设置已有Handler日志级别之后，因为已有的Handler可能被别处引用
    # 如果放置在最前面会导致在别处引用的handler日志级别无法受level参数控制
    if not append:
        clean_handler()

    # 往日志句柄中添加处理器
    if handlers:
        for handler in handlers:
            if isinstance(handler, logging.Handler):
                handler.setLevel(level)
                logger.addHandler(handler)
            else:
                raise TypeError(f"类型错误，预期为{logging.Handler}类型，实际为{type(handler)}类型")

    if log_file:
        log_file = Path(log_file)
        if not log_file.parent.exists():
            log_file.parent.mkdir(parents=True)

        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file, when="D", backupCount=15, encoding="utf-8"
        )
        file_handler.setFormatter(log_format)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

    logger.debug("日志配置完成")
