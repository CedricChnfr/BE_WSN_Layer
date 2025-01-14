import struct
from MAC_layer import Sensor, Frame, TDMAMAC

def test_sensor_init():
    sensor = Sensor(1, 'temperature')
    assert sensor.sensor_id == 1
    assert sensor.sensor_type == 'temperature'
    print(f"Sensor initialized: ID={sensor.sensor_id}, Type={sensor.sensor_type}")

def test_sensor_read_data_temperature():
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
    frame = Frame(1, 1, 1, 'temperature', 25)
    assert frame.sfd == 0xA5
    assert frame.frame_id == 1
    assert frame.metro_id == 1
    assert frame.car_id == 1
    assert frame.sensor_id == 1  # 'temperature' mapped to 1
    assert frame.data == 25
    assert frame.address == (1 << 4) | 1  # 4 bits for car_id + sensor_id
    assert 0 <= frame.randomization <= 15  # 4 bits for randomization
    assert frame.crc == frame.calculate_crc()
    assert frame.efd == 0x5A
    print(f"Frame initialized: SFD={frame.sfd}, Frame ID={frame.frame_id}, Metro ID={frame.metro_id}, Car ID={frame.car_id}, Sensor ID={frame.sensor_id}, Data={frame.data}, Address={frame.address}, Randomization={frame.randomization}, CRC={frame.crc}, EFD={frame.efd}")

def test_frame_calculate_crc():
    frame = Frame(1, 1, 1, 'temperature', 25)
    crc = frame.calculate_crc()
    assert crc == sum(struct.pack('B', frame.sfd) + struct.pack('B', frame.frame_id) + struct.pack('B', (frame.address & 0xF0) | (frame.randomization & 0x0F)) + struct.pack('h', frame.data)) % 256
    print(f"Calculated CRC: {crc}")

def test_frame_to_bytes():
    frame = Frame(1, 1, 1, 'temperature', 25)
    frame_bytes = frame.to_bytes()
    expected_bytes = struct.pack('B', frame.sfd) + struct.pack('B', frame.frame_id) + struct.pack('B', (frame.address & 0xF0) | (frame.randomization & 0x0F)) + struct.pack('h', frame.data) + struct.pack('B', frame.crc) + struct.pack('B', frame.efd)
    assert frame_bytes == expected_bytes
    print(f"Frame to bytes: {frame_bytes}")
    
    # Imprimer la trame en bits
    frame_bits = ''.join(format(byte, '08b') for byte in frame_bytes)
    print(f"Frame to bits: {frame_bits}")
    
    # Vérification des valeurs des capteurs dans la trame convertie en octets
    assert format(frame_bytes[0], '08b') == '10100101'  # SFD
    assert format(frame_bytes[1], '08b') == '00000001'  # Frame ID
    assert format(frame_bytes[2], '08b') == format((frame.address & 0xF0) | (frame.randomization & 0x0F), '08b')  # Address and Randomization
    assert frame_bytes[3:5] == struct.pack('h', 25)  # Data
    assert format(frame_bytes[5], '08b') == format(frame.crc, '08b')  # CRC
    assert format(frame_bytes[6], '08b') == '01011010'  # EFD

def test_tdmac_init():
    tdma_mac = TDMAMAC(300)
    assert tdma_mac.slot_duration == 300
    assert tdma_mac.sensors == []
    assert tdma_mac.current_slot == 0
    print(f"TDMA MAC initialized: Slot Duration={tdma_mac.slot_duration}, Sensors={tdma_mac.sensors}, Current Slot={tdma_mac.current_slot}")

if __name__ == '__main__':
    test_sensor_init()
    test_sensor_read_data_temperature()
    test_sensor_read_data_people_count()
    test_sensor_read_data_co2()
    test_frame_init()
    test_frame_calculate_crc()
    test_frame_to_bytes()
    test_tdmac_init()
    print("All tests passed.")