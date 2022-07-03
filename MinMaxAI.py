import numpy as np


class MinMaxGoBang():
    def __init__(self,player) -> None:
        self.player = player
        self.board = player.board
        self.def_consts()

    def get_line(self,pos_index,direction):
        hop_range=4
        if direction=='col':
            left_end = max(0,pos_index[1]-hop_range)
            right_end = min(self.board.Board_cols,pos_index[1]+hop_range+1)
            this_line = self.board.Board_status[pos_index[0],left_end:right_end]
            return np.array(this_line)
        elif direction=='row':
            left_end = max(0,pos_index[0]-hop_range)
            right_end = min(self.board.Board_cols,pos_index[0]+hop_range+1)
            this_line = self.board.Board_status[left_end:right_end,pos_index[1]]
            return np.array(this_line)
        elif direction=='diag':
            left_end = max(-hop_range,-pos_index[0],-pos_index[1])
            right_end = min(hop_range+1,self.board.Board_rows-pos_index[0],self.board.Board_cols-pos_index[1])
            this_line = [self.board.Board_status[pos_index[0]+ind,pos_index[1]+ind] for ind in range(left_end,right_end,1)]
            return np.array(this_line)
        elif direction=='offdiag':
            left_end = max(-hop_range,-pos_index[0],pos_index[1]-self.board.Board_rows+1)
            right_end = min(hop_range+1,self.board.Board_cols-pos_index[0],pos_index[1]+1)
            this_line = [self.board.Board_status[pos_index[0]+ind,pos_index[1]-ind] for ind in range(left_end,right_end,1)]
            return np.array(this_line)
        else:
            return []

    def get_neighb_lines(self,pos_index):
        lines = []
        lines.append(self.get_line(pos_index,'row'))
        lines.append(self.get_line(pos_index,'col'))
        lines.append(self.get_line(pos_index,'diag'))
        lines.append(self.get_line(pos_index,'offdiag'))
        return lines

    def get_lines(self,pos_index):
        lines = []
        lines.append(np.array(self.board.Board_status[:,pos_index[1]]))
        lines.append(np.array(self.board.Board_status[pos_index[0],:]))
        lines.append(np.array(np.diag(self.board.Board_status,pos_index[1]-pos_index[0])))
        lines.append(np.array(np.diag(np.fliplr(self.board.Board_status),self.board.Board_cols-pos_index[1]-pos_index[0]-1)))
        return lines

    def def_consts(self):
        self.LIVE_FIVE={'type':'live five','type_index':0,'modes':[[1,1,1,1,1],[1,1,1,1,1]],'score':10000}
        self.LIVE_FOUR={'type':'live four','type_index':1,'modes':[[0,1,1,1,1,0]],'score':10000}
        self.SLEEP_FOUR={'type':'sleep four','type_index':2,'modes':[[0,1,1,1,1,-1],[1,0,1,1,1,-1],[1,1,0,1,1,-1]],'score':10000}
        self.LIVE_THREE={'type':'live three','type_index':3,'modes':[[0,1,1,1,0,0]],'score':10000}
        self.SLEEP_THREE={'type':'sleep three','type_index':4,'score':10000}
        self.LIVE_TWO={'type':'live two','type_index':5,'score':10000}
        self.SLEEP_TWO={'type':'sleep two','type_index':6,'score':10000}
        self.LIVE_ONE={'type':'live one','type_index':7,'score':10000}
        self.SLEEP_ONE={'type':'sleep one','type_index':8,'score':10000}
        self.DEAD_LINE={'type':'dead line','type_index':9,'score':10000}
        self.TYPE_HASH = [self.LIVE_FIVE,self.LIVE_FOUR,self.SLEEP_FOUR,self.LIVE_THREE,self.SLEEP_THREE,self.LIVE_TWO,self.SLEEP_TWO,self.LIVE_ONE,self.SLEEP_ONE,self.DEAD_LINE]
        pass

    def has_this_type(self,line,line_type):
        if ('modes' not in line_type):
            return False
        for mode in line_type['modes']:
            if len(line)<len(mode):
                return False
            else:
                print('--------------blocks-------------')
                for ind in range(len(line)-len(mode)+1):
                    block = line[ind:ind+len(mode)]
                    print(block)
                    black_right = (block == mode).all()
                    black_left = (block == mode.reverse()).all()
                    black_check = black_right or black_left
                    neg_mode = [-num for num in mode]
                    white_right = (block == neg_mode).all()
                    white_left = (block == neg_mode.reverse()).all()
                    white_check= white_right or white_left

                    if black_check or white_check:
                        print(line_type['type'])
                        return True
                return False

    def get_line_type(self,line):
        line_types=[]
        for line_type in self.TYPE_HASH:
            if self.has_this_type(line,line_type):
                line_types.append(line_type['type'])
                print(line_types)

    def evaluate(self,pos_index):
        lines = self.get_lines(pos_index)
        # print(lines)
        for line in lines:
            print(line)
            self.get_line_type(line)


    def get_minmax(self):
        print(np.shape(self.board.round_history)[0])
        print(np.shape(self.board.Board_status))
        
        layer0 = self.board.Board_status
        print(np.where(layer0==1))

        valid_length = int(400-np.shape(self.board.round_history)[0])
        # layer1 = np.zeros((valid_length,self.board.Board_rows,self.board.Board_cols))
        # layer2 = np.zeros((valid_length,valid_length-1,self.board.Board_rows,self.board.Board_cols))
        # layer3 = np.zeros((valid_length,valid_length-1,valid_length-2,self.board.Board_rows,self.board.Board_cols))