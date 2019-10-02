from mqtt_as import MQTTClient, config
from config import app_config, machine_config
import uasyncio as asyncio
from flamingo import Flamingo
from machine import reset
from encoder import Encoder

# Subscription callback
def sub_cb(topic, msg):
    print(msg.decode('utf-8'))
    #loop.create_task(
    #    flamingo.flashLed(msg.decode('utf-8'))
    #    )


async def heartbeat():
    while True:
        await asyncio.sleep_ms(25)
        if not flamingo.power_switch.value():
            print("sleep")
            flamingo.putToSleep()
        await asyncio.sleep_ms(900)


async def batteryProcess():
    while True:
        if(flamingo.batteryCheck() < flamingo.battery_threshold):
            print("battery warning, on")
            await asyncio.sleep_ms(150)
            flamingo.toggleLed(flamingo.battery_led)
            await asyncio.sleep_ms(1500)
            print("battery warning, off")
        else:
            print("battery ok!")
            await asyncio.sleep(60)
            

async def wifi_han(state):
    global wifi_attempts
    global wifi_max_attempts
    app_config['wifi_led'](not state)
    print('Wifi is ', 'up' if state else 'down')
    
    # Restart after x attempts
    if not state:
        if (wifi_attempts >= wifi_max_attempts):
            reset()
        wifi_attempts += 1
    await asyncio.sleep(3)
        
    

async def conn_han(client):
    await client.subscribe(app_config['sub_topic'], 1)


async def main(client, enc):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        reset()
        return
    lastval = 0
    while True:
        await asyncio.sleep_ms(50)
        #await client.publish('timing', '1')
        val = enc.value
        if lastval != val:
            lastval = val
            print(val)
            await client.publish('timing', str(val))
            await asyncio.sleep_ms(100)
        if(not flamingo.button1.value()):
            print("button1")
            await client.publish('interactions', '1')
            await asyncio.sleep_ms(500)
        if(not flamingo.button2.value()):
            print("button2")
            await client.publish('interactions', '2')
            await asyncio.sleep_ms(500)
        
        if(not flamingo.button3.value()):
            print("button3")
            await client.publish('interactions', '3')
            await asyncio.sleep_ms(500)

# Define configuration
config['subs_cb'] = sub_cb
config['wifi_coro'] = wifi_han
config['connect_coro'] = conn_han
config['clean'] = True

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

# Set up Flamingo
flamingo = Flamingo(machine_config)
enc = Encoder(23, 19)


# Set up async
loop = asyncio.get_event_loop()
loop.create_task(heartbeat())
loop.create_task(batteryProcess())

wifi_attempts = 0
wifi_max_attempts = 3

try:
    loop.run_until_complete(main(client, enc))
except KeyboardInterrupt:
    client.close()
    print("Bye")    
except OSError as e:
    reset()
finally:
    client.close()