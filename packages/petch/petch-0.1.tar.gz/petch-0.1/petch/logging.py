import logging


def setup_logger(log_file_name:str="app.log",log_on_file:bool=False):
    l = logging.getLogger()
    
    if l.hasHandlers(): return

    formatter = logging.Formatter('%(asctime)s| %(message)s', datefmt='%d/%b/%Y-%H:%M:%S')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    l.addHandler(streamHandler)  

    if log_on_file :
        fileHandler = logging.FileHandler(log_file_name, mode='a')
        fileHandler.setFormatter(formatter)
        l.addHandler(fileHandler)
        
    l.setLevel("INFO")


def log(msg:str):
    l = logging.getLogger()
    l.info(msg)


