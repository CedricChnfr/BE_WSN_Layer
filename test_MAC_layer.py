import pytest
import struct
from MAC_layer import Sensor, Frame, TDMAMAC

def test_sensor_init():
    sensor = Sensor(1, 'temperature')
    assert sensor.sensor_id == 1
    assert sensor.sensor_type == 'temperature'

def test_sensor_read_data():
    sensor = Sensor(1, 'temperature')
    data = sensor.read_data()
    assert -10 <= data <= 40
    return data

def test_frame_init():
    frame = Frame(1, 'temperature', 25)
    assert frame.preamble == 0xAA
    assert frame.sensor_id == 1
    assert frame.sensor_type == Frame.SENSOR_TYPES['temperature']  # Correction ici
    assert frame.data == 25
    assert frame.checksum == frame.calculate_checksum()

def test_frame_calculate_checksum():
    frame = Frame(1, 'temperature', 25)
    checksum = frame.calculate_checksum()
    assert checksum == sum(struct.pack('B', frame.preamble) + struct.pack('B', frame.sensor_id) + struct.pack('B', frame.sensor_type) + struct.pack('I', frame.data)) % 256

def test_frame_to_bytes():
    frame = Frame(1, 'temperature', 25)
    frame_bytes = frame.to_bytes()
    expected_bytes = struct.pack('B', frame.preamble) + struct.pack('B', frame.sensor_id) + struct.pack('B', frame.sensor_type) + struct.pack('I', frame.data) + struct.pack('B', frame.checksum)
    assert frame_bytes == expected_bytes

def test_tdmac_init():
    tdma_mac = TDMAMAC(300)
    assert tdma_mac.slot_duration == 300
    assert tdma_mac.sensors == []
    assert tdma_mac.current_slot == 0
    

if __name__ == '__main__':
    pytest.main()