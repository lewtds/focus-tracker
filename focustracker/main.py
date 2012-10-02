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
        logging.debug("Opening database")
        self.__conn = sqlite3.connect('focus_log.db')
        self.__c = self.__conn.cursor()
        
        self.__c.executescript("""
            CREATE TABLE IF NOT EXISTS Applications (name text primary key);
            
            CREATE TABLE IF NOT EXISTS Logs (
                app_name text not null,
                stamp timestamp,
                elapsed datetime,
                constraint PK_Logs_time primary key (stamp),
                constraint FK_Application_name foreign key (app_name) references Applications (name)
            );
            """)
        
    def close(self):
        logging.debug("Closing database")
        self.__c.close()
    
    def add_entry(self, app_name, elapsed):
        self.__c.execute("INSERT INTO Logs(stamp, app_name, elapsed) VALUES (strftime('%Y-%m-%d %H:%M:%f', 'now'), ?, ?)", (app_name, elapsed))
        self.__conn.commit()

class View:
    """
    Class này hiển thị thông tin ra ngoài. Có thể là một Gtk.Window.
    """
    def __init__(self, model):
        self.__model = model
        window = Gtk.Window()
        window.connect("destroy", on_quit, self.__model)
        window.show()

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
        self.__model.add_entry(self.__current_window.get_application().get_name(), elapsed)
        self.__current_window = self.__screen.get_active_window()
        self.__start = time.time()

def on_quit(widget, model):
    model.close()
    logging.info("Quitting")
    Gtk.main_quit()

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Application started")
    
    # Handle Ctrl-C
    #signal.signal(signal.SIG, signal.SIG_DFL)

    model = Model()
    controller = Controller(model)
    view = View(model)
    
    Gtk.main()

if __name__ == "__main__":
    main()
