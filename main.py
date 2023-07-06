import psycopg2

def create_db(cur1):
         cur1.execute("""           
                      DROP TABLE Un CASCADE;
                      DROP TABLE Number CASCADE;
                      """)
  
         cur1.execute (""" 
                      CREATE TABLE IF NOT EXISTS Un (
                          ID SERIAL PRIMARY KEY,
                          Name VARCHAR (30) NOT NULL,
                          surname VARCHAR (40) NOT NULL,
                          email VARCHAR (40) UNIQUE NOT NULL);
                          
                          CREATE TABLE IF NOT EXISTS Number (
                          numberID SERIAL PRIMARY KEY,
                          number VARCHAR,
                          clientID INTEGER NOT NULL REFERENCES Un(ID));
                          """)
           
         return print('1.База данных создана!')
          
def add_client(cur1, Name_in, Surname_in, Email_in):
       cur1.execute ("""
                      INSERT INTO Un(Name, surname, email) 
                      VALUES (%s, %s, %s)
                      RETURNING ID, Name, surname, email;
                      """, (Name_in, Surname_in, Email_in))
       ID = cur1.fetchall()
       return print('2.Клиент добавлен', ID)
      

def add_phone(cur1, client_in, phone_in):
           cur1.execute ("""
                        INSERT INTO Number(number, clientID)
                        VALUES (%s, %s)
                        RETURNING number, clientID;
                        """, (phone_in, client_in)) 
           ID = cur1.fetchall()
           
           cur1.execute ("""
                        UPDATE Number
                        SET clientID = %s WHERE number =%s
                        RETURNING numberID, number, clientID;
                        """, (client_in, phone_in)) 
           ID = cur1.fetchall()
           return print('3.Телефон добавлен', ID)
          
    
def change_client(cur1, client_in, Name_in, Surname_in, Email_in, Number_in):
        
        client = input ('Какие данные клиента Вы бы хотели изменить:')
        if client == 'имя' or client_in == 'Имя':
                cur1.execute("""
                        UPDATE Un
                        SET Name = %s WHERE ID = %s
                        RETURNING ID, Name, surname, email;
                        """, (Name_in, client_in))
                ID = cur1.fetchall()
                return print('4.Данные клиента изменены', ID)
                   
        elif client == 'фамилия' or client_in == 'Фамилия':
            cur1.execute("""
                        UPDATE Un
                        SET surname = %s WHERE ID = %s
                        RETURNING ID, Name, surname, email;
                        """, (Surname_in, client_in))
            ID = cur1.fetchall()
            return print('4.Данные клиента изменены', ID)    
            
        elif client == 'email' or client_in == 'Email':
                cur1.execute("""
                        UPDATE Un
                        SET email = %s WHERE ID = %s
                        RETURNING ID, Name, surname, email;
                        """, (Email_in, client_in))
                ID = cur1.fetchall()
                return print('4.Данные клиента изменены', ID)
        
        
        elif client == 'телефон' or client_in == 'Телефон':        
                 cur1.execute("""
                        UPDATE Number
                        SET number = %s WHERE clientID = %s
                        RETURNING numberID, number, clientID;
                        """, (Number_in, client_in))
                 ID = cur1.fetchall()
                 return print('4.Данные клиента изменены', ID)
                        
def delete_phone(cur1, client_in, phone_in):
        
        cur1.execute ("""   
                     DELETE FROM Number
                     WHERE clientID = %s AND number = %s
                     RETURNING numberID, number, clientID; 
                     """, (client_in, phone_in))
        ID = cur1.fetchall()
        return print('5.Телефон удален', cur1.fetchall())

def find_client(cur1, Name_in, Surname_in, Email_in, Number_in):
        cur1.execute ("""   
                     SELECT clientID, Name, surname, email, number FROM Number
                     FULL JOIN UN ON Number.clientID = Un.ID
                     WHERE Name = %s AND surname = %s AND email = %s AND number = %s;
                     """, (Name_in, Surname_in, Email_in, Number_in))
        iD = cur1.fetchall()
        return print ('7.Данные клиента:', iD)

def delete_client(cur1, client_in):
        
         cur1.execute ("""   
                     DELETE FROM Un
                     WHERE ID = %s
                     RETURNING ID, Name, surname, email; 
                     """, (client_in,))
         ID1 = cur1.fetchall()
        
         cur1.execute  ("""   
                     DELETE FROM Number
                     WHERE clientID = %s
                     RETURNING numberID, number, clientID;; 
                     """, (client_in,))
         ID1 = cur1.fetchall()
         return print('6.Клиент удален', cur1.fetchall())
    
with psycopg2.connect(database="clients", user="postgres", password="1025") as conn:
  with conn.cursor() as cur:
    print(create_db(cur))
    print(add_client(cur, 'first_name', 'last_name', 'email'))
    print(add_phone(cur, 1, 'phone'))
    print(change_client(cur, 1,'first_name2', 'last_name2', 'email2','phone2'))
    print(find_client(cur,'first_name', 'last_name', 'email','phone'))
    print(delete_phone(cur, 1, 'phone2'))
    print(delete_client(cur, 1))
