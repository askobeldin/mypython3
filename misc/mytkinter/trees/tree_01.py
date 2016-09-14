# -*- coding: utf-8 -*-
# python 3
################################################################################
import tkinter as tk
from tkinter import ttk
from os import urandom


class MainWindow(object):
    def __init__(self, master, title=None, data=None):
        self.data = data
        self.tree = None
        self.style = ttk.Style()
        self.style.theme_use('alt')
        # self.style.theme_use('clam')

        self.container = ttk.Frame(master)
        self.container.pack(side='top', fill='both', expand=True)
        self.master = self.container.master

        width = 540
        height = 300
        self.master.geometry('%dx%d' % (width, height))
        self.master.minsize(width-200, height-120)
        self.master.title(title)

        # setting up an icon
        # icon = tk.PhotoImage(file='img/fusion-icon.gif')
        # self.master.tk.call('wm', 'iconphoto',
                            # self.master._w, icon)

        # connecting to the external styling optionDB.txt
        # self.master.option_readfile('optionDB.txt')

        self.__setup_widgets()
        self.__build_tree()

    def __setup_widgets(self):
        # top frame
        top = ttk.Frame(self.container)
        top.pack(side='top', fill='both', expand=True)
        # bottom frame
        bottom = ttk.Frame(self.container,
                          padding=(1, 1, 1, 1))

        self.tree = ttk.Treeview(top,
                            columns = ("first", "second"),
                            padding=(0,),
                            selectmode='browse')
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)

        self.tree.column("#0", width=340, anchor="w")
        self.tree.heading("#0", text=u"Наименование")

        self.tree.column("first", width=25, minwidth=15, stretch=True,
                         anchor="center")
        self.tree.column("second", width=25, minwidth=15, stretch=True,
                         anchor="center")
        self.tree.heading("first", text=u"Один")
        self.tree.heading("second", text=u"Два")

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=top)

        vsb.grid(column=1, row=0, sticky='ns', in_=top)
        hsb.grid(column=0, row=1, sticky='ew', in_=top)

        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)

        # events
        self.tree.bind('<Double-Button-1>', self.print_node_data)

        # buttons
        btn1 = ttk.Button(bottom, text='Show',
                          command=self.tree_info)
        btn2 = ttk.Button(bottom, text='Add item',
                          command=self.additem)
        btn3 = ttk.Button(bottom, text='Del item',
                          command=self.deleteitem)
        btn4 = ttk.Button(bottom, text='Get children',
                          command=self.getchildren)
        # packing
        bottom.pack(side='bottom', fill='x')

        btn1.pack(side='left')
        btn2.pack(side='left')
        btn3.pack(side='left')
        btn4.pack(side='left')


    def __build_tree(self):
        tree = self.tree
        # img = tk.PhotoImage(file='img/brush1.gif')
        # self.tree.img = img
        if self.data:
            # insert data to tree
            for item in self.data:
                iid = item.get('iid', '')
                pid = item.get('pid', '')
                text = item.get('text', u'')
                values = [str(i) for i in item.get('values', [])]
                index = item.get('index', 'end')

                # add image
                tree.insert(iid=iid,
                            parent=pid,
                            index=index,
                            text=text,
                            values=values)

    def print_node_data(self, event):
        tree = event.widget
        node = tree.focus()
        print('node iid is', node)
        print('.set of node is', tree.set(node))
        print('.item of node is', tree.item(node))
        print('.selection of node is', tree.selection())

    def tree_info(self):
        node = self.tree.focus()
        print('Button: .item of node is', self.tree.item(node))

    def additem(self):
        node = self.tree.focus()
        print('Add item to node:', self.tree.item(node))
        text='text: %s' % ''.join(['%02x' % c for c in urandom(3)])
        self.tree.insert(parent=node,
                         index='end',
                         text=text,
                         values=('a: %s' % text, 'b: %s' % text))

    def deleteitem(self):
        node = self.tree.focus()
        print('Try to delete item:', self.tree.item(node))
        self.tree.delete(node)

    def getchildren(self):
        node = self.tree.focus()
        print('Try to get children')
        # print self.tree.get_children()
        print(self.tree.get_children(node))


# data 
DATA = (
    {'iid': 'm1',
     'pid': '',
     'text': u'material 1',
     'values': (3, 4),
    },
    {'iid': 'm2',
     'pid': 'm1',
     'text': u'material 2',
     'values': (2, 4),
    },
    {'iid': 'm3',
     'pid': 'm1',
     'text': u'submaterial 1',
     'values': (3, 4),
    },
    {'iid': 'm4',
     'pid': 'm1',
     'text': u'submaterial 2',
     'values': (3, u'тест'),
    },
    {'iid': 'm5',
     'pid': 'm2',
     'text': u'submaterial 20',
     'values': (2, 4),
    },
    {'iid': 'm6',
     'pid': 'm4',
     'text': u'submaterial 200',
     'values': (2, 4),
    },
    {'iid': 'm10',
     'pid': '',
     'text': u'material 1200',
     'values': (2, 4),
    },
    {'iid': 'm12',
     'pid': '',
     'text': u'material 1600',
     'values': (20, 40),
    },
)


def main():
    root = tk.Tk()
    app = MainWindow(root, title=u'My application',
                    data=DATA)
    root.mainloop()


if __name__ == '__main__':
    main()
