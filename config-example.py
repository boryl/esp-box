from machine import Pin

try:
    from mqtt_as import config
except Exception:
    config = {}


def ledfunc(pin):
    pin = pin

    def func(v):
        pin(not v)  # Active low on ESP8266
    return func


# MQTT config
config['server'] = ''
config['port'] = 1833
config['user'] = ''
config['password'] = ''

# Wifi config
config['ssid'] = ''
config['wifi_pw'] = ''

# Other config
app_config = {}
app_config['sub_topic'] = ''
app_config['wifi_led'] = ledfunc(Pin(5, Pin.OUT, value=0))

machine_config = {}
machine_config['battery_led'] = 2
machine_config['power_switch'] = 14
machine_config['button1'] = 15
machine_config['button2'] = 4
machine_config['button3'] = 18
machine_config['battery_threshold'] = 3.6
