from pprint import pprint

import psycopg2

def create_db(conn1):
      with conn1.cursor() as cur:
         cur.execute("""
         DROP TABLE name CASCADE;
         DROP TABLE surname CASCADE;
         DROP TABLE email CASCADE;
         DROP TABLE Number CASCADE;
         DROP TABLE Un;
         """)
  
      with conn1.cursor() as cur:
          cur.execute ("""
                      CREATE TABLE IF NOT EXISTS name (
                          nameID SERIAL PRIMARY KEY,
                          Name VARCHAR (30) NOT NULL);
                          
                      CREATE TABLE IF NOT EXISTS surname (
                          surnameID SERIAL PRIMARY KEY,
                          surname VARCHAR (40) NOT NULL);   
                          
                      CREATE TABLE IF NOT EXISTS email (
                          emailID SERIAL PRIMARY KEY,
                          email VARCHAR (40) UNIQUE NOT NULL);   
                          
                      CREATE TABLE IF NOT EXISTS Number (
                          numberID SERIAL PRIMARY KEY,
                          number VARCHAR);
                          
                      CREATE TABLE IF NOT EXISTS Un (
                          ID SERIAL PRIMARY KEY,
                          NameU INTEGER REFERENCES name(nameID),
                          SurnameU INTEGER REFERENCES  surname(surnameID),
                          emailU INTEGER REFERENCES email(emailID),
                          numberU INTEGER REFERENCES Number(numberID));
                          """)
          conn1.commit()
          
      return print('База данных создана!')
          
def add_client(conn1):
  Number_in = 0
  Name_in = input('Введите имя клиента:')
  Surname_in = input('Введите фамилию клиента:')
  Email_in = input('Введите Email клиента:')
  Number_in = input('Введите номер телефона клиента:')
  print(Number_in)
  if Number_in == '':
     Number_in = 0
     with conn1.cursor() as cur:
       cur.execute ("""
                      INSERT INTO name(Name) 
                      VALUES (%s)
                      RETURNING nameID;
                      """, (Name_in,))
       name_ID = cur.fetchone()[0]
       conn1.commit()
       
     with conn1.cursor() as cur:
        cur.execute ("""
                      INSERT INTO surname(surname) VALUES 
                      (%s)
                      RETURNING surnameID;
                      """, (Surname_in,))
        surname_ID = cur.fetchone()[0]
        conn1.commit()
        
     with conn1.cursor() as cur:
        cur.execute ("""
                      INSERT INTO email(email) VALUES 
                      (%s)
                      RETURNING emailID,email;
                      """, (Email_in,))
        email_ID = cur.fetchone()[0]
        conn1.commit()
        
     with conn1.cursor() as cur:
        cur.execute ("""
                      INSERT INTO Number(number) VALUES 
                      (%s)
                      RETURNING numberID,number;
                      """, (Number_in,))
        Number_ID = cur.fetchone()[0]
        conn1.commit()
        
     with conn1.cursor() as cur:
        cur.execute ("""   
                      INSERT INTO Un(NameU, SurnameU, emailU, numberU) 
                      VALUES (%s, %s, %s, %s)
                      RETURNING ID, NameU, SurnameU, emailU, numberU; 
                       """, (name_ID, surname_ID, email_ID, Number_ID))
        return print('Клиент добавлен')
        
        
  else:
    with conn1.cursor() as cur:
       cur.execute ("""
                      INSERT INTO name(Name) 
                      VALUES (%s)
                      RETURNING nameID;
                      """, (Name_in,))
       name_ID = cur.fetchone()[0]
       conn1.commit()
     
    with conn1.cursor() as cur:
        cur.execute ("""
                      INSERT INTO surname(surname) VALUES 
                      (%s)
                      RETURNING surnameID;
                      """, (Surname_in,))
        surname_ID = cur.fetchone()[0]
        conn1.commit()
        
    with conn1.cursor() as cur:
        cur.execute ("""
                      INSERT INTO email(email) VALUES 
                      (%s)
                      RETURNING emailID,email;
                      """, (Email_in,))
        email_ID = cur.fetchone()[0]
        conn1.commit()
        
    with conn1.cursor() as cur:
        cur.execute ("""
                      INSERT INTO Number(number) VALUES 
                      (%s)
                      RETURNING numberID,number;
                      """, (Number_in,))
        Number_ID = cur.fetchone()[0]
        conn1.commit()
        
    with conn1.cursor() as cur:
        cur.execute ("""   
                      INSERT INTO Un(NameU, SurnameU, emailU, numberU) 
                      VALUES (%s, %s, %s, %s)
                      RETURNING ID, NameU, SurnameU, emailU, numberU; 
                       """, (name_ID, surname_ID, email_ID, Number_ID))
        return print('Клиент добавлен')
      

