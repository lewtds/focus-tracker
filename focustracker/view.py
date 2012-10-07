#  view.py
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

import logging
from gi.repository import Gtk, WebKit
import os
import json

current_path = os.path.dirname(__file__)

class View:
    """
    The View class. Presents the user with various useful views of the database.
    """
    def __init__(self, model):
        self.__model = model
        self.__window = Gtk.Window()
        
        # Gtk.Window.hide_on_delete() should be the handler here
        # but God knows why it doesn't work
        self.__window.connect("delete-event", self.__on_delete_event)
        self.__window.resize(500, 500)
        
        self.__web_view = WebKit.WebView()
        self.__web_view.load_uri("file://" + os.path.join(current_path, "gui/index.html"))
        
        # View note on self.__message_received()
        self.__web_view.connect("notify::load-status", self.__on_load)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.__web_view)
        
        self.__window.add(scroll)
        self.__window.show_all()
        
    def __on_load(self, object, property):
        if object.get_load_status() == WebKit.LoadStatus.FINISHED:         
            self.__web_view.connect("notify::title", self.__message_received)
            self.refresh()
    
    def __message_received(self, object, property):
        """Handler for self.__web_view's "notify::title" event.
        
        This is actually a hack. There's no easy way for the WebKit GUI
        to communicate with us without setting up a whole HTTP server
        and port thingy. And also as we are not using the webpage's title
        for anything, we use it to send back messages and events.
        """
        pass
        
    def __update_list_store(self):
        pass
        
    def refresh(self):
        percentage = self.__model.get_total()
        self.__web_view.execute_script("refresh('" + 
        json.dumps({"percentage": percentage}) + "')" );

    def show(self, widget=None):
        self.__window.show_all()
    
    def hide(self, widget=None):
        self.__window.hide()
        
    def toggle(self, widget=None):
        if self.__window.get_visible():
            self.hide()
        else:
            self.show()

    def __on_delete_event(self, widget=None, event=None):
        """Main window's delete-event handler. Prevents it from being destroyed.
        """
        self.hide()
        return True    # Return True to stop the delete
