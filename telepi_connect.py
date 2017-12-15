import RPi.GPIO as GPIO
import time
import os
import singlecheck

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
 
# Define GPIO to use on Pi
GPIO_PIR = 7
 
print "TELEPI Ebee system (CTRL-C to exit)"

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo
 
Current_State  = 1
Previous_State = 1
#time.sleep(5) 
try:
 
  print "Waiting for  to Trigger ..."
 
  # Loop until PIR output is 0
 # while GPIO.input(GPIO_PIR)==1:
  #  Current_State  = 0
 
  print "  Ready"
 
  # Loop until users quits with CTRL-C
  while True :
 
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
 
    if Current_State==0 and Previous_State==1:
      #Switch is triggered
      print "  PUSH detected!"
      if singlecheck.connct == 1:
        # Take the image and save it in folder /home/pi folder with name photo.jpg
        os.system('fswebcam -p YUYV -d /dev/video0 -S 8 -r 640x480  /home/dietpi/snap/abc.jpg')
        #os.system('streamer -c /dev/video0 -b 16 -o /home/dietpi/snap/photo.jpeg')
        # start the telegram and echo the command to send photo to user
        os.system('/home/dietpi/tg/bin/telegram-cli server.pub -WR -e "send_photo Arfath_jambu /home/dietpi/snap/abc.jpg"')
        # Record previous state
        print " Connected & Sent online !!! "
        Previous_State=0
        # Previous_State=0
      else :
        #os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save /home/bgs/Documents/Aj_Box/test_files/temp_snapbin/%H%M%S.jpg')  
        os.system('fswebcam -p YUYV -d /dev/video0 -S 8 -r 640x480  /home/dietpi/snap/offline/%H%M%S.jpg')
        Previous_State = 0
	print " Not connected & Saved offline !!! "
    elif Current_State==1 and Previous_State==0:
      # PIR has returned to ready state
      print "  Ready"
      Previous_State=1

    # Wait for 1 second
    time.sleep(0.1)
 
except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()
