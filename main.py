# main.py

import logging
import time
import qrcode
import os
import configparser
import threading
import readchar
from StoppableTimer import StoppableTimer







class CodeGenerator:
    def  __init__(self, secret):
        self._secret = secret
        
    def generate_code(self, time_value_s):
        timestamp_ms = time.time_ns() // 1000000
        code = self._secret + "%" + str(timestamp_ms) + "%" + str(time_value_s) 
        logging.info("code length = %i characters: %s", len(code), code)
        return code
    
    def create_qr(self, code):
        qr = qrcode.QRCode(
        version = None)
        qr.add_data(code)
        qr.make(fit=True)
        type(qr)
        img = qr.make_image()
        return img
    
    def print_ticket(self, code):
        try:
            self.validate(code)
        except:
            logging.exception("Generate another code or contact administrator")
        qr_image = self.create_qr(code)
        qr_image.save("qr.png")


class CodeValidator:
    def  __init__(self, secret, codes_filename):
        if not secret:
            raise Exception(2, "Secret must not be empty")
        self._secret = secret
        self._code_length = 2
        self.codes_filename = codes_filename
        self.used_codes = CodeValidator._read_code_file(codes_filename)
        self.used_codes_lock = threading.Lock()
        
    def decode(self, code):
        split_list = code.rsplit("%", self._code_length)
        if (len(split_list) != self._code_length):
            raise Exception(1, "Incorrect code length")
        return {"secret" : split_list[0], "timestamp_ms" : int(split_list[1]), "time_value_s" : int(split_list[2]), "code_expiration_time_s" : int(split_list[3])}

    # return { "STATUS": ["VALID", "INVALID_SECRET", "INVALID_FORMAT", "USED_CODE"], "TIME_S" : int}
    def validate(self, code):
        try:
            decoded_info = self.decode(code)
        except ValueError as a:
            logging.exception("Decoding Error")
            return ("INVALID_FORMAT_VALUE", 0)
        except Exception as exc:
            _, message = exc.args
            logging.exception(message)
            return ("INVALID_FORMAT", 0)
        finally:
            if self.used_codes.get(code) != None:
                self.used_codes_lock.release()
                return ("USED_CODE", 0)
            elif decoded_info.get("secret") != self._secret:
                return ("INVALID_SECRET", 0)
            elif decoded_info.get("time_value_s") <= 0:
                return ("INVALID_TIME_VALUE", 0)
            else:
                return ("VALID", decoded_info.get("time_value_s"))
    
    # only use for __init__
    def _read_code_file(codes_filename):
        used_codes_list = []
        used_codes_dict = {}
        with open(codes_filename) as f:
            for line in f.readline():
                if line != '\n':
                    used_codes_list.append(line)          
            used_codes_dict.fromkeys(used_codes_list, True)
            return used_codes_dict
        
    def use_code(self, code):
        with open(self.codes_filename) as f, self.used_codes_lock:
            self.used_codes.update(code, True)
            f.seek(0,2)
            f.write(code + '/n')
            
            
class MainController:
    CONFIG_FILENAME = 'config.ini'

    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(MainController.CONFIG_FILENAME)        
        if os.getenv("APP_ENV") == "DEVELOPMENT":
            self.settings = config["DEVELOPMENT"]
            logging.basicConfig(format="%(asctime)s : %(message)s",level=logging.DEBUG)
        else: 
            self.settings = config["PRODUCTION"]
            logging.basicConfig(filename="log.txt",format="%(asctime)s : %(message)s",level=logging.WARNING)
    
        validator = CodeValidator(self.settings.get('secret'), self.settings.get('codes_filename'))
        devices = [VacuumController(self, id=1), VacuumController(self, id=2)]
            
        
class VacuumController:

    def __init__(self, main_controller, id=0):
        self._main_controller = main_controller
        self.Id = id
        self._time_factor = 0
        self._lock = threading.Lock()
        self._state = "WAITING"
        self.t_key = threading.Thread(target = self.wait_key)
        self.t_key.start()

    

    def wait_key(self):
        c = None
        print("Press C to stop\n1 - READY\n2 - RUN\n3 - STOP")
        while True:
            c = readchar.readchar()
            if c == "1":
                self.read_code(None)
            if c == "2":
                self.start()
            if c == "3":
                self.stop()
            if str(c).upper != "C":
                break
            print(self.state)
    
    def read_code(self, code):
        self.state = "READY"
        self.time_left = 10
        self.t_timer = threading.Thread(target=self.run_timer, args=(self.time_left,))
        self.t_timer.start()
    
    def start(self):
        self.state = "RUNNING"
    
    def stop(self):
        self.state = "STOPPED"


class Device:
    def __init__():
        _state = 1
        _time_left = 0
        _timer = None
        
TIME = 5
timer = StoppableTimer(TIME)
event = timer.get_event()
start = time.perf_counter()
timer.start()
event.wait()
elapsed = time.perf_counter() - start
error = abs(TIME - elapsed) / TIME









