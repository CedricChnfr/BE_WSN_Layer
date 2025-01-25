import sys
from MAC.Frame import TSFrame, FlagType
from MAC.Sensor import Sensor
from PHY.PHY_layer_functions import modulate_bpsk, show_constellation_diagram, simulate_canal, demodulate_bpsk


# Check if noise argument is provided
if len(sys.argv) != 2:
    noise = 0.05
else:
    try:
        noise = float(sys.argv[1])
    except ValueError:
        noise = 0.05

#Create the sensors
person_counter = Sensor(1, 'people_count')
temperature_sensor = Sensor(2, 'temperature')
air_quality_sensor = Sensor(3, 'co2')

#Create frame from data
frame = TSFrame(FlagType.DATA, 
                12, 
                15, 
                person_counter.read_data(), 
                temperature_sensor.read_data(), 
                int(air_quality_sensor.read_data()*0.01))
print("New frame:\n" + frame.to_string())
frame_bytes = frame.to_bytes()

# Modulate
signal = modulate_bpsk(frame_bytes)
print("Modulation of the signal\n")
show_constellation_diagram(signal, "Constellation Diagram before passing through the canal")

#Pass through canal (get noise)

signal = simulate_canal(signal, noise)
print("Passing through the canal, getting noised\n")
show_constellation_diagram(signal, "Constellation Diagram after passing through the canal")

#Demodulate the signal
received_frame_bytes = demodulate_bpsk(signal)
print("Demodulation of the signal\n")

#Get info from frame
received_frame = TSFrame.create_frame_from_bytes(received_frame_bytes)
print("Received frame:\n" + received_frame.to_string())
if(received_frame.test_current_crc()):
    print(f"Frame corrupted. Current crc: {str(received_frame.crc)}, expected: {str(received_frame.calculate_crc())}")