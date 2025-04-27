import os
os.system("pip install -r C:\\TAOS\\requirements.txt")

import sys
import pygame
import subprocess
import tempfile
import threading
import time
import math

IMAGE_PATH = "C:\\TaOS\\BOOT\\FORM8"  # Updated to your image file path

# === DISPLAY STRETCHED IMAGE AND SLIDING BAR ===
def show_image_while_work(running_flag):
    pygame.init()
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

    pygame.mouse.set_visible(False)
    
    image = pygame.image.load(IMAGE_PATH)
    stretched = pygame.transform.scale(image, (screen_width, screen_height))
    
    # Bar properties
    bar_height = 50  # Height of the bar
    bar_x = 0
    bar_y = 0
    bar_width = screen_width
    transparency = 255  # Start fully opaque
    bar_color = (150, 87, 156)  # Purple color

    clock = pygame.time.Clock()

    while running_flag[0]:
        screen.fill((0, 0, 0))  # Fill the screen with black before drawing new frames

        # Draw the stretched image
        screen.blit(stretched, (0, 0))

        # Draw the sliding purple bar with changing transparency
        surface = pygame.Surface((bar_width, bar_height))  # Create a surface for the bar
        surface.fill(bar_color)  # Fill with purple color
        surface.set_alpha(transparency)  # Set transparency level
        screen.blit(surface, (bar_x, bar_y))

        # Alternate transparency effect
        transparency = int(255 * (0.5 * math.sin(pygame.time.get_ticks() / 1000.0) + 0.5))  # Sine wave for smooth transparency transition

        pygame.display.update()
        clock.tick(60)  # Limit FPS to 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_flag[0] = False

        time.sleep(0.05)

    pygame.quit()

# === CREATE VENV IN TEMP DIRECTORY ===
def install_venv(running_flag):
    with tempfile.TemporaryDirectory() as tempdir:
        print(f"Creating venv in: {tempdir}")
        subprocess.run([sys.executable, "-m", "venv", tempdir], stdout=subprocess.DEVNULL)
        print("Venv setup complete.")
        time.sleep(1)  # Optional: let the image hang for a second
        running_flag[0] = False  # Signal image window to close

        # Run next script
        subprocess.Popen([sys.executable, "C:\\TAOS\\BOOT\\S.PYW"])
        subprocess.Popen([sys.executable, "C:\\TAOS\\TASK.PYW"])

# === MAIN ===
if __name__ == "__main__":
    running = [True]

    image_thread = threading.Thread(target=show_image_while_work, args=(running,))
    venv_thread = threading.Thread(target=install_venv, args=(running,))

    image_thread.start()
    venv_thread.start()

    image_thread.join()
    venv_thread.join()
