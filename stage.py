import random
import block


class Stage:
    """
    ぽゆぽゆの盤面を管理するクラスです。
    """
    WIDTH = 6  # 盤面の幅
    HEIGHT = 12  # 盤面の高さ

    NONE = 0    # 空マス
    BLOCK = 1   # ブロックマス
    FIX = 2     # 固定ブロックマス
    VANISH = 3  # 消去(予定)ブロック

    COL1 = 1  # 'red'
    COL2 = 2  # 'blue'
    COL3 = 3  # 'yellow'
    COL4 = 4  # 'green'

    def __init__(self):
        """
        盤面を生成させます。
        """
        self.data = [[Stage.NONE for i in range(Stage.WIDTH)] for j in range(Stage.HEIGHT)]     # ブロックの種類
        self.coldata = [[Stage.NONE for i in range(Stage.WIDTH)] for j in range(Stage.HEIGHT)]  # ブロックの色
        self.chkdata = [[Stage.NONE for i in range(Stage.WIDTH)] for j in range(Stage.HEIGHT)]  # ブロックの接続ラベル

        self.hbridge = [[Stage.NONE for i in range(Stage.WIDTH)] for j in range(Stage.HEIGHT)]  # 水平ブリッジ
        self.vbridge = [[Stage.NONE for i in range(Stage.WIDTH)] for j in range(Stage.HEIGHT)]  # 垂直ブリッジ

        self.block = block.Block()
        self.type = 0
        self.rot = 0
        self.can_drop = True
        self.remove_line = [False for i in range(Stage.HEIGHT)]
        self.is_fix = False
        self.__select_block()
        self.cnt = [0]
        self.chain = 0  # 連鎖中フラグ 0(00):連鎖中でない　1(01):VANISHあり　2(10):VANISH消した　3(11):01かつ10
        self.chaincnt = 0   # 連鎖数カウンタ
        self.gameflg = 0  # 0:title 1:game 2:gameover

        self.cntblk = [0, 0]    # 操作中心ブロックのステージ座標
        self.msgren = False     # 連鎖メッセージの有無


    def update(self):
        """
        ステージの更新処理を行うメソッドです。
        """
        print('update()')
#        self.block.y += 10
        self.__marge_block()    # 操作ブロックをFIX

#        self.__remove_lines()
#        self.__fall_block()
#        self.chain = self.__check_remove_lines()

        if self.chain != 0:  # 連鎖中
            print("---chain now---")
#            self.chain = self.__remove_lines()
            self.__remove_lines()   # 消去予定だったブロックを消す(NONE)
            self.__fall_block()     # 浮いてるブロックを落とす
            self.__check_bridge()   # ブリッジ描画用に連結しているブロックをチェックする
            ret = self.__check_remove_lines()   # ４つ以上 連結しているブロックを消去予定にする
            print("ret={}".format(ret))
            if ret:     # 更に消去予定のブロックあり(２連鎖以上)
                print("chaincnt={}".format(self.chaincnt), end='')
                self.chaincnt += 1
                print("->{}".format(self.chaincnt))
                print("{}連鎖".format(self.chaincnt))
                self.msgren = True

            else:       # 消去予定のブロックなし(連鎖終了)
                self.chaincnt = 0
                print("chaincnt={}".format(self.chaincnt))


#        else:
        if self.chain == 0:  # 連鎖中でない
            print("---not chain now---(icb={}, isfix={}, candrp={})".format(self.is_collision_bottom(), self.is_fix, self.can_drop))
            self.chaincnt = 0

            # もし下方向に衝突しない場合
            if not self.is_collision_bottom():
                self.is_fix = False
                if self.can_drop:   # pause中でなければ
                    self.__drop_block()

                # もし下方向に衝突する場合
            else:
                self.is_fix = True
#            self.__separate_block()
                self.__fix_block()
                self.__fall_block()
                self.__check_bridge()
#            self.__fix_block()
#            self.__check_remove_lines()
#            self.__remove_lines()
#                self.chain = self.__check_remove_lines()
#                self.__check_remove_lines()
                ret = self.__check_remove_lines()
                print("ret={}".format(ret))
                if ret:     # 消去予定のブロックあり(連鎖開始)
                    print("chaincnt={}".format(self.chaincnt), end='')
                    self.chaincnt += 1
                    print("->{}".format(self.chaincnt))
                    print("{}連鎖".format(self.chaincnt))
                    self.msgren = True

                else:       # 消去予定のブロックなし(連鎖開始ならず)
                    self.chaincnt = 0
                    print("chaincnt={}".format(self.chaincnt))

