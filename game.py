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
        self.img_col1 = tkinter.PhotoImage(file='col1.png')
        self.img_col2 = tkinter.PhotoImage(file='col2.png')
        self.img_col3 = tkinter.PhotoImage(file='col3.png')
        self.img_col4 = tkinter.PhotoImage(file='col4.png')

        self.speed = 300

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
        self.__update()
        self.__render()
        if not self.stage.is_end():
#            self.root.after(self.speed, self.__game_loop)
            self.root.after(500, self.__game_loop)
        else:
            self.__render(True)

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
        self.canvas.delete('block')

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
                    if cell_coldata == stage.Stage.COL2:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_col2,  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )
                    if cell_coldata == stage.Stage.COL3:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_col3,  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )
                    if cell_coldata == stage.Stage.COL4:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # ｘ座標
                            y * block.Block.SCALE,  # ｙ座標
                            image=self.img_col4,  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )









