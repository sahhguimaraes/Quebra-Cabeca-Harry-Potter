import pygame
import random
import os

#    Inicialização do Pygame
pygame.init()

#    Configurações do jogo, como tamanho de tela e cores selecionadas
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 800
TILE_SIZE = 100
FPS = 30
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (196, 46, 47)

def load_images(folder):    
    return [pygame.image.load(os.path.join(folder, f)) for f in os.listdir(folder) if f.endswith(('png', 'jpg', 'jpeg'))]

def create_tiles(images, rows, cols):
    return [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in images[:rows * cols]]

def start_game(nivel): 
    levels = {1: ('HP1', 5, 5), 2: ('HP2', 7, 7), 3: ('HP3', 8, 8)}
    folder, rows, cols = levels[nivel]
    images = load_images(folder)
    tiles = create_tiles(images, rows, cols)
    positions = [(x * TILE_SIZE, y * TILE_SIZE) for y in range(rows) for x in range(cols)]
    random.shuffle(positions)
    return tiles, positions

def select_level(screen):    
    font = pygame.font.Font(None, 50)
    buttons = {
        1: pygame.Rect(SCREEN_WIDTH // 2 - 100, 200, 200, 50),
        2: pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 50),
        3: pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 50)
    }
    # Adicionando o botão de sair
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 50)
    
    while True:
        screen.fill(WHITE)

        # Adiciona o texto "Escolha um nível" acima dos botões
        level_text = font.render("Escolha um nível", True, RED)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 100))
        
        # Desenha os botões de nível
        for level, rect in buttons.items():
            pygame.draw.rect(screen, RED, rect)
            text = font.render(f"Nível {level}", True, WHITE)
            screen.blit(text, (rect.x + (rect.width - text.get_width()) // 2, rect.y + (rect.height - text.get_height()) // 2))
        
        # Desenha o botão de sair
        pygame.draw.rect(screen, RED, exit_button)
        exit_text = font.render("Sair", True, WHITE)
        screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, exit_button.y + (exit_button.height - exit_text.get_height()) // 2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica clique nos botões de nível
                for level, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return level
                # Verifica clique no botão de sair
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    return None

def start_screen(screen):    
    font = pygame.font.Font(None, 50)
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 125, 300, 250, 70)
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 125, 400, 250, 70)
    while True:
        screen.fill(WHITE)
        title_text = font.render("Enigma de Hogwarts", True, RED)
        screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 170))

        pygame.draw.rect(screen, RED, start_button)
        start_text = font.render("Iniciar Jogo", True, WHITE)
        screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + 20))

        pygame.draw.rect(screen, RED, exit_button)
        exit_text = font.render("Sair", True, WHITE)
        screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, exit_button.y + 15))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return True
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    return False

def main():    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Enigma de Hogwarts")
    if not start_screen(screen):
        return

    while True:
        nivel = select_level(screen)
        if nivel is None:
            return

        tiles, positions = start_game(nivel)
        clock = pygame.time.Clock()
        running, selected_tile, offset_x, offset_y = True, None, 0, 0
        complete_button = pygame.Rect(SCREEN_WIDTH - 150, 20, 130, 50)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if complete_button.collidepoint(event.pos):
                        running = False
                    for i, pos in enumerate(positions):
                        if pygame.Rect(pos, (TILE_SIZE, TILE_SIZE)).collidepoint(event.pos):
                            selected_tile, offset_x, offset_y = i, pos[0] - event.pos[0], pos[1] - event.pos[1]
                            break
                elif event.type == pygame.MOUSEBUTTONUP:
                    selected_tile = None
                elif event.type == pygame.MOUSEMOTION and selected_tile is not None:
                    positions[selected_tile] = (event.pos[0] + offset_x, event.pos[1] + offset_y)

            screen.fill(WHITE)
            for tile, pos in zip(tiles, positions):
                screen.blit(tile, pos)

            pygame.draw.rect(screen, RED, complete_button)
            complete_text = pygame.font.Font(None, 36).render("Concluído", True, WHITE)
            screen.blit(complete_text, (
                complete_button.x + (complete_button.width - complete_text.get_width()) // 2,
                complete_button.y + (complete_button.height - complete_text.get_height()) // 2
            ))

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
