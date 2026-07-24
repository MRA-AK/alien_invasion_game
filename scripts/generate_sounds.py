"""Generate deterministic, original arcade sound effects as PCM WAV files."""

from pathlib import Path
import math
import struct
import wave


SAMPLE_RATE = 44_100
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "sounds"


def _write_sound(filename, duration, sample_function, volume=0.35):
    """Write a mono 16-bit waveform with a short fade-out envelope."""
    frame_count = int(SAMPLE_RATE * duration)
    frames = bytearray()
    for index in range(frame_count):
        time = index / SAMPLE_RATE
        envelope = max(0.0, 1.0 - index / frame_count)
        sample = max(-1.0, min(1.0, sample_function(time)))
        frames.extend(struct.pack("<h", int(32_767 * volume * envelope * sample)))

    OUTPUT_DIR.mkdir(exist_ok=True)
    with wave.open(str(OUTPUT_DIR / filename), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(frames)


def generate_sounds():
    """Generate the complete sound set; no external samples are used."""
    _write_sound(
        "laser.wav",
        0.14,
        lambda time: math.sin(2 * math.pi * (880 - 2_400 * time) * time),
        0.28,
    )
    _write_sound(
        "explosion.wav",
        0.28,
        lambda time: (
            math.sin(2 * math.pi * 110 * time)
            + 0.55 * math.sin(2 * math.pi * 173 * time)
            + 0.25 * math.sin(2 * math.pi * 347 * time)
        )
        / 1.8,
        0.42,
    )
    _write_sound(
        "game_over.wav",
        0.75,
        lambda time: math.sin(
            2 * math.pi * (330 if time < 0.25 else 220 if time < 0.5 else 147) * time
        ),
        0.32,
    )


if __name__ == "__main__":
    generate_sounds()
