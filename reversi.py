from pprint import pprint
import sys
from collections import Counter
from random import shuffle

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

        # 先手か後手かによって駒の色を変える
        self.player = player
        if self.player == 0:
            self.piece = "◯"
            self.rival =  "●"
        elif self.player == 1:
            self.piece = "●"
            self.rival = "◯"
        else:
            print("invalid player")
            sys.exit(1)
        
        # modeが0なら対人モード、1なら対CPUモード
        self.mode = mode

        # print(f"your piece is {self.piece}")
        # self.show()
    
    # 駒を置く
    def put(self):
        print(f"\nyour piece is {self.piece}\n")
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
        self.clear()
        # self.show()
        self.switch()
    
    # とりあえず打てるところからランダムに置くcpuを作る
    def cpu(self):
        self.search()
        # self.show()
        if self.count == 0:
            pass
        else:
            print(self.coordinate)
            shuffle(self.coordinate)
            print(self.coordinate)
            x = self.coordinate[0][0]
            y = self.coordinate[0][1]
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
        for x in range(1, 9):
            for y in range(1, 9):
                # print(x, y)
                if self.field[x][y] != " ":
                    continue
                coordinate = [[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]]
                temp = []
                for dx, dy in coordinate:
                    # もしコマをおける場合、コマを取る方向を格納
                    current_x = x
                    current_y = y
                    connect = False
                    while True:
                        current_x += dx
                        current_y += dy
                        # print(f"x: {current_x}, y: {current_y}")
                        if 1 <= current_x <= 8 and 1 <= current_y <= 8:
                            if self.field[current_x][current_y] == self.rival:
                                # print("rival")
                                # 相手のコマを通って、突き当たりで自分のコマがくれば、[x,y]にコマをおける
                                if not connect:
                                    connect = True
                                # # 相手のコマを２回以上通るときはない
                                # else:
                                #     break
                            elif self.field[current_x][current_y] == self.piece:
                                # print("player")
                                # 相手のコマを通っていて、かつ突き当たりに自分のコマがあれば、[x,y]に駒を置ける
                                if connect:
                                    # print("ok")
                                    self.field[x][y] = "*"
                                    temp.append([dx, dy])
                                    # 置ける場所に追加
                                    self.coordinate.append([x, y])
                                    self.count += 1
                                    break
                                # 相手のコマを通っていなければ取れない
                                else:
                                    break
                            elif self.field[current_x][current_y] == " ":
                                # print("none")
                                break
                            elif self.field[current_x][current_y] == "*":
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
        self.field[x][y] = self.piece
        # 探索するベクトル
        for direction in self.direction[x][y]:
            dx = direction[0]
            dy = direction[1]
            current_x = x + dx
            current_y = y + dy
            while self.field[current_x][current_y] == self.rival:
                self.field[current_x][current_y] = self.piece
                current_x += dx
                current_y += dy

    # 相手のターンと自分のターンを切り替える
    def switch(self):
        if self.player == 1:
            self.piece = "◯"
            self.rival =  "●"
            self.player = 0
        elif self.player == 0:
            self.piece = "●"
            self.rival = "◯"
            self.player = 1
    
    # 実行する関数
    def main(self):
        if self.mode == 0:
            print("PvP!")
            # TODO
            # とりあえず無限ループで実行
            while True:
                self.put()
        elif self.mode == 1:
            print("cpu!")
            if self.player == 0:
                # TODO
                # とりあえず無限ループで実行
                while True:
                    self.put()
                    self.cpu()
            else:
                while True:
                    self.cpu()
                    self.put()
        else:
            print("invalid mode !")
            sys.exit(1)





if __name__ == "__main__":
    reversi = Reversi(player=0, mode=1)
    # while True:
    reversi.main()