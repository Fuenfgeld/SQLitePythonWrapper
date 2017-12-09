#/usr/local/bin/python
# Python programm für KDM Aufgabe 3/2
import csv
import sqlite3
import re

class dbVersandhaus:

    def __init__(self,inFileName, inDbName):
        self.conn = sqlite3.connect(":memory:")        
        self.c = self.conn.cursor()
        self.fileName = inFileName
        self.dbName = inDbName
        self.loadCSV()

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

    def loadCSV(self):
        with open(self.fileName, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            self.createDBShema(header)
            for row in reader:
                self.addNewEntryToDB(row)
                
    def createDBShema(self, header):        
        createStatement = "CREATE TABLE "
        createStatement += self.dbName + " ("

        for item in header:
            createStatement += item + " text," 

        createStatement = createStatement[0:len(createStatement)-1]
        createStatement += ")"
        
        self.c.execute(createStatement)
        self.conn.commit()
                     

    def addNewEntryToDB(self, newRow):
         #self.c.execute('''INSERT INTO versandhaus VALUES (?,?,?,?,?)''', rowCSV)
        insertStatement = "INSERT INTO " + self.dbName + " VALUES (" + (len(newRow)*"?,") 
        insertStatement = insertStatement[0:len(insertStatement)-1] + ")"
         
        self.c.execute(insertStatement, newRow)
        self.conn.commit()

if __name__ == '__main__':
    db = dbVersandhaus("weather.nominal.csv", "weather")
    #db.SQL('SELECT * FROM versandhaus')
    #print(db.isSELECT('select'))
    print(db.SQL('SELECT * FROM weather'))
