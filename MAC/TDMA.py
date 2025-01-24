from Frame import Frame
import time

class TDMA:
    #Doit être mis à jour
    def __init__(self, slot_duration=300):
        self.slot_duration = slot_duration
        self.sensors = []
        self.current_slot = 0
        self.frame_id = 1

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def start(self):
        while True:
            for sensor in self.sensors:
                data = sensor.read_data()
                frame = Frame(self.frame_id, 1, sensor.sensor_id, sensor.sensor_type, data)
                self.transmit(frame)
                self.frame_id = (self.frame_id % 100) + 1
                time.sleep(self.slot_duration / len(self.sensors))

    def transmit(self, frame):
        print(f"Transmitting frame: {frame.to_bytes()}")