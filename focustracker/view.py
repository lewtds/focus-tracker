# -*- coding: utf-8 -*-
import logging
from gi.repository import Gtk

class View:
    """
    Class này hiển thị thông tin ra ngoài. Có thể là một Gtk.Window.
    """
    def __init__(self, model):
        self.__model = model
        window = Gtk.Window()
        #window.connect("destroy", on_quit, self.__model)
        #window.show()
