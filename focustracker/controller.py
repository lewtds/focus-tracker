# -*- coding: utf-8 -*-

from gi.repository import Wnck
from gi.repository import Gtk

import time
import logging

using_appindicator = True
try: from gi.repository import AppIndicator3 as Indicator
except:
    using_appindicator = False

class Controller:
    """
    Class này lo việc thu gom thông tin. Giao tiếp và bắt các event của Wnck.
    """
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__screen = Wnck.Screen.get_default()
        self.__screen.connect("active-window-changed", self.__on_active_window_changed)
        self.__create_tray_icon()
        
    def __on_active_window_changed(self, screen, previous):
        logging.debug("Active window changed")
        if previous == None:
            logging.debug("previous == None")
            self.__start = time.time()
            self.__current_window = self.__screen.get_active_window()
            return

        elapsed = time.time() - self.__start
        logging.debug("Prev window: %s - %d" % 
            (self.__current_window.get_application().get_name(), elapsed))
        self.__model.add_entry(self.__current_window.get_application().get_name(), elapsed)
        self.__current_window = self.__screen.get_active_window()
        self.__start = time.time()

    def __create_tray_icon(self):
        menu = Gtk.Menu()
        quit_item = Gtk.MenuItem("Quit")
        quit_item.connect("activate", self.__on_quit)
        quit_item.show()
        menu.append(quit_item)
        
        logging.info("using_appindicator = " + str(using_appindicator))
        if using_appindicator:
            self.__indicator = Indicator.Indicator.new(
                "focus-tracker",
                "find",
                Indicator.IndicatorCategory.APPLICATION_STATUS
            )
            self.__indicator.set_status (Indicator.IndicatorStatus.ACTIVE)
            #self.__indicator.set_attention_icon("indicator-messages-new")
            self.__indicator.set_menu(menu)

    def __on_quit(self, widget):
        self.__on_active_window_changed(self.__screen, self.__current_window)
        self.__model.close()
        logging.info("Quitting")
        Gtk.main_quit()