#            while self.chain:  # 連鎖中
#                self.chain = self.__remove_lines()
#                self.__fall_block()
#                self.__check_remove_lines()

#            if not self.chain:
                self.block.reset()
                self.__select_block()
            # self.block.y = -1
    #            self.clear_check()

        if self.chain >= 2:     # VANISH消去フラグをクリア
            self.chain -= 2



    def input(self, key):
        """
        キー入力を受け付けるメソッドです。
        各キーの入力に対しての処理を記述してください
        """
        if key == 'space':   # スペースキー

            if self.gameflg == 0:       # title画面の場合
                self.gameflg = 1        # ゲーム開始
                self.__init_stage()     # ステージ初期化

            elif self.gameflg == 2:     # gameover画面の場合
                self.gameflg = 0        # titleに戻る

            else:
                self.can_drop = not self.can_drop   # pause

        if key == 'w':  # Wキー(回転)
            # print('wキーが押されました')
            self.__rotation_block()

        if key == 'a':  # Aキー(左移動)
            # print('aキーが押されました')
            if not self.is_collision_left():
                self.block.x -= 1

        if key == 's':  # Sキー(下移動)
            # print('sキーが押されました')
            self.hard_drop()

        if key == 'd':  # Dキー(右移動)
            # print('dキーが押されました')
            if not self.is_collision_right():
                self.block.x += 1

    def __select_block(self):
        """
        ブロックの色の組み合わせをランダムに選びます。
        """
        print('__select_block()')
        # ランダムにブロックの角度を選ぶ
        #　self.rot = random.randint(0, block.Block.ROT_MAX - 1)
        self.rot = 0

        # ランダムにブロックの色を選ぶ
        self.block.col[0] = random.randint(1, 4)
        self.block.col[1] = random.randint(1, 4)

#DBG        print('col[0]={}, col[1]={}'.format(self.block.col[0], self.block.col[1]))

    def __rotation_block(self):
        """
        ブロックを回転させるメソッドです。
        """
        print('__rotation_block()')
        """
        self.rot += 1
        if self.rot == block.Block.ROT_MAX
            self.rot = 0
        """
        if self.__can_rotation_block():
            self.rot = (self.rot + 1) % block.Block.ROT_MAX

    def __can_rotation_block(self):
        """
        現在のブロックが回転可能かを判定するメソッドです。
        回転することが出来るのであればTrueを返却し、
        そうでなければ、Falseを返却します。
        """
        print('__can_rotation_block()')

        # 次の角度
        n_rot = (self.rot + 1) % block.Block.ROT_MAX
        # ブロックの座標
        b_x = self.block.x
        b_y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 次の角度のブロック情報を取得する
                if self.block.get_cell_data(n_rot, j, i) == Stage.BLOCK:
                    # 範囲外チェック
                    if self.is_out_of_stage(b_x + j, b_y + i):
                        return False
                    # 固定ブロックとの衝突チェック
                    if self.data[b_y + i][b_x + j] == Stage.FIX:
                        return False
        return True


    def __drop_block(self):
        """
        操作ブロックを１段下げるメソッドです。
        """
        print('__drop_block()')
        self.block.y += 1


    def __separate_block(self):
        """
        ブロックが下衝突後に衝突しなかった方が、更に落下できるなら、
        分離して落下させる
        ※不使用
        __fix_block() → __fall_block() で分離して落ちる
        """
        print('__separate_block()')
        b_r = self.rot
        b_x = self.block.x
        b_y = self.block.y

