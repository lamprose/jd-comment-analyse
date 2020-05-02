from tkinter import ttk
import tkinter as tk
from analyse import anaylyse


class Chart(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.master = master
        print(type(self.master))
        self.lists = []
        self.treeview = ttk.Treeview(master, show="headings", columns=data)
        for l in data:
            self.treeview.column(l, width=100, anchor='center')
            self.treeview.heading(l, text=l)
        self.treeview.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        #y滚动条
        self.yscrollbar = tk.Scrollbar(master,
                                       orient=tk.VERTICAL,
                                       command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.bind('<Button-3>', self.popup)
        self.popup_menu = tk.Menu(self.master, tearoff=0)
        for k in ['查看', '删除']:
            m = tk.Menu(self.popup_menu, tearoff=0)
            # 添加子菜单
            self.popup_menu.add_command(label=k,
                                        command=self.handlerAdaptor(
                                            self.choose, x=k))
        # for i in range(100):
        #     self.treeview.insert('', i, values=(i, '1234', '12345', i))

    def init_data(self, data):
        children = self.treeview.get_children()
        for item in children:
            self.treeview.delete(item)
        i = 0
        for item in data:
            self.treeview.insert('',
                                 i,
                                 values=(item['name'], item['price'],
                                         item['shop'], item['img'],
                                         item['pid']))
            i += 1

    def popup(self, event):
        # 在指定位置显示菜单
        self.popup_menu.post(event.x_root, event.y_root)  #①

    def choose(self, x):
        # 如果用户选择修改字体大小的子菜单项
        if x == "查看":
            print(self.treeview.item(self.treeview.selection()[0], 'values'))
            anaylyse(
                self.master,
                self.treeview.item(self.treeview.selection()[0], 'values'))
        else:
            print("qqqq")

    def handlerAdaptor(self, fun, **kwds):
        return lambda fun=fun, kwds=kwds: fun(**kwds)
