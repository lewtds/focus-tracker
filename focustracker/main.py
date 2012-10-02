# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import Wnck

import logging
import signal # for Ctrl-C
import sqlite3

class Model:
    """
    Class này quản lý dữ liệu. Ghi lại tất cả mọi thứ vào database và cung
    cấp một giao diện đơn giản đến database đấy luôn.
    """
    def __init__(self):
        pass

class View:
    """
    Class này hiển thị thông tin ra ngoài. Có thể là một Gtk.Window.
    """
    def __init__(self, model):
        self.__model = model

class Controller:
    """
    Class này lo việc thu gom thông tin. Giao tiếp và bắt các event của Wnck.
    """
    def __init__(self, model):
        self.__model = model
        self.__screen = Wnck.Screen.get_default()
        self.__screen.connect("active-window-changed", self.on_active_window_changed)
    
    def on_active_window_changed(self, screen, previous):
        current = self.__screen.get_active_window()
        #logging.debug("Prev: " + previous.get_name())
        logging.debug("Current: " + current.get_name())
        import pdb; pdb.set_trace()

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Application started")
    
    # Handle Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    model = Model()
    controller = Controller(model)
    view = View(model)
    
    Gtk.main()

if __name__ == "__main__":
    main()
