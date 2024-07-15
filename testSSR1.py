import RPi.GPIO as GPIO
import time

# Pin configuration
SSR_PIN = 17  # Change this to the pin you are using

# Setup
GPIO.setmode(GPIO.BCM)  # Set the pin numbering system to BCM
GPIO.setup(SSR_PIN, GPIO.OUT)  # Set the pin as an output

try:
    while True:
        # Turn the SSR on
        GPIO.output(SSR_PIN, GPIO.HIGH)
        print("SSR ON")
        time.sleep(10)  # Wait for 10 seconds

        # Turn the SSR off
        GPIO.output(SSR_PIN, GPIO.LOW)
        print("SSR OFF")
        time.sleep(10)  # Wait for 10 seconds

except KeyboardInterrupt:
    # Clean up GPIO settings before exiting
    GPIO.cleanup()
    print("Exiting and cleaning up GPIO")

