import numpy as np
import matplotlib.pyplot as plt

def modulate_bpsk(trame: bytes) -> np.ndarray:
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
    signal = np.cos(x_radians) + 1j * np.sin(x_radians)
    return signal

def demodulate_bpsk(signal: np.ndarray) -> bytes:
    """
    Demodulate a BPSK signal to a byte frame.
    
    Parameters:
    signal (np.ndarray): The modulated signal.
    
    Returns:
    bytes: The demodulated byte frame.
    """
    # BPSK demodulation: map positive values to 1 and negative values to 0
    bits = np.where(np.real(signal) > 0, 1, 0)
    
    # Convert bits to bytes
    byte_frame = np.packbits(bits)
    
    return byte_frame.tobytes()

def show_constellation_diagram(signal: np.ndarray, title: str = "Constellation Diagram"):
    plt.plot(np.real(signal), np.imag(signal), '.')
    circle = plt.Circle((0, 0), 1, color='grey', fill=False)
    plt.gca().add_artist(circle)
    plt.grid(True)
    plt.title(title)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def simulate_canal(signal: np.ndarray, noise_strength: float = 0.05) -> np.ndarray:
    phase_noise = np.random.randn(len(signal)) * noise_strength
    signal = signal * np.exp(1j * phase_noise)
    other_noise = np.random.randn(len(signal))*noise_strength
    signal += other_noise
    return signal


