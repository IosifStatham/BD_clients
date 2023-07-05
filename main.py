import psycopg2

def create_db(cur1):
         cur1.execute("""
  
         DROP TABLE Number CASCADE;
         DROP TABLE Un;
         """)
  
         cur1.execute ("""
                       CREATE TABLE IF NOT EXISTS Number (
                          numberID INTEGER PRIMARY KEY,
                          number VARCHAR);
                          
                      CREATE TABLE IF NOT EXISTS Un (
                          ID SERIAL PRIMARY KEY,
                          Name VARCHAR (30) NOT NULL,
                          surname VARCHAR (40) NOT NULL,
                          email VARCHAR (40) UNIQUE NOT NULL,
                          numberU INTEGER REFERENCES Number(numberID));
                          """)
           
         return print('1.База данных создана!')
          
def add_client(cur1, Name_in, Surname_in, Email_in, Number_in):
       cur1.execute ("""
                      INSERT INTO Un(Name, surname, email, numberU) 
                      VALUES (%s, %s, %s, %s)
                      RETURNING ID, Name, surname, email, numberU;
                      """, (Name_in, Surname_in, Email_in, Number_in))
       ID = cur1.fetchall()
       return print('2.Клиент добавлен', ID)
      

def add_phone(cur1, client_in, phone_in):
           cur1.execute ("""
                        INSERT INTO Number(numberID,number)
                        VALUES (%s, %s)
                        RETURNING numberID, number;
                        """, (client_in,phone_in)) 
           ID = cur1.fetchall()
           
           cur1.execute ("""
                        UPDATE Un
                        SET numberU = %s WHERE ID = %s
                        RETURNING ID, Name, surname, email, numberU;
                        """, (client_in, client_in))
           ID = cur1.fetchall()
           return print('3.Телефон добавлен', ID)
          
    
def change_client(cur1, client_in, Name_in, Surname_in, Email_in, Number_in):
        cur1.execute ("""   
                     UPDATE Number
                     SET number = %s WHERE numberID = %s
                     RETURNING numberID, number;
                     """, (Number_in, client_in))
        ID = cur1.fetchall()
        
        cur1.execute("""
                        UPDATE Un
                        SET Name = %s, surname = %s, email = %s, numberU = %s WHERE ID = %s
                        RETURNING ID, Name, surname, email, numberU;
                        """, (Name_in, Surname_in, Email_in, client_in, client_in))
        ID = cur1.fetchall()
        return print('4.Данные клиента изменены', ID)
                        
def delete_phone(cur1, client_in, phone_in):
        cur1.execute ("""   
                    UPDATE Un
                    SET numberU = %s WHERE ID = %s
                    RETURNING ID, Name, surname, email, numberU;
                    """, (phone_in, client_in))
        ID = cur1.fetchall()
        
        cur1.execute ("""   
                     DELETE FROM Number
                     WHERE numberID = %s
                     RETURNING numberID, number; 
                     """, (client_in,))
        ID = cur1.fetchall()
        return print('5.Телефон удален', cur1.fetchall())

def find_client(cur1, Name_in, Surname_in, Email_in, Number_in):
        cur1.execute ("""   
                     SELECT ID, Name, surname, email, number FROM Un
                     FULL JOIN Number ON Un.numberU = Number.numberID
                     WHERE Name = %s OR surname = %s OR email = %s OR number = %s;
                     """, (Name_in, Surname_in, Email_in, Number_in))
        iD = cur1.fetchall()
        return print ('7.Данные клиента:', iD)

def delete_client(cur1, client_in):
        cur1.execute  ("""   
                     DELETE FROM Number
                     WHERE numberID = %s
                     RETURNING numberID, number; 
                     """, (client_in,))
        ID1 = cur1.fetchall()
        
        cur1.execute ("""   
                     DELETE FROM Un
                     WHERE ID = %s
                     RETURNING ID, Name, surname, email, numberU; 
                     """, (client_in,))
        iD = cur1.fetchall()
        return print('6.Клиент удален', cur1.fetchall())
    
with psycopg2.connect(database="clients", user="postgres", password="1025") as conn:
  with conn.cursor() as cur:
    print(create_db(cur))
    print(add_client(cur, 'first_name', 'last_name', 'email', None))
    print(add_phone(cur, 1, 'phone'))
    print(change_client(cur, 1,'first_name2', 'last_name2', 'email2','phone2'))
    print(find_client(cur,'first_name2', 'last_name2', 'email2','phone2'))
    print(delete_phone(cur, 1, None))
    print(delete_client(cur, 1))
