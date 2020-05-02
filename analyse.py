import tkinter as tk
from PIL import Image, ImageTk
from urllib.request import urlopen
from Spider.CommentSpider import CommentSpider
import _thread
import io
from Model import Model
from MyThread import MyThread
import time


class anaylyse(tk.Toplevel):
    def __init__(self, master, goods):
        tk.Toplevel.__init__(self, master=master)
        self.goods = goods
        self.master = master
        self.resultStr = tk.StringVar(value="分析结果")
        self.frameTop = tk.Frame(self, bg='red')
        self.frameBottom = tk.Frame(self, bg='blue')
        self.init_widget()

    def init_widget(self):
        image_bytes = urlopen('https:' + self.goods[3]).read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        self.tk_image = ImageTk.PhotoImage(
            pil_image.resize((200, 200), Image.ANTIALIAS))
        self.goodsPic = tk.Label(self.frameTop,
                                 image=self.tk_image,
                                 width=200,
                                 height=200,
                                 bg='brown').pack(side=tk.LEFT,
                                                  expand=False,
                                                  fill=tk.X)
        self.commentWordcloud = tk.Label(self.frameTop,
                                         image=self.tk_image,
                                         width=200,
                                         height=200,
                                         bg='brown')
        self.commentWordcloud.pack(side=tk.RIGHT, expand=False, fill=tk.X)
        frameInfo = tk.Frame(self.frameTop)
        frameInfoLeft = tk.Frame(frameInfo)
        tk.Label(frameInfoLeft)
        tk.Label(frameInfo, text=self.goods[0], wraplength=400,
                 justify='left').pack(side=tk.TOP, fill=tk.X, ipady=10)
        tk.Label(frameInfo,
                 text=self.goods[1],
                 wraplength=400,
                 justify='left',
                 bg='red').pack(side=tk.TOP, fill=tk.X)
        tk.Label(frameInfo, text=self.goods[2], wraplength=400,
                 justify='left').pack(side=tk.TOP, ipady=10)
        self.btn = tk.Button(frameInfo,
                             text="分析",
                             command=self.anaylyse_comment).pack()
        tk.Label(frameInfo,
                 wraplength=400,
                 textvariable=self.resultStr,
                 justify='left').pack(side=tk.TOP, ipady=10)
        frameInfo.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.commentFileName = "temp/{}.txt".format(self.goods[4])
        self.commentList = tk.Listbox(self.frameBottom)
        MyThread(self.read_comment, args=())
        _thread.start_new_thread(self.read_comment, ())
        self.commentList.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.frameTop.pack(side=tk.TOP, fill=tk.X)
        self.frameBottom.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def read_comment(self):
        try:
            fpath = open(self.commentFileName, 'r', encoding='utf-8')
            if fpath:
                line = fpath.readline()
                while line:
                    self.commentList.insert(tk.END, line)
                    line = fpath.readline()
        except:
            CommentSpider(self.goods[4]).get_data(self.commentFileName)
            # _thread.start_new_thread(
            #     CommentSpider(self.goods[4]).get_data,.
            #     (self.commentFileName, ))
            fpath = open(self.commentFileName, 'r', encoding='utf-8')
            if len(fpath.readlines()) > 100:
                line = fpath.readline()
                while line:
                    self.commentList.insert(tk.END, line)
                    line = fpath.readline()
                fpath = None

    def anaylyse_comment(self):
        model = Model('./my_db.d2v', 'classifier.model')
        p1 = MyThread(model.analyse, args=(self.commentFileName, ))
        p1.start()
        # re = p1.get_result()
        # print(re)
        c1 = MyThread(self.anaylyse_start, args=(p1, model))
        c1.start()

    def anaylyse_start(self, p1, model):
        while True:
            if (p1.get_result()[0] == 1):
                break
        # result = model.analyse('./7652063.txt')
        print(p1.get_result())
        result = p1.get_result()
        positive = (result[2] + result[3] + result[4] + result[5]) / (
            result[1] + result[2] + result[3] + result[4] + result[5])
        self.resultStr.set("分析结果:正面占{:.2%},反面占{:.2%}".format(
            positive, 1.0 - positive))
        time.sleep(10)
        self.wordcloud = ImageTk.PhotoImage(image=model.get_wordcloud())
        self.commentWordcloud.configure(image=self.wordcloud)
        return

    def resize_image(self, im, w, h):
        return ImageTk.PhotoImage(im.resize((w, h), Image.ANTIALIAS))
