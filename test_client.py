#!/usr/bin/env python3
"""
Test client for the synthesizer webserver.
This script demonstrates how to control the audio synthesizer via HTTP requests.
"""

import requests
import time
import json

BASE_URL = "http://localhost:8080"


def test_synthesizer():
    print("Testing Synthesizer Webserver")
    print("=" * 40)

    # Test basic connection
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Server status: {response.text}")
    except requests.exceptions.ConnectionError:
        print("ERROR: Server is not running. Start it with: python server.py")
        return

    # Test getting all notes (should be all False initially)
    response = requests.get(f"{BASE_URL}/notes")
    print(
        f"Initial notes state: {len([n for n in response.json() if n])} notes playing"
    )

    # Play some notes (C major chord: C4=60, E4=64, G4=67)
    print("\nPlaying C major chord (C4, E4, G4)...")
    notes_to_play = [60, 64, 67]  # MIDI note numbers

    for note in notes_to_play:
        response = requests.put(f"{BASE_URL}/note/{note}")
        print(f"Started note {note}: {response.json()}")
        time.sleep(0.1)  # Small delay between notes

    print("Chord should be playing now! Waiting 3 seconds...")
    time.sleep(3)

    # Stop one note (E4)
    print("\nStopping E4 (note 64)...")
    response = requests.delete(f"{BASE_URL}/note/64")
    print(f"Stopped note 64: {response.json()}")

    print("Now only C4 and G4 should be playing. Waiting 2 seconds...")
    time.sleep(2)

    # Play a melody note (F4=65)
    print("\nAdding F4 (note 65)...")
    response = requests.put(f"{BASE_URL}/note/65")
    print(f"Started note 65: {response.json()}")

    print("Now C4, G4, and F4 should be playing. Waiting 2 seconds...")
    time.sleep(2)

    # Reset all notes
    print("\nResetting all notes...")
    response = requests.post(f"{BASE_URL}/notes/reset")
    print(f"All notes stopped. Active notes: {len([n for n in response.json() if n])}")

    print("\nTest completed!")


if __name__ == "__main__":
    test_synthesizer()
