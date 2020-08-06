import tkinter
import stage
import block


class Game:
    """
    ゲーム全体を管理するクラスです。
    このクラスを生成し、start()を呼び出すことで
    ゲームを開始させることができます。
    """

    def __init__(self, title, width, height):
        """
        ゲームの各パラメータの状態を初期化し、
        ゲームを開始させる準備を整えます。

        title:  ゲームのタイトル
        width:  画面の幅
        height: 画面の高さ
        """
#        self.x = 0
        self.block = block.Block()
        self.title = title
        self.width = width
        self.height = height
        self.root = tkinter.Tk()
        self.root.bind('<KeyPress>', self.__input)
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self.stage = stage.Stage()
#        self.y
        self.img_col1 = tkinter.PhotoImage(file='col1.png')     # 赤ぽゆ 画像
        self.img_col2 = tkinter.PhotoImage(file='col2.png')     # 青ぽゆ 画像
        self.img_col3 = tkinter.PhotoImage(file='col3.png')     # 黄ぽゆ 画像
        self.img_col4 = tkinter.PhotoImage(file='col4.png')     # 緑ぽゆ 画像
        self.img_tmp = tkinter.PhotoImage(file='tmp.png')       # 不明ぽゆ 画像(主にデバッグ用)
        self.img_vns = tkinter.PhotoImage(file='vanish.png')    # ぽゆ消滅 画像(不採用)
        self.img_vns2 = tkinter.PhotoImage(file='vanish2.png')  # ぽゆ消滅 画像２

        self.img_title = tkinter.PhotoImage(file='title.png')   # タイトル画像
        self.img_ren1 = tkinter.PhotoImage(file='ren1.png')     # 1連鎖画像(不使用)
        self.img_ren2 = tkinter.PhotoImage(file='ren2.png')     # 2連鎖画像
        self.img_ren3 = tkinter.PhotoImage(file='ren3.png')     # 3連鎖画像
        self.img_ren4 = tkinter.PhotoImage(file='ren4.png')     # 4連鎖画像
        self.img_ren5 = tkinter.PhotoImage(file='ren5.png')     # 5連鎖画像
        self.img_dairen = tkinter.PhotoImage(file='dairen.png')     # 大連鎖画像(6連鎖以上)
        self.img_gameover = tkinter.PhotoImage(file='gameover.png')     # ゲームオーバー画像
        self.img_waku = tkinter.PhotoImage(file='waku.png')     # 操作ぽゆ用白枠画像

        self.speed = 1000
#        self.msgflg = False

    def start(self):
        """
        ゲームを開始させるメソッドです。
        """
        self.__init()

    def __init(self):
        """
        ゲームの初期化を行るメソッドです。
        """
        self.__make_window()
        self.__game_loop()
        self.root.mainloop()

    def __make_window(self):
        """
        ゲームの画面を作成するメソッドです。
        """
        self.root.title(self.title)
        self.canvas.pack()

    def __game_loop(self):
        """
        ゲームのメインロジックを定義するメソッドです。
        """
        print("gameflg={}".format(self.stage.gameflg))

        if self.stage.gameflg == 0:     # title画面
            self.__render_msg("title")
            self.root.after(1200, self.__game_loop)

        elif self.stage.gameflg == 2:   # GameOver画面
            self.__render_msg("gameover")
            self.root.after(1200, self.__game_loop)

        else:   # Game画面

            # 連鎖演出
#            if self.msgflg and self.stage.chaincnt >= 1:
#            if self.stage.msgren:

#            else:
#            self.msgflg = True
            self.__update()
            # if self.stage.chaincnt == 0:
            self.__render()

            if self.stage.msgren:
#                if self.stage.chaincnt == 1:   # 1連鎖は表示しない(連鎖じゃないので)
#                    self.__render_msg("ren1")
                if self.stage.chaincnt == 2:
                    self.__render_msg("ren2")
                elif self.stage.chaincnt == 3:
                    self.__render_msg("ren3")
                elif self.stage.chaincnt == 4:
                    self.__render_msg("ren4")
                elif self.stage.chaincnt == 5:
                    self.__render_msg("ren5")
                elif self.stage.chaincnt >= 6:
                    self.__render_msg("dairen")

                print("in game.py {}連鎖".format(self.stage.chaincnt))

                self.stage.msgren = False

            if not self.stage.is_end():
#            if not self.stage.is_end():
#            self.root.after(self.speed, self.__game_loop)
                self.root.after(self.speed, self.__game_loop)
#            else:
#                self.__render(True)
            else:
                self.stage.gameflg = 2
                self.root.after(self.speed, self.__game_loop)



    def __input(self, e):
        """
        ユーザからの入力処理を定義するメソッドです。
        """
        self.stage.input(e.keysym)

    def __update(self):
        """
        ゲーム全体の更新処理を定義するメソッドです。
        """
 #       self.x += 32
 #       self.stage.block.y += 1

        self.stage.update()

        if self.stage.is_fix:
            # 速度を下げる
            self.speed -= 1
