# -*- coding: utf-8 -*-
import re
import time
import logging
import pymysql.cursors
import argparse
import database_osint as db
from pyvirtualdisplay import Display
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from unidecode import unidecode
from bs4 import BeautifulSoup


def store_ld_contact(name, name2, surname, position, company):
    dab = db.db_conection()
    try:
        cursor = dab.cursor()
        insert_query = "INSERT INTO `ldcontacts` (`name`,`name2`, `surname`, `position`, `company`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, name2, surname, position, company))
        dab.commit()
        cursor.close()
        dab.close()
    except pymysql.Error as mysql_err:
        logging.info("store_ld_contact - ", mysql_err)
        dab.close()
    return


def get_unicode(string):
    s = unidecode(string)
    return s


def get_name(result):
    name = ''
    name2 = ''
    surname = ''

    nomb = result.partition("|")[0]
    lista = nomb.split(" ")
    
    if len(lista) <= 3:
        name = get_unicode(lista[0])
        surname = get_unicode(lista[1])
        
    if len(lista) > 3:
        name = get_unicode(lista[0])
        name2 = get_unicode(lista[1])
        surname = get_unicode(lista[2])

    desc = result.partition("-")[2]
    desc2 = re.sub(r"(?:LinkedInhttps?\://)\S+", "", desc)
    desc3 = re.findall(r'-(.*?)-', desc2)
    position = ''.join(desc3)
    info = [name, name2, surname, position]
    return info


def scrap(w, pro, cp):
    soup = ''
    display = Display(visible=0, size=(800, 600))
    display.start()
    firefox = FirefoxBinary('/usr/bin/firefox-esr')
    if pro:
        proxyparsed = urlparse(pro)
        miproxy = proxyparsed.hostname
        port = proxyparsed.port
        desired_capability = webdriver.DesiredCapabilities.FIREFOX
        desired_capability['proxy']={
         'proxyType': "manual",
         'httpProxy': miproxy,
         'httpProxyPort': port,
         'ftpProxy': miproxy,
         'ftpProxyPort': port,
         'sslProxy': miproxy,
         'sslProxyPort': port
         }
        webdrv = webdriver.Firefox(firefox_binary=firefox, capabilities=desired_capability)
    else:
        webdrv = webdriver.Firefox(firefox_binary=firefox)

    webdrv.implicitly_wait(30)
    webdrv.get(w)

    try:
        soup = BeautifulSoup(webdrv.page_source, 'html.parser')
    except Exception as e:
        logging.info(e)
    for enlace_etq in soup.find_all('div', attrs={'class': 'rc'}):
        enlace = enlace_etq.text
        info = get_name(enlace)
        infoname = ''.join(info[0]).encode("utf8")
        infoname2 = ''.join(info[1]).encode("utf8")
        infosurname = ''.join(info[2]).encode("utf8")
        infoposition = ''.join(info[3]).encode("utf8")
        store_ld_contact(infoname, infoname2, infosurname, infoposition, cp)
    webdrv.close()
    display.stop()


def get_results(comp, num, start, inc, pro, hl):
    query = '"' + comp + '"+site:linkedin.com/in/ OR site:linkedin.com/pub/ -intitle:profiles -inurl:"/dir"'

    while start < num:
        url = 'https://www.google.com/search?num=' + str(num) + '&hl=' + hl + '&start=' + str(start) + '&q=' + query
        scrap(url, pro, comp)
        time.sleep(10)
        start += inc


def main(args):
    
    company = args.company
    number = args.number
    start = args.start
    incr = args.incr
    proxy = args.proxy
    lang = args.lang
    logging.basicConfig(level=logging.DEBUG, filename="/var/log/getlkdcontacts.log", filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")
                            
    get_results(company, number, start, incr, proxy, lang)
    
    
if __name__ == '__main__':


    intro = '''
        
    Examples of use:
      getlkdcontacts.py 'Cisco' 
      
      getlkdcontacts.py 'Cisco' -n 10 -s 0 -i 10 -la en -p http://127.0.0.1:8080
                        
      getlkdcontacts.py 'Cisco' -n 400 -s 0 -i 100  
    '''
                                    
    par = argparse.ArgumentParser(description='@networkseg1 - v1.0.0 - Find contacts at a company',
                                      epilog=intro, formatter_class=argparse.RawTextHelpFormatter )
    par.add_argument('company', help='My company')
    par.add_argument('-n', '--number', type=int, help='nº google results, default=10', default=10)
    par.add_argument('-s', '--start', type=int, help='start in result default=0', default=0)
    par.add_argument('-i', '--incr',  type=int, choices=range(10,101), help='scrap step by step. max 100, default=10', default=10)
    par.add_argument('-la', '--lang', help='language, default=es', default='es')
    par.add_argument('-p', '--proxy', help='i.e.: http://127.0.0.1:8080')
    argus = par.parse_args()
    main(argus)
    
