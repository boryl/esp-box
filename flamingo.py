from machine import Pin, ADC, deepsleep
import uasyncio as asyncio
import ujson
import esp32

class Flamingo:

    def __init__(self, machine_config):
        self.battery_reader = ADC(Pin(35))
        self.battery_reader.atten(ADC.ATTN_11DB)
        self.battery_threshold = machine_config['battery_threshold']
        self.battery_led = Pin(machine_config['battery_led'], Pin.OUT)
        self.battery_level = self.batteryCheck()
        
        #self.led_strip1 = Pin(led_strip1, Pin.OUT)
        #self.led_strip2 = Pin(led_strip2, Pin.OUT)
        
        self.button1 = Pin(machine_config['button1'], Pin.IN)
        self.button2 = Pin(machine_config['button2'], Pin.IN)
        self.button3 = Pin(machine_config['button3'], Pin.IN)
            
        self.battery_led.value(0)
        
        self.power_switch = Pin(machine_config['power_switch'], Pin.IN)
        esp32.wake_on_ext0(pin = self.power_switch, level = esp32.WAKEUP_ANY_HIGH)
    
    def batteryCheck(self):
        self.battery_level = (self.battery_reader.read()/4095)*2*3.3*1.1
        warning = False      
        if (self.battery_level < self.battery_threshold):
            warning = True
        return self.battery_level
    
    def toggleLed(self, led):
        led.value(not(led.value()))
    
    def putToSleep(self):
        deepsleep()
        
    
    async def flashLed(self, json):
        json = ujson.loads(json)
        self.led_strip1.value(1)
        self.led_strip2.value(1)
        print("strips on")
        try:
            on_for = int(json['on_for'])
        except Exception:
            on_for = 1200
            print("invalid json: on_for")
        await asyncio.sleep_ms(on_for)
        self.led_strip1.value(0)
        self.led_strip2.value(0)
        print("strips off")
        
        
        
