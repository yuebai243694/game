import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 600  # 窗口的宽度和高度
TILE_SIZE = 100  # 每个图案块的大小
ROWS, COLS = 6, 6  # 游戏板的行数和列数
FPS = 30  # 游戏帧率（每秒钟帧数）
WHITE = (255, 255, 255)  # 白色
BLACK = (0, 0, 0)  # 黑色
RED = (255, 0, 0)  # 红色
BG_COLOR = (200, 200, 200)  # 背景颜色
DEFAULT_COUNTDOWN_TIME = 30  # 默认倒计时秒数
HARD_MODE_COUNTDOWN_TIME = DEFAULT_COUNTDOWN_TIME - 10  # 困难模式倒计时（比普通模式少10秒）

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 设置窗口大小
pygame.display.set_caption("羊了个羊小游戏")  # 设置窗口标题

# 加载背景图
background_img = pygame.image.load("background.png")  # 加载背景图
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # 调整背景图的大小以适应窗口

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]  # 加载六种图案图片
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]  # 调整每张图片的大小

# 加载结束界面背景图片
game_over_bg = pygame.image.load("game_over_bg.png")  # 加载结束界面的背景图片
game_over_bg = pygame.transform.scale(game_over_bg, (WIDTH, HEIGHT))  # 调整背景图片的大小以适应窗口

# 加载胜利界面背景图片
victory_bg = pygame.image.load("victory_bg.png")  # 加载胜利界面的背景图片
victory_bg = pygame.transform.scale(victory_bg, (WIDTH, HEIGHT))  # 调整背景图片的大小以适应窗口

# 加载楷体常规字体
try:
    font_path = "C://Windows//Fonts//simkai.ttf"  # 确保你有楷体常规字体文件，文件路径需要根据实际情况设置
    font = pygame.font.Font(font_path, 30)  # 加载楷体常规字体，设置字体大小为30
    menu_font = pygame.font.Font(font_path, 40)  # 菜单字体大小为40
except FileNotFoundError:
    font = pygame.font.SysFont("kai", 30)  # 如果找不到自定义字体文件，使用系统字体作为替代
    menu_font = pygame.font.SysFont("kai", 40)

