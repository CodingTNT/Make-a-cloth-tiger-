import pygame

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("换装游戏")

background = pygame.image.load('backgroundtiger.png').convert_alpha()

body = pygame.image.load('body.png').convert_alpha()

ears = pygame.image.load('ears.png').convert_alpha()
eye_left = pygame.image.load('eye_left.png').convert_alpha()
eye_right = pygame.image.load('eye_right.png').convert_alpha()
mustache = pygame.image.load('mustache.png').convert_alpha()
nose = pygame.image.load('nose.png').convert_alpha()

mouse_cursor = pygame.image.load('mouse.png').convert_alpha()

ears_pos = [500, 550]
eye_left_pos = [600, 450]
eye_right_pos = [650, 470]
mustache_pos = [400, 600]
nose_pos = [450, 480]

parts = {
    "ears": {"image": ears, "pos": ears_pos},
    "eye_left": {"image": eye_left, "pos": eye_left_pos},
    "eye_right": {"image": eye_right, "pos": eye_right_pos},
    "mustache": {"image": mustache, "pos": mustache_pos},
    "nose": {"image": nose, "pos": nose_pos}
}

dragging_part = None
offset_x, offset_y = 0, 0

def create_final_image():
    final_image = body.copy()  # 复制基础图像

    for part in parts.values():
        final_image.blit(part["image"], part["pos"])

    pygame.image.save(final_image, 'bodyfinal.png')
    print("Final image saved as bodyfinal.png")

def handle_dragging(pos):
    global offset_x, offset_y
    if dragging_part:
        part = parts[dragging_part]
        part["pos"][0] = pos[0] - offset_x
        part["pos"][1] = pos[1] - offset_y

def game_loop():
    global dragging_part, offset_x, offset_y, screen, background
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for part_name, part in parts.items():
                    part_rect = part["image"].get_rect(topleft=part["pos"])
                    if part_rect.collidepoint(mouse_pos):
                        dragging_part = part_name
                        offset_x = mouse_pos[0] - part["pos"][0]
                        offset_y = mouse_pos[1] - part["pos"][1]
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                dragging_part = None 

            if event.type == pygame.MOUSEMOTION and dragging_part:
                handle_dragging(pygame.mouse.get_pos())

            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                
                background = pygame.transform.scale(background, (screen_width, screen_height))


        screen_width, screen_height = screen.get_size()

        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))  
        screen.blit(body, (screen_width * 0.52, screen_height * 0.25))

        for part in parts.values():
            screen.blit(part["image"], part["pos"])

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(mouse_cursor, (mouse_x - mouse_cursor.get_width() / 2, mouse_y - mouse_cursor.get_height() / 2))

        pygame.display.update()


        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: 
            create_final_image()


    pygame.quit()


game_loop()
