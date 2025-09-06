import sqlite3,pygame, sys, random
from tkinter import *

with sqlite3.connect("Dynamic Labyrinth.db") as connection:
    cursor=connection.cursor()



class Manager:
        gameState= "not playing"
        gameSelected=None
        gameSelectedInfo=None
        gameID=None
        accountOpen=None
       
        @classmethod
        def display_menu(cls):
       
    
        

      
                window=Tk()
                Manager.window=window
                window.geometry("500x500")
                window.configure(bg='#4169E1')
                window.title("Login Screen")
                usernameLabel=Label(text= "Username", bg='#4169E1', fg='#FFFFFF')
                passwordLabel=Label(text= "Password", bg='#4169E1', fg='#FFFFFF')
                username_box=Entry(window)
                username_box["justify"]= "center"
                password_box=Entry(window, show='*')
                password_box["justify"]= "center"
                
                
                
                

                login_button=Button(text= "Login", bg='#00CED1', fg='#FFFFFF', command=lambda: login(username_box.get(), password_box.get()))
                                    
                register_button=Button(text= "sign up", bg='#00CED1', fg='#FFFFFF', command=lambda: sign_up(username_box.get(), password_box.get()))
                

                usernameLabel.place(x=150, y=50)
                username_box.place(x=150, y=100)

                passwordLabel.place(x=150, y=150)
                password_box.place(x=150, y=200)

                
                

                login_button.place(x=300, y=250)
                register_button.place(x=80, y=250)

                window.mainloop()
       

        @classmethod
        def resetState(cls,state, game, levelInfo):
                cls.gameState = state
                cls.gameSelected=game
               
                cls.gameSelectedInfo=levelInfo[game]
                
              
                
                if game != "New Game":
                        cls.gameID=cls.gameSelectedInfo[0]
                        cls.gameSelectedInfo=cls.gameSelectedInfo[1:]
                
                
                
                
                cls.window.destroy() # closes login window
                

        @classmethod
        def logOff(cls, score,levelStartScore, level, maze_size, condition,gameLost=False):
                
                
                if cls.gameSelected != "New Game" and gameLost: #deletes saved game is lost
                       
                        
                        cursor.execute("DELETE FROM savedGames WHERE gameID=:gameID", {"gameID": cls.gameID})
                        connection.commit()

                if cls.gameSelected != "New Game" and not gameLost and condition: #deletes saved game if a new game is saved after making progress with a saved game
                        cursor.execute("DELETE FROM savedGames WHERE gameID=:gameID", {"gameID":cls.gameID})
                        connection.commit()
                        
                updateDB(score,levelStartScore, level, maze_size, condition)
                cls.gameState= "not playing"
                cls.gameSelected=None
                cls.accountOpen=None

        @classmethod
        def getTop10(cls):
                leaderboard=cursor.execute("SELECT username, bestScore  FROM accounts ").fetchall()
                mergeSort(leaderboard)
              
                leaderboard=leaderboard[:10]
              

                return leaderboard

                
                

        
                
                
