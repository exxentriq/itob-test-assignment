import os
import threading
import time
import datetime

from database import Database

from dotenv import load_dotenv


load_dotenv() # Take environment variables from .env


def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class Kettle:
    STATE_OFF = 'OFF'
    STATE_ON = 'ON'

    WATER_MIN_LEVEL = float(os.getenv("WATER_MIN_LEVEL"))
    WATER_MAX_LEVEL = float(os.getenv("WATER_MAX_LEVEL"))
    WATER_BOILING_TIME = float(os.getenv("WATER_BOILING_TIME"))  # How long it takes for water to boil
    WATER_BOILING_TEMPERATURE = float(os.getenv("WATER_BOILING_TEMPERATURE"))  # Water boiling temperature in Celsius

    # Calculate water boiling speed (Degrees Per Second)
    # TODO: More advanced formula based on current water level and water/environment temperature can be used
    DPS = WATER_BOILING_TEMPERATURE / WATER_BOILING_TIME

    def __init__(self):
        self.state = Kettle.STATE_OFF
        self.water_level = 0.0
        self.water_temperature = 0.0
        self.thread = None
        self.db = Database()

    def set_state(self, value):
        self.state = value
        print(f"[ STATE ] Kettle state is '{value}'.")

        data = (
            self.state,
            self.water_level,
            self.water_temperature,
            f"STATE: Kettle state is '{value}'.",
            datetime.datetime.timestamp(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
        )
        self.db.insert_data(data)

    def turn_on(self):
        # Check if kettle is already turned on
        if self.state == Kettle.STATE_ON:
            data = (
                self.state,
                self.water_level,
                self.water_temperature,
                "ERROR: Kettle is already on.",
                datetime.datetime.timestamp(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
            )
            self.db.insert_data(data)

            raise Exception('Kettle is already on.')

        # Check if the water level meets the safety requirements
        if self.water_level < Kettle.WATER_MIN_LEVEL:
            data = (
                self.state,
                self.water_level,
                self.water_temperature,
                "ERROR: Water level is too low.",
                datetime.datetime.timestamp(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
            )
            self.db.insert_data(data)

            raise Exception('Water level is too low.')

        # Start boiling
        self.set_state(Kettle.STATE_ON)

        self.thread = KettleThread(self)
        self.thread.start()

        print("[ INFO ] The kettle is turned on.")

        data = (
            self.state,
            self.water_level,
            self.water_temperature,
            "INFO: The kettle is turned on.",
            datetime.datetime.timestamp(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
        )
        self.db.insert_data(data)

    def turn_off(self):
        # Stop boiling
        self.set_state(Kettle.STATE_OFF)

        if self.thread.is_alive():
            self.thread.join()  # Wait until thread is stopped

        print("[ INFO ] The kettle is turned off.")

        data = (
            self.state,
            self.water_level,
            self.water_temperature,
            "INFO: The kettle is turned off.",
            datetime.datetime.timestamp(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
        )
        self.db.insert_data(data)

    def set_water_level(self, water_level):
        self.water_level = clamp(water_level, 0.0, Kettle.WATER_MAX_LEVEL)  # Clamp to prevent water overflowing

    def set_water_temperature(self, water_temperature):
        self.water_temperature = water_temperature


class KettleThread(threading.Thread):
    def __init__(self, kettle):
        threading.Thread.__init__(self)
        self.kettle = kettle

    def run(self):
        while self.kettle.state == Kettle.STATE_ON:

            # Check if water is boiled
            if self.kettle.water_temperature >= Kettle.WATER_BOILING_TEMPERATURE:
                self.kettle.state = Kettle.STATE_OFF

                print("[ INFO ] Water is boiling.")

                data = (
                    self.kettle.state,
                    self.kettle.water_level,
                    self.kettle.water_temperature,
                    "INFO: Water is boiling.",
                    datetime.datetime.timestamp(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
                )
                self.kettle.db.insert_data(data)

                break

            time.sleep(1)

            # Boil water for 1 second
            self.kettle.water_temperature += Kettle.DPS
            print(f"[ TEMPERATURE ] Water temperature is {self.kettle.water_temperature}°C.")

            data = (
                self.kettle.state,
                self.kettle.water_level,
                self.kettle.water_temperature,
                f"TEMPERATURE: Water temperature is {self.kettle.water_temperature}°C.",
                datetime.datetime.timestamp(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
            )
            self.kettle.db.insert_data(data)