def add_phone(conn1):
      with conn1.cursor() as cur:
        cur.execute ("""   
                     SELECT ID, Name, surname, email, number FROM Un
                     FULL JOIN name ON Un.NameU = name.nameID
                     FULL JOIN surname ON Un.SurnameU = surname.surnameID
                     FULL JOIN email ON Un.emailU = email.emailID
                     FULL JOIN Number ON Un.numberU = Number.numberID;
                       """)
        List_clients = cur.fetchall()
        pprint(List_clients)
        client = int(input ('Введите номер интересующего Вас клиента'))
        number_client = input ('Введите номер телефона клиента:')
        with conn1.cursor() as cur:
           cur.execute ("""
                        UPDATE Number 
                        SET number = %s WHERE numberID = %s;
                        """, (number_client, client)) 
           conn1.commit()
        with conn1.cursor() as cur:
          cur.execute ("""
                      SELECT * FROM Number;
                      """)
          return print('Данные обновлены')   
      
def change_client(conn1):
       with conn1.cursor() as cur:
        cur.execute ("""   
                     SELECT ID, Name, surname, email, number FROM Un
                     FULL JOIN name ON Un.NameU = name.nameID
                     FULL JOIN surname ON Un.SurnameU = surname.surnameID
                     FULL JOIN email ON Un.emailU = email.emailID
                     FULL JOIN Number ON Un.numberU = Number.numberID;
                       """)
        List_clients = cur.fetchall()
        pprint(List_clients) 
        client = int(input ('Введите номер интересующего Вас клиента'))
        client_in = input ('Какие данные клиента Вы бы хотели изменить:')
        if client_in == 'имя' or client_in == 'Имя':
            number_client = input ('Введите обновленные данные:')
            with conn1.cursor() as cur:
              cur.execute ("""
                            UPDATE name 
                            SET Name = %s WHERE nameID = %s;
                            """, (number_client, client)) 
              conn1.commit()
            with conn1.cursor() as cur:
              cur.execute ("""
                          SELECT * FROM name;
                          """)
              return print('Данные обновлены') 
            
        elif client_in == 'фамилия' or client_in == 'Фамилия':
            number_client = input ('Введите обновленные данные:')
            with conn1.cursor() as cur:
              cur.execute ("""
                            UPDATE surname
                            SET surname = %s WHERE surnameID = %s;
                            """, (number_client, client)) 
              conn1.commit()
            with conn1.cursor() as cur:
              cur.execute ("""
                          SELECT * FROM surname;
                          """)
              return print('Данные обновлены') 
            
        elif client_in == 'email' or client_in == 'Email':
            number_client = input ('Введите обновленные данные:')
            with conn1.cursor() as cur:
              cur.execute ("""
                            UPDATE email
                            SET email = %s WHERE emailID = %s;
                            """, (number_client, client)) 
              conn1.commit()
            with conn1.cursor() as cur:
              cur.execute ("""
                          SELECT * FROM email;
                          """)
              return print('Данные обновлены')
        else: 
          return print('Данный параметр не создан')
                        
