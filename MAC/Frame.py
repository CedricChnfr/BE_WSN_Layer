
import struct
import ctypes
from enum import Enum

class FlagType(Enum):
    ACK = 0
    DATA = 1
    DISCOVER = 2

class Frame:
    def __init__(self, flag: FlagType | int, dest_address: int, src_address: int, data: int):
        self.sfd = 0xA5  # Start Frame Delimiter
        if flag.__class__ == FlagType:
            self.flag = flag.value  # Convert FlagType to integer
        elif flag.__class__ == int:
            self.flag = flag
        else:
            raise TypeError("Flag should be of type FlagType or int")
        self.dest_address = dest_address  # 10 bits
        self.src_address = src_address  # 10 bits
        self.data = data  # 24 bits
        self.crc = self.calculate_crc()  # 8 bits

    @classmethod
    def create_frame_from_bytes(cls, frame_as_bytes: bytes) -> "Frame":
        """
        Given an 8-bytes long frame, create the equivalent frame object to be read and manipulated.
        """

        if len(frame_as_bytes) != 8:
            print(len(frame_as_bytes))
            raise ValueError("Invalid frame length")
        
        first_half, second_half = struct.unpack('II', frame_as_bytes)
        first_half = ~first_half & 0xFFFFFFFF  # Invert bits and mask to 32 bits
        second_half = ~second_half & 0xFFFFFFFF  # Invert bits and mask to 32 bits
        flag = (first_half & 0x00F00000) >> 20
        dest_address = (first_half & 0xFFC00) >> 10
        src_address = (first_half & 0x3FF)
        data= second_half >> 8
        crc = second_half & 0xFF
        frame = cls(flag, dest_address, src_address, data)
        frame.crc = crc
        return frame

    def calculate_crc(self) -> int:
        """
        Calculate a simple CRC (Cyclic Redundancy Check) for the frame.
        This is a placeholder for an actual CRC calculation.
        """
        crc_data = (self.flag << 44) | (self.dest_address << 34) | (self.src_address << 24) | self.data
        crc = 0
        while crc_data:
            crc ^= crc_data & 0xFF
            crc_data >>= 8
        return crc

    def to_bytes(self) -> bytes:
        """
        Convert the frame to bytes.
        """
        frame_bytes = struct.pack(
            'II',
            self.sfd << 24 | self.flag << 20  | self.dest_address << 10 | self.src_address,
            self.data << 8 | self.crc
        )
        return frame_bytes

    def to_string_as_bits(self) -> str:
        """
        Return the frame as a string representing the bits.
        """
        frame_bits = ''.join(format(byte, '08b') for byte in self.to_bytes())
        return frame_bits

    def to_string(self) -> str:
        """
        Return the frame as a string with all the contained information.
        """
        return f"""---frame---
sfd: {self.sfd},
flag: {self.flag},
destination address: {self.dest_address},
source address: {self.src_address},
crc: {self.src_address},
data: {self.data},
binary: {self.to_string_as_bits()}
-----------"""
    
class TSFrame(Frame):
    def __init__(self, flag: FlagType | int, dest_address: int, src_address: int, nb_person: int, temperature: int, air_quality: int):
        self.sfd = 0xA5  # Start Frame Delimiter
        if flag.__class__ == FlagType:
            self.flag = flag.value  # Convert FlagType to integer
        elif flag.__class__ == int:
            self.flag = flag
        else:
            raise TypeError("Flag should be of type FlagType or int")
        self.dest_address = dest_address  # 10 bits
        self.src_address = src_address  # 10 bits
        self.nb_person = nb_person
        self.temperature = ctypes.c_int8(temperature).value 
        self.air_quality = air_quality
        self.data = ((nb_person & (0xFF)) << 16) | ((temperature & (0xFF)) << 8) | (air_quality & (0xFF))
        self.crc = self.calculate_crc()  # 8 bits

    @classmethod
    def cast_frame_to_tsframe(cls, frame: Frame) -> "TSFrame":
        nb_person = (frame.data >> 16) & 0xFF
        temperature = ctypes.c_int8((frame.data >> 8) & 0xFF).value  # Ensure temperature is signed
        air_quality = frame.data & 0xFF
        return TSFrame(frame.flag, frame.dest_address, frame.src_address, nb_person, temperature, air_quality)
    @classmethod
    def create_frame_from_bytes(cls, frame_as_bytes: bytes) -> "TSFrame":
        """
        Given an 8-bytes long frame, create the equivalent frame object to be read and manipulated.
        """
        return TSFrame.cast_frame_to_tsframe(Frame.create_frame_from_bytes(frame_as_bytes))

    def to_string(self) -> str:
        """
        Return the frame as a string with all the contained information.
        """
        return f"""---frame---
sfd: {self.sfd},
flag: {self.flag},
destination address: {self.dest_address},
source address: {self.src_address},
crc: {self.src_address},
number of persons: {self.nb_person},
temperature: {self.temperature},
air quality: {self.air_quality},
binary: {self.to_string_as_bits()}
-----------"""
    
