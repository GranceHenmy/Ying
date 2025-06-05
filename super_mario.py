import pygame
import random # Add this import for random number generation
# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 800, 600
FPS = 60

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("超级玛丽")
clock = pygame.time.Clock()

# Enhanced image loading with multiple fallbacks
def load_image(filename, size, default_color):
    try:
        img = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        img = pygame.Surface(size)
        img.fill(default_color)
        return img

# Load game assets with proper scaling
mario_image = load_image('mario.png', (40, 60), (255, 0, 0))
mushroom_img = load_image('mushroom.png', (30, 30), (255, 0, 255))
coin_img = load_image('coin.png', (20, 20), (255, 215, 0))
bomb_img = load_image('bomb.png', (25, 25), (0, 0, 0))

# 创建物品列表和分数
items = []
score = 0
font = pygame.font.SysFont(None, 36)

# 随机生成物品
def create_items():
    for i in range(5):  # 5个蘑菇
        items.append({
            'type': 'mushroom',
            'rect': pygame.Rect(
                random.randint(100, WIDTH-100),
                random.randint(100, HEIGHT-100),
                30, 30),
            'img': mushroom_img
        })
    for i in range(3):  # 3个炸弹
        items.append({
            'type': 'bomb',
            'rect': pygame.Rect(
                random.randint(100, WIDTH-100),
                random.randint(100, HEIGHT-100),
                25, 25),
            'img': bomb_img
        })
    for i in range(10):  # 10个金币
        items.append({
            'type': 'coin',
            'rect': pygame.Rect(
                random.randint(100, WIDTH-100),
                random.randint(100, HEIGHT-100),
                20, 20),
            'img': coin_img
        })

create_items()

mario_rect = mario_image.get_rect()
mario_rect.x = 50
mario_rect.y = HEIGHT - mario_rect.height

# 游戏主循环
running = True
# 添加游戏状态变量
game_started = False
start_button = pygame.Rect(WIDTH//2-100, HEIGHT//2-25, 200, 50)
mario_speed = 3
is_jumping = False
jump_count = 10
ground_level = HEIGHT - 100  # 地面高度

# 创建道路障碍物
class Obstacle:
    def __init__(self, x, width, height, type):
        self.rect = pygame.Rect(x, ground_level-height, width, height)
        self.type = type  # 'mushroom', 'pit' 或 'coin'
        
obstacles = []
for i in range(10):  # 生成10个障碍物
    obs_type = random.choice(['mushroom', 'pit', 'coin'])
    width = random.randint(50, 150)
    height = random.randint(20, 60) if obs_type != 'pit' else 0
    obstacles.append(Obstacle(200 + i*200, width, height, obs_type))

# 修改游戏主循环
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started and start_button.collidepoint(event.pos):
                game_started = True
    
    screen.fill((0, 128, 255))
    
    if not game_started:
        # 绘制开始按钮
        pygame.draw.rect(screen, (255, 0, 0), start_button)
        start_text = font.render("开始游戏", True, (255, 255, 255))
        screen.blit(start_text, (WIDTH//2-50, HEIGHT//2-15))
    else:
        # 马里奥自动移动和跳跃
        mario_rect.x += mario_speed
        
        # 跳跃逻辑
        if not is_jumping:
            # 检测是否需要跳跃（遇到障碍物）
            for obs in obstacles:
                if mario_rect.colliderect(obs.rect) and obs.type != 'pit':
                    is_jumping = True
                    break
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                mario_rect.y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10
                mario_rect.y = ground_level - mario_rect.height
        
        # 绘制地面和障碍物
        pygame.draw.rect(screen, (139, 69, 19), (0, ground_level, WIDTH, HEIGHT-ground_level))
        for obs in obstacles:
            if obs.type == 'mushroom':
                pygame.draw.rect(screen, (255, 0, 255), obs.rect)
            elif obs.type == 'coin':
                pygame.draw.rect(screen, (255, 215, 0), obs.rect)
            elif obs.type == 'pit':
                pygame.draw.rect(screen, (0, 0, 0), (obs.rect.x, ground_level, obs.rect.width, 20))
        
        # 绘制马里奥和分数
        screen.blit(mario_image, mario_rect)
        screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

# 退出 Pygame
pygame.quit()