#DBG            print(self.speed)


    def __render(self, is_end=False):
        """
        ゲームの描画処理を定義するメソッドです。
        """
        print("__render()")

        self.canvas.delete('block')
        self.canvas.delete('bridge')
        self.canvas.delete('msg')

        # 水平ブリッジの描画
        for y in range(stage.Stage.HEIGHT):
            for x in range(stage.Stage.WIDTH-1):
                if self.stage.hbridge[y][x] != stage.Stage.NONE:
                    if self.stage.hbridge[y][x] == stage.Stage.COL1:
                        self.canvas.create_rectangle(
                            x * 32 + 16,  # x0座標
                            y * 32 + 10,  # y0座標
                            x * 32 + +16 + 32,  # x1座標
                            y * 32 + 10 + 12,  # y1座標
                            fill='red',  # 装飾色
                            tag='bridge'
                        )
                    elif self.stage.hbridge[y][x] == stage.Stage.COL2:
                        self.canvas.create_rectangle(
                            x * 32 + 16,  # x0座標
                            y * 32 + 10,  # y0座標
                            x * 32 + +16 + 32,  # x1座標
                            y * 32 + 10 + 12,  # y1座標
                            fill='blue',  # 装飾色
                            tag='bridge'
                        )
                    elif self.stage.hbridge[y][x] == stage.Stage.COL3:
                        self.canvas.create_rectangle(
                            x * 32 + 16,  # x0座標
                            y * 32 + 10,  # y0座標
                            x * 32 + +16 + 32,  # x1座標
                            y * 32 + 10 + 12,  # y1座標
                            fill='yellow',  # 装飾色
                            tag='bridge'
                        )
                    elif self.stage.hbridge[y][x] == stage.Stage.COL4:
                        self.canvas.create_rectangle(
                            x * 32 + 16,  # x0座標
                            y * 32 + 10,  # y0座標
                            x * 32 + +16 + 32,  # x1座標
                            y * 32 + 10 + 12,  # y1座標
                            fill='green',  # 装飾色
                            tag='bridge'
                        )

        # 垂直ブリッジの描画
        for y in range(stage.Stage.HEIGHT-1):
            for x in range(stage.Stage.WIDTH):
                if self.stage.vbridge[y][x] != stage.Stage.NONE:
                    if self.stage.vbridge[y][x] == stage.Stage.COL1:
                        self.canvas.create_rectangle(
                            x * 32 + 10,  # x0座標
                            y * 32 + 16,  # y0座標
                            x * 32 + 10 + 12,  # x1座標
                            y * 32 + 16 + 32,  # y1座標
                            fill='red',  # 装飾色
                            tag='bridge'
                        )
                    elif self.stage.vbridge[y][x] == stage.Stage.COL2:
                        self.canvas.create_rectangle(
                            x * 32 + 10,  # x0座標
                            y * 32 + 16,  # y0座標
                            x * 32 + 10 + 12,  # x1座標
                            y * 32 + 16 + 32,  # y1座標
                            fill='blue',  # 装飾色
                            tag='bridge'
                        )
                    elif self.stage.vbridge[y][x] == stage.Stage.COL3:
                        self.canvas.create_rectangle(
                            x * 32 + 10,  # x0座標
                            y * 32 + 16,  # y0座標
                            x * 32 + 10 + 12,  # x1座標
                            y * 32 + 16 + 32,  # y1座標
                            fill='yellow',  # 装飾色
                            tag='bridge'
                        )
                    elif self.stage.vbridge[y][x] == stage.Stage.COL4:
                        self.canvas.create_rectangle(
                            x * 32 + 10,  # x0座標
                            y * 32 + 16,  # y0座標
                            x * 32 + 10 + 12,  # x1座標
                            y * 32 + 16 + 32,  # y1座標
                            fill='green',  # 装飾色
                            tag='bridge'
                        )

        # ブロックの描画
        for y in range(stage.Stage.HEIGHT):
            for x in range(stage.Stage.WIDTH):
                linecol = 'black'

                # ステージの各マスのデータを取得する
                cell_data = self.stage.data[y][x]
                cell_coldata = self.stage.coldata[y][x]

