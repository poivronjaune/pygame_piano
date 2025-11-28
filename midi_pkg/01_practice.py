import pygame
import pygame.midi
import random

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(2, 7))  # Octaves 2 to 6
WHITE_KEY_INDICES = [0, 2, 4, 5, 7, 9, 11]  # Indices for C, D, E, F, G, A, B

FRENCH_NOTE_NAMES = {
    'C': 'Do',
    'D': 'Ré',
    'E': 'Mi',
    'F': 'Fa',
    'G': 'Sol',
    'A': 'La',
    'B': 'Si'
}

def note_to_string(note_number):
    note_name = NOTE_NAMES[note_number % 12]
    octave = (note_number // 12) - 1
    return f"{note_name}{octave}"

def get_french_note(note_number):
    note_name = NOTE_NAMES[note_number % 12]
    if len(note_name) == 1 and note_name in FRENCH_NOTE_NAMES:
        return FRENCH_NOTE_NAMES[note_name]
    return note_name  # fallback for sharps

def get_notes_for_octaves(selected_octaves, only_white_keys):
    notes = []
    for octave in selected_octaves:
        base = (octave + 1) * 12
        if only_white_keys:
            notes.extend([base + i for i in WHITE_KEY_INDICES])
        else:
            notes.extend(range(base, base + 12))
    return notes

def random_note(selected_octaves, only_white_keys):
    notes = get_notes_for_octaves(selected_octaves, only_white_keys)
    return random.choice(notes) if notes else 60

def main():
    pygame.init()
    pygame.midi.init()
    input_id = pygame.midi.get_default_input_id()
    if input_id == -1:
        print("No MIDI input device found.")
        return

    midi_input = pygame.midi.Input(input_id)
    width, height = 800, 550
    header_height = 60
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Practice Notes")

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    header_font = pygame.font.SysFont(None, int(22 * 0.75))  # Reduce header text size by 25%
    clock = pygame.time.Clock()

    selected_octaves = {octave: (octave == 4) for octave in OCTAVES}
    checkbox_rects = {}

    white_keys_only = True
    white_key_checkbox_rect = pygame.Rect(600, 18, 18, 18)

    show_french_note = True
    french_note_checkbox_rect = pygame.Rect(720, 18, 18, 18)

    start_x = 30
    box_size = 18
    spacing = 90
    for i, octave in enumerate(OCTAVES):
        checkbox_rects[octave] = pygame.Rect(start_x + i * spacing, 18, box_size, box_size)

    lines = []
    running = True
    def make_request_str(note):
        base = f"Play: {note_to_string(note)}"
        if show_french_note:
            base += f" ({get_french_note(note)})"
        return base

    current_note = random_note([oct for oct, sel in selected_octaves.items() if sel], white_keys_only)
    request_str = make_request_str(current_note)
    lines.append(request_str)
    show_checkmark = False
    checkmark_timer = 0

    while running:
        header_changed = False  # Track if header config changed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for octave, rect in checkbox_rects.items():
                    if rect.collidepoint(mouse_pos):
                        selected_octaves[octave] = not selected_octaves[octave]
                        if not any(selected_octaves.values()):
                            selected_octaves[4] = True
                        header_changed = True
                if white_key_checkbox_rect.collidepoint(mouse_pos):
                    white_keys_only = not white_keys_only
                    header_changed = True
                if french_note_checkbox_rect.collidepoint(mouse_pos):
                    show_french_note = not show_french_note
                    header_changed = True

        # If header changed, generate a new note and update the request line
        if header_changed:
            allowed_octaves = [oct for oct, sel in selected_octaves.items() if sel]
            current_note = random_note(allowed_octaves, white_keys_only)
            request_str = make_request_str(current_note)
            lines.append((request_str, "normal"))

        if midi_input.poll():
            midi_events = midi_input.read(10)
            for event in midi_events:
                data, timestamp = event
                status, note, velocity, _ = data
                if status == 144 and velocity > 0:
                    pressed_str = note_to_string(note)
                    if note == current_note:
                        lines[-1] = (f"{request_str} | You played: {pressed_str}", "success")
                        show_checkmark = True
                        checkmark_timer = pygame.time.get_ticks()
                        allowed_octaves = [oct for oct, sel in selected_octaves.items() if sel]
                        current_note = random_note(allowed_octaves, white_keys_only)
                        request_str = make_request_str(current_note)
                        lines.append((request_str, "normal"))
                    else:
                        lines[-1] = (f"{request_str} | You played: {pressed_str} (error)", "error")
                        lines.append((request_str, "normal"))

        screen.fill((40, 40, 40))
        pygame.draw.rect(screen, (220, 220, 220), (0, 0, width, header_height))

        for octave, rect in checkbox_rects.items():
            pygame.draw.rect(screen, (180, 180, 180), rect)
            if selected_octaves[octave]:
                pygame.draw.rect(screen, (0, 120, 0), rect.inflate(-6, -6))
            label = header_font.render(f"Oct {octave}", True, (0, 0, 0))
            screen.blit(label, (rect.x + box_size + 6, rect.y - 2))

        pygame.draw.rect(screen, (180, 180, 180), white_key_checkbox_rect)
        if white_keys_only:
            pygame.draw.rect(screen, (0, 120, 0), white_key_checkbox_rect.inflate(-6, -6))
        label = header_font.render("White keys only", True, (0, 0, 0))
        screen.blit(label, (white_key_checkbox_rect.x + box_size + 8, white_key_checkbox_rect.y - 2))

        pygame.draw.rect(screen, (180, 180, 180), french_note_checkbox_rect)
        if show_french_note:
            pygame.draw.rect(screen, (0, 120, 0), french_note_checkbox_rect.inflate(-6, -6))
        label = header_font.render("Show French note", True, (0, 0, 0))
        screen.blit(label, (french_note_checkbox_rect.x + box_size + 8, french_note_checkbox_rect.y - 2))

        for i, line_data in enumerate(lines[-8:]):
            if isinstance(line_data, tuple):
                line, status = line_data
            else:
                line, status = line_data, "normal"
            if status == "success":
                color = (0, 255, 0)
            elif status == "error":
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            text_surface = small_font.render(line, True, color)
            screen.blit(text_surface, (30, header_height + 20 + i * 40))

        if show_checkmark:
            if pygame.time.get_ticks() - checkmark_timer < 1000:
                check_surface = font.render("✔", True, (0, 200, 0))
                screen.blit(check_surface, (600, header_height + 20 + (len(lines[-8:]) - 2) * 40))
            else:
                show_checkmark = False

        pygame.display.flip()
        clock.tick(60)

    midi_input.close()
    pygame.midi.quit()
    pygame.quit()

if __name__ == "__main__":
    main()