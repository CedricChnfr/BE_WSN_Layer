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
    assert frame.sfd == 0xA5
    assert frame.car_id == 1
    assert frame.temperature == 25
    assert frame.people_count == 30
    assert frame.co2 == 500
    assert frame.crc == frame.calculate_crc()
    assert frame.efd == 0x5A
    print(f"Frame initialized: SFD={frame.sfd}, Car ID={frame.car_id}, Temperature={frame.temperature}, People Count={frame.people_count}, CO2={frame.co2}, CRC={frame.crc}, EFD={frame.efd}")

def test_frame_calculate_crc():
    frame = Frame(1, 25, 30, 500)
    crc = frame.calculate_crc()
    assert crc == sum(struct.pack('B', frame.sfd) + struct.pack('B', frame.car_id) + struct.pack('h', frame.temperature) + struct.pack('B', frame.people_count) + struct.pack('H', frame.co2)) % 256
    print(f"Calculated CRC: {crc}")

def test_frame_to_bytes():
    frame = Frame(1, 25, 30, 500)
    frame_bytes = frame.to_bytes()
    expected_bytes = struct.pack('B', frame.sfd) + struct.pack('B', frame.car_id) + struct.pack('h', frame.temperature) + struct.pack('B', frame.people_count) + struct.pack('H', frame.co2) + struct.pack('B', frame.crc) + struct.pack('B', frame.efd)
    assert frame_bytes == expected_bytes
    print(f"Frame to bytes: {frame_bytes}")
    
    # Vérification des valeurs des capteurs dans la trame convertie en octets
    assert frame_bytes[0] == 0xA5  # SFD
    assert frame_bytes[1] == 1  # Car ID
    assert frame_bytes[2:4] == struct.pack('h', 25)  # Temperature
    assert frame_bytes[4] == 30  # People Count
    assert frame_bytes[5:7] == struct.pack('H', 500)  # CO2
    assert frame_bytes[7] == frame.crc  # CRC
    assert frame_bytes[8] == 0x5A  # EFD

def test_tdmac_init():
    tdma_mac = TDMAMAC(300)
    assert tdma_mac.slot_duration == 300
    assert tdma_mac.sensors == []
    assert tdma_mac.current_slot == 0
    print(f"TDMA MAC initialized: Slot Duration={tdma_mac.slot_duration}, Sensors={tdma_mac.sensors}, Current Slot={tdma_mac.current_slot}")

if __name__ == '__main__':
    pytest.main()