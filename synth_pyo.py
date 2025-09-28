from typing import Dict, Set
from pyo import Server, Sine  # <-- explicit imports

# Generate sine waves for audio synthesis using PYO

MIDI_NOTE_TO_FREQUENCY = {
    note: 440.0 * 2 ** ((note - 69) / 12) for note in range(21, 109)
}


class AudioSynthesizer:
    def __init__(self, sample_rate=44100, chunk_size=1024, volume=0.5):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.volume = volume
        self.playing_notes: Set[int] = set()
        self.sine_oscillators: Dict[int, Sine] = {}
        self.running = False

        # Initialize PYO server
        self.server = Server(sr=sample_rate, buffersize=chunk_size)

    def start(self):
        """Start the audio engine"""
        if self.running:
            return

        self.running = True

        # Boot and start the PYO server
        self.server.boot()
        self.server.start()

        print(f"Audio synthesizer started (sample rate: {self.sample_rate}Hz)")

    def stop(self):
        """Stop the audio engine"""
        if not self.running:
            return

        self.running = False

        # Stop all oscillators
        for osc in self.sine_oscillators.values():
            osc.stop()
        self.sine_oscillators.clear()

        # Stop and shutdown the PYO server
        self.server.stop()
        self.server.shutdown()

        print("Audio synthesizer stopped")

    def add_note(self, note_number: int):
        """Start playing a MIDI note"""
        if (
            note_number in MIDI_NOTE_TO_FREQUENCY
            and note_number not in self.playing_notes
        ):
            frequency = MIDI_NOTE_TO_FREQUENCY[note_number]

            # Create a sine wave oscillator for this note
            # Apply volume scaling and divide by max possible notes for headroom
            amplitude = self.volume / 10  # Prevent clipping with multiple notes
            sine_osc = Sine(freq=frequency, mul=amplitude).out()

            self.playing_notes.add(note_number)
            self.sine_oscillators[note_number] = sine_osc

            print(f"Started playing note {note_number} ({frequency:.2f} Hz)")
        elif note_number not in MIDI_NOTE_TO_FREQUENCY:
            print(f"Invalid note number: {note_number}")
        else:
            print(f"Note {note_number} is already playing")

    def remove_note(self, note_number: int):
        """Stop playing a MIDI note"""
        if note_number in self.playing_notes:
            # Stop and remove the oscillator
            self.sine_oscillators[note_number].stop()
            del self.sine_oscillators[note_number]

            self.playing_notes.remove(note_number)
            print(f"Stopped playing note {note_number}")
        else:
            print(f"Note {note_number} is not currently playing")

    def reset_notes(self):
        """Stop playing all notes"""
        for osc in self.sine_oscillators.values():
            osc.stop()

        self.playing_notes.clear()
        self.sine_oscillators.clear()
        print("All notes stopped")
