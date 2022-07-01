import numpy as np


class MinMaxGoBang():
    def __init__(self,player) -> None:
        self.player = player
        self.board = player.board
        self.def_consts()

    def get_line(self,pos_index,direction):
        if direction=='col':
            left_end = max(0,pos_index[1]-4)
            right_end = min(self.board.Board_cols,pos_index[1]+5)
            this_line = self.board.Board_status[pos_index[0],left_end:right_end]
            return np.array(this_line)
        elif direction=='row':
            left_end = max(0,pos_index[0]-4)
            right_end = min(self.board.Board_cols,pos_index[0]+5)
            this_line = self.board.Board_status[left_end:right_end,pos_index[1]]
            return np.array(this_line)
        elif direction=='diag':
            left_end = max(-4,-pos_index[0],-pos_index[1])
            right_end = min(5,self.board.Board_rows-pos_index[0],self.board.Board_cols-pos_index[1])
            this_line = [self.board.Board_status[pos_index[0]+ind,pos_index[1]+ind] for ind in range(left_end,right_end,1)]
            return np.array(this_line)
        elif direction=='offdiag':
            left_end = max(-4,-pos_index[0],pos_index[1]-self.board.Board_rows+1)
            right_end = min(5,self.board.Board_cols-pos_index[0],pos_index[1]+1)
            this_line = [self.board.Board_status[pos_index[0]+ind,pos_index[1]-ind] for ind in range(left_end,right_end,1)]
            return np.array(this_line)
        else:
            return []

    def get_lines(self,pos_index):
        lines = []
        lines.append(self.get_line(pos_index,'row'))
        lines.append(self.get_line(pos_index,'col'))
        lines.append(self.get_line(pos_index,'diag'))
        lines.append(self.get_line(pos_index,'offdiag'))
        return lines


    def def_consts(self):
        self.LIVE_FIVE={'type':0,'modes':[[0,1,1,1,1,1],[-1,1,1,1,1,1]],'score':10000}
        self.LIVE_FOUR={'type':1,'modes':[[0,1,1,1,1,0]],'score':10000}
        self.SLEEP_FOUR={'type':2,'modes':[[0,1,1,1,1,-1],[1,0,1,1,1,-1],[1,1,0,1,1,-1]],'score':10000}
        self.LIVE_THREE={'type':3,'modes':[0,1,1,1,0,0],'score':10000}
        self.SLEEP_THREE={'type':4,'score':10000}
        self.LIVE_TWO={'type':5,'score':10000}
        self.SLEEP_TWO={'type':6,'score':10000}
        self.LIVE_ONE={'type':7,'score':10000}
        self.SLEEP_ONE={'type':8,'score':10000}
        self.DEAD_LINE={'type':9,'score':10000}
        self.TYPE_HASH = [self.LIVE_FIVE,self.LIVE_FOUR,self.SLEEP_FOUR,self.LIVE_THREE,self.SLEEP_THREE,self.LIVE_TWO,self.SLEEP_TWO,self.LIVE_ONE,self.SLEEP_ONE,self.DEAD_LINE]
        pass

    def has_this_type(self,line,line_type):
        for mode in line_type['modes']:
            if len(line)<len(mode):
                return False
            else:
                for ind in range(len(line)-7+1):
                    block = line[ind:ind+len(mode)]
                    if block == mode:
                        return True
                    else:
                        pass
                return False

    def get_line_type(self,line):
        if len(line)<5:
            return self.DEAD_LINE
        else:
            for ind in range(len(line)+1):
                fives = line[ind,ind+5]
                if (sum(fives)==5) or (sum(fives)==-5):
                    return self.LIVE_FIVE
        pass

    def evaluate(self,pos_index):
        lines = self.get_lines(pos_index)
        print(lines)
        for line in lines:
            print(self.get_line_type(line))
            pass
        pass


    def get_minmax(self):
        print(np.shape(self.board.round_history)[0])
        print(np.shape(self.board.Board_status))
        
        layer0 = self.board.Board_status
        print(np.where(layer0==1))

        valid_length = int(400-np.shape(self.board.round_history)[0])
        # layer1 = np.zeros((valid_length,self.board.Board_rows,self.board.Board_cols))
        # layer2 = np.zeros((valid_length,valid_length-1,self.board.Board_rows,self.board.Board_cols))
        # layer3 = np.zeros((valid_length,valid_length-1,valid_length-2,self.board.Board_rows,self.board.Board_cols))