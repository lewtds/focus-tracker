# -*- coding: utf-8 -*-
import sqlite3
import logging

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
        self.__c.execute("""
            INSERT INTO Logs(stamp, app_name, elapsed) 
                VALUES (strftime('%Y-%m-%d %H:%M:%f', 'now'), ?, ?)
            """, (app_name, elapsed))
        self.__conn.commit()

    def get_app_total(self, app_name):
        t = (app_name, )
        self.__c.execute(
            'SELECT SUM(elapsed) FROM Logs WHERE app_name=?',
            t)
        return self.__c.fetchone()[0]
        
    def get_apps(self):
        self.__c.execute('SELECT DISTINCT app_name FROM Logs')
        l = self.__c.fetchall()  # Note: This returns a list of tuples
        return [a[0] for a in l] # So we have to use a list comprehension to simplify it like this