def create_board():
    """
    创建并返回一个新的游戏板，确保每种图案的数量是2的倍数
    """
    num_tiles = ROWS * COLS  # 总共的格子数
    num_patterns = len(patterns)  # 图案种类数量

    # 每种图案的数量（2的倍数），确保总数等于游戏板上的总格子数
    tiles_per_pattern = (num_tiles // num_patterns)  # 每种图案的数量
    if tiles_per_pattern % 2 != 0:  # 确保是2的倍数
        tiles_per_pattern -= 1

    # 创建一个列表，包含每种图案相应数量的副本
    tiles = []
    for pattern in patterns:
        tiles.extend([pattern] * tiles_per_pattern)

    random.shuffle(tiles)  # 随机打乱图案的顺序

    # 将打乱的图案分配到游戏板
    board = [tiles[i * COLS:(i + 1) * COLS] for i in range(ROWS)]
    return board

def fill_board_with_random_patterns():
    """
    随机填充整个窗口区域的图案
    """
    num_tiles = (WIDTH // TILE_SIZE) * (HEIGHT // TILE_SIZE)  # 计算整个窗口区域的总格子数
    tiles = [random.choice(patterns) for _ in range(num_tiles)]  # 随机选择图案

    board = []
    for i in range(HEIGHT // TILE_SIZE):
        row = []
        for j in range(WIDTH // TILE_SIZE):
            row.append(tiles.pop())  # 从剩余图案中选择并添加到当前行
        board.append(row)
    return board

def draw_board():
    """
    绘制游戏板上的所有图案
    """
    start_x = WIDTH - COLS * TILE_SIZE  # 游戏板左上角的 X 坐标
    start_y = HEIGHT - ROWS * TILE_SIZE  # 游戏板左上角的 Y 坐标

    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]  # 获取当前格子的图案
            if tile is not None:
                # 将图案绘制到屏幕上的正确位置
                screen.blit(tile, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE))

def check_match():
    """
    检查用户选择的两个图案是否匹配，并处理匹配的结果
    """
    global score
    if len(selected) == 2:
        r1, c1 = selected[0]  # 第一个选择的图案坐标
        r2, c2 = selected[1]  # 第二个选择的图案坐标
        if board[r1][c1] == board[r2][c2]:
            # 如果两个选择的图案匹配，移除它们
            board[r1][c1] = None
            board[r2][c2] = None
            score += 10  # 每消除一组图案加10分
        # 清空选中列表
        selected.clear()

def draw_game_over_screen():
    """
    绘制游戏结束界面
    """
    screen.blit(game_over_bg, (0, 0))  # 绘制游戏结束背景图
    text = font.render("游戏结束", True, RED)  # 绘制“游戏结束”文本
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    score_text = font.render(f"你的得分: {score}", True, RED)  # 绘制分数文本
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    screen.blit(score_text, score_rect)

    restart_text = font.render("按 R 重新开始", True, RED)  # 绘制“按 R 重新开始”文本
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(restart_text, restart_rect)

    quit_text = font.render("按 Q 退出游戏", True, RED)  # 绘制“按 Q 退出游戏”文本
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
    screen.blit(quit_text, quit_rect)


def draw_victory_screen():
    """
    绘制胜利界面
    """
    screen.blit(victory_bg, (0, 0))  # 绘制胜利背景图
    text = font.render("胜利！", True, RED)  # 绘制“胜利”文本
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    score_text = font.render(f"你的得分: {score}", True, RED)  # 绘制分数文本
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    screen.blit(score_text, score_rect)

    restart_text = font.render("按 R 重新开始", True, RED)  # 绘制“按 R 重新开始”文本
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(restart_text, restart_rect)

    quit_text = font.render("按 Q 退出游戏", True, RED)  # 绘制“按 Q 退出游戏”文本
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
    screen.blit(quit_text, quit_rect)


def draw_countdown_and_score(timer):
    """
    绘制倒计时和分数
    """
    text = font.render(f"剩余时间: {timer:.1f}秒", True, RED)  # 绘制倒计时文本
    text_rect = text.get_rect(topleft=(10, 10))
    screen.blit(text, text_rect)
    
    score_text = font.render(f"分数: {score}", True, RED)  # 绘制分数文本
    score_rect = score_text.get_rect(topleft=(10, 50))  # 分数显示在倒计时下方
    screen.blit(score_text, score_rect)

def draw_menu_screen():
    """
    绘制主菜单界面
    """
    screen.blit(background_img, (0, 0))  # 绘制背景图

    title_text = menu_font.render("喵~喵~喵~", True, RED)  # 绘制标题文本
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)

    start_game_text = menu_font.render("游戏开始", True, BLACK)  # 绘制“游戏开始”文本
    start_game_rect = start_game_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_game_text, start_game_rect)

    difficulty_text = menu_font.render("难度选项", True, BLACK)  # 绘制“难度选项”文本
    difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(difficulty_text, difficulty_rect)

def draw_difficulty_screen():
    """
    绘制难度选择界面
    """
    screen.blit(background_img, (0, 0))  # 绘制背景图

    easy_text = menu_font.render("简单", True, BLACK)  # 绘制“简单”选项
    easy_rect = easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(easy_text, easy_rect)

    normal_text = menu_font.render("普通", True, BLACK)  # 绘制“普通”选项
    normal_rect = normal_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(normal_text, normal_rect)

    hard_text = menu_font.render("困难", True, BLACK)  # 绘制“困难”选项
    hard_rect = hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(hard_text, hard_rect)

def handle_menu_input(event):
    """
    处理主菜单的输入事件
    """
    global current_screen
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        # 根据点击位置确定选择的菜单项
        if WIDTH // 2 - 100 < x < WIDTH // 2 + 100:
            if HEIGHT // 2 - 50 < y < HEIGHT // 2 + 50:
                current_screen = "difficulty"  # 进入难度选择界面
            elif HEIGHT // 2 + 50 < y < HEIGHT // 2 + 150:
                current_screen = "difficulty"  # 进入难度选择界面

def handle_difficulty_input(event):
    """
    处理难度选择界面的输入事件
    """
    global current_screen, COUNTDOWN_TIME, board
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        # 根据点击位置确定选择的难度
        if WIDTH // 2 - 100 < x < WIDTH // 2 + 100:
            if HEIGHT // 2 - 150 < y < HEIGHT // 2 - 50:
                COUNTDOWN_TIME = DEFAULT_COUNTDOWN_TIME + 10  # 简单模式增加10秒
                board = create_board()  # 重新生成游戏板
                current_screen = "game"  # 切换到游戏界面
            elif HEIGHT // 2 - 50 < y < HEIGHT // 2 + 50:
                COUNTDOWN_TIME = DEFAULT_COUNTDOWN_TIME  # 普通模式倒计时不变
                board = create_board()  # 重新生成游戏板
                current_screen = "game"  # 切换到游戏界面
            elif HEIGHT // 2 + 50 < y < HEIGHT // 2 + 150:
                COUNTDOWN_TIME = HARD_MODE_COUNTDOWN_TIME  # 困难模式倒计时少40秒
                board = fill_board_with_random_patterns()  # 随机填充游戏板
                current_screen = "game"  # 切换到游戏界面

