from pprint import pprint
import sys
from collections import Counter
from random import shuffle
import itertools
import time

class Reversi:
    def __init__(self, player: int, mode: int):
        self.field = [[" " for _ in range(10)] for __ in range(10)] # 盤目
        # その場所にコマを置いた時に、どの方向に相手のコマを取れるかのベクトルを格納
        self.direction = [[" " for _ in range(10)] for __ in range(10)]
        # 座標が分かりやすいように左右に数字を出す
        for i in range(1, 9):
            self.field[0][i] = i
            self.field[9][i] = i
        # 座標が分かりやすいように上下にアルファベットを出す
        for i in range(97, 105):
            self.field[i-96][0] = chr(i)
            self.field[i-96][9] = chr(i)
        # 初期駒の設定
        self.field[4][4] = "◯"
        self.field[5][5] = "◯"
        self.field[4][5] = "●"
        self.field[5][4] = "●"

        # コマの数
        self.num = 4

        # 先手か後手かによって駒の色を変える
        self.player = player
        if self.player == 0:
            self.player_color = "◯"
            self.rival_color =  "●"
        elif self.player == 1:
            self.player_color = "●"
            self.rival_color = "◯"
        else:
            print("invalid player")
            sys.exit(1)
        
        # modeが0なら対人モード、1なら対CPUモード
        self.mode = mode

        # print(f"your player_color is {self.player_color}")
        # self.show()
    
    # 駒を置く
    def put(self):
        print(f"\nyour player_color is {self.player_color}\n")
        self.Count()
        self.search()
        # 置くところがない時の処理
        if self.count == 0:
            print("There is no place to put")
        else:
            while True:
                try:
                    x = input("\nx(a~h): ")
                    y = input("y(1~8): ")
                    x = ord(x) - 96
                    y = int(y)
                except ValueError:
                    print("invalid number")
                    continue
                if 1 <= x <= 8 and 1 <= y <= 8:
                    if self.field[x][y] == "*":
                        break
                print("you cannot put on here.")

            self.reverse(x, y)
        # self.show_direction()
        # print(self.direction[x][y])
        self.Count()
        self.clear()
        # self.show()
        self.switch()
    
    # とりあえず打てるところからランダムに置くcpuを作る
    def cpu(self):
        self.search()
        # self.show()
        # print(self.count)
        if self.count == 0:
            print("no ")
            pass
        else:
            print(self.coordinate)
            shuffle(self.coordinate)
            print(self.coordinate)
            x = self.coordinate[0][0]
            y = self.coordinate[0][1]
            print(x, y)
            self.reverse(x, y)
        self.clear()
        self.switch()
    
    # 現在の盤目の表示
    def show(self):
        for i in range(10):
            for j in range(10):
                print(self.field[j][i], end=" ")
            print()

    # 現在ある場所にコマを置いた時に相手のコマを取れるベクトルの表示
    def show_direction(self):
        for i in range(10):
            for j in range(10):
                print(self.direction[j][i], end="|")
            print()

    # 駒を置けるか捜索
    def search(self):
        # おける数をカウントする
        self.count = 0
        # おける場所のインデックスを保持
        self.coordinate = []

        dx = [1, 1, 0, -1, -1, -1, 0, 1]
        dy = [0, 1, 1, 1, 0, -1, -1, -1]
        for x in range(1, 9):
            for y in range(1, 9):
                # print(x, y)
                if self.field[x][y] != " ":
                    continue
                temp = []
                for nx in dx:
                    for ny in dy:
                        # もしコマをおける場合、コマを取る方向を格納
                        current_x = x
                        current_y = y
                        connect = False
                        while True:
                            current_x += nx
                            current_y += ny
                            # print(f"x: {current_x}, y: {current_y}")
                            if 1 <= current_x <= 8 and 1 <= current_y <= 8:
                                if self.field[current_x][current_y] == self.rival_color:
                                    # 相手のコマを通って、突き当たりで自分のコマがくれば、[x,y]にコマをおける
                                    connect = True
                                    # if not connect:
                                    #     connect = True
                                elif self.field[current_x][current_y] == self.player_color:
                                    # print("player")
                                    # 相手のコマを通っていて、かつ突き当たりに自分のコマがあれば、[x,y]に駒を置ける
                                    if connect:
                                        # print("ok")
                                        self.field[x][y] = "*"
                                        temp.append([nx, ny])
                                        # 置ける場所に追加
                                        self.coordinate.append([x, y])
                                        self.count += 1
                                        break
                                    # 相手のコマを通っていなければ取れない
                                    else:
                                        break
                                else:
                                    break
                            else:
                                break
                    # print(temp)
                self.direction[x][y] = temp
        self.show()
    
    # 盤上の*を一旦取り払う
    def clear(self):
        for x in range(1, 9):
            for y in range(1, 9):
                if self.field[x][y] == "*":
                    self.field[x][y] = " "
    
    # 相手のコマを裏返す
    def reverse(self, x, y):
        self.field[x][y] = self.player_color
        # 探索するベクトル
        for direction in self.direction[x][y]:
            dx = direction[0]
            dy = direction[1]
            current_x = x + dx
            current_y = y + dy
            while self.field[current_x][current_y] == self.rival_color:
                self.field[current_x][current_y] = self.player_color
                current_x += dx
                current_y += dy

    # 相手のターンと自分のターンを切り替える
    def switch(self):
        if self.player == 1:
            self.player_color = "◯"
            self.rival_color =  "●"
            self.player = 0
        elif self.player == 0:
            self.player_color = "●"
            self.rival_color = "◯"
            self.player = 1
        # elif self.palyer == 2:

    # 自分のコマと相手のコマの数を数える
    def Count(self):
        field_1d = list(itertools.chain.from_iterable(self.field))
        color_num = Counter(field_1d)
        self.player_color_num = int(color_num[self.player_color])
        self.rival_color_num = int(color_num[self.rival_color])
        self.num = self.player_color_num + self.rival_color_num
        print(f"rival  {self.rival_color}: {self.rival_color_num}\nplayer {self.player_color}: {self.player_color_num}")
    
    # 実行する関数
    def main(self):
        if self.mode == 0:
            print("PvP!")
            while self.num < 64:
                self.put()
        elif self.mode == 1:
            print("cpu!")
            if self.player == 0:
                while self.num < 64:
                    self.put()
                    self.cpu()
                    # time.sleep(0.5)
            else:
                while self.num < 64:
                    self.cpu()
                    self.put()
        else:
            print("invalid mode !")
            sys.exit(1)


if __name__ == "__main__":
    reversi = Reversi(player=0, mode=1)
    # while True:
    reversi.main()