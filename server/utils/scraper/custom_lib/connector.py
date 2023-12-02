import mysql.connector
import configparser
import os

class main_db_connector:
    def __init__(self, configPath=f"{os.path.dirname(os.path.realpath(__file__))}/config.ini", strict=False) -> None:
        try:
            # Open Config
            config = configparser.ConfigParser()
            config.read(configPath)

            # Get infos for Database-Connection
            self.host = config["DATABASE"]["host"]
            self.user = config["DATABASE"]["user"]
            self.password = config["DATABASE"]["password"]
            self.database = config["DATABASE"]["database"]

            self.strict = strict
            self.connection = None
            self.cursor = None
        except Exception as error:
            raise Exception("Config File Error:", error)

    def connectDB(self):
        # Establish a connection to the MariaDB database
        self.connection = mysql.connector.connect(
            host= self.host,
            user= self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
    
    def buildExecuteQuerry(self,tabbleName:str, informations: list(tuple())):
        if self.connection == None:
            if self.strict:
                raise Exception("No Database connection exists")
            else:
                self.connectDB()
            
        insert_query = f'INSERT IGNORE INTO {tabbleName} (product_ean, product_category, product_name, product_currentPrice, product_regularPrice, \
                        product_basePrice, product_baseUnit, product_vendor, product_image) VALUES '
        counter = 0
        for information in informations:
            insert_query += f'("{information[0]}", "{information[1]}", "{information[2]}", "{information[3]}", "{information[4]}", "{information[5]}", "{information[6]}", "{information[7]}", "{information[8]}")'

            # If one Article remains end querry
            if counter < len(informations) - 1:
                insert_query += ',\n'
            else:
                insert_query += ';'
            counter += 1
        self.cursor.execute(insert_query)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
        
    def commitAndClose(self):
        self.commit()
        self.close()



#! Not completed
class helper_db_connector:
    def __init__(self, configPath="config.ini", strict=False) -> None:
        try:
            # Open Config
            config = configparser.ConfigParser()
            config.read(configPath)

            # Get infos for Database-Connection
            self.host = config["DATABASE"]["host"]
            self.user = config["DATABASE"]["user"]
            self.password = config["DATABASE"]["password"]
            self.database = config["DATABASE"]["database"]

            self.strict = strict
            self.connection = None
            self.cursor = None
        except Exception as error:
            raise Exception("Config File Error:", error)

    def connectDB(self):
        # Establish a connection to the MariaDB database
        self.connection = mysql.connector.connect(
            host= self.host,
            user= self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
    
    def buildExecuteQuerry(self,tabbleName:str, informations: list(tuple())):
        if self.connection == None:
            if self.strict:
                raise Exception("No Database connection exists")
            else:
                self.connectDB()
            
        insert_query = f'INSERT IGNORE INTO {tabbleName} (product_id, product_category, product_title, product_subtitle, product_price, product_image) VALUES '
        counter = 0
        for information in informations:
            insert_query += f'("{information.get[0]}", "{information[1]}", "{information[2]}", "{information[3]}", "{information[4]}", "{information[5]}")'

            # If one Article remains end querry
            if counter < len(informations):
                insert_query += ',\n'
            else:
                insert_query += ';'
            counter += 1
        self.cursor.execute(insert_query)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
        
    def commitAndClose(self):
        self.commit()
        self.close()