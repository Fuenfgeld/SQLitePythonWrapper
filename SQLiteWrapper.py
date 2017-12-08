#/usr/local/bin/python
# Python programm für KDM Aufgabe 3/2
import csv
import sqlite3
import re

class dbVersandhaus:

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        
        self.c = self.conn.cursor()
        self.c.execute('''
        CREATE TABLE versandhaus
                     (Kunde text,
                     Textilien text, 
                     Geschenkartikel text,
                     Durchschnittspreis text, 
                     Klasse text)''')
        
        self.conn.commit()
        
        with open('Versandhaus.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for rowCSV in reader:
                self.c.execute('''INSERT INTO versandhaus VALUES (?,?,?,?,?)''', rowCSV)
                
        self.conn.commit()

    def SQL(self,inString):
        try:
            if self.isSELECT(inString):
                self.executeSELECT(inString)    
            else:
                self.executeSQL(inString) 
        except Exception as ex:
            print("Incorrect SQL statement")
            print(ex)

    def isSELECT(self,inString):
        if re.search('select',inString, re.IGNORECASE):
            return True
        else:
            return False

    def executeSQL(self,sqlStatement): 
        self.c.execute(sqlStatement)
        self.conn.commit()

    def executeSELECT(self, selectStatement):   
        # like 'SELECT * FROM versandhaus'
        for row in self.c.execute(selectStatement):
                print(row)
        
        #conn.close()

if __name__ == '__main__':
    db = dbVersandhaus()
    #db.SQL('SELECT * FROM versandhaus')
    print(db.isSELECT('select'))