#        for i in range(block.Block.SIZE):
#            for j in range(block.Block.SIZE):
#                if self.block.get_cell_data(b_r, j, i) == Stage.BLOCK or self.block.get_cell_data(b_r, j, i) == Stage.FIX:
#                    while not self.is_collision_bottom(b_x + j, b_y + i):
#                        if not self.is_out_of_stage(b_x + j, b_y + i + 1):
#                            if self.data[b_y + i + 1][b_x + j] == Stage.NONE:
#                        self.data[b_y + i + 1][b_x + j] = Stage.BLOCK
#                        self.coldata[b_y + i + 1][b_x + j] = self.coldata[b_y + i][b_x + j]
#                        self.data[b_y + i][b_x + j] = Stage.NONE
#                        self.coldata[b_y + i][b_x + j] = Stage.NONE
#                                i += 1
#                        continue
#                            else:
#                                break
#                        else:
#                            break

        """
        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_r, j, i) == Stage.BLOCK:
                    if i == 1 and j == 1:
                        self.data[b_y + i][b_x + j] = Stage.BLOCK
                        self.coldata[b_y + i][b_x + j] = self.block.col[0]
                    else:
                        self.data[b_y + i][b_x + j] = Stage.BLOCK
                        self.coldata[b_y + i][b_x + j] = self.block.col[1]
        """

        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if self.data[i][j] == Stage.BLOCK:
                    self.data[i][j] = Stage.FIX
                    """
                    if not self.is_out_of_stage(j, i + 1):
                        if self.data[i + 1][j] == Stage.NONE:
                            self.data[i + 1][j] = Stage.BLOCK
                            self.coldata[i + 1][j] = self.coldata[i][j]
                            self.data[i][j] = Stage.NONE
                            self.coldata[i][j] = Stage.NONE
                            i -= 1
                        else:
                            self.data[i][j] = Stage.FIX
                    else:
                        self.data[i][j] = Stage.FIX
                    """

    def __marge_block(self):
        """
        ブロックのデータをステージのデータにマージするメソッドです。
        """
        print('__marge_block()')
#        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot
        b_x = self.block.x
        b_y = self.block.y

        # ステージの状態を一度リセット
        for i in range(Stage.HEIGHT):
            for j in range(Stage.WIDTH):
                if self.data[i][j] == Stage.BLOCK:
                    self.data[i][j] = Stage.NONE
                    self.coldata[i][j] = Stage.NONE

        # ブロックデータをステージに反映
        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_r, j, i) == Stage.BLOCK:
                    if not self.is_out_of_stage(b_x + j, b_y + i):
                        if i == 1 and j == 1:
                            self.data[b_y + i][b_x + j] = Stage.BLOCK
                            self.coldata[b_y + i][b_x + j] = self.block.col[0]
                            self.cntblk[0] = b_x + j    # 操作中心ブロックのステージ座標を保存
                            self.cntblk[1] = b_y + i
                        else:
                            self.data[b_y + i][b_x + j] = Stage.BLOCK
                            self.coldata[b_y + i][b_x + j] = self.block.col[1]

    def __fix_block(self):
        """
        ブロックを固定(FIX)するメソッドです。
        """
        print('__fix_block()')

#        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot
        b_x = self.block.x
        b_y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_r, j, i) == Stage.BLOCK:
                    self.data[b_y + i][b_x + j] = Stage.FIX

    def is_out_of_stage(self, x, y):
        """
        指定されたステージの座標が範囲外かを調べるメソッドです。
        x: ステージセルのＸ軸
        y: ステージセルのＹ軸
        """
# DBG        print('is_out_of_stage()')

        return x < 0 or x >=Stage.WIDTH or y < 0 or y >= Stage.HEIGHT

    def is_collision_bottom(self, x=-1, y=-1):
        """
        下方向の衝突判定を行うメソッドです。
        衝突していればTrueが返却され、そうでなければFalseが返却されます。
        x: 対象のブロックのX軸座標
        y: 対象のブロックのY軸座標
        """
# DBG        print('is_collision_bottom()')

