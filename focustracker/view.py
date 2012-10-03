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
from gi.repository import Gtk

class View:
    """
    The View class. Presents the user with various useful views of the database.
    """
    def __init__(self, model):
        self.__model = model
        self.__window = Gtk.Window()
        self.__tree_view = Gtk.TreeView()
        self.__list_store = Gtk.ListStore(str, float)
        
        # Gtk.Window.hide_on_delete() should be the handler here
        # but God knows why it doesn't work
        self.__window.connect("delete-event", self.__on_delete_event)
        
        self.__update_list_store()
        self.__tree_view.set_model(self.__list_store)
        
        app_renderer = Gtk.CellRendererText()
        app_name_col = Gtk.TreeViewColumn("App", app_renderer, text=0)
        self.__tree_view.append_column(app_name_col)
        
        elapsed_renderer = Gtk.CellRendererText()
        elapsed_col = Gtk.TreeViewColumn("Elapsed", elapsed_renderer, text=1)
        self.__tree_view.append_column(elapsed_col)
        
        self.__window.add(self.__tree_view)
        self.__window.show_all()
        
    def __update_list_store(self):
        # TODO Only update the rows that need updating
        self.__list_store.clear()
        apps = self.__model.get_apps()
        elapsed = []
        for app in apps:
            self.__list_store.append((app, self.__model.get_app_total(app)))
        
    def refresh(self):
        self.__update_list_store()

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
        # Return True to stop the delete
        return True
