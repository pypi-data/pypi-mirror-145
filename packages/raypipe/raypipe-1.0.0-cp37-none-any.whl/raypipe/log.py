import logging  # 引入logging模块

class Logger(object):
    def __init__(self,name:str):
        logging.basicConfig(filename=name,level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        self.logger=logging

    def info(self,*args):
        self.logger.info(*args)

    def warning(self,*args):
        msg, err = args
        self.logger.warning(msg, err)

    def debug(self, *args):
        self.logger.debug(*args)

    def error(self, *args):
        self.logger.debug(*args)