def delete_phone(conn1):
      with conn1.cursor() as cur:
        cur.execute ("""   
                     SELECT ID, Name, surname, email, number FROM Un
                     FULL JOIN name ON Un.NameU = name.nameID
                     FULL JOIN surname ON Un.SurnameU = surname.surnameID
                     FULL JOIN email ON Un.emailU = email.emailID
                     FULL JOIN Number ON Un.numberU = Number.numberID;
                       """)
        List_clients = cur.fetchall()
        pprint(List_clients)
        client = int(input ('Введите номер интересующего Вас клиента'))
        client_in = input ('Вы уверены что хотите удалить номер клиента?')
        if client_in == 'Да' or client_in == 'да':
           new_number = ''
           with conn1.cursor() as cur:
              cur.execute ("""
                            UPDATE Number 
                            SET number = %s WHERE numberID = %s;
                            """, (new_number, client)) 
              conn1.commit()
              return print ('Данные обновлены') 
        
        
        

def delete_client(conn1):
    with conn1.cursor() as cur:
        cur.execute ("""   
                     SELECT ID, Name, surname, email, number FROM Un
                     FULL JOIN name ON Un.NameU = name.nameID
                     FULL JOIN surname ON Un.SurnameU = surname.surnameID
                     FULL JOIN email ON Un.emailU = email.emailID
                     FULL JOIN Number ON Un.numberU = Number.numberID;
                       """)
        List_clients = cur.fetchall()
        pprint(List_clients)  
        client = input ('Введите номер интересующего Вас клиента')
        with conn1.cursor() as cur:
              cur.execute ("""
                           DELETE FROM Un
                            WHERE ID = %s;
                           """, (client))
              conn1.commit()
              
        with conn1.cursor() as cur:
              cur.execute ("""   
                            DELETE FROM name
                            WHERE nameID = %s;
                            """, (client))
              conn1.commit()
             
        with conn1.cursor() as cur:
              cur.execute ("""   
                            DELETE FROM surname
                            WHERE surnameID = %s;
                            """, (client))
              conn1.commit()
              
        with conn1.cursor() as cur:
              cur.execute ("""   
                            DELETE FROM email
                            WHERE emailID = %s;
                            """, (client))
              conn1.commit()
               
        with conn1.cursor() as cur:
              cur.execute ("""   
                            DELETE FROM Number
                            WHERE numberID = %s;
                            """, (client))
              conn1.commit()                 
              return print ('Данные обновлены')

def find_client(conn1):
      find_email = input ('Введите email Вашего клиента:')
      with conn1.cursor() as cur:
        cur.execute ("""   
                     SELECT ID, Name, surname, email, number FROM Un
                     FULL JOIN name ON Un.NameU = name.nameID
                     FULL JOIN surname ON Un.SurnameU = surname.surnameID
                     FULL JOIN email ON Un.emailU = email.emailID
                     FULL JOIN Number ON Un.numberU = Number.numberID
                     WHERE email = %s;
                    """, (find_email,))
        all_tables = cur.fetchall()
        print ('Данные клиента:', all_tables)
  
def main(comand):
  print('____________________________')
  print('1-Функция, создающая структуру БД (таблицы),2-Функция, позволяющая добавить нового клиента,')
  print('3-Функция, позволяющая добавить телефон для существующего клиента,4-Функция, позволяющая изменить данные о клиенте,')
  print('5-Функция, позволяющая удалить телефон для существующего клиента.,6-Функция, позволяющая удалить существующего клиента.')
  print('7-Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону')
  print('____________________________') 

  conn = psycopg2.connect(database="clients", user="postgres", password="1025") 

  while True:
     
    comand = input('Введите команду:')
    
    if comand == '1':
      print (create_db(conn))
      
    elif comand == '2':
      print (add_client(conn))   
        
    elif comand == '3':
     print(add_phone(conn))
       
    elif comand == '4':
      print(change_client(conn))
    
    elif comand == '5':
      print(delete_phone(conn))
      
    elif comand == '6':
      print(delete_client(conn))
      
    elif comand == '7':
      print(find_client(conn))
    
    elif comand =='`':
      print('выход')
      conn.close()
      return    

comand1 = 1
   
print(main(comand1))