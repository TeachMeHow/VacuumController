import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.HIGH)   # Set pin 8 to be an output pin and set initial value to low (off)

def timed_on(seconds):
    GPIO.output(8, GPIO.LOW) # Turn on
    sleep(seconds)                  # Sleep for 1 second
    GPIO.output(8, GPIO.HIGH)  # Turn off

def wait_on(event):
    GPIO.output(8, GPIO.LOW) # Turn on
    event.wait()             # Sleep for 1 second
    GPIO.output(8, GPIO.HIGH)  # Turn off
    
def off():
    GPIO.output(8, GPIO.HIGH)  # Turn off
    
def cleanup():
    GPIO.cleanup()