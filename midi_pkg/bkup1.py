import pygame.midi

def main():
    pygame.midi.init()
    input_id = pygame.midi.get_default_input_id()
    if input_id == -1:
        print("No MIDI input device found.")
        return

    midi_input = pygame.midi.Input(input_id)
    print("Listening for MIDI input. Press Ctrl+C to exit.")

    try:
        while True:
            if midi_input.poll():
                midi_events = midi_input.read(10)
                for event in midi_events:
                    data, timestamp = event
                    status, note, velocity, _ = data
                    # Note On event (status 144) and velocity > 0
                    if status == 144 and velocity > 0:
         import pygame.midi

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_to_string(note_number):
    note_name = NOTE_NAMES[note_number % 12]
    octave = (note_number // 12) - 1
    return f"{note_name}{octave}"

def main():
    pygame.midi.init()
    input_id = pygame.midi.get_default_input_id()
    if input_id == -1:
        print("No MIDI input device found.")
        return

    midi_input = pygame.midi.Input(input_id)
    print("Listening for MIDI input. Press Ctrl+C to exit.")

    try:
        while True:
            if midi_input.poll():
                midi_events = midi_input.read(10)
                for event in midi_events:
                    data, timestamp = event
                    status, note, velocity, _ = data
                    if status == 144 and velocity > 0:
                        note_str = note_to_string(note)
                        print(f"Note: {note} ({note_str}, {velocity}) .", end="", flush=True)
                    elif status == 128 or (status == 144 and velocity == 0):
                        print(" Note Off")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        midi_input.close()
        pygame.midi.quit()

if __name__ == "__main__":
    main()               print(f"Note: {note} ({velocity}) .", end="", flush=True)
                    # Note Off event (status 128) or Note On with velocity 0
                    elif status == 128 or (status == 144 and velocity == 0):
                        print(" Note Off")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        midi_input.close()
        pygame.midi.quit()

if __name__ == "__main__":
    main()