import tkinter as TK
import threading
import MyThread
from MainView import *
from Spider.SearchSpider import SearchSpider


class App():
    def __init__(self, master):
        self.master = master
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        alignstr = '800x500+%d+%d' % ((screenwidth - 800) / 2,
                                      (screenheight - 500) / 2)
        self.master.geometry(alignstr)
        TK.Label(self.master, text="MultiListbox").pack()
        frame_root = TK.Frame(tk)
        self.keyword = TK.StringVar()
        TK.Entry(frame_root, textvariable=keyword).pack(side=TK.LEFT,
                                                        expand=TK.YES,
                                                        fill=TK.BOTH)
        TK.Button(frame_root,
                  text='搜索',
                  command=lambda: search(self.keyword.get(), self.chart)).pack(
                      side=TK.RIGHT)
        frame_root.pack(fill=TK.BOTH)
        self.chart = Chart(self.master, ('商品名', '价格', '店铺名'))
        chart.pack(expand=TK.YES, fill=TK.BOTH)


def search(kw, chart):
    #print(keyword.get())
    searchSpider = SearchSpider(kw)
    p1 = MyThread.MyThread(searchSpider.get_data, args=())
    p1.start()
    # re = p1.get_result()
    # print(re)
    c1 = MyThread.MyThread(search_start, args=(p1, chart))
    c1.start()


def search_start(p1, chart):
    while True:
        if (p1.get_result() != None):
            break
    # for i in p1.get_result():
    #     print('name:%s,price:%s' % (i['name'], i['price']))
    chart.init_data(p1.get_result())
    return


if __name__ == '__main__':
    #初始化Tk()
    # global chart
    tk = TK.Tk()
    #设置标题
    tk.title('京东商品评论分析')
    #获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = tk.winfo_screenwidth()
    screenheight = tk.winfo_screenheight()
    alignstr = '800x500+%d+%d' % ((screenwidth - 800) / 2,
                                  (screenheight - 500) / 2)
    tk.geometry(alignstr)
    TK.Label(tk, text="Hello !").pack()
    frame_root = TK.Frame(tk)
    keyword = TK.StringVar()
    TK.Entry(frame_root, textvariable=keyword).pack(side=TK.LEFT,
                                                    expand=TK.YES,
                                                    fill=TK.BOTH)
    TK.Button(frame_root,
              text='搜索',
              command=lambda: search(keyword.get(), chart)).pack(side=TK.RIGHT)
    frame_root.pack(fill=TK.BOTH)
    chart = Chart(tk, ('商品名', '价格', '店铺名'))
    chart.pack(expand=TK.YES, fill=TK.BOTH)
    tk.mainloop()