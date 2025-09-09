import pygame
import pygame.midi

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_to_string(note_number):
    note_name = NOTE_NAMES[note_number % 12]
    octave = (note_number // 12) - 1
    return f"{note_name}{octave}"

def main():
    pygame.init()
    pygame.midi.init()
    input_id = pygame.midi.get_default_input_id()
    if input_id == -1:
        print("No MIDI input device found.")
        return

    midi_input = pygame.midi.Input(input_id)
    width, height = 400, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MIDI Note Visualizer")

    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    notes_display = []
    scroll_y = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if midi_input.poll():
            midi_events = midi_input.read(10)
            for event in midi_events:
                data, timestamp = event
                status, note, velocity, _ = data
                if status == 144 and velocity > 0:
                    note_str = note_to_string(note)
                    notes_display.append(f"Note: {note} ({note_str}, {velocity})")
                    scroll_y += 40  # Scroll down for each note

        screen.fill((30, 30, 30))

        # Only show the last 20 notes for performance
        for i, note_text in enumerate(notes_display[-20:]):
            text_surface = font.render(note_text, True, (255, 255, 255))
            y_pos = 20 + i * 40 - max(0, scroll_y - height + 40)
            screen.blit(text_surface, (20, y_pos))

        pygame.display.flip()
        clock.tick(60)

    midi_input.close()
    pygame.midi.quit()
    pygame.quit()

if __name__ == "__main__":
    main()