import numpy as np
import matplotlib.pyplot as plt
from .Signal import Signal

def modulate_bpsk(trame: bytes) -> Signal:
    """
    Modulate a byte frame to a signal using BPSK modulation.
    
    Parameters:
    bytes: The demodulated byte frame.
    
    Returns:
    signal (np.ndarray): The modulated signal.
    """
    bits = np.unpackbits(np.frombuffer(trame, dtype=np.uint8))
    x_degrees = bits * 360 / 2.0
    x_radians = x_degrees * np.pi / 180.0
    signal_array = np.cos(x_radians) + 1j * np.sin(x_radians)
    return Signal(signal_array)

def demodulate_bpsk(signal: Signal) -> bytes:
    """
    Demodulate a BPSK signal to a byte frame.
    
    Parameters:
    signal (np.ndarray): The modulated signal.
    
    Returns:
    bytes: The demodulated byte frame.
    """
    # BPSK demodulation: map positive values to 1 and negative values to 0
    bits = np.where(np.real(signal.value) > 0, 1, 0)
    
    # Convert bits to bytes
    byte_frame = np.packbits(bits)
    
    return byte_frame.tobytes()

def show_constellation_diagram(signal: Signal, title: str = "Constellation Diagram"):
    plt.plot(np.real(signal.value), np.imag(signal.value), '.')
    circle = plt.Circle((0, 0), 1, color='grey', fill=False)
    plt.gca().add_artist(circle)
    plt.grid(True)
    plt.title(title)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def simulate_canal(signal: Signal, noise_strength: float = 0.05) -> Signal:
    phase_noise = np.random.randn(len(signal.value)) * noise_strength
    other_noise = np.random.randn(len(signal.value))*noise_strength
    signal_noise_array = signal.value * np.exp(1j * phase_noise) + other_noise
    return Signal(signal_noise_array)


