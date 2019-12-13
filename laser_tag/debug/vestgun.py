import RPi.GPIO as GPIO
import signal


class VestGun:

    def __init__(self,player,laser,trigger,reload_pin,motor,vest,green,red):

        GPIO.setmode(GPIO.BCM)

        # Laser
        GPIO.setup(laser, GPIO.OUT)

        # Trigger
        GPIO.setup(trigger, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(trigger, GPIO.FALLING, callback=self.__trigger_cb, bouncetime=200)
        signal.signal(signal.SIGALRM, self.__laser_off_cb)
        # signal.signal(signal.SIGIALRM, self.__add_ammo_cb)

        # Reload
        GPIO.setup(reload_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(reload_pin, GPIO.FALLING, callback=self.__reload_cb, bouncetime=200)
        signal.signal(signal.SIGVTALRM, self.__add_ammo_cb)

        # Vibration motor
        GPIO.setup(motor, GPIO.OUT)

        # Vest sensors
        GPIO.setup(vest, GPIO.IN)
        GPIO.add_event_detect(vest, GPIO.FALLING, callback=self.__hit_cb, bouncetime=1000)

        # Vest LEDs
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(red, GPIO.OUT)

        self.ammo = 12
        self.health = 100
        self.max_ammo = 12
        self.max_health = 100
        self.fire_length = 1
        self.reload_interval = 0.1
        self.hit_dmg = 10
        self.alive = False
        self.reloading = False
        self.firing = False
        self.player = player
        self.laser = laser
        self.trigger = trigger
        self.reload_pin = reload_pin
        self.vest = vest
        self.green = green
        self.red = red

    def set_team(self,team):
        if team == 'A':
            GPIO.output(self.green, GPIO.HIGH)
            GPIO.output(self.red, GPIO.LOW)
        elif team == 'B':
            GPIO.output(self.green, GPIO.LOW)
            GPIO.output(self.red, GPIO.HIGH)
        else:
            GPIO.output(self.green, GPIO.LOW)
            GPIO.output(self.red, GPIO.LOW)            

    def __trigger_cb(self,channel):
        # Trigger pressed
        if not self.reloading and not self.firing and self.alive:
            GPIO.output(self.laser, GPIO.HIGH)
            GPIO.output(self.motor, GPIO.HIGH)
            self.firing = True
            signal.setitimer(signal.ITIMER_REAL, self.fire_length)

    def __laser_off_cb(self):
        # Turning laser off
        GPIO.output(self.laser, GPIO.LOW)
        GPIO.output(self.motor, GPIO.LOW)
        self.firing = False

    def __reload_cb(self,channel):
        # Reloading button pressed
        if not self.reloading and not self.firing and self.ammo < self.max_ammo and self.alive:
            self.reloading = True
            signal.setitimer(signal.ITIMER_VIRTUAL, self.reload_interval)

    def __add_ammo_cb(self):
        # Add one to ammo
        self.ammo += 1
        if self.ammo < self.max_ammo and self.alive:
            signal.setitimer(signal.ITIMER_VIRTUAL, self.reload_interval)

    def __hit_cb(self,channel):
        # Hit detected on vest
        if self.alive:
            self.health -= self.hit_dmg
            if self.health <= 0:
                # dead
                self.alive = False
                # self.player.notifyDeath()
    

if __name__ == '__main__':
    
    try:

        running = True
        
        laser = 16
        motor = 12
        trigger = 20
        reload_pin = 21
        vest = 13
        green = 19
        red = 26

        player = None
        vest_gun = VestGun(player,laser,trigger,reload_pin,motor,vest,green,red)

        while running:
            pass
    except Exception as e:
        print(e) 
