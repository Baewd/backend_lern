import psycopg2
from psycopg2 import OperationalError, sql


class MyDbUs:
    def __init__(self, db_name, db_pass):
        self.db_host = "localhost"
        self.db_user = "postgres"
        self.db_port = 5432
        self.db_name = db_name
        self.db_pass = db_pass
        

    # создаём экземпляр класса psycopg2
    def create_connection(self): 
        connection = None
        try:
            
            connection = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_pass,
                host=self.db_host,
                port=self.db_port,
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        return connection
    

    # утилита для создания sql забросов
    def work_wis_bash(self, db_query, params = None, show = False):

        connection = self.create_connection()  #подключаемся к бд
        connection.autocommit = True

        cursor = connection.cursor()    #создаём курсор
        try:                                    #трай для обращения к бд
            if params:
                cursor.execute(db_query, params)    #вариант с параметрами в образении
            else:
                cursor.execute(db_query)            #вариант без параметров в образении
            if show:                                #нужно ли отображать ответ
                results = cursor.fetchall()
                for row in results:                 #перебор масива с ответом
                    print(row)
            print("Query executed successfully")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

        cursor.close()  # Закрываем курсор
        connection.close() #отключаемся от бд
    

    def vue_db(self):

        db_query = "SELECT * FROM users"
        self.work_wis_bash(db_query, show=True)
        

    def create_user(self, user_id, user_name, user_role):
        db_query = "INSERT INTO users (user_id, name, role) VALUES (%s, %s, %s)"
        params = (user_id, user_name,user_role)
        self.work_wis_bash(db_query, params = params)


        db_query = "SELECT * FROM users WHERE user_id = %s"
        self.work_wis_bash(db_query, user_id, True )

        # create_database_query = "CREATE DATABASE sm_app"
        # create_database(connection, create_database_query)