# 初始化游戏参数
score = 0  # 初始分数设置为0
board = create_board()  # 创建游戏板
selected = []  # 选中的图案坐标列表
COUNTDOWN_TIME = DEFAULT_COUNTDOWN_TIME  # 初始倒计时设置
start_time = time.time()  # 记录游戏开始的时间
current_screen = "menu"  # 初始屏幕为菜单

# 主游戏循环
running = True  # 游戏运行标志，初始设置为 True
clock = pygame.time.Clock()  # 创建一个时钟对象以控制游戏的帧率
game_over = False  # 游戏结束标志
victory = False  # 胜利标志

while running:  # 游戏主循环
    clock.tick(FPS)  # 控制游戏的帧率（每秒钟允许的最大帧数）
    current_time = time.time()  # 获取当前时间
    elapsed_time = current_time - start_time  # 计算已经过去的时间
    remaining_time = COUNTDOWN_TIME - elapsed_time  # 计算剩余的时间

    if remaining_time <= 0:  # 如果倒计时结束
        remaining_time = 0  # 确保剩余时间为0
        if not victory:  # 如果没有胜利
            game_over = True  # 设置游戏结束标志

    for event in pygame.event.get():  # 处理所有事件
        if event.type == pygame.QUIT:  # 如果用户点击关闭窗口
            running = False  # 结束游戏循环
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 如果用户点击鼠标
            if current_screen == "menu":
                handle_menu_input(event)  # 处理主菜单的输入
            elif current_screen == "difficulty":
                handle_difficulty_input(event)  # 处理难度选择界面的输入
            else:
                x, y = event.pos  # 获取鼠标点击的坐标
                col, row = (x - (WIDTH - COLS * TILE_SIZE)) // TILE_SIZE, (y - (HEIGHT - ROWS * TILE_SIZE)) // TILE_SIZE  # 计算点击的格子所在的列和行
                if not game_over and not victory and 0 <= row < ROWS and 0 <= col < COLS and board[row][col] is not None:  # 如果游戏没有结束且没有胜利且点击的格子有图案
                    selected.append((row, col))  # 将点击的图案坐标添加到选中列表
                    if len(selected) == 2:  # 如果用户选择了两个图案
                        check_match()  # 检查这两个图案是否匹配
                        if all(tile is None for row in board for tile in row):  # 如果所有图案都被移除
                            victory = True  # 设置胜利标志
        elif event.type == pygame.KEYDOWN:  # 如果用户按下键盘
            if event.key == pygame.K_r:  # 如果按下 R 键
                # 重置游戏
                board = create_board()  # 重新生成游戏板
                selected.clear()  # 清空选择的图案
                game_over = False  # 重置游戏结束标志
                victory = False  # 重置胜利标志
                score = 0  # 重置分数
                start_time = time.time()  # 重置游戏开始时间
                current_screen = "game"  # 切换到游戏屏幕
            elif event.key == pygame.K_q:  # 如果按下 Q 键
                running = False  # 结束游戏循环

    if current_screen == "menu":  # 如果在主菜单界面
        draw_menu_screen()  # 绘制主菜单界面
    elif current_screen == "difficulty":  # 如果在难度选择界面
        draw_difficulty_screen()  # 绘制难度选择界面
    elif not (game_over or victory):  # 如果游戏尚未结束且未胜利
        screen.blit(background_img, (0, 0))  # 绘制背景图
        draw_board()  # 绘制游戏板
        draw_countdown_and_score(remaining_time)  # 绘制倒计时和分数
    elif victory:  # 如果游戏胜利
        draw_victory_screen()  # 绘制胜利界面
    else:  # 如果游戏结束但未胜利
        draw_game_over_screen()  # 绘制游戏结束界面

    pygame.display.flip()  # 更新屏幕显示

pygame.quit()  # 退出 Pygame
