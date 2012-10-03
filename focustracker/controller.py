#  controller.py
#  
#  Copyright 2012 Trung Ngo <ndtrung4419@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# -*- coding: utf-8 -*-

from gi.repository import Wnck
from gi.repository import Gtk

import time
import logging

using_appindicator = True
try: from gi.repository import AppIndicator3 as Indicator
except ImportError:
    using_appindicator = False

class Controller:
    """
    The Controller class. Interfaces with Wnck and catches its events. Calculates
    apps' elapsed time and writes into the database (the model).
    """
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__screen = Wnck.Screen.get_default()
        self.__screen.connect("active-window-changed", self.__on_active_window_changed)
        self.__create_tray_icon()
        
    def __on_active_window_changed(self, screen, previous):
        """active-window-changed signal handler. Calculates the last
        focused window's elapsed time and writes that into the database.
        """
        logging.debug("Active window changed")
        if previous == None:
            logging.debug("previous == None")
            self.__start = time.time()
            self.__current_window = self.__screen.get_active_window()
            logging.debug("Current window: %s" % self.__current_window.get_application().get_name())
            return
        
        if self.__current_window.get_application() != None:
            elapsed = time.time() - self.__start
            name = self.__current_window.get_application().get_name()
            logging.debug("Prev window: %s - %d second(s)" % (name, elapsed))
            self.__model.add_entry(name, elapsed)
        else:
            logging.debug("self.__current_window.get_application() == None")
            
        self.__current_window = self.__screen.get_active_window()
        self.__start = time.time()
        self.__view.refresh()

    def __create_tray_icon(self):
        """Creates a tray icon using AppIndicator or Gtk.StatusIcon depending
        on the current environment.
        """
        menu = Gtk.Menu()
        
        toggle_item = Gtk.MenuItem("Toggle")
        toggle_item.connect("activate", self.__view.toggle)
        toggle_item.show()
        menu.append(toggle_item)
        
        quit_item = Gtk.MenuItem("Quit")
        quit_item.connect("activate", self.__on_quit)
        quit_item.show()
        menu.append(quit_item)
        
        logging.info("using_appindicator = " + str(using_appindicator))
        # TODO Add the Gtk.StatusIcon case
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
        """Does various cleaning necessary before quitting
        """
        self.__on_active_window_changed(self.__screen, self.__current_window)
        self.__model.close()
        logging.info("Quitting")
        Gtk.main_quit()
