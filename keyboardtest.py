import gpiotest
from threading import Thread, Event, Timer
import time

secret = "1234"
def timer(e):
    e.set()
    
try:
    while True:
        line = input("Enter password: ")
        if line == secret:
            print("Password correct!")
            e = Event()
            t = Thread(target=gpiotest.wait_on, args=(e,))
            tt = Timer(5, function=e.set)
            t.start()
            tt.start()
            
        if line == "s":
            e.set()
        else:
            print("Wrong password!")
except KeyboardInterrupt:
    gpiotest.cleanup()
    print("Application stopped")
        