# Night light project
# 4 LEDs with brightness controlled by PWM, controlled by photoresistor. 

from machine import ADC, Pin, PWM
from time import sleep

# Set up photoresistor input
photo_pin = Pin(26)
photoRes = ADC(photo_pin)

# Set up pwm
pwm_pin = Pin(17)
pwm = PWM(pwm_pin)
pwm.freq(1000)

# Constants
max_value = 65535 # highest 16-bit value
darkness_low_threshold = 80 # Any lower % than this, lights will be off

# functions
def read_darkness() -> tuple:
    """Read the resistance from the photoresistor and transform into a percentage
    High percentage = more darkness. 
    """
    light = photoRes.read_u16() # Read the 16-bit value for how bright it is.
    darkness = max_value - light # Inverse the value read.
    darkness_percentage = int(darkness/max_value*100) # Get a % of the darkness. 
    if darkness_percentage <= darkness_low_threshold:
        # Keep the lights off if below threshold. 
        darkness = 0 
    return darkness, darkness_percentage

def rescale_brightness(darkness, dark_percentage) -> tuple:
    """Rescale the PWM brightness of the LEDs based on the thresholds"""
    if dark_percentage >= darkness_low_threshold:
        # If darkness within set range, modulate the brightness of the LED bulbs accordingly. 
        new_percentage = int((dark_percentage - darkness_low_threshold)/(100-darkness_low_threshold)*100)
        new_darkness = int(darkness*new_percentage/100)
    else:
        # If it is too bright just keep the LEDs off. 
        new_percentage, new_darkness = 0, 0
    return new_darkness, new_percentage
    
# Main loop
while True:
    darkness_tuple = read_darkness()
    rescaled_values = rescale_brightness(*darkness_tuple)
    #print(f"darkness: {darkness_tuple}%")
    #print(f"new_darkness: {rescaled_values}%")
    sleep(0.001) # set a delay between readings
    pwm.duty_u16(rescaled_values[0]) # lights on


        
        