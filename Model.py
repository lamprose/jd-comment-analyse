# using third-party package jieba to
import jieba, os, traceback
import gensim
import smart_open
from gensim.models import Doc2Vec
import joblib
from collections import defaultdict
from operator import add
import wordcloud


class Train():
    def __init__(self):
        super().__init__()


class Model():
    def __init__(self, d2vPath, modelPath):
        self.d2v = Doc2Vec.load(d2vPath)
        self.model = joblib.load(modelPath)
        self.result = [0, 0, 0, 0, 0, 0]
        self.wordcloud = None

    def wordCut(self):
        with open(f'temp/{self.file_name}_cut.txt', 'w',
                  encoding='utf-8') as f:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as ff:
                    filter_chars = "\r\n\t，。；！,.:;：、“”‘’"
                    trans_dict = dict.fromkeys((ord(_) for _ in filter_chars),
                                               '')
                    for line in ff.readlines():
                        line = line.translate(trans_dict)
                        # words segment
                        it = jieba.cut(line, cut_all=False)
                        _ = []
                        for w in it:
                            _.append(w)

                        f.write(' '.join(_) + '\n')
            except:
                pass
        print('OK2')

    def analyse(self, filePath):
        self.file_path = filePath
        self.file_name = os.path.basename(filePath).split('.')[0]
        if not os.path.exists(f'temp/{self.file_name}_cut.txt'):
            print('OK')
            self.wordCut()
        with open(f'temp/{self.file_name}_cut.txt', 'r',
                  encoding='utf-8') as f:
            txt = ''
            print('OK1')
            while True:
                line = f.readline()
                if not line:
                    break
                txt += line.replace('\n', ' ')
                line_ls = line.replace('\n', '').split(' ')
                # pls fine-tune your hyper-parameters: alpha & steps
                # as there is random seed, you could infer for N times and use the average as the final infer vector
                # it will take more time but have high accuracy
                line_vec = self.d2v.infer_vector(line_ls, alpha=0.95, steps=50)
                for _ in range(0, 9):
                    line_vec += self.d2v.infer_vector(line_ls,
                                                      alpha=0.95,
                                                      steps=50)
                line_vec /= 10
                self.result[int(self.model.predict([line_vec]))] += 1
        self.result[0] = 1
        self.generate_wordcloud(txt)
        os.remove(f'temp/{self.file_name}_cut.txt')
        return self.result

    def generate_wordcloud(self, txt):
        w = wordcloud.WordCloud(width=200,
                                height=200,
                                background_color='white',
                                font_path='msyh.ttc')
        print(txt)
        w.generate(txt)
        self.wordcloud = w.to_image()

    def get_wordcloud(self):
        return self.wordcloud