#        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot
#        b_x = self.block.x
#        b_y = self.block.y

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
               if self.block.get_cell_data(b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ下げたマスが
                    # ステージの範囲外だった場合
                    tx = x + j
                    ty = y + i + 1
                    if self.is_out_of_stage(tx, ty):
                        return True
                    # 対象のブロックマスの位置から１つ下げたマスが
                    # 固定されたブロックのマス(2)だった場合
                    if self.data[y+i+1][x+j] == Stage.FIX:
                        return True

        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def is_collision_left(self, x=-1, y=-1):
        """
        左方向の衝突判定を行うメソッドです。
        衝突していればTrueが返却され、そうでなければFalseが返却されます。
        x: 対象のブロックのX軸座標
        y: 対象のブロックのY軸座標
        """
# DBG        print('is_collision_left()')

#        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot

#        b_x = self.block.x
#        b_y = self.block.y

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ左のマスが
                    # ステージの範囲外だった場合
                    if self.is_out_of_stage(x + j - 1, y + i):
                        return True
                    # 対象のブロックマスの位置から１つ左のマスが
                    # 固定されたブロックのマス(2)だった場合
                    if self.data[y+i][x+j-1] == Stage.FIX:
                        return True

        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def is_collision_right(self, x=-1, y=-1):
        """
        右方向の衝突判定を行うメソッドです。
        衝突していればTrueが返却され、そうでなければFalseが返却されます。
        x: 対象のブロックのX軸座標
        y: 対象のブロックのY軸座標
        """
# DBG        print('is_collision_right()')

#        b_x = self.block.x
#        b_y = self.block.y
#        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ右のマスが
                    # ステージの範囲外だった場合
                    if self.is_out_of_stage(x + j + 1, y + i):
                        return True
                    # 対象のブロックマスの位置から１つ右のマスが
                    # 固定されたブロックのマス(2)だった場合
                    if self.data[y+i][x+j+1] == Stage.FIX:
                        return True

        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def hard_drop(self):
        """
        ハードドロップ処理です。
        """
        print('hard_drop()')
        # 下に衝突判定がない限りブロックを下げ続ける
        while True:
            if not self.is_collision_bottom():
                self.__drop_block()
            else:
                break

    def __check_remove_lines(self):
        """
        次に消えるブロックをチェックするメソッドです。
        """
        print('__check_remove_lines()')

        flg = 0
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                self.chkdata[i][j] = Stage.NONE    # ラベル初期化
#        self.cnt.clear()
        self.cnt = [0]  # ラベルごとの接続数カウンタ


        for i in range(self.HEIGHT):
            # この下、デバッグ用のコンソール表示
            print('i={},    data=['.format(i), end='')
            for j in range(self.WIDTH):
                print('{}, '.format(self.data[i][j]), end='')
            print(']   ', end='')
            print('coldata=['.format(i), end='')
            for j in range(self.WIDTH):
                print('{}, '.format(self.coldata[i][j]), end='')
            print(']  ', end='')
            print('chkdata=['.format(i), end='')
            for j in range(self.WIDTH):
                print('{}, '.format(self.chkdata[i][j]), end='')
            print(']  ', end='')
            print('cnt={}'.format(self.cnt))

            for j in range(self.WIDTH):
                if self.data[i][j] == Stage.FIX:
                    if self.chkdata[i][j] == Stage.NONE:    # 注目ブロックにラベルがなければ、ここで新たなラベルを追加して付与する
#DBG                        print('1 [{}, {}] col={} chk={} cnt={} flg={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt, flg))
                        flg += 1    # 新ラベル
                        self.cnt.append(0)  # 隣接ブロック数カウンタに新ラベル分の枠を追加
#DBG                        print('2 [{}, {}] col={} chk={} cnt={} flg={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt, flg))
                        self.chkdata[i][j] = flg
                        self.cnt[flg] += 1
#DBG                        print('3 [{}, {}] col={} chk={} cnt={} flg={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt, flg))

                    # 右方向
                    if (not self.is_out_of_stage(j+1, i)) and self.coldata[i][j + 1] == self.coldata[i][j] and self.data[i][j + 1] == Stage.FIX:
                        if self.chkdata[i][j + 1] == Stage.NONE:    # 右隣接ブロックにラベルが付いてなかった
                            self.chkdata[i][j + 1] = self.chkdata[i][j]
                            self.cnt[self.chkdata[i][j]] += 1
#DBG                            print('R1[{}, {}] col={} chk={} cnt={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j],
#DBG                                                                           self.cnt))
                        elif self.chkdata[i][j + 1] != self.chkdata[i][j]:  # 右隣接ブロックが違うラベルだったら、ラベルの統合処理
                            tmp = self.chkdata[i][j + 1]    # 違っていたラベルを一時保管
                            for i2 in range(self.HEIGHT):   # メインの二重ループとは別の二重ループ
                                for j2 in range(self.WIDTH):
                                    if self.chkdata[i2][j2] == tmp:     # 統合されるラベルを持つブロックを全てラベル書き換え
                                        self.chkdata[i2][j2] = self.chkdata[i][j]
                            print('flg={}, tmp={}, in {}'.format(flg, tmp, self.cnt))
                            self.cnt[self.chkdata[i][j]] += self.cnt[tmp]   # 統合元のカウンタを統合先のカウンタに加算
                            self.cnt[tmp] = 0   # 統合元のカウンタを0にする(このラベルはもう使われないけど、一応)
#DBG                            print('R2[{}, {}] col={} chk={} cnt={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt))

                    # 下方向
                    if (not self.is_out_of_stage(j, i+1)) and self.coldata[i + 1][j] == self.coldata[i][j] and self.data[i + 1][j] == Stage.FIX:
                        if self.chkdata[i + 1][j] == Stage.NONE:    # 下隣接ブロックにラベルが付いてなかった
                            self.chkdata[i + 1][j] = self.chkdata[i][j]
                            self.cnt[self.chkdata[i][j]] += 1
#DBG                            print('U1[{}, {}] col={} chk={} cnt={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt))
                        elif self.chkdata[i + 1][j] != self.chkdata[i][j]:  # 下隣接ブロックが違うラベルだったら、ラベルの統合処理
                            tmp = self.chkdata[i + 1][j]    # 違っていたラベルを一時保管
                            for i2 in range(self.HEIGHT):
                                for j2 in range(self.WIDTH):
                                    if self.chkdata[i2][j2] == tmp:
                                        self.chkdata[i2][j2] = self.chkdata[i][j]
                            self.cnt[self.chkdata[i][j]] += self.cnt[tmp]
                            self.cnt[tmp] = 0
#DBG                            print('U2[{}, {}] col={} chk={} cnt={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt))

                    """
                    ※右方向と下方向をちゃんとやれば、左方向と上方向は不要
                    
                    # 左方向
#                    if self.chkdata[i][j - 1] == Stage.NONE and self.coldata[i][j - 1] == self.coldata[i][j]:
#                        self.chkdata[i][j - 1] = self.chkdata[i][j]
#                        self.cnt[self.chkdata[i][j]] += 1
                    if (not self.is_out_of_stage(j-1, i)) and self.coldata[i][j - 1] == self.coldata[i][j] and self.data[i][j - 1] == Stage.FIX:
                        if self.chkdata[i][j - 1] == Stage.NONE:    # ラベルが付いてなかった
                            self.chkdata[i][j - 1] = self.chkdata[i][j]
                            self.cnt[self.chkdata[i][j]] += 1
                            print('R1[{}, {}] col={} chk={} cnt={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j],
                                                                           self.cnt))
                        elif self.chkdata[i][j - 1] != self.chkdata[i][j]:  # 違うラベルだった
                            tmp = self.chkdata[i][j - 1]
                            for i2 in range(self.HEIGHT):
                                for j2 in range(self.WIDTH):
                                    if self.chkdata[i2][j2] == tmp:
                                        self.chkdata[i2][j2] = self.chkdata[i][j]
                            print('flg={}, tmp={}, in {}'.format(flg, tmp, self.cnt))
                            self.cnt[self.chkdata[i][j]] += self.cnt[tmp]
                            self.cnt[tmp] = 0
                            print('R2[{}, {}] col={} chk={} cnt={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt))

                    # 上方向
#                    if self.chkdata[i - 1][j] == Stage.NONE and self.coldata[i - 1][j] == self.coldata[i][j]:
#                        self.chkdata[i - 1][j] = self.chkdata[i][j]
#                        self.cnt[self.chkdata[i][j]] += 1
                    if (not self.is_out_of_stage(j, i-1)) and self.coldata[i - 1][j] == self.coldata[i][j] and self.data[i-1][j] == Stage.FIX:
                        if self.chkdata[i - 1][j] == Stage.NONE:    # ラベルが付いてなかった
                            self.chkdata[i - 1][j] = self.chkdata[i][j]
                            self.cnt[self.chkdata[i][j]] += 1
                            print('U1[{}, {}] col={} chk={} cnt={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt))
                        elif self.chkdata[i - 1][j] != self.chkdata[i][j]:  # 違うラベルだった
                            tmp = self.chkdata[i-1][j]
                            for i2 in range(self.HEIGHT):
                                for j2 in range(self.WIDTH):
                                    if self.chkdata[i2][j2] == tmp:
                                        self.chkdata[i2][j2] = self.chkdata[i][j]
                            self.cnt[self.chkdata[i][j]] += self.cnt[tmp]
                            self.cnt[tmp] = 0
                            print('U2[{}, {}] col={} chk={} cnt={}'.format(j, i, self.coldata[i][j], self.chkdata[i][j], self.cnt))
                    """


        # 4ブロック以上、同じ色なら消す
        ret = False
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
#DBG                if self.chkdata[i][j] != 0:
#DBG                    print('{}({}) in {}'.format(self.chkdata[i][j], self.coldata[i][j], self.cnt))
                if self.cnt[self.chkdata[i][j]] >= 4:
                    self.data[i][j] = Stage.VANISH
                    ret = True      # 一つでもVANISHにしたらTrue,一つもVANISHにしなかったらFalse
                    if self.chain%2 == 0:
                        self.chain += 1     # VANISHありのフラグON
        print("(ret={})".format(ret))
        return ret



    def __remove_lines(self):
        """
        列を消すメソッドです。
        """
        print('__remove_lines()')
        # ret = False
        flg = False
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if self.data[i][j] == Stage.VANISH:
                    self.data[i][j] = Stage.NONE
                    self.coldata[i][j] = Stage.NONE
                    self.chkdata[i][j] = Stage.NONE
                    # ret = True
                    flg = True
        # return ret
        if flg: # 1つでもVANISHを消したら、VANISH有フラグOFF、VANISH消去フラグON
            if self.chain%2 == 1:
                self.chain -= 1
            if self.chain < 2:
                self.chain += 2
        return flg


    def __fall_block(self):
        """
        落下後に浮いているブロックを落とす
        """
        print('__fall_block()')
        for i in reversed(range(self.HEIGHT-1)):
            for j in range(self.WIDTH):
                if self.data[i][j] == Stage.FIX:
                    now = i
                    while True:
                        if not self.is_out_of_stage(j, now + 1):
                            if self.data[now + 1][j] == Stage.NONE:
                                self.data[now + 1][j] = Stage.FIX
                                self.coldata[now + 1][j] = self.coldata[now][j]
                                self.data[now][j] = Stage.NONE
                                self.coldata[now][j] = Stage.NONE
                                now += 1
                            else:   # 下が空いてない
                                break
                        else:   # 最下段
                            break


    def is_end(self):
        """
        ぽゆぽゆのゲームオーバー判定を行うメソッドです。
        ゲームオーバーであればTrueを返却し、
        そうでなければFalseを返却します。
        """
#        print('is_end()')
        if self.data[1][2] == Stage.FIX:    # 次の新しいブロックが出る位置が詰まっていると終了
            self.gameflg = 2
            print('is_end() return True gameflg={}'.format(self.gameflg))
            return True
        else:
            print('is_end() return False gameflg={}'.format(self.gameflg))
            return False

    def __init_stage(self):
        """
        ステージの初期化
        """
        for i in reversed(range(self.HEIGHT)):
            for j in range(self.WIDTH):
                self.data[i][j] = Stage.NONE
                self.coldata[i][j] = Stage.NONE
                self.chkdata[i][j] = Stage.NONE
                self.hbridge[i][j] = Stage.NONE
                self.vbridge[i][j] = Stage.NONE



    def __check_bridge(self):
        """
        連結ブリッジの調査
        """
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH-1):
                if self.data[i][j] == Stage.FIX and self.data[i][j+1] == Stage.FIX and self.coldata[i][j] == self.coldata[i][j+1]:
                    self.hbridge[i][j] = self.coldata[i][j]
                else:
                    self.hbridge[i][j] = Stage.NONE

        for i in range(self.HEIGHT-1):
            for j in range(self.WIDTH):
                if self.data[i][j] == Stage.FIX and self.data[i+1][j] == Stage.FIX and self.coldata[i][j] == self.coldata[i+1][j]:
                    self.vbridge[i][j] = self.coldata[i][j]
                else:
                    self.vbridge[i][j] = Stage.NONE








