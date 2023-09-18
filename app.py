import asyncio

from raspberry_grove_pi_service import consts, senders

if __name__ == "__main__":
    sensors_pin_data: dict[consts.Sensor, int] = {
        consts.Sensor.temperature: 4,
        consts.Sensor.humidity: 4,
        consts.Sensor.sound: 1,
        consts.Sensor.light: 2,
    }
    ws_connect_checker_pin: int = 3

    sender: senders.BaseDataSender = senders.BaseDataSender(ws_connect_checker_pin, sensors_pin_data)

    asyncio.get_event_loop().run_until_complete(sender.run())
