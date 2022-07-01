#导入所需的模块
import sys

import pygame
from BoardSJB import Board,Player,info_area
from MinMaxAI import MinMaxGoBang

# initialize pygame windows
pygame.init()

# set pygame window title
pygame.display.set_caption('行不行五子')
back_img=pygame.image.load('./figures/black_piece1.jpg')
pygame.display.set_icon(back_img)
clock = pygame.time.Clock()

# set window properties
size = width,height = 1100,800
screen = pygame.display.set_mode(size)
screen_back_color=[255,255,255]
screen.fill(screen_back_color)






Temp_board = Board(screen)
Temp_board.draw_board()

player1 = Player(Temp_board,'Mouse','white')
player2 = Player(Temp_board,'CPU','black')

this_info = info_area(screen,Temp_board)

this_ai = MinMaxGoBang(player1)





# 固定代码段，实现点击"X"号退出界面的功能，几乎所有的pygame都会使用该段代码
while True:
    # 循环获取事件，监听事件状态
    for event in pygame.event.get():
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT:
            #卸载所有模块
            pygame.quit()
            #终止程序，确保退出程序
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if Temp_board.game_statu=='active':
                Temp_board.add_piece(event.pos)
            Temp_board.board_trigger()
            this_pos_index = Temp_board.get_pos_index(event.pos)
            this_ai.evaluate(this_pos_index)

    if Temp_board.game_statu=='active':
        screen.fill(screen_back_color)
        pos = pygame.mouse.get_pos()
        Temp_board.draw_board()
        Temp_board.draw_all_pieces()
        Temp_board.player_thinking(pos)

        player1.show_player_info()
        player2.show_player_info()

        this_info.show_info_boundary()

        

    pygame.display.update()

    clock.tick(60)
    # pygame.display.flip() #更新屏幕内容
