# -*- coding: utf-8 -*-
# python 3
############################################################
import tkinter as tk
from tkinter import ttk

# from sys import exit


class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid(sticky='nsew')
        self.master = master

        # counter for tabs in notebook
        self.tabscounter = 0

        self._applyStyle()
        self._makeMenu()
        self._createWidgets()
        self.__setup_widgets()
        self.__show_info()

    def _applyStyle(self):
        # theming
        self.style = ttk.Style()
        # self.style.theme_use('classic')
        self.style.theme_use('alt')
        # self.style.theme_use('clam')

    def _makeMenu(self):
        # main menubar
        self.menubar = tk.Menu(self.master)

        # actions menu
        actionsmenu = tk.Menu(self.menubar, tearoff=0)
        actionsmenu.add_command(label="Add new tab",
                                accelerator='Ctrl+N',
                                compound='left',
                                command=self._addnewtab)
        actionsmenu.add_command(label="cmd 2",
                                command=(lambda: 0))
        self.menubar.add_cascade(label="Actions", menu=actionsmenu)

        # windows menubar
        self.windowsmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Windows", menu=self.windowsmenu)

        # add menubar
        self.master.config(menu=self.menubar)

    def _createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # container widget
        self.container = ttk.Frame(self.master)
        self.container.grid(row=0, column=0, sticky='nsew')
        # stretch by column
        self.container.columnconfigure(0, weight=1)
        # stretch by row
        self.container.rowconfigure(0, weight=1)

        # status line
        self.statusline = ttk.Frame(self.master)
        self.statusline.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.statusline.columnconfigure(0, weight=1)

        textline = ttk.Label(self.statusline, text=u'Строка статуса',
                             anchor='w')
        textline.grid(row=0, column=0, sticky='ew')
        grip = ttk.Sizegrip(self.statusline)
        grip.grid(row=0, column=1, sticky='se')

        # notebook widget in container
        self.nb = ttk.Notebook(self.container)
        self.nb.grid(row=0, column=0, sticky='nsew')

        # events
        self.nb.bind_class('TNotebook', '<Button-2>', self.midbtn_1)
        self.nb.bind('<<NotebookTabChanged>>', self.tabchanged_1)
        self.master.bind('<Control-n>', self._addnewtab)

    def __setup_widgets(self):
        width = 540
        height = 300

        self.master.minsize(width-200, height-120)

        # setting up an icon
        icon = tk.PhotoImage(file='img/fusion-icon.gif')
        self.master.tk.call('wm', 'iconphoto',
                            self.master._w, icon)

        # centering window
        x = int(0.5 * (self.master.winfo_screenwidth() - width))
        y = int(0.5 * (self.master.winfo_screenheight() - height))
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.master.update_idletasks()

    def __show_info(self):
        print(u'winfo_screenwidth(): %s' % self.master.winfo_screenwidth())
        print(u'winfo_screenheight(): %s' % self.master.winfo_screenheight())

        print(u'master.winfo_height(): %s' % self.master.winfo_height())
        print(u'master.winfo_width(): %s' % self.master.winfo_width())

    def midbtn_1(self, event):
        """
        Destroying tab
        """
        try:
            x, y, widget = event.x, event.y, event.widget
            elem = widget.identify(x, y)
            index = widget.index('@%d,%d' % (x, y))
            print('### DESTROY: tab  \'%s\' ###' % widget.tab(index, 'text'))
            # try to close panel with index
            widget.forget(index)

            # if self.tabscounter > 0:
                # self.tabscounter -= 1
            # else:
                # self.tabscounter = 0

            self._update_windows_menu()
        except:
            pass

    def tabchanged_1(self, event):
        try:
            widget = event.widget
            # notebook.select() returns name as '.945839.3393983'
            # notebook.index(notebook.select()) returns index as 2
            print('Changed to:', widget.tab(widget.select(), 'text'))
            tabindexes = [widget.index(name) for name in widget.tabs()]
            tabnames = [widget.tab(name, 'text') for name in widget.tabs()]
            # print tabnames, tabindexes
        except:
            pass

    def _addnewtab(self, event=None):
        """
        Add new tab to notebook
        """
        # ntabs = len(self.nb.tabs())
        # newtabname = u'Tab No. %s' % (ntabs + 1)
        self.tabscounter += 1
        newtabname = u'Tab No. %s' % (self.tabscounter,)
        tabindexes = [self.nb.index(name) for name in self.nb.tabs()]
        if tabindexes:
            newindex = max(tabindexes) + 1
        else:
            newindex = 0

        newframe = ttk.Frame(self.nb)
        self.nb.add(newframe, text=newtabname, padding=2)
        # windowsmenu
        self.windowsmenu.add_radiobutton(label=newtabname,
                                         command=lambda i=newindex: self._select_window(i))


    def _update_windows_menu(self):
        # clean
        self.windowsmenu.delete(0,
                                self.windowsmenu.index(tk.END))
        # fill
        tabnames = [self.nb.tab(name, 'text') for name in self.nb.tabs()]
        tabindexes = [self.nb.index(name) for name in self.nb.tabs()]
        for name, index in zip(tabnames, tabindexes):
            self.windowsmenu.add_radiobutton(label=name,
                                             command=lambda i=index: self._select_window(i))

    def _select_window(self, index):
        # print 'Windows menu %s' % (index,)
        self.nb.select(index)


def main():
    root = tk.Tk()
    app = Application(root)
    app.master.title(u'Main super window')
    app.mainloop()


if __name__ == '__main__':
    main()
