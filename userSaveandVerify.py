import random
import sqlite3



conn = sqlite3.connect("database.db")
cursor = conn.cursor()


def generateUserId():
    sampleUserId = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ123456789"
    lst = list(sampleUserId)

    userId = []
    while len(userId) < 12:
        userId.append(random.choice(lst))

    userId = "".join(userId)

    return userId




def checkUserExist(email, provider):
    query1 = "SELECT 1 FROM users WHERE email = ? AND provider = ?"
    cursor.execute(query1, (email, provider))
    row1 = cursor.fetchone()

    if row1:
        return True
    else:
        return False
    
#AFTER THIS JUST LOGIN BY TAKING THE NECESSARY DATA
    

def checkEmailExist(email):
    query2 = "SELECT 1 FROM users WHERE email = ?"
    cursor.execute(query2, (email,))
    row2 = cursor.fetchone()

    if row2:
        return True
    else:
        return False
#IF EMAIL EXIST THEN USE THE SAME USERID FOR THE OTHER PROVIDER


def userSave(userId, email, provider):
    query3 = "INSERT INTO users (userId, email, provider) VALUES (?, ?, ?)"
    cursor.execute(query3, (userId, email, provider))

    conn.commit()
#THIS IS TO SAVE THE USER EITHER NEW OR WITH SAME EMAIL
    


def sameUsername(email, provider):
    userExist = checkUserExist(email, provider)

    if userExist != True:
        res = checkEmailExist(email)

        if res == True:
            query3 = "SELECT userId FROM users WHERE email = ?"
            cursor.execute(query3, (email,))
            userId = cursor.fetchone()[0]
            userSave(userId, email, provider)
            return "PROVIDER-LINKED"

        if res == False:
            while True:
                userId = generateUserId()

                query2 = "SELECT 1 FROM users WHERE userId = ?"
                cursor.execute(query2, (userId,))
                row = cursor.fetchone()
                if row:
                    continue
                else:
                    userSave(userId, email, provider)
                    break
            return "NEW-USER"

    else:
        return "LOGIN"

# THIS IS THE MAIN THING WHICH SAVES USER


