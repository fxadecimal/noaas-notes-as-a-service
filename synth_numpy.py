import pyaudio
import numpy as np
import threading
import time
from typing import Dict, Set

# Generate sine waves for audio synthesis

MIDI_NOTE_TO_FREQUENCY = {
    note: 440.0 * 2 ** ((note - 69) / 12) for note in range(21, 109)
}


class AudioSynthesizer:
    def __init__(self, sample_rate=44100, chunk_size=1024, volume=0.5):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.volume = volume
        self.playing_notes: Set[int] = set()
        self.note_phases: Dict[int, float] = {}
        self.running = False
        self.audio_thread = None

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start(self):
        """Start the audio engine"""
        if self.running:
            return

        self.running = True

        # Open audio stream
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            output=True,
            frames_per_buffer=self.chunk_size,
        )

        # Start audio generation thread
        self.audio_thread = threading.Thread(target=self._audio_loop, daemon=True)
        self.audio_thread.start()

        print(f"Audio synthesizer started (sample rate: {self.sample_rate}Hz)")

    def stop(self):
        """Stop the audio engine"""
        if not self.running:
            return

        self.running = False

        if self.audio_thread:
            self.audio_thread.join()

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.p.terminate()
        print("Audio synthesizer stopped")

    def add_note(self, note_number: int):
        """Start playing a MIDI note"""
        if note_number in MIDI_NOTE_TO_FREQUENCY:
            self.playing_notes.add(note_number)
            self.note_phases[note_number] = 0.0
            print(
                f"Started playing note {note_number} ({MIDI_NOTE_TO_FREQUENCY[note_number]:.2f} Hz)"
            )
        else:
            print(f"Invalid note number: {note_number}")

    def remove_note(self, note_number: int):
        """Stop playing a MIDI note"""
        if note_number in self.playing_notes:
            self.playing_notes.remove(note_number)
            if note_number in self.note_phases:
                del self.note_phases[note_number]
            print(f"Stopped playing note {note_number}")

    def reset_notes(self):
        """Stop playing all notes"""
        self.playing_notes.clear()
        self.note_phases.clear()
        print("All notes stopped")

    def _audio_loop(self):
        """Main audio generation loop"""
        while self.running:
            if not self.playing_notes:
                # Generate silence when no notes are playing
                audio_data = np.zeros(self.chunk_size, dtype=np.float32)
            else:
                # Generate and mix sine waves for all playing notes
                audio_data = np.zeros(self.chunk_size, dtype=np.float32)

                for (
                    note_number
                ) in (
                    self.playing_notes.copy()
                ):  # Copy to avoid modification during iteration
                    frequency = MIDI_NOTE_TO_FREQUENCY[note_number]
                    phase = self.note_phases[note_number]

                    # Generate time array for this chunk
                    time_array = np.arange(self.chunk_size) / self.sample_rate

                    # Generate sine wave
                    sine_wave = np.sin(2 * np.pi * frequency * time_array + phase)

                    # Add to the mix (with equal amplitude for each note)
                    audio_data += sine_wave / len(self.playing_notes)

                    # Update phase for continuity
                    self.note_phases[note_number] = (
                        phase
                        + 2 * np.pi * frequency * self.chunk_size / self.sample_rate
                    ) % (2 * np.pi)

                # Apply volume
                audio_data *= self.volume

                # Clip to prevent distortion
                audio_data = np.clip(audio_data, -1.0, 1.0)

            # Output audio
            try:
                self.stream.write(audio_data.tobytes())
            except Exception as e:
                print(f"Audio output error: {e}")
                break
