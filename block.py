import stage
import random

class Block:
    """
    テトリミノブロックを定義するクラスです。
    """

    SIZE = 3    # ブロックのサイズ
    SCALE = 32  # ブロックの描画サイズ
    ROT_MAX = 4      # 最高回転回数

    def __init__(self):
        """
        テトリミノブロックのポジションを初期化し
        テトリスで使用する全てのブロックを生成させます。
        """
        self.x = int(stage.Stage.WIDTH / 2 - Block.SIZE / 2)
        self.y = -1
#        self.type = random.randint(0, 6)
#        self.rot = random.randint(0, 3)
        self.blocks = [

            # Block
            # 0度
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 0, 0]

            ],
            # 90度
            [
                [0, 0, 0],
                [0, 1, 1],
                [0, 0, 0]

            ],
            # 180度
            [
                [0, 0, 0],
                [0, 1, 0],
                [0, 1, 0]

            ],
            # 270度
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 0, 0]

            ]
        ]
        self.col = [1, 1]


    def get_cell_data(self, rot, x, y):
        """
        指定されたブロックのひとマスのデータを取得します
        type: ブロックの種類
        rot: ブロックの回転
        x: ブロックのＸ軸
        y: ブロックのＹ軸
        """
        return self.blocks[rot][y][x]

    def reset(self):
        """
        ブロックの状態を初期状態に戻すメソッドです。
        """
        self.x = int(stage.Stage.WIDTH / 2 - Block.SIZE / 2)
        self.y = -1
#        stage.Stage.type = random.randint(0, 6)
#        stage.Stage.rot = random.randint(0, 3)
#        self.type = random.randint(0, 6)
#        self.rot = random.randint(0, 3)

#        print('type={}, rot={}'.format(stage.Stage.type, stage.Stage.rot))


