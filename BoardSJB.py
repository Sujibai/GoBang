import math
import numpy as np
import pygame

class Board(object):
    Board_back_color = [255,255,255]
    Board_margins=[30,30,100,30]
    Board_position = [Board_margins[0],Board_margins[1]]
    Board_rows = 20
    Board_cols = 20
    round_history=[]
    Board_status=np.zeros([Board_rows,Board_cols])
    Current_palyer='white'
    game_statu = 'active'
    
    
    Board_line_color = [0,0,0]
    
    def __init__(self,screen):
        window_width=pygame.display.get_surface().get_width()
        window_height=pygame.display.get_surface().get_height()
        Max_size = min(window_width-self.Board_margins[0]-self.Board_margins[2],window_height-self.Board_margins[1]-self.Board_margins[3])
        self.Board_size=[Max_size,Max_size]
        self.Board_blocksize = Max_size/(self.Board_rows-1)

        self.screen = screen

        self.White_piece = pygame.image.load('./figures/white_piece1.jpg')
        self.Black_piece = pygame.image.load('./figures/black_piece1.jpg')
        self.White_hover_piece = pygame.transform.rotozoom(self.White_piece,0,1.03)
        self.Black_hover_piece = pygame.transform.rotozoom(self.Black_piece,0,1.03)
        self.game_statu = 'active'

    def draw_board(self):
        for row in range(self.Board_rows):
            start_point = [self.Board_position[0], self.Board_position[1]+row*self.Board_blocksize]
            end_point = [self.Board_position[0]+self.Board_size[1], self.Board_position[1]+row*self.Board_blocksize]
            pygame.draw.line(self.screen,self.Board_line_color,start_point,end_point,2)
        for col in range(self.Board_rows):
            start_point = [self.Board_position[0]+col*self.Board_blocksize, self.Board_position[1]]
            end_point = [self.Board_position[0]+col*self.Board_blocksize, self.Board_position[1]+self.Board_size[1]]
            pygame.draw.line(self.screen,self.Board_line_color,start_point,end_point,2)

    #### add piece by board position index
    def add_piece_with_index(self,piece_cat,pos_index):
        this_step = {'piece_cat':piece_cat,'x':pos_index[0],'y':pos_index[1]}
        self.round_history.append(this_step)
        if piece_cat=='white':
            self.Board_status[pos_index[0],pos_index[1]]=-1
        elif piece_cat=='black':
            self.Board_status[pos_index[0],pos_index[1]]=1

    def add_piece(self,pos):
        valid = self.is_valid(pos)
        if valid:
            piece_cat = self.Current_palyer
            pos_index = self.get_pos_index(pos)
            self.add_piece_with_index(piece_cat,pos_index)
            self.piece_cat_flip()
        else:
            return

    def piece_cat_flip(self):
        if self.Current_palyer=='white':
            self.Current_palyer='black'
        elif self.Current_palyer=='black':
            self.Current_palyer='white'

    def draw_piece(self,piece_cat,pos_index):
        piece_position = [self.Board_blocksize*pos_index[0]+self.Board_position[0]-20,self.Board_blocksize*pos_index[1]+self.Board_position[1]-20]
        if piece_cat=='white':
            self.screen.blit(self.White_piece,piece_position)
        elif piece_cat=='black':
            self.screen.blit(self.Black_piece,piece_position)

    def draw_hover_piece(self,piece_cat,pos_index):
        piece_position = [self.Board_blocksize*pos_index[0]+self.Board_position[0]-20,self.Board_blocksize*pos_index[1]+self.Board_position[1]-20]
        if piece_cat=='white':
            self.screen.blit(self.White_hover_piece,piece_position)
        elif piece_cat=='black':
            self.screen.blit(self.Black_hover_piece,piece_position)

    def draw_all_pieces(self):
        for step in self.round_history:
            self.draw_piece(step['piece_cat'],[step['x'],step['y']])

    def is_on_cross(self,pos):
        x_index = (pos[0]-self.Board_position[0]+self.Board_blocksize/2)//self.Board_blocksize
        y_index = (pos[1]-self.Board_position[1]+self.Board_blocksize/2)//self.Board_blocksize
        cross_x = self.Board_blocksize*x_index+self.Board_position[0]
        cross_y = self.Board_blocksize*y_index+self.Board_position[1]

        dis_x = pos[0]-cross_x
        dis_y = pos[1]-cross_y
        dis = math.sqrt(dis_x**2+dis_y**2)

        if (dis<=25) and (0<=x_index<self.Board_rows) and (0<=y_index<self.Board_cols):
            return True
        else:
            return False

    def is_empty(self,pos_index):
        if not self.round_history:
            return True
        for step in self.round_history:
            step_pos_index = [step['x'],step['y']]
            if pos_index == step_pos_index:
                return False
        return True

    def is_valid(self,pos):
        on_cross = self.is_on_cross(pos)
        if on_cross:
            pos_index = self.get_pos_index(pos)
            empty = self.is_empty(pos_index)
            if empty:
                return True
        return False

    def get_pos_index(self,pos):
        x_index = (pos[0]-self.Board_position[0]+self.Board_blocksize/2)//self.Board_blocksize
        y_index = (pos[1]-self.Board_position[1]+self.Board_blocksize/2)//self.Board_blocksize
        return [int(x_index),int(y_index)]

    def player_thinking(self,pos):
        valid = self.is_valid(pos)
        if valid:
            pos_index = self.get_pos_index(pos)
            self.draw_hover_piece(self.Current_palyer,pos_index)
        else:
            return False

    def Check_line(self,line):
        flag = 0
        type=line[0]
        for ind in range(len(line)):
            if line[ind]==type:
                flag = flag + line[ind]
                if flag==5:
                    return 'black'
                elif flag==-5:
                    return 'white'
            else:
                flag=line[ind]
                type=line[ind]
        return False

    def Check_result(self):
        #### check all rows
        for row in range(self.Board_rows):
            this_line = self.Board_status[:,row]
            check_result = self.Check_line(this_line)
            if check_result:
                return check_result
        
        #### check all cols
        for col in range(self.Board_rows):
            this_line = self.Board_status[col,:]
            check_result = self.Check_line(this_line)
            if check_result:
                return check_result

        #### check all on-diag line
        for row in range(-self.Board_rows+1,self.Board_rows,1):
            this_line = np.diag(self.Board_status,row)
            check_result = self.Check_line(this_line)
            if check_result:
                return check_result
            
        #### check all anti-diag line
        for row in range(-self.Board_rows+1,self.Board_rows,1):
            this_line = np.diag(np.fliplr(self.Board_status),row)
            check_result = self.Check_line(this_line)
            if check_result:
                return check_result

    def board_trigger(self):
        check_result = self.Check_result()
        if check_result:
            self.game_statu=check_result
            if self.game_statu=='white':
                pygame.display.set_caption('白子，赢！')
            if self.game_statu=='black':
                pygame.display.set_caption('黑子，赢！')


class info_area():
    def __init__(self,screen,board):
        self.screen = screen
        self.board = board
        # window_width=pygame.display.get_surface().get_width()
        # window_height=pygame.display.get_surface().get_height()
        temp_x = board.Board_margins[0]*2 + board.Board_size[1] +20
        temp_y = board.Board_margins[1]
        self.position = [temp_x,temp_y]
        self.width = 200
        self.height = board.Board_size[1]+2
        

    def show_info_boundary(self):
        info_rect = (self.position[0],self.position[1],self.width,self.height)
        pygame.draw.rect(self.screen,[0,0,0],info_rect,2)
        self.show_piece_cat()

    def show_piece_cat(self):
        my_font = pygame.font.SysFont("microsoft Yahei", 25)
        tmp_text = my_font.render('当前棋子：', True,(0,0,0),(255,255,255))
        self.screen.blit(tmp_text,(self.position[0]+10,self.position[1]+12))
        if self.board.Current_palyer=='black':
            self.screen.blit(self.board.Black_piece,(self.position[0]+130,self.position[1]+10))
        elif self.board.Current_palyer=='white':
            self.screen.blit(self.board.White_piece,(self.position[0]+130,self.position[1]+10))