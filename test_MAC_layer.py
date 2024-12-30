import pytest
import struct
from MAC_layer import Sensor, Frame, TDMAMAC

def test_sensor_init():
    sensor = Sensor(1, 'temperature')
    assert sensor.sensor_id == 1
    assert sensor.sensor_type == 'temperature'
    print(f"Sensor initialized: ID={sensor.sensor_id}, Type={sensor.sensor_type}")

def test_sensor_read_data():
    sensor = Sensor(1, 'temperature')
    data = sensor.read_data()
    assert -10 <= data <= 40
    print(f"Sensor read data (temperature): {data}")

def test_sensor_read_data_people_count():
    sensor = Sensor(2, 'people_count')
    data = sensor.read_data()
    assert 0 <= data <= 50
    print(f"Sensor read data (people_count): {data}")

def test_sensor_read_data_co2():
    sensor = Sensor(3, 'co2')
    data = sensor.read_data()
    assert 300 <= data <= 2000
    print(f"Sensor read data (co2): {data}")

def test_frame_init():
    frame = Frame(1, 25, 30, 500)
    assert frame.preamble == 0xAA
    assert frame.car_id == 1
    assert frame.temperature == 25
    assert frame.people_count == 30
    assert frame.co2 == 500
    assert frame.checksum == frame.calculate_checksum()
    print(f"Frame initialized: Preamble={frame.preamble}, Car ID={frame.car_id}, Temperature={frame.temperature}, People Count={frame.people_count}, CO2={frame.co2}, Checksum={frame.checksum}")

def test_frame_calculate_checksum():
    frame = Frame(1, 25, 30, 500)
    checksum = frame.calculate_checksum()
    assert checksum == sum(struct.pack('B', frame.preamble) + struct.pack('B', frame.car_id) + struct.pack('h', frame.temperature) + struct.pack('B', frame.people_count) + struct.pack('H', frame.co2)) % 256
    print(f"Calculated checksum: {checksum}")

def test_frame_to_bytes():
    frame = Frame(1, 25, 30, 500)
    frame_bytes = frame.to_bytes()
    expected_bytes = struct.pack('B', frame.preamble) + struct.pack('B', frame.car_id) + struct.pack('h', frame.temperature) + struct.pack('B', frame.people_count) + struct.pack('H', frame.co2) + struct.pack('B', frame.checksum)
    assert frame_bytes == expected_bytes
    print(f"Frame to bytes: {frame_bytes}")

def test_tdmac_init():
    tdma_mac = TDMAMAC(300)
    assert tdma_mac.slot_duration == 300
    assert tdma_mac.sensors == []
    assert tdma_mac.current_slot == 0
    print(f"TDMA MAC initialized: Slot Duration={tdma_mac.slot_duration}, Sensors={tdma_mac.sensors}, Current Slot={tdma_mac.current_slot}")

if __name__ == '__main__':
    pytest.main()