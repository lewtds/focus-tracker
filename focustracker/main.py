# -*- coding: utf-8 -*-

from gi.repository import Gtk

import logging
import signal # for Ctrl-C
    
from . import model
from . import view
from . import controller

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Application started")
    
    # Handle Ctrl-C
    #signal.signal(signal.SIG, signal.SIG_DFL)

    _model = model.Model()
    _view = view.View(_model)
    _controller = controller.Controller(_model, _view)
    
    Gtk.main()

if __name__ == "__main__":
    main()
