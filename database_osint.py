import pymysql.cursors
import logging

def db_conection():
        config = {
            'user': 'osintuser',
            'password': 'password',
            'host': 'localhost',
            'port': 3306,
            'database': 'osint',
            'charset': 'utf8mb4'          
        }
        try:
            cnx = pymysql.connect(**config)
        except pymysql.Error as err:
                logging.info("store_emails.py - ", err)
                cnx.close()
        return cnx