import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Setup screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Penguins")

def draw_bg():
    """Displays the background image on the screen."""
    bg_image_path = os.path.join("images", "bg_01.jpg")
    try:
        # Using convert_alpha() as requested
        bg_image = pygame.image.load(bg_image_path).convert_alpha()
        # Scale the background to fit the screen
        bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
        screen.blit(bg_image, (0, 0))
    except Exception as e:
        print(f"Error loading background: {e}")

class Penguin(pygame.sprite.Sprite):
    """A class to represent a penguin sprite."""
    def __init__(self, file_name: str, resize: float, x: int, y: int):
        super().__init__()
        penguin_image_path = os.path.join("images", file_name)
        try:
            # Load the image and call convert_alpha() for performance
            self.image = pygame.image.load(penguin_image_path).convert_alpha()
            
            # Resize image
            new_width = int(self.image.get_width() * resize)
            new_height = int(self.image.get_height() * resize)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
            
            # Get rect and mask for positioning and collision
            self.rect = self.image.get_rect(center=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
        except Exception as e:
            print(f"Error loading penguin image {file_name}: {e}")
            # If image fails to load, kill the sprite
            self.kill()

    def handle_click(self, pos):
        """Checks if the sprite was clicked and hides it if so."""
        # First, check bounding box collision
        if self.rect.collidepoint(pos):
            # Then, check pixel-perfect collision using the mask
            local_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
            if self.mask.get_at(local_pos):
                self.kill()  # Remove the sprite from all groups it's in

def main():
    running = True
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    
    # Create penguin instances and add them to the group
    # Note: "pin2.jpeg" does not exist in your images folder and will cause an error.
    penguins_to_create = [
        ("penguin01.jpeg", 0.5, 100, 100),
        ("penguin01.jpeg", 0.5, 300, 300),
        # ("pin2.jpeg", 0.5, 400, 100)
        ("pin3.png", 0.5, 400, 100)
    ]
    
    for file, resize, x, y in penguins_to_create:
        penguin = Penguin(file, resize, x, y)
        all_sprites.add(penguin)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle mouse click for all sprites
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sprite in all_sprites:
                    # Check if the sprite has a handle_click method
                    if hasattr(sprite, 'handle_click'):
                        sprite.handle_click(event.pos)

        # --- Drawing ---
        draw_bg()
        
        # Update and draw all sprites in the group
        all_sprites.update()
        all_sprites.draw(screen)
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate to 60 FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
