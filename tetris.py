import pygame as pyg
import random as rand
# initialize


color = {1: (0xff,0x87,0x87),
         2: (0xff,0xdd,0x87 ),
         3: (0xff,0xeb,0x87),
         4: (0xbd,0xff,0x87),
         5: (0x85,0xc5,0xfc),
         6: (0xa5,0x87,0xff),
         7: (0x7f,0xef,0xeb),
         8:(0,0,0),#상태배경
         9:(0x32,0x32,0x32),#블록배경
         10:(0x78,0x78,0x78),#그림자
         11:(255,255,255),#글자
         12:(255,255,0),#글자
         13:(0x7c,0x47,0x47),
         14:(255,0,0)
         }


# 테트리스모양
shape = [
    [[1, 1, 1, 1]],  # ㅡH
    [[2, 2], [2, 2]],  # ㅁ
    [[0, 3, 0], [3, 3, 3]],  # ㅗ
    [[4, 0, 0], [4, 4, 4]],  # ㄴ
    [[0, 0, 5], [5, 5, 5]],  # ㄴㄴ
    [[0, 6, 6], [6, 6, 0]],  # 2
    [[7, 7, 0], [0, 7, 7]],  # s
]

# set size,title 가로 18칸 세로 28칸
# pyg.display.set_caption('nrtetris')

# 모양 바꾸기 range(
def change(shape):
    return [
        [shape[y][x] for y in range(len(shape) - 1, -1, -1)]
        for x in range(len(shape[0]))
    ]


# 충돌 체크
def collision(board, block, pos):
    p_x, p_y = pos

    for yi, y in enumerate(block):
        for xi, x in enumerate(y):
            try:
                if x and board[yi + p_y -1][xi + p_x -1]:  # (yi+p_y)>=0#
                    return True
            except IndexError:
                return True
    return False


#
def remove_new(board,board_x):
    cnt = 0
    for yi, y in enumerate(board):
        if 0 not in y:
            del board[yi]
            board.insert(0, [0 for x in range(board_x)])
            cnt += 1

    return cnt
    # 라인을 없애는것과 동시에 처음에한줄추가


def save_block(board, block, pos):
    p_x, p_y = pos
    for yi, y in enumerate(block):
        for xi, x in enumerate(y):
            if x:
                board[yi + p_y - 1][xi + p_x - 1] = x


