import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Setup screen
screen_width, screen_height = 1000, 600
game_area_width = 800
panel_width = 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Penguins")

# Fonts
font = pygame.font.Font(None, 32)
large_font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)

# Global State
good_count = 0
bad_count = 0
total_good_penguins = 0
num_penguins_input = "15"
input_active = False
game_state = "playing"  # Can be "playing" or "success"

def draw_bg():
    """Displays the background image on the game area."""
    bg_image_path = os.path.join("images", "bg_02.jpeg")
    try:
        bg_image = pygame.image.load(bg_image_path).convert()
        bg_image = pygame.transform.scale(bg_image, (game_area_width, screen_height))
        screen.blit(bg_image, (0, 0))
    except Exception as e:
        print(f"Error loading background: {e}")
        pygame.draw.rect(screen, LIGHT_BLUE, (0, 0, game_area_width, screen_height))

class Penguin(pygame.sprite.Sprite):
    """A class to represent a penguin sprite."""
    def __init__(self, penguin_type: str, resize: float, x: int, y: int):
        super().__init__()
        self.penguin_type = penguin_type
        file_name = "pin_redhat.png" if penguin_type == "good" else "pin_pirate.png"
        penguin_image_path = os.path.join("images", file_name)
        try:
            self.image = pygame.image.load(penguin_image_path).convert_alpha() if file_name.endswith('.png') else pygame.image.load(penguin_image_path).convert()
            new_width, new_height = int(self.image.get_width() * resize), int(self.image.get_height() * resize)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
            self.rect = self.image.get_rect(center=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
        except Exception as e:
            print(f"Error loading penguin image {file_name}: {e}")
            self.kill()

    def handle_click(self, pos):
        """Checks if the sprite was clicked and updates counters. Returns True if a good penguin was clicked."""
        global good_count, bad_count
        if self.rect.collidepoint(pos):
            local_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
            try:
                if self.mask.get_at(local_pos):
                    if self.penguin_type == "good":
                        good_count += 1
                        self.kill()
                        return True
                    else:
                        bad_count += 1
                        self.kill()
            except IndexError:
                pass
        return False

def init_penguins(num_penguins, all_sprites):
    """Initializes penguins and returns the count of 'good' penguins."""
    all_sprites.empty()
    good_penguins_spawned = 0
    for _ in range(num_penguins):
        penguin_type = random.choice(["good", "bad"])
        if penguin_type == "good":
            good_penguins_spawned += 1
        x, y = random.randint(50, game_area_width - 50), random.randint(50, screen_height - 50)
        resize = random.uniform(0.1, 0.5)
        penguin = Penguin(penguin_type, resize, x, y)
        all_sprites.add(penguin)
    return good_penguins_spawned

def draw_panel(input_box, ok_button):
    """Draws the side panel with settings and counters."""
    pygame.draw.rect(screen, GRAY, (game_area_width, 0, panel_width, screen_height))
    good_text = font.render(f"Good: {good_count}", True, GREEN)
    screen.blit(good_text, (game_area_width + 20, 50))
    bad_text = font.render(f"Bad: {bad_count}", True, RED)
    screen.blit(bad_text, (game_area_width + 20, 100))
    label = small_font.render("Number of Penguins:", True, BLACK)
    screen.blit(label, (game_area_width + 10, 200))
    color = pygame.Color('dodgerblue2') if input_active else pygame.Color('lightskyblue3')
    pygame.draw.rect(screen, color, input_box, 2)
    text_surface = font.render(num_penguins_input, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, (100, 100, 100), ok_button)
    ok_text = font.render("OK", True, WHITE)
    screen.blit(ok_text, (ok_button.x + 15, ok_button.y + 5))

def draw_success_popup(restart_button):
    """Draws a success message and restart button."""
    # Semi-transparent overlay
    overlay = pygame.Surface((game_area_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Success message
    success_text = large_font.render("Success!", True, GREEN)
    text_rect = success_text.get_rect(center=(game_area_width // 2, screen_height // 2 - 50))
    screen.blit(success_text, text_rect)
    
    # Restart button
    pygame.draw.rect(screen, (100, 100, 100), restart_button)
    restart_text = font.render("Restart", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)

def restart_game(all_sprites):
    """Resets the game to its initial state."""
    global good_count, bad_count, total_good_penguins, game_state
    good_count, bad_count = 0, 0
    try:
        num_to_spawn = int(num_penguins_input)
    except ValueError:
        num_to_spawn = 5
    total_good_penguins = init_penguins(num_to_spawn, all_sprites)
    game_state = "playing"

def main():
    global input_active, num_penguins_input, game_state, total_good_penguins
    running = True
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    
    input_box = pygame.Rect(game_area_width + 20, 230, 140, 32)
    ok_button = pygame.Rect(game_area_width + 20, 280, 80, 32)
    restart_button = pygame.Rect(game_area_width // 2 - 60, screen_height // 2 + 20, 120, 40)

    total_good_penguins = init_penguins(int(num_penguins_input), all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if mouse_pos[0] < game_area_width:
                        for sprite in all_sprites:
                            if hasattr(sprite, 'handle_click') and sprite.handle_click(mouse_pos):
                                if total_good_penguins > 0 and good_count == total_good_penguins:
                                    game_state = "success"
                    else:
                        if input_box.collidepoint(mouse_pos): input_active = True
                        else: input_active = False
                        if ok_button.collidepoint(mouse_pos):
                            restart_game(all_sprites)
                elif event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_RETURN:
                        restart_game(all_sprites)
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        num_penguins_input = num_penguins_input[:-1]
                    elif event.unicode.isdigit() and len(num_penguins_input) < 3:
                        num_penguins_input += event.unicode
            
            elif game_state == "success":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button.collidepoint(event.pos):
                        restart_game(all_sprites)

        # --- Drawing ---
        draw_bg()
        all_sprites.draw(screen)
        draw_panel(input_box, ok_button)
        
        if game_state == "success":
            draw_success_popup(restart_button)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
