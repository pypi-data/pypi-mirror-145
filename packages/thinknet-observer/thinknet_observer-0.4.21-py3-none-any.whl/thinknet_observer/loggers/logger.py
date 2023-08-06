import logging
import os


class Logger:

    LOG_LEVEL = str(os.environ.get("LOG_LEVEL", "info").isupper())
    if LOG_LEVEL not in list(logging._nameToLevel.keys()):
        LOG_LEVEL = "INFO"

    
    def __init__(self,
                 logger_name: str = "",
                 logger_source: str = "",
                 logger_version: str = "",
                 logger_level: str = "",
                 logger_format: str = ""):
        self.logger_handler = logging.StreamHandler()
        self.logger_format = logger_format
        self.logger_name = logger_name
        self.logger_source = logger_source
        self.logger_version = logger_version
        self.logger_level = logger_level
        
        self.logger = logging.getLogger(self.logger_name)
        
        self.logger_handler.setFormatter(logging.Formatter(self.logger_format, "%Y-%m-%dT%H:%M:%SZ"))
        self.logger_handler.setLevel(Logger.LOG_LEVEL)
        self.logger.addHandler(self.logger_handler)
        
    @classmethod
    def logging(cls):
        logger_source = "application"
        logger_version = "1"
        logger_format = (
            "{"
            + f"'timestamp':'%(asctime)s','level':'%(levelname)s','message':'%(message)s','log.source':'{logger_source}','log.version':{logger_version}"
            + "}"
        )
        logging_instance = cls(logger_name = "logging",
                               logger_source = logger_source,
                               logger_version = logger_version,
                               logger_level = Logger.LOG_LEVEL,
                               logger_format = logger_format)
        
        return logging_instance.logger

    @classmethod
    def analyzer(cls):
        logger_source = "analyzer"
        logger_version = "1"
        logger_format = (
            "{"
            + f"'timestamp':'%(asctime)s','level':'%(levelname)s','message':'%(message)s','log.source':'{logger_source}','log.version':{logger_version}"
            + "}"
        )
        logging_instance = cls(logger_name = "analyzer",
                               logger_source = logger_source,
                               logger_version = logger_version,
                               logger_level = "INFO",
                               logger_format = logger_format)

        return logging_instance.logger

    @classmethod
    def cronlogger(cls,
                   version: str, 
                   repo_name: str, 
                   project_name: str,
                   repo_tags: str = "",
                   repo_service: str or dict = {}):
        
        logger_version = version
        repo_name = repo_name
        project_name = project_name
        
        logger_name = "cron"
        logger_source = "cron"
        
        logger_format = (
            "{"
            + f"'name': {repo_name},'project': {project_name},'status': '%(status)s','type': {logger_source},'tags': {repo_tags},'service': {repo_service},'@timestamp':'%(asctime)s','message': '%(message)s','_version':{logger_version}"
            + "}"
        )
        logging_instance = cls(
            logger_name = logger_name,
            logger_source = logger_source,
            logger_version = logger_version,
            logger_format = logger_format)
        return logging_instance.logger