def mergeSort(leaderboard):
        
        if len(leaderboard)>1:
                #splits array recursively
                left=leaderboard[:len(leaderboard)//2]
                right=leaderboard[len(leaderboard)//2:]

                mergeSort(left)
                mergeSort(right)

                #merge
                i=0 # left array index
                j=0 # right array index
                m=0 # sorted array index
                
                while i<len(left) and j<len(right):
                        
                        
                        if left[i][1] > right[j][1]:
                                leaderboard[m]=left[i]
                                
                                i+=1
                                m+=1
                        else:
                                leaderboard[m]=right[j]
                                j+=1
                                m+=1
                        

             
               
                
                while i<len(left):
                        leaderboard[m]=left[i]
                        i+=1
                        m+=1
                        
                while j<len(right):
                        leaderboard[m]=right[j]
                        j+=1
                        m+=1
                

def encrypt(password):
        key=""
        for i in range(len(password)):
                key+=chr(random.randint(0,127))
                
        cipher=""

        for i in range(len(password)):
                
                cipher+= chr(ord(key[i]) ^ ord(password[i]))
        return cipher + key

def decrypt(cipher):
        password, key = cipher[:len(cipher)//2], cipher[len(cipher)//2:]

        plainText=""
        for i in range(len(password)):
                
                plainText += chr(ord(password[i]) ^ ord(key[i]))
                
        
        # creates a new key (one-time pad)
        cipher= encrypt(plainText)
        
        return plainText, cipher
                
        
    
def login(username, password):
        
        data=getGames(username, password)
        
        
        if data != "Incorrect username or password":
            levels=["New Game"]
            levelInfo={"New Game":(1,10,0)} #(level, maze_size, score)
           
            
            for level in data:
               
                
              option=f"Game {level[0]} level {level[1]} Points: {level[3]}"
              levels.append(option)
              
              levelInfo[f"Game {level[0]} level {level[1]} Points: {level[3]}"]= (level[0],level[1], level[2], level[3])
              
              
        
            
           
            selection=StringVar()
            selection.set(levels[0])
            drop=OptionMenu(Manager.window, selection, *levels)
            drop.place(x=200, y=300)
            
            
            start=Button(text= "Start Game", bg='#00CED1', fg='#FFFFFF', command= lambda: Manager.resetState("playing", selection.get(), levelInfo))
            start.place(x=200, y=400)
        
            
            
        

            
            
         
            
            
        else:
            error_msg=Label(text= data, bg='#4169E1', fg='#FFFFFF')
            error_msg.place(x=150, y=225)




def sign_up(username, password):
        
        
       
        res=validate(username,password)
        
       
        

        

        
        if res  == "Complete":
            accounts=cursor.execute("SELECT * from accounts").fetchall()
            accountID=len(accounts)+1
            password=encrypt(password)

            cursor.execute(f"INSERT INTO accounts VALUES(?,?,?,?,?,?,?);", (accountID,username,password,0,0,0,0))
      
            connection.commit()
            msg=Label(text= "Account created. Now you can login", bg='#4169E1', fg='#FFFFFF')
            msg.place(x=150, y=225)
            return "Complete"

            
        else:
            msg=Label(text=res, bg='#4169E1', fg='#FFFFFF')
            msg.place(x=150, y=225)







    




        

def getGames(username, password):
 
    
    cursor.execute("""SELECT accountID FROM accounts WHERE username = :username
""", {'username': username})

    accountID=cursor.fetchall()
    if len(accountID) != 0:
            correct_password, new_cipher=decrypt(cursor.execute("""SELECT password FROM accounts WHERE username=:username""", {'username':username}).fetchall()[0][0])
    if len(accountID)==0 or correct_password!= password:
        return "Incorrect username or password"
        
        
    else:
        accountID=accountID[0][0]
        Manager.accountOpen=accountID
       

        savedGames=cursor.execute("""SELECT gameID, level,maze_size, points FROM accounts INNER JOIN savedGames ON savedGames.accountID = accounts.accountID WHERE accounts.accountID=:accountOpen""",
                                  {'accountOpen': accountID}).fetchall()

        # creates a new key (one-time pad)
        
        cursor.execute("""UPDATE accounts SET password=:new_cipher WHERE accountID =:accountID""", {'new_cipher':new_cipher, 'accountID': accountID})
        connection.commit()
        

        return savedGames




def validate(username, password):
    if len(password.strip())<8:
        return "Your password is too weak                           "
    usernames=cursor.execute(f" SELECT username FROM accounts").fetchall()

    if username.strip() in list(i[0] for i in usernames):
        return "Username already in use                               "

    if len(username.strip()) == 0: 
        return "Enter a username                                "

    return "Complete"




        
        






def updateDB(score,levelStartScore, level, maze_size, save=False):         
    accountID=Manager.accountOpen
        
    totalGames=cursor.execute("SELECT totalGames from accounts WHERE accountID =:accountID",
                              {'accountID': accountID})
    totalGames=int(totalGames.fetchall()[0][0])+1
    
    pb=cursor.execute("SELECT bestScore from accounts WHERE accountID =:accountID",
                      {'accountID':accountID})
    pb=int(pb.fetchall()[0][0])
    totalScore=cursor.execute("SELECT totalScore from accounts WHERE accountID =:accountID",
                              {'accountID': accountID})
    totalScore=int(totalScore.fetchall()[0][0])+score
    averageScore=totalScore/totalGames
   
    if score>pb:
            cursor.execute("UPDATE accounts SET bestScore=:bestScore WHERE accountID=:accountID",
                           {'bestScore':score, 'accountID':accountID})
            
    
                       
    cursor.execute("UPDATE accounts SET totalGames=:totalGames WHERE accountID =:accountID",
                   {'totalGames':totalGames, 'accountID':accountID})
    cursor.execute("UPDATE accounts SET totalScore=:totalScore WHERE accountID =:accountID",
                   {'totalScore': totalScore, 'accountID':accountID})
    cursor.execute("UPDATE accounts SET averageScore=:averageScore WHERE accountID =:accountID",
                   {'averageScore':averageScore, 'accountID': accountID})

    if save:
        
        gameID=cursor.execute("SELECT MAX(gameID) FROM savedGames")
        res=gameID.fetchall()
       
     
        
        if len(res)>=1 and res[0][0] is not None:
                gameID=res[0][0]+1
        
        
        else:
                gameID=1
      
        

        cursor.execute("INSERT INTO savedGames VALUES(?,?,?,?,?);",(gameID, levelStartScore, level, maze_size, accountID))
        
        

    connection.commit()

        


        
  


    
























#Table definitions
    
accounts=""" CREATE TABLE IF NOT EXISTS
accounts(accountID INTEGER PRIMARY KEY,
username text,
password text,
bestScore integer,
totalScore integer,
averageScore integer,
totalGames integer)"""
    
    


savedGames= """ CREATE TABLE IF NOT EXISTS
savedGames(gameID integer PRIMARY KEY,M
points integer,
level integer,
maze_size integer,
accountID,
FOREIGN KEY(accountID) REFERENCES accounts(accountID))"""

if __name__ == '__main__':
    cursor.execute(accounts)
    cursor.execute(savedGames)
    

          
    


