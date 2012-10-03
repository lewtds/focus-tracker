#  model.py
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

import sqlite3
import logging

class Model:
    """
    The Model class. A convenient wrapper around the sqlite3 database.
    """
    def __init__(self):
        logging.debug("Opening database")
        self.__conn = sqlite3.connect('focus_log.db')
        self.__c = self.__conn.cursor()
        
        self.__c.executescript("""
            CREATE TABLE IF NOT EXISTS Applications (name TEXT PRIMARY KEY);
            
            CREATE TABLE IF NOT EXISTS Logs (
                app_name TEXT NOT NULL,
                stamp TIMEPSTAMP,
                elapsed DATETIME,
                CONSTRAINT PK_Logs_time PRIMARY KEY (stamp),
                CONSTRAINT FK_Application_name FOREIGN KEY (app_name) REFERENCES Applications (name)
            );
            """)
        
    def close(self):
        """Closes the database safely
        """
        logging.debug("Closing database")
        self.__c.close()
    
    def add_entry(self, app_name, elapsed):
        """Adds an entry into the log
        """
        self.__c.execute("""
            INSERT INTO Logs(stamp, app_name, elapsed) 
                VALUES (strftime('%Y-%m-%d %H:%M:%f', 'now'), ?, ?)
            """, (app_name, elapsed))
        self.__conn.commit()

    def get_app_total(self, app_name):
        """Gets the total elapsed seconds of a given app_name
        """
        t = (app_name, )
        self.__c.execute(
            'SELECT SUM(elapsed) FROM Logs WHERE app_name=?',
            t)
        return self.__c.fetchone()[0]
        
    def get_apps(self):
        """Gets a list of all apps in the database
        """
        self.__c.execute('SELECT DISTINCT app_name FROM Logs')
        l = self.__c.fetchall()  # Note: This returns a list of tuples
        return [a[0] for a in l] # So we have to use a list comprehension to simplify it like this
