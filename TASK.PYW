import pygame
import sys
import win32gui
import win32ui
import win32con
import win32api
import win32process
import psutil

# VALUES
IMAGE_PATH = "C:\\TaOS\\RESOURCES\\bgu"
BAR_HEIGHT = 35
BAR_OFFSET = 0
DEFAULT_ICON_PATH = "C:\\TaOS\\RESOURCES\\ico.bmp"
TASK_PY_ICON_PATH = "C:\\TaOS\\RESOURCES\\ico.bmp"

def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)

def get_active_process_name():
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        exe_name = process.name().replace(".exe", "")
        return exe_name.capitalize() if exe_name else None
    except Exception as e:
        print(f"Error getting process name: {e}")
        return None

def get_active_window_icon_surface():
    hwnd = win32gui.GetForegroundWindow()

    hicon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_SMALL, 0)

    if not hicon:
        hicon = win32gui.GetClassLong(hwnd, win32con.GCL_HICON)

    if not hicon:
        return load_default_icon()

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 32, 32)
    hdc_mem = hdc.CreateCompatibleDC()
    hdc_mem.SelectObject(hbmp)
    hdc_mem.DrawIcon((0, 0), hicon)

    bmpinfo = hbmp.GetInfo()
    bmpstr = hbmp.GetBitmapBits(True)

    icon_surface = pygame.image.frombuffer(bmpstr, (bmpinfo['bmWidth'], bmpinfo['bmHeight']), 'BGRA')
    return pygame.transform.smoothscale(icon_surface, (24, 24))

def load_icon_from_file(icon_path):
    try:
        icon_surface = pygame.image.load(icon_path)
        return pygame.transform.smoothscale(icon_surface, (24, 24))
    except pygame.error:
        print(f"Failed to load icon from {icon_path}")
        return None

def load_default_icon():
    return load_icon_from_file(DEFAULT_ICON_PATH)

def draw_block(surface, bar_rect, icon_surface=None, text=None, font=None):
    bar_surface = pygame.Surface((bar_rect.width, bar_rect.height))
    bar_surface.fill((50, 50, 50))  # RGB(50, 50, 50)
    surface.blit(bar_surface, bar_rect.topleft)

    if icon_surface:
        surface.blit(icon_surface, (5, 5))  # Draw icon at top-left

    if text and font:
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(bar_rect.centerx, bar_rect.centery))
        surface.blit(text_surface, text_rect)

def main():
    pygame.init()

    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((screen_width, screen_height))

    background_image = pygame.image.load(IMAGE_PATH)
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    pygame.display.set_caption("TASK.PYW")

    font = pygame.font.SysFont("Lucida Console", 22)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        process_name = get_active_process_name()
        window_title = get_active_window_title()

        if process_name and process_name.lower() == ("pythonw" or "python"):
            display_title = "TaskOS"
            icon_surface = load_icon_from_file(TASK_PY_ICON_PATH)
        else:
            display_title = process_name or ""
            icon_surface = get_active_window_icon_surface()

        screen.blit(background_image, (0, 0))

        block_rect = pygame.Rect(0, BAR_OFFSET, screen_width, BAR_HEIGHT)
        draw_block(screen, block_rect, icon_surface, display_title, font)

        # ALWAYS PUT THIS WINDOW AT THE BOTTOM
        hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
