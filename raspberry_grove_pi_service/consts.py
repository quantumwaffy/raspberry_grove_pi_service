from enum import StrEnum


class Sensor(StrEnum):
    temperature = "temp"
    humidity = "hum"
    sound = "snd"
    light = "lght"
    led = "led"


class TaskAction(StrEnum):
    on = "on"
    off = "off"
