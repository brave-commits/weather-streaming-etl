import logging 

class Logger:
    @classmethod
    def get_logger(cls):
        logging.basicConfig(
            filename= './.logs/app.log',
            level=logging.INFO,
            filemode='a',
            format=f"[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] : %(message)s",
            datefmt="%Y=%m-%d %H:%M:%S"
        )

        return logging.getLogger('WeatherAppLogger')
    
    @classmethod
    def log_info(cls, message):
        logger = cls.get_logger()
        logger.info(message)

    @classmethod
    def log_error(cls, exception=None):
        logger = cls.get_logger()
        logger.error(f'Exception: {exception}', exc_info=True)