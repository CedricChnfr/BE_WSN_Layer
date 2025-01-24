
import random

class Sensor:
    def __init__(self, sensor_id, sensor_type):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type

    def read_data(self):
        if self.sensor_type == 'temperature':
            return random.randint(-10, 40)
        elif self.sensor_type == 'people_count':
            return random.randint(0, 50)
        elif self.sensor_type == 'co2':
            return random.randint(300, 2000)
        else:
            raise ValueError("Unknown sensor type")
