import asyncio
import multiprocessing

from raspberry_grove_pi_service import consts, receivers, senders

if __name__ == "__main__":
    sender_sensors_pin_data: dict[consts.Sensor, int] = {
        consts.Sensor.temperature: 4,
        consts.Sensor.humidity: 4,
        consts.Sensor.sound: 1,
        consts.Sensor.light: 2,
    }
    receiver_sensors_pin_data: dict[consts.Sensor, int] = {
        consts.Sensor.led: 6,
    }

    ws_connect_sender_checker_pin: int = 3
    ws_connect_receiver_checker_pin: int = 2

    sender: senders.BaseLEDConnectorDataSender = senders.BaseLEDConnectorDataSender(
        ws_connect_sender_checker_pin, sender_sensors_pin_data
    )
    receiver: receivers.BaseLEDConnectorDataReceiver = receivers.BaseLEDConnectorDataReceiver(
        ws_connect_receiver_checker_pin, receiver_sensors_pin_data
    )

    sender_process = multiprocessing.Process(
        target=lambda: asyncio.get_event_loop().run_until_complete(sender.run()), daemon=True
    )
    receiver_process = multiprocessing.Process(
        target=lambda: asyncio.get_event_loop().run_until_complete(receiver.run()), daemon=True
    )

    sender_process.start()
    receiver_process.start()

    sender_process.join()
    receiver_process.join()