#DBG                print(str(self.stage.data[y][x]) + ' ', end='')

                """
                if is_end:
                    # ゲームオーバーの画面を描画
                    if cell_data == stage.Stage.FIX:
                        # ゲームオーバーのブロックを描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_game_over,  # 描画画像
                            anchor='nw',             # アンカー
                            tag='block'             # タグ
                        )


                else:
                """
                # ゲームプレイ画面を描画
                # 取得したマスのデータがブロックまたは固定ブロックだった場合
                if cell_data == stage.Stage.BLOCK or cell_data == stage.Stage.FIX:
                    if  cell_coldata == stage.Stage.COL1:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_col1,  # 描画画像
                            anchor='nw',             # アンカー
                            tag='block'             # タグ
                        )
                    elif cell_coldata == stage.Stage.COL2:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_col2,  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )
                    elif cell_coldata == stage.Stage.COL3:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_col3,  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )
                    elif cell_coldata == stage.Stage.COL4:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_col4,  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )
                    else:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_tmp,  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )
                elif cell_data == stage.Stage.VANISH:
                    # 消去予定の画像を描画する
                    self.canvas.create_image(
                        x * block.Block.SCALE,  # ｘ座標
                        y * block.Block.SCALE,  # ｙ座標
                        image=self.img_vns2,  # 描画画像
                        anchor='nw',  # アンカー
                        tag='block'  # タグ
                    )
                if cell_data == stage.Stage.BLOCK and x == self.stage.cntblk[0] and y == self.stage.cntblk[1]:
                    # 操作中心ブロックに白枠をつける
                    self.canvas.create_image(
                        x * block.Block.SCALE,  # ｘ座標
                        y * block.Block.SCALE,  # ｙ座標
                        image=self.img_waku,  # 描画画像
                        anchor='nw',  # アンカー
                        tag='block'  # タグ
                    )



    def __render_msg(self, msg):
        """
        メッセージ(title,連鎖,gameover)を表示する
        連鎖はゲーム画面に重ねる(block消さない)
        """
        print("__render_msg({})".format(msg))

#        self.canvas.delete('block')
        self.canvas.delete('msg')

        if msg == "title":
            self.canvas.delete('block')
            self.canvas.delete('bridge')
            self.canvas.create_image(
                stage.Stage.WIDTH * block.Block.SCALE / 2,  # ｘ座標
                stage.Stage.HEIGHT * block.Block.SCALE / 2,  # ｙ座標
                image=self.img_title,  # 描画画像
                anchor='center',  # アンカー
                tag='msg'  # タグ
            )

        elif msg == "ren1":
            self.canvas.create_image(
                stage.Stage.WIDTH * block.Block.SCALE / 2,  # ｘ座標
                stage.Stage.HEIGHT * block.Block.SCALE / 2,  # ｙ座標
                image=self.img_ren1,  # 描画画像
                anchor='center',  # アンカー
                tag='msg'  # タグ
            )

        elif msg == "ren2":
            self.canvas.create_image(
                stage.Stage.WIDTH * block.Block.SCALE / 2,  # ｘ座標
                stage.Stage.HEIGHT * block.Block.SCALE / 2,  # ｙ座標
                image=self.img_ren2,  # 描画画像
                anchor='center',  # アンカー
                tag='msg'  # タグ
            )

        elif msg == "ren3":
            self.canvas.create_image(
                stage.Stage.WIDTH * block.Block.SCALE / 2,  # ｘ座標
                stage.Stage.HEIGHT * block.Block.SCALE / 2,  # ｙ座標
                image=self.img_ren3,  # 描画画像
                anchor='center',  # アンカー
                tag='msg'  # タグ
            )

        elif msg == "ren4":
            self.canvas.create_image(
                stage.Stage.WIDTH * block.Block.SCALE / 2,  # ｘ座標
                stage.Stage.HEIGHT * block.Block.SCALE / 2,  # ｙ座標
                image=self.img_ren4,  # 描画画像
                anchor='center',  # アンカー
                tag='msg'  # タグ
            )

        elif msg == "ren5":
            self.canvas.create_image(
                stage.Stage.WIDTH * block.Block.SCALE / 2,  # ｘ座標
                stage.Stage.HEIGHT * block.Block.SCALE / 2,  # ｙ座標
                image=self.img_ren5,  # 描画画像
                anchor='center',  # アンカー
                tag='msg'  # タグ
            )

        elif msg == "dairen":
            self.canvas.create_image(
                stage.Stage.WIDTH * block.Block.SCALE / 2,  # ｘ座標
                stage.Stage.HEIGHT * block.Block.SCALE / 2,  # ｙ座標
                image=self.img_dairen,  # 描画画像
                anchor='center',  # アンカー
                tag='msg'  # タグ
            )

        elif msg == "gameover":
            self.canvas.delete('block')
            self.canvas.delete('bridge')
            self.canvas.create_image(
                stage.Stage.WIDTH * block.Block.SCALE / 2,  # ｘ座標
                stage.Stage.HEIGHT * block.Block.SCALE / 2,  # ｙ座標
                image=self.img_gameover,  # 描画画像
                anchor='center',  # アンカー
                tag='msg'  # タグ
            )









