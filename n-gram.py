from sqlite_select import SelectTweet
import MeCab


class BiGram(object):
    def __init__(self):
        self.gram_num = 2
        self.db_comment = SelectTweet().export_tweet()

        self.mecab = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        self.mecab.parse('')

    def gram(self, comment):
        length = len(comment) - self.gram_num + 1  # た。みたいに最後のもだしてしまうので+1
        element = [comment[i:i+self.gram_num] for i in range(length)]  # 要素番号

        return element

    def process_morgram(self):  #形態素 = morpheme
        pos_list = ["名詞", "動詞", "形容詞"]
        skip_list = ["*"]

        data_list = []  # 各txtごとにまとめたリスト
        for txt in self.db_comment:
            """
            形態素情報が欲しいためテキストで結果を返すparseではなくparseToNodeを使用する
            surface...表層形、feature...形態素情報
            """
            text = txt[0]  # 返り値が(hoge, )になるので0番目nodeを取得
            node = self.mecab.parseToNode(text)

            node_list = []  # txt内のnodeをまとめたリスト
            while node:
                """
                feats返り値例 : ['動詞', '自立', '*', '*', '五段・ラ行', '体言接続特殊２', '戻る', 'モド', 'モド']
                よって原型を取得するにはnode6を取得すれば良い
                """
                feats = node.feature.split(',')
                if feats[0] in pos_list and feats[6] not in skip_list:
                    try:
                        node_list.append(feats[6])
                    except Exception as e:
                        print("err:{0}, cause:{1}".format(str(node.surface), e))

                node = node.next  # ジェネレーター
            data_list.append(node_list)

        return data_list

    def vec_bigram(self):
        data_list = self.db_comment[:10]
        length = len(data_list)

        for i in range(length):
            print("################")
            base = data_list[i][0]
            print(base)
            print("################")
            for j in range(length):
                if not i == j:
                    comp = data_list[j][0]
                    word = [b for b in base for c in comp if b == c]
                    cnt = len(word)
                    print(comp, cnt / len(base))

    def vec_morgram(self):
        length = len(self.process_morgram()[:10])

        for i in range(length):
            print("################")
            base = self.process_morgram()[i]
            print(base)
            print("################")
            for j in range(length):
                if not i == j:
                    comp = self.process_morgram()[j]
                    word = [b for b in base for c in comp if b == c]
                    cnt = len(word)
                    print(comp, cnt/len(base))


if __name__ == "__main__":
    bi = BiGram()
    bi.vec_bigram()
    # bi.vec_morgram()
