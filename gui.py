import pygame
import pygame_gui

pygame.init()
pygame.display.set_caption('Login Form')
window_surface = pygame.display.set_mode((800, 600))
ui_manager = pygame_gui.UIManager((800, 600))
username_text_box = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((275, 200), (250, 50)),
    manager=ui_manager, html_text = ''
)
login_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 300), (100, 50)),
    text='Login',
    manager=ui_manager
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == login_button:
                    # Handle login functionality here
                    pass
                    
        ui_manager.process_events(event)

    ui_manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
