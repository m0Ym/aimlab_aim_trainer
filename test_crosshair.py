"""
测试准星切换功能
"""
import pygame
from crosshair import Crosshair, CrosshairStyle

# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("准星切换测试 - 按 C 键切换，按 ESC 退出")
clock = pygame.time.Clock()

# 创建准星
crosshair = Crosshair()

print("=" * 50)
print("准星切换测试")
print("=" * 50)
print(f"初始准星：{crosshair.get_style_name()}")
print("按 C 键切换准星")
print("按 ESC 退出")
print("=" * 50)

running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                crosshair.next_style()
                print(f"切换到准星：{crosshair.get_style_name()}")
            
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # 更新准星位置
    mouse_x, mouse_y = pygame.mouse.get_pos()
    crosshair.update(mouse_x, mouse_y)
    
    # 绘制
    screen.fill((50, 50, 50))
    crosshair.draw(screen)
    
    # 显示当前准星名称
    font = pygame.font.Font(None, 36)
    text = font.render(f"Crosshair: {crosshair.get_style_name()}", True, (255, 255, 255))
    screen.blit(text, (20, 20))
    
    pygame.display.flip()

pygame.quit()
print("\n测试结束！")
