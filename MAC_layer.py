import time
import random
import struct
import threading

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

class Frame:
    def __init__(self, car_id, temperature, people_count, co2):
        self.preamble = 0xAA
        self.car_id = car_id
        self.temperature = temperature
        self.people_count = people_count
        self.co2 = co2
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        frame_data = struct.pack('B', self.preamble) + struct.pack('B', self.car_id) + struct.pack('h', self.temperature) + struct.pack('B', self.people_count) + struct.pack('H', self.co2)
        return sum(frame_data) % 256

    def to_bytes(self):
        return struct.pack('B', self.preamble) + struct.pack('B', self.car_id) + struct.pack('h', self.temperature) + struct.pack('B', self.people_count) + struct.pack('H', self.co2) + struct.pack('B', self.checksum)

class TDMAMAC:
    def __init__(self, slot_duration=300):
        self.slot_duration = slot_duration
        self.sensors = []
        self.current_slot = 0

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def start(self):
        while True:
            temperature = random.randint(-10, 40)
            people_count = random.randint(0, 50)
            co2 = random.randint(300, 2000)
            frame = Frame(1, temperature, people_count, co2)
            self.transmit(frame)
            time.sleep(self.slot_duration / len(self.sensors))

    def transmit(self, frame):
        print(f"Transmitting frame: {frame.to_bytes()}")

if __name__ == "__main__":
    tdma_mac = TDMAMAC()

    temp_sensor = Sensor(1, 'temperature')
    people_sensor = Sensor(2, 'people_count')
    co2_sensor = Sensor(3, 'co2')

    tdma_mac.add_sensor(temp_sensor)
    tdma_mac.add_sensor(people_sensor)
    tdma_mac.add_sensor(co2_sensor)

    tdma_thread = threading.Thread(target=tdma_mac.start)
    tdma_thread.start()