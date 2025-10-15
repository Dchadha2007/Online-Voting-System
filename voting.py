import pwinput  ## For Password Input
import datetime ## For Recording VoteTime
import time     ## For Adding Time Delay
import mysql.connector as m
import shutil
import os
from dotenv import load_dotenv
import mysql.connector as m

load_dotenv()

def print_fast_centered(text, delay=0.01):
    columns = shutil.get_terminal_size().columns
    centered_text = text.center(columns)
    for char in centered_text:
        print(char, end = '', flush=True)
        time.sleep(delay)
    print()

##TEXT ANIMATION
def print_fast(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

## Building Connection For SQL
con=m.connect(
    username=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    password=os.getenv("DB_PASS"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)
if con.is_connected():
    print("~ ~ ~ ~ ~Connected Successfully to the Server~ ~ ~ ~ ~")
c=con.cursor()  ##cursor object



## Creating Vote Counting Table
c.execute("""CREATE TABLE IF NOT EXISTS Final_Vote(
          PARTY_NAME VARCHAR(100) PRIMARY KEY,
          VOTE_COUNT INT DEFAULT 0)""")

## ADDING DATA INTO TABLE
parties = ['BJP','BSP','CPI','CPM','INC','NCP']
for party in parties:
    c.execute("INSERT IGNORE INTO Final_Vote (PARTY_NAME, VOTE_COUNT) VALUES (%s, 0)", (party,))
con.commit()


### User Class To Manage User Registration, Login And Voting Status
class User:
    users_data={}  ## Class Variable To Store All Registered Users For Voting   

    def __init__(self, USERNAME, PASSWORD):
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.voted = False  ## To Check If The User Has Already Voted Or Not
        self.vote_time=None ## Check Time For Voting
        
    @classmethod
    def add_user(cls, USERNAME, PASSWORD):
        if USERNAME in cls.users_data:
            print_fast("\n🔴THIS USERNAME ALREADY EXIST!!!!\nTRY REGISTRATION WITH NEW USERNAME...\n")
            return False
        cls.users_data[USERNAME] = User(USERNAME,PASSWORD)
        return True
    
    @classmethod
    def Authentication(cls, USERNAME, PASSWORD):
        user = cls.users_data.get(USERNAME)
        if user and user.PASSWORD==PASSWORD:
            return user
        return None
    
    @classmethod
    def load_users(cls):
        c.execute("SELECT USER_NAME, VOTED, VOTE_TIME FROM User_Details")
        for uname, voted, vote_time in c.fetchall():
            user = User(uname,"dummy")
            user.voted = voted
            if vote_time:
                user.vote_time = vote_time.strftime("%d-%m-%Y %H-%M-%S")
            cls.users_data[uname] = user


## Manage User Registration
class RegisterUser():
    def register(self):
        USERNAME = input("\nENTER USERNAME FOR REGISTRATION:- ")
        while True:
            PASSWORD = pwinput.pwinput("\nENTER YOUR PASSWORD:- ")
            if len(PASSWORD)<6:
                print_fast("\nPASSWORD MUST CONTAIN MORE THAN OR ATLEAST 6 CHARACTERS\n")
                continue
            break
        confirm=pwinput.pwinput("\nCONFIRM YOUR PASSWORD:- ")
        if PASSWORD!=confirm:
            print_fast("\nPASSWORD DOESN'T MATCH !!! TRY AGAIN\n")
            return None
        if User.add_user(USERNAME, PASSWORD):
            print_fast("\nTHANK YOU FOR REGISTERING!😊\nYOU HAVE BEEN REGISTERED SUCCESSFULLY✅\n")
            try:
                c.execute("INSERT INTO User_Details (USER_NAME, VOTED) VALUES (%s, %s)", (USERNAME,False))
                c.execute("INSERT INTO Login_Details (USER_NAME, PASSWORD) VALUES (%s, %s)", (USERNAME, PASSWORD))
                con.commit()
            except Exception as e:
                print(f"Error Storing Registration date: {e}")   
        else:
            print_fast("❌ ❌REGISTRATION FAILED...❌ ❌")

    @staticmethod
    def Create_Table():
        try:
            c.execute("SHOW TABLES LIKE 'User_Details';")
            if not c.fetchone():
                c.execute("""
                     CREATE TABLE User_Details (
                          USER_NAME VARCHAR(50) PRIMARY KEY,
                          VOTED BOOLEAN DEFAULT FALSE,
                          VOTE_TIME DATETIME);""")
                print("TABLE 'User_Details' CREATED SUCCESSFULY..")
        except Exception as e:
            print(f"ERROR IN CREATING User_Details TABLE: {e}")
        con.commit()

    
## Manage User Login Data
class LoginUser():
    def Login_User(self):
        USERNAME = input("\nENTER YOUR USERNAME FOR LOGIN:- ")
        PASSWORD = pwinput.pwinput("\nENTER YOUR PASSWORD:- ")
        user = User.Authentication(USERNAME,PASSWORD)
        if user:
            print_fast("\nYOU ARE SUCCESSFULLY LOGGED IN ✅ ✅")
            return user
        else:
            print_fast("\nINVALID USERNAME OR PASSWORD\n \nTRY AGAIN AFTER 5 SECONDS")
            time.sleep(5)

    @staticmethod
    def Login_Table():
        try:
            c.execute("SHOW TABLES LIKE 'Login_Details';")
            if not c.fetchone():
                c.execute("""
                     CREATE TABLE Login_Details (
                          USER_NAME VARCHAR(50) PRIMARY KEY,
                          PASSWORD VARCHAR(50) NOT NULL);""")
                print("TABLE 'Login_Details' CREATED SUCCESSFULY..")
        except Exception as e:
            print(f"ERROR IN CREATING Login_Details TABLE: {e}")
        con.commit()


## Main Class For Voting System
class VotingSystem:
    def __init__(self):

        ## Dictionary To Show Votes Scored By Each Party
        self.Parties={"BJP":0, "BSP":0, "CPI":0, "CPM":0, "INC":0, "NCP":0} 

    def vote(self,user):
        if user.voted:
            print_fast("\nYOU HAVE ALREADY VOTED")
            return
        

        ## Party Options
        party_list=["BJP","BSP","CPI","CPM","INC","NCP"]
        print_fast("\n1. BJP (Bharatiya Janta Party)")
        print_fast("\n2. BSP (Bhaujan Samaj Party)")
        print_fast("\n3. CPI (Communist Party Of India)")
        print_fast("\n4. CPM (Communist Party Of India Marxist)")
        print_fast("\n5. INC (Indian National Congress)")
        print_fast("\n6. NCP (Nationalist Congress Party)")
        choice=input("\nWHICH PARTY WOULD YOU LIKE TO VOTE? (1 to 6):- ").strip()

        ## Choices To Choose Party
        if choice=="1":
            selected_party="BJP"
        elif choice=="2":
            selected_party="BSP"
        elif choice=="3":
            selected_party="CPI"
        elif choice=="4":
            selected_party="CPM" 
        elif choice=="5":
            selected_party="INC"
        elif choice=="6":
            selected_party="NCP"
        else:
            print_fast("\nINVALID CHOICE. VOTE NOT RECORDED")
            return
        

        ## Record Voting
        self.Parties[selected_party]+= 1
        user.voted = True
        now=datetime.datetime.now()
        user.vote_time=now.strftime("%d-%m-%Y %H-%M-%S")
        print_fast("\n✅ YOUR VOTE HAS BEEN RECORDED...")

        try:
            c.execute("UPDATE User_Details SET VOTED = %s, VOTE_TIME = %s WHERE USER_NAME = %s", (True, now, user.USERNAME))
            c.execute("INSERT INTO Voting_Details (USER_NAME, PARTY_VOTED, VOTE_TIME) VALUES (%s, %s, %s)", (user.USERNAME, selected_party, now))
            c.execute("UPDATE Final_Vote SET VOTE_COUNT = VOTE_COUNT +1 WHERE PARTY_NAME = %s",(selected_party,))
            con.commit()
        except Exception as e:
            print(f"Error in storing vote: {e}")

    @staticmethod
    def Voting_Table():
        try:
            c.execute("SHOW TABLES LIKE 'Voting_Details';")
            if not c.fetchone():
                c.execute("""
                     CREATE TABLE Voting_Details (
                          USER_NAME VARCHAR(50) PRIMARY KEY,
                          PARTY_VOTED VARCHAR(50) NOT NULL,
                          VOTE_TIME DATETIME NOT NULL);""")
                print("TABLE 'Voting_Details' CREATED SUCCESSFULY..")
        except Exception as e:
            print(f"ERROR IN CREATING Voting_Details TABLE: {e}")
        con.commit()


    def view_results(self):
        print_fast("\nVOTING RESULTS")
        c.execute("SELECT PARTY_VOTED, COUNT(*) FROM Voting_Details GROUP BY PARTY_VOTED")
        db_results = c.fetchall()
        total_votes=sum([count for _, count in db_results])

        if total_votes==0:
            print_fast("\nNO VOTES HAVE BEEN CASTED BY THE USER")
            return
        
        ## Vote Count And Percentage Of Each Party
        for party in self.Parties:
            count = next((cnt for p, cnt in db_results if p == party), 0)
            percent = (count / total_votes) * 100 if total_votes > 0 else 0
            print_fast(f"\nPARTY {party}: {count} VOTES ({percent:.2f}%)")

        print_fast(f"\n🧮 TOTAL VOTES CASTED: {total_votes} ")
        print_fast("\n🗂️ VOTER DETAILS: ")
        
        c.execute("SELECT USER_NAME, VOTE_TIME FROM Voting_Details")
        voted_users = dict(c.fetchall())

        for username in User.users_data:
            if username in voted_users:
                formatted_time = voted_users[username].strftime("%d-%m-%Y %H-%M-%S")
                print_fast(f"\n{username} VOTED AT {formatted_time}")
            else:
                print_fast(f"\n{username} HAS NOT VOTED YET..")


## Admin Login For Viewing Results
class Admin:
    def admin_login(self):
        username = input("\nENTER THE ADMIN USERNAME:- ")
        password = pwinput.pwinput("\nENTER THE ADMIN PASSWORD:- ")
        if username == os.getenv("ADMIN_USER") and password == os.getenv("ADMIN_PASS"):
            print_fast("\n✅ ADMIN LOGIN SUCCESSFUL")
            return True
        else:
            print_fast("\n❌ INVALID ADMIN USERNAME AND PASSWORD") 
            return False
        
## Main Control Function
        
def Voting_main():
    currently_logged_in_user = None
    Voting_System = VotingSystem()
    Register_User = RegisterUser()
    Login_User = LoginUser()

    LoginUser.Login_Table()
    RegisterUser.Create_Table()
    VotingSystem.Voting_Table()
    User.load_users()

    print_fast_centered("🗳️  🗳️-------------------------------- WELCOME TO VOTING SYSTEM--------------------------------🗳️  🗳️\n",delay=0.01)
    while True: 
        print("\n⬇️  ⬇️-------VOTING MENU-------⬇️  ⬇️\n")
        if not currently_logged_in_user:
            print_fast("\n1. REGISTER YOURSELF FOR VOTING\n")
            print_fast("\n2. LOGIN FOR VOTING\n")
        if currently_logged_in_user:
            print_fast("\n3. VOTE HERE\n")

        print_fast("\n4. VIEW THE VOTING RESULTS  (ADMIN ONLY)\n")
        print_fast("\n5. EXIT\n")

        Your_choice=input("\nENTER YOUR CHOICE:- ")

        if Your_choice == "1" and not currently_logged_in_user:
            Register_User.register()

        elif Your_choice == "2" and not currently_logged_in_user:
            if not User.users_data:
                print_fast("\n⚠️ YOU NEED TO REGISTER FIRST ")
            else:
                user= Login_User.Login_User()
                if user:
                    currently_logged_in_user=user
        elif Your_choice == "3":
            if currently_logged_in_user:
                Voting_System.vote(currently_logged_in_user)
            else:
                print_fast("\n⚠️ YOU MUST LOGIN BEFORE VOTING")
        elif Your_choice == "4":
            if Admin().admin_login():
                while True:
                    print_fast("\n 📊 ADMIN MENU:")
                    print_fast("\n1. VIEW VOTING RESULTS")
                    print_fast("\n2. BACK TO MAIN MENU")
                    choice=input("\nENTER YOUR CHOICE: ")

                    if choice == "1":
                        Voting_System.view_results()
                    elif choice == "2":
                        break
                    else:
                        print_fast("❌ INVALID CHOICE")

        elif Your_choice == "5":
            print_fast("\n🙏 THANK YOU FOR VOTING😊\n \nEXITING THE SYSTEM...\n")
            break
        else:
            print_fast("\n❌ THE CHOICE YOU ENTERED IS INVALID!!!\nTry Again..")


## Run The Voting System
if __name__=="__main__":
    Voting_main()



