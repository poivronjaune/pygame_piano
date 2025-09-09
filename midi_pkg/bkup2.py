import pygame
import pygame.midi
import random

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_to_string(note_number):
    note_name = NOTE_NAMES[note_number % 12]
    octave = (note_number // 12) - 1
    return f"{note_name}{octave}"

def random_note():
    # MIDI note numbers for piano range (A0=21 to C8=108)
    note_number = random.randint(48, 72)  # C3 to C5 for easier practice
    return note_number

def main():
    pygame.init()
    pygame.midi.init()
    input_id = pygame.midi.get_default_input_id()
    if input_id == -1:
        print("No MIDI input device found.")
        return

    midi_input = pygame.midi.Input(input_id)
    width, height = 500, 300
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Practice Notes")

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    lines = []
    running = True
    current_note = random_note()
    request_str = f"Play: {note_to_string(current_note)}"
    lines.append(request_str)
    show_checkmark = False
    checkmark_timer = 0

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
                    pressed_str = note_to_string(note)
                    # Display pressed note on same line
                    if note == current_note:
                        lines[-1] = f"{request_str} | You played: {pressed_str}"
                        show_checkmark = True
                        checkmark_timer = pygame.time.get_ticks()
                        # Prepare next note
                        current_note = random_note()
                        request_str = f"Play: {note_to_string(current_note)}"
                        lines.append(request_str)
                    else:
                        lines[-1] = f"{request_str} | You played: {pressed_str} (error)"
                        # Request same note again on next line
                        lines.append(request_str)

        screen.fill((40, 40, 40))

        # Draw lines
        for i, line in enumerate(lines[-6:]):  # Show last 6 lines
            text_surface = small_font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (30, 40 + i * 40))

        # Draw checkmark if correct
        if show_checkmark:
            if pygame.time.get_ticks() - checkmark_timer < 1000:
                check_surface = font.render("✔", True, (0, 255, 0))
                screen.blit(check_surface, (400, 40 + (len(lines[-6:]) - 2) * 40))
            else:
                show_checkmark = False

        pygame.display.flip()
        clock.tick(60)

    midi_input.close()
    pygame.midi.quit()
    pygame.quit()

if __name__ == "__main__":
    main()