class Tetris(object):

    def __init__(self):

        pyg.init()
        pyg.key.set_repeat(260, 50)# 키보드 반복 횟수 조절 (지연시간,간격
        pyg.display.set_caption("Nara's Tetris Ver.1.2")
        self.board_x = 18 #보드의 너비
        self.board_y = 28 #보드의 높이
        self.cell = 20 # 블록 한칸의 크기
        self.width = 27 # 창의 너비
        self.height = 30 # 창의 높이
        self.disp = pyg.display.set_mode((self.cell * self.width, self.cell * self.height)) # 창 크기를 설정
        self.clock = pyg.time.Clock() # 시간당 출력
        self.rev_sound=pyg.mixer.Sound('sound/remove.wav') # 한줄 제거시 효과음
        self.down_sound=pyg.mixer.Sound('sound/down.mp3') # 블록의 저장 효과음
        self.down_sound.set_volume(0.2) # 소리 조절
        self.back_b = [[9 for x in range(self.board_x)] for y in range(self.board_y)]#보드의 뒷 배경 설정
        #보드 주변을 둘러 싼 외벽
        #보드 주변을 둘러 싼 외벽
        self.wall2 = [
            [(4 if x == 0 or x == self.board_x + 1 or y == 0 or y == self.board_y + 1 else 0) for x in range(self.board_x + 2)] for y
            in range(self.board_y + 2)]

        #점수, 레벨 등의 뒷 배경
        self.state_wall = [
            [(6 if (0<=x<6 and 0<=y<4) or 4<y<9 or 9<y<13 or 13<y<28 else 0) for x in range(6)] for y in range(28)]




    def game_start(self): #게임을 시작한다.
        if self.game_over :
            self.game_over=False
        if self.pause:
            return
        self.board = [[0 for i in range(self.board_x)] for i in range(self.board_y)] #board를 생성
        self.new_block()
        self.level = 1
        self.score = 0
        pyg.time.set_timer(pyg.USEREVENT + 1, 1200//(self.level*20)+250)
        # pyg.time.set_timer(pyg.USEREVENT+)

    def new_block(self): #새 블록을 생성
        self.next_b = shape[rand.randint(0, 6)]
        # self.next_b = shape[1]
        self.block = self.next_b
        # self.next_b = shape[0] #test
        self.p_x = 8  # 가로 7칸과
        self.p_y = 1
        self.shadow_y = self.shadow()
    # 그려주기
    def draw(self, block, pos, ch=3):
        p_x, p_y = pos
        for yi, y in enumerate(block):
            for xi, x in enumerate(y):
                if x:
                    # try:
                        if ch==0:#일반블록

                            pyg.draw.rect(self.disp, color[x],pyg.Rect((p_x + xi) * self.cell+1,(p_y + yi) * self.cell+1,
                                          self.cell-1, self.cell-1))
                            pyg.draw.rect(self.disp, color[10],[(p_x+xi)*self.cell,(p_y + yi) * self.cell,self.cell,self.cell],1)
                        elif ch==1: #그림자블록
                             pyg.draw.rect(self.disp, color[10],pyg.Rect((p_x + xi) * self.cell,(p_y + yi) * self.cell,
                                          self.cell, self.cell))
                        elif ch==2: #저장된 블록
                             pyg.draw.rect(self.disp, color[x],pyg.Rect((p_x + xi) * self.cell+1,(p_y + yi) * self.cell+1,
                                          self.cell-1, self.cell-1))
                             pyg.draw.rect(self.disp, color[11],[(p_x+xi)*self.cell,(p_y + yi) * self.cell,self.cell,self.cell],1)

                        else :# 배경 보드
                            pyg.draw.rect(self.disp, color[8],pyg.Rect((p_x + xi) * self.cell,(p_y + yi) * self.cell,
                                          self.cell, self.cell))


                    # except :
                    #     pass


    # 좌우하 이동 함수
    def move(self, pos):
        if not self.pause and not self.game_over:
            x, y = pos
            temp_x = self.p_x + x
            temp_y = self.p_y + y
            if temp_x > 0 and not collision(self.board, self.block, (temp_x, temp_y)):
                self.p_x = temp_x
            if not collision(self.board, self.block, (temp_x, temp_y)):
                self.p_y = temp_y
            else:
                if not x:
                    self.check_all()

            self.shadow_y = self.shadow()
        # print(self.shadow_y)
        # 1,1에서 시작한다는 것을 생각하자..

    def down(self): #블록의 바로 하강
        for y in range(self.board_y+1):
            if  collision(self.board, self.block, (self.p_x, y + self.p_y)):
                self.p_y = y + self.p_y - 1
                break
    # 그림자
    def shadow(self):
        for y in range(self.board_y+1):
            if  collision(self.board, self.block, (self.p_x, y + self.p_y)):
                return (y + self.p_y - 1)

    # 모양 변화가 가능한지 체크
    def check_change(self):
        if not self.pause and not self.game_over:
            test_block = change(self.block)
            if not collision(self.board, test_block, (self.p_x, self.p_y)):
                self.block = test_block[:]
                self.shadow_y = self.shadow()

    def pause_msg(self):
        self.font=pyg.font.SysFont('Sans',70)
        self.text=self.font.render(("PUASE"),True,(255,255,255))
        self.disp.blit(self.text,(6*self.cell,self.cell*14))
    def auto_msg(self):
        self.font=pyg.font.SysFont('Sans',70)
        self.text=self.font.render(("AUTO"),True,(255,255,255))
        self.disp.blit(self.text,(6*self.cell,self.cell*14))

    def state(self,score,level):
        self.disp.fill(color[13])
        self.draw(self.state_wall,(20,1))
        self.draw(self.next_b, (21, 2),0)
        self.draw(self.back_b, (1, 1),0)
        self.draw(self.block, (self.p_x, self.shadow_y),1)
        self.draw(self.block, (self.p_x, self.p_y),0)
        self.draw(self.board, (1, 1),2)
        self.font=pyg.font.SysFont('Sans',20)
        self.text=self.font.render(" NEXT",True,color[12])
        self.disp.blit(self.text,(21*self.cell,self.cell*1))
        self.text=self.font.render(" SCORE",True,color[12])
        self.disp.blit(self.text,(21*self.cell,self.cell*6))
        self.text=self.font.render(" LEVEL",True,color[12])
        self.disp.blit(self.text,(21*self.cell,self.cell*11))
        self.text=self.font.render("  KEY",True,color[12])
        self.disp.blit(self.text,(21*self.cell,self.cell*15))
        self.font=pyg.font.SysFont('Sans',35)
        self.text=self.font.render(str(score),True,color[11])
        self.disp.blit(self.text,(23*self.cell-10,self.cell*8))
        self.text=self.font.render(str(level),True,color[11])
        self.disp.blit(self.text,(23*self.cell-10,self.cell*12))
        self.font=pyg.font.SysFont('malgungothic',16)
        self.text=self.font.render('MOVE',True,color[11])
        self.disp.blit(self.text,(22*self.cell-10,self.cell*17))
        self.text=self.font.render('← ↑ → ↓',True,color[11])
        self.disp.blit(self.text,(21*self.cell-5,self.cell*18))
        self.text=self.font.render('PAUSE',True,color[11])
        self.disp.blit(self.text,(22*self.cell-10,self.cell*20))
        self.text=self.font.render('P',True,color[11])
        self.disp.blit(self.text,(23*self.cell-13,self.cell*21))
        self.text=self.font.render('RESTART',True,color[11])
        self.disp.blit(self.text,(22*self.cell-16,self.cell*23))
        self.text=self.font.render('R',True,color[11])
        self.disp.blit(self.text,(23*self.cell-13,self.cell*24))
        self.text=self.font.render('AUTO-PLAY',True,color[11])
        self.disp.blit(self.text,(21*self.cell-10,self.cell*26))
        self.text=self.font.render('A',True,color[11])
        self.disp.blit(self.text,(23*self.cell-13,self.cell*27))
        if self.auto and not self.game_over:
            self.auto_msg()


    def gameover(self,score):
        self.font=pyg.font.SysFont('Sans',80)
        self.text=self.font.render("GAME OVER",True,color[14])
        self.disp.blit(self.text,(1*self.cell+5,self.cell*10))
        self.font=pyg.font.SysFont('Sans',60)
        self.text=self.font.render("YOUR SCORE",True,color[14])
        self.disp.blit(self.text,(3*self.cell,self.cell*13))
        self.font=pyg.font.SysFont('Sans',70)
        self.text=self.font.render(str(score),True,color[14])
        self.disp.blit(self.text,(9*self.cell,self.cell*16))

    # 스페이스 누르면~
    def check_all(self):
        if not self.pause and not self.game_over:
            check=0
            self.down()
            self.down_sound.play()
            save_block(self.board, self.block, (self.p_x, self.p_y))
            check=remove_new(self.board,self.board_x) * 10
            if check:#sound발생을위한 체킹
                self.score += check
                self.rev_sound.play()
            self.level=self.score//100*1+1
            self.new_block()

            if collision(self.board, self.block, (self.p_x, self.p_y)):
                self.game_over=True
                self.gameover(self.score)

    def auto_t(self):
        if not self.pause and not self.game_over:
            temp_x=1
            temp_y=1
            temp_b=[]
            sum=0
            cmp=0

            for r in range(4):
                self.block=change(self.block)[:]
                for x in range(self.board_x):
                    if not collision(self.board, self.block, (x+1,self.p_y)):
                        for y in range(self.board_y+1):
                            if collision(self.board,  self.block, (x+1, y + self.p_y)) :
                                sum+=self.auto_wallside((x+1,y+self.p_y-1))
                                sum-=self.auto_empty((x+1,y+self.p_y-1))
                                sum-=self.auto_long((x+1,y+self.p_y-1))

                                if cmp<=sum:
                                    cmp=sum
                                    temp_y=(y+self.p_y-1)
                                    temp_x=x+1
                                    temp_b=self.block[:]
                                break;
                        sum=0
            print('aaaa')
            #저장 결과
            # self.p_y=temp_y
            # self.p_x=temp_x
            self.block=temp_b[:]

            while True:
               if not self.block==temp_b:
                    self.block=change(self.block)

               elif self.p_x==temp_x:
                    self.state(self.score,self.level)
                    pyg.display.update()
                    break
               elif self.p_x>temp_x:
                    self.move([-1,0])

               elif self.p_x<temp_x:
                    self.move([1,0])

               self.state(self.score,self.level)
               pyg.display.update()
               pyg.time.delay(10)

            pyg.time.delay(100)
            self.p_y=temp_y

            # print("ssss")

    def auto2(self):
        if not self.pause and not self.game_over:
            temp_x=1
            temp_y=1
            temp_b=[]
            sum=0
            cmp=0

            for r in range(4):
                self.block=change(self.block)[:]
                for x in range(self.board_x):
                    if not collision(self.board, self.block, (x+1,self.p_y)):
                        for y in range(self.board_y+1):
                            if collision(self.board,  self.block, (x+1, y + self.p_y)) :
                                sum+=self.auto_wallside((x+1,y+self.p_y-1))
                                sum-=self.auto_empty((x+1,y+self.p_y-1))
                                sum-=self.auto_long((x+1,y+self.p_y-1))
                                if cmp<=sum:
                                    cmp=sum
                                    temp_y=(y+self.p_y-1)
                                    temp_x=x+1
                                    temp_b=self.block[:]
                                break;
                        sum=0

            #저장 결과
            self.p_y=temp_y
            self.p_x=temp_x
            self.block=temp_b[:]






    def auto_move(self):

        pass

    #아래빈공간

    def auto_empty(self,pos):# 빈공간개수
        cnt=0
        p_x,p_y=pos
        for x in range(len(self.block[0])):
            for y in range(4):
                if y+p_y+len(self.block)-1<self.board_y and not self.board[y+p_y+-1+len(self.block)][x+p_x-1]:
                    cnt+=1
        return cnt*60
    def auto_wallside(self,pos):#벽면구하기 side of wall
        cnt=0
        bottom=0
        save=0
        left_right=0
        p_x, p_y = pos
        for yi, y in enumerate(self.block):
                for xi, x in enumerate(y):
                    if x and yi+p_y<=self.board_y:
                        # print(yi+p_y,xi+p_x-1,self.block)
                        if (yi+p_y)==self.board_y :
                            bottom+=1
                        if (xi+p_x)==self.board_x or (xi+p_x-2)==-1 :
                            left_right+=1
                        if yi+p_y<self.board_y and self.board[yi+p_y][xi+p_x-1] :
                                    save+=1
                        if xi+p_x<self.board_x and self.board[yi+p_y-1][xi+p_x]  :
                                    save+=1
                        if xi+p_x>-1 and  self.board[yi+p_y-1][xi+p_x-2] :
                                    save+=1
        cnt+=bottom*10
        cnt+=left_right*2
        cnt+=save*7
        return cnt*80
    def auto_long(self,pos):#
        cnt=0
        p_x,p_y=pos
        for x in range(len(self.block[0])):
            for y in range(self.board_y):
                if y+p_y<self.board_y and self.board[y+p_y][x+p_x-1]:
                    cnt=1
                #위기준 길이 작으면
        return cnt*2.2
                            #아래벽면,오른쪽벽면,왼쪽벽면








    #############################################
    def pause_tog(self):
        self.pause=not self.pause
    def auto_tog(self):
        self.auto=not self.auto
    def main(self):
        pyg.mixer.music.load("sound/music.mp3")
        pyg.mixer.music.play(-1)
        pyg.mixer.music.set_volume(0.01)
        self.quit = False
        self.auto=False
        self.pause = True
        self.game_over=False
        self.clock.tick(30)  # 30fps
        # print(self.b_x)#위치 체크
        self.font=pyg.font.SysFont('Sans',40)
        self.text=self.font.render("press any key",True,(255,255,255))
        self.disp.blit(self.text,(7*self.cell,self.cell*int(self.height/2-1)))

        while self.pause and not self.quit:
            for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        self.quit = True
                    elif event.type == pyg.KEYUP:
                        self.pause= False
            pyg.display.update()

        self.game_start()

        ekey={
            'pyg.K_UP':self.check_change,
            'pyg.K_LEFT':lambda :self.move([-1, 0]),
            'pyg.K_RIGHT':lambda :self.move([1, 0]),
            'pyg.K_DOWN':lambda :self.move([0, 1]),
            'pyg.K_SPACE':self.check_all,
            'pyg.K_p':self.pause_tog,
            'pyg.K_a':self.auto_tog,
            'pyg.K_r':self.game_start
        }

        while not self.quit:
            if not self.pause and not self.game_over:
                self.state(self.score,self.level)
            elif self.pause:
                self.pause_msg()
            # elif self. game_over:
            #     self.gameover(self.score)


            for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        self.quit = True
                    elif event.type == pyg.KEYDOWN:
                        for key in ekey:
                            if event.key == eval(key):
                                ekey[key]()
                    elif event.type == pyg.USEREVENT + 1:
                            self.move([0, 1])
            if self.auto:

                self.auto_t()
                # self.auto2()
                self.check_all()
            pyg.display.update()
        pyg.quit()
#실행
if __name__=='__main__':
    start = Tetris()
    start.main()
