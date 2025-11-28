import pygame
import pygame.midi
import random

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(2, 7))
WHITE_KEY_INDICES = [0, 2, 4, 5, 7, 9, 11]
FRENCH_NOTE_NAMES = {
    'C': 'Do', 'D': 'Ré', 'E': 'Mi', 'F': 'Fa',
    'G': 'Sol', 'A': 'La', 'B': 'Si'
}

class Checkbox:
    def __init__(self, rect, label, checked=True):
        self.rect = rect
        self.label = label
        self.checked = checked

    def draw(self, surface, font, box_size=18):
        pygame.draw.rect(surface, (180, 180, 180), self.rect)
        if self.checked:
            pygame.draw.rect(surface, (0, 120, 0), self.rect.inflate(-6, -6))
        label_surface = font.render(self.label, True, (0, 0, 0))
        surface.blit(label_surface, (self.rect.x + box_size + 6, self.rect.y - 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                return True
        return False

class PracticeApp:
    def __init__(self):
        pygame.init()
        pygame.midi.init()
        self.input_id = pygame.midi.get_default_input_id()
        if self.input_id == -1:
            print("No MIDI input device found.")
            exit()
        self.midi_input = pygame.midi.Input(self.input_id)
        self.width, self.height = 800, 550
        self.header_height = 60
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Practice Notes")
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 36)
        self.header_font = pygame.font.SysFont(None, int(22 * 0.75))
        self.clock = pygame.time.Clock()
        self.lines = []
        self.show_checkmark = False
        self.checkmark_timer = 0

        # Octave checkboxes
        self.octave_checkboxes = []
        start_x, box_size, spacing = 30, 18, 90
        for i, octave in enumerate(OCTAVES):
            checked = (octave == 4)
            rect = pygame.Rect(start_x + i * spacing, 18, box_size, box_size)
            self.octave_checkboxes.append(Checkbox(rect, f"Oct {octave}", checked))

        # White key only checkbox
        self.white_key_checkbox = Checkbox(pygame.Rect(600, 18, 18, 18), "White keys only", True)
        # French note checkbox
        self.french_note_checkbox = Checkbox(pygame.Rect(720, 18, 18, 18), "Show French note", True)

        self.current_note = self.generate_note()
        self.request_str = self.make_request_str(self.current_note)
        self.lines.append((self.request_str, "normal"))

    def get_selected_octaves(self):
        return [OCTAVES[i] for i, cb in enumerate(self.octave_checkboxes) if cb.checked]

    def generate_note(self):
        selected_octaves = self.get_selected_octaves()
        only_white_keys = self.white_key_checkbox.checked
        notes = []
        for octave in selected_octaves:
            base = (octave + 1) * 12
            if only_white_keys:
                notes.extend([base + i for i in WHITE_KEY_INDICES])
            else:
                notes.extend(range(base, base + 12))
        return random.choice(notes) if notes else 60

    def note_to_string(self, note_number):
        note_name = NOTE_NAMES[note_number % 12]
        octave = (note_number // 12) - 1
        return f"{note_name}{octave}"

    def get_french_note(self, note_number):
        note_name = NOTE_NAMES[note_number % 12]
        if len(note_name) == 1 and note_name in FRENCH_NOTE_NAMES:
            return FRENCH_NOTE_NAMES[note_name]
        return note_name

    def make_request_str(self, note):
        base = f"Play: {self.note_to_string(note)}"
        if self.french_note_checkbox.checked:
            base += f" ({self.get_french_note(note)})"
        return base

    def handle_header_event(self, event):
        header_changed = False
        for cb in self.octave_checkboxes:
            if cb.handle_event(event):
                if not any(c.checked for c in self.octave_checkboxes):
                    # Always keep at least Oct4 selected
                    self.octave_checkboxes[2].checked = True
                header_changed = True
        if self.white_key_checkbox.handle_event(event):
            header_changed = True
        if self.french_note_checkbox.handle_event(event):
            header_changed = True
        return header_changed

    def handle_midi_event(self, note):
        pressed_str = self.note_to_string(note)
        if note == self.current_note:
            self.lines[-1] = (f"{self.request_str} | You played: {pressed_str}", "success")
            self.show_checkmark = True
            self.checkmark_timer = pygame.time.get_ticks()
            self.current_note = self.generate_note()
            self.request_str = self.make_request_str(self.current_note)
            self.lines.append((self.request_str, "normal"))
        else:
            self.lines[-1] = (f"{self.request_str} | You played: {pressed_str} (error)", "error")
            self.lines.append((self.request_str, "normal"))

    def draw_header(self):
        pygame.draw.rect(self.screen, (220, 220, 220), (0, 0, self.width, self.header_height))
        for cb in self.octave_checkboxes:
            cb.draw(self.screen, self.header_font)
        self.white_key_checkbox.draw(self.screen, self.header_font)
        self.french_note_checkbox.draw(self.screen, self.header_font)

    def draw_lines(self):
        for i, line_data in enumerate(self.lines[-8:]):
            line, status = line_data if isinstance(line_data, tuple) else (line_data, "normal")
            color = (0, 255, 0) if status == "success" else (255, 0, 0) if status == "error" else (255, 255, 255)
            text_surface = self.small_font.render(line, True, color)
            self.screen.blit(text_surface, (30, self.header_height + 20 + i * 40))

    def draw_checkmark(self):
        if self.show_checkmark and pygame.time.get_ticks() - self.checkmark_timer < 1000:
            check_surface = self.font.render("✔", True, (0, 200, 0))
            self.screen.blit(check_surface, (600, self.header_height + 20 + (len(self.lines[-8:]) - 2) * 40))
        elif self.show_checkmark:
            self.show_checkmark = False

    def run(self):
        running = True
        while running:
            header_changed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.handle_header_event(event):
                        self.current_note = self.generate_note()
                        self.request_str = self.make_request_str(self.current_note)
                        self.lines.append((self.request_str, "normal"))
                        header_changed = True

            if self.midi_input.poll():
                midi_events = self.midi_input.read(10)
                for event in midi_events:
                    data, timestamp = event
                    status, note, velocity, _ = data
                    if status == 144 and velocity > 0:
                        self.handle_midi_event(note)

            self.screen.fill((40, 40, 40))
            self.draw_header()
            self.draw_lines()
            self.draw_checkmark()
            pygame.display.flip()
            self.clock.tick(60)

        self.midi_input.close()
        pygame.midi.quit()
        pygame.quit()

if __name__ == "__main__":
    PracticeApp().run()