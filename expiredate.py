import sqlite3
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib




# Create a SQL connection to our SQLite database
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
today=datetime.date.today()
tomorrow = str(today + datetime.timedelta(1))
print(tomorrow)
# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('''SELECT auth_user.username,library_issuedbook.expirydate,library_issuedbook.enrollment,library_book.name FROM library_book,
                       library_issuedbook,auth_user, library_studentextra where auth_user.id==library_studentextra.user_id and
                       library_studentextra.enrollment==library_issuedbook.enrollment and library_book.isbn==library_issuedbook.isbn;'''):
    #print(row)
    if row[1]==tomorrow:
        message=MIMEMultipart()
        message["from"]="ABES LIbrary"
        message["subject"] = f"book {row[3]} isssued"
        message.attach(MIMEText(f"""Book name- {row[3]} have been issued and is expiring on date {row[1]} and tomorrow is the last date to submit it back to library. Please returnby tomorrow .\n Regards\n ABES Library """))
        message["to"]=row[0]
        print("message to-",message["to"])
        print(row[0])
        with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("redwarrior031@gmail.com","nqmwtpiarngdaqwg")
            try:
                smtp.send_message(message)
                print("sent")
            except:
                print("cant send")
                
con.close()
 
