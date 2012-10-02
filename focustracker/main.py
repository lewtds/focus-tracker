# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import Wnck

import logging
import signal # for Ctrl-C
import sqlite3
import time

class Model:
    """
    Class này quản lý dữ liệu. Ghi lại tất cả mọi thứ vào database và cung
    cấp một giao diện đơn giản đến database đấy luôn.
    """
    def __init__(self):
        pass
    
    def add_time(self, app_name, elapsed):
        pass

class View:
    """
    Class này hiển thị thông tin ra ngoài. Có thể là một Gtk.Window.
    """
    def __init__(self, model):
        self.__model = model

class Controller:
    # TODO Đưa nó ra thành một thread riêng
    """
    Class này lo việc thu gom thông tin. Giao tiếp và bắt các event của Wnck.
    """
    def __init__(self, model):
        self.__model = model
        self.__screen = Wnck.Screen.get_default()
        self.__screen.connect("active-window-changed", self.__on_active_window_changed)
    
    def __on_active_window_changed(self, screen, previous):
        if previous == None:
            self.__start = time.time()
            self.__current_window = self.__screen.get_active_window()
            return

        elapsed = time.time() - self.__start
        logging.debug("%s - %d" % (self.__current_window.get_application().get_name(), elapsed))
        self.__model.add_time(self.__current_window.get_application().get_name(), elapsed)
        self.__current_window = self.__screen.get_active_window()
        self.__start = time.time()

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
