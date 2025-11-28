"""Main screen module for the piano practice application."""

import pygame
import sys


class MainWindow:
    """Main application window with menu bar and content area."""
    
    def __init__(self, width=800, height=600):
        """Initialize the main window."""
        pygame.init()
        
        # Window setup
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Piano Practice")
        
        # Colors
        self.bg_color = (255, 255, 255)
        self.menu_bg_color = (240, 240, 240)
        self.menu_hover_color = (200, 200, 200)
        self.text_color = (0, 0, 0)
        self.dropdown_bg = (250, 250, 250)
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        self.menu_font = pygame.font.Font(None, 20)
        
        # Menu setup
        self.menu_height = 30
        self.dropdown_item_height = 25
        self.menus = []    # Defined in init_menus()
        self.init_menus()  # Then populate it
        
        # State
        self.active_dropdown = None
        self.midi_device_name = "No MIDI Device"
        self.running = True
        self.clock = pygame.time.Clock()
            
    def init_menus(self):
        """Initialize menu structure and positions."""
        self.menus = [
            {
                "name": "File",
                "items": ["Item"],
                "rect": pygame.Rect(10, 0, 60, self.menu_height),
                "dropdown_rects": []
            },
            {
                "name": "Edit", 
                "items": ["Preferences"],
                "rect": pygame.Rect(80, 0, 60, self.menu_height),
                "dropdown_rects": []
            },
            {
                "name": "About",
                "items": ["Item"],
                "rect": pygame.Rect(150, 0, 60, self.menu_height),
                "dropdown_rects": []
            }
        ]
        
        # Calculate dropdown item rectangles
        for menu in self.menus:
            menu["dropdown_rects"] = []
            for i, item in enumerate(menu["items"]):
                rect = pygame.Rect(
                    menu["rect"].x,
                    self.menu_height + i * self.dropdown_item_height,
                    120,  # Dropdown width
                    self.dropdown_item_height
                )
                menu["dropdown_rects"].append(rect)
    
    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.QUIT:
            self.running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_menu_click(event.pos)
                
        elif event.type == pygame.VIDEORESIZE:
            # Update screen size when window is resized
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    
    def handle_menu_click(self, pos):
        """Handle mouse clicks on menus."""
        # Check if clicking on a menu header
        for menu in self.menus:
            if menu["rect"].collidepoint(pos):
                if self.active_dropdown == menu["name"]:
                    self.active_dropdown = None  # Close if already open
                else:
                    self.active_dropdown = menu["name"]  # Open this menu
                return
        
        # Check if clicking on dropdown items
        if self.active_dropdown:
            for menu in self.menus:
                if menu["name"] == self.active_dropdown:
                    for i, rect in enumerate(menu["dropdown_rects"]):
                        if rect.collidepoint(pos):
                            self.on_menu_item_click(menu["name"], menu["items"][i])
                            self.active_dropdown = None
                            return
        
        # Clicking elsewhere closes dropdown
        self.active_dropdown = None
    
    def on_menu_item_click(self, menu_name, item_name):
        """Handle menu item selection."""
        print(f"Clicked: {menu_name} -> {item_name}")
        
        if menu_name == "Edit" and item_name == "Preferences":
            print("Opening preferences...")  # Placeholder for future
            
    def draw_menu_bar(self):
        """Draw the menu bar at the top of the window."""
        # Menu bar background
        menu_rect = pygame.Rect(0, 0, self.screen.get_width(), self.menu_height)
        pygame.draw.rect(self.screen, self.menu_bg_color, menu_rect)
        
        # Draw each menu
        mouse_pos = pygame.mouse.get_pos()
        
        for menu in self.menus:
            # Highlight if hovered or active
            if menu["rect"].collidepoint(mouse_pos) or self.active_dropdown == menu["name"]:
                pygame.draw.rect(self.screen, self.menu_hover_color, menu["rect"])
            
            # Draw menu text
            text = self.menu_font.render(menu["name"], True, self.text_color)
            text_rect = text.get_rect(center=menu["rect"].center)
            self.screen.blit(text, text_rect)
            
            # Draw dropdown if active
            if self.active_dropdown == menu["name"]:
                self.draw_dropdown(menu)
        
        # Draw MIDI device label on the right
        midi_text = self.menu_font.render(f"MIDI: {self.midi_device_name}", True, self.text_color)
        midi_rect = midi_text.get_rect(midright=(self.screen.get_width() - 20, self.menu_height // 2))
        self.screen.blit(midi_text, midi_rect)
        
        # Draw separator line
        pygame.draw.line(self.screen, (200, 200, 200), 
                        (0, self.menu_height), 
                        (self.screen.get_width(), self.menu_height))
    
    def draw_dropdown(self, menu):
        """Draw dropdown menu items."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Calculate dropdown dimensions
        if menu["dropdown_rects"]:
            dropdown_surface = pygame.Rect(
                menu["rect"].x,
                self.menu_height,
                120,
                len(menu["items"]) * self.dropdown_item_height
            )
            # Draw dropdown background
            pygame.draw.rect(self.screen, self.dropdown_bg, dropdown_surface)
            pygame.draw.rect(self.screen, (180, 180, 180), dropdown_surface, 1)
        
        # Draw each dropdown item
        for i, (item, rect) in enumerate(zip(menu["items"], menu["dropdown_rects"])):
            # Highlight on hover
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.menu_hover_color, rect)
            
            # Draw item text
            text = self.menu_font.render(item, True, self.text_color)
            text_rect = text.get_rect(midleft=(rect.x + 10, rect.centery))
            self.screen.blit(text, text_rect)
    
    def draw_content(self):
        """Draw the main content area."""
        # Calculate center position for title
        title_text = self.title_font.render("Piano Practice V1", True, self.text_color)
        title_rect = title_text.get_rect(
            center=(self.screen.get_width() // 2, 
                   self.screen.get_height() // 2)
        )
        self.screen.blit(title_text, title_rect)
    
    def draw(self):
        """Draw everything on screen."""
        self.screen.fill(self.bg_color)
        self.draw_menu_bar()
        self.draw_content()
        pygame.display.flip()
    
    def run(self):
        """Main application loop."""
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()
    
    def set_midi_device(self, device_name):
        """Update the MIDI device name display."""
        self.midi_device_name = device_name


# For testing the module directly
if __name__ == "__main__":
    window = MainWindow()
    window.run()