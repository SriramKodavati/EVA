
from datetime import timedelta, date, datetime
from playsound import playsound
import Responce
import psycopg2
import time
import confirmationGUI

dbError = False

def alert():
    alertText = "You have a notification."
    playsound('alert.wav')
    Responce.justDisplay(alertText)


def takenMedsConfirmaiton(medID, curID, reportID):

    print(medID)
    print(reportID)
    yesdbUpdate = "update reportMetrics set takenConfirmation = 1 where id = "  + reportID + ";"
    nodbUpdate = "update reportMetrics set takenConfirmation = 2 where id = " + reportID + ";"
    idkdbUpdate = "update reportMetrics set takenConfirmation = 3 where id = " + reportID + ";"

    picturedbGrabPath = "select imagepath from medicine1 where id = " + medID + ";"

    print("Have you taken your medicine yet?")
    Responce.justDisplay("Have you taken your medicine yet?")
    #add yesno button via Angular
    print(medID)
    cur.execute(picturedbGrabPath)
    imagePath = cur.fetchone()
    print(imagePath)
    confirmationGUI.loadingGui(imagePath)

    yesno = confirmationGUI.confir

    #yesno = input()
    if yesno == 2:
        print("Nice job!")
        cur.execute(yesdbUpdate)
    elif yesno == 1:
        print("Thanks for letting me know")
        cur.execute(nodbUpdate)
    elif yesno == 3:
        print("Thats alright, thanks for letting me know")
        cur.execute(idkdbUpdate)
    else:
        print("default no")
        cur.execute(nodbUpdate)

    now = time.strftime('%H:%M')


    takentimeCommand = "update reportMetrics set timetaken = '"+ now +"' where id = " + reportID + ";" # may need to tweak time format
    cur.execute(takentimeCommand)

def computedRefilDate(dateFilled, quantity, timesPerDay, weeklyCount):
    quantity = int(quantity)
    daysOfMeds = quantity / timesPerDay
    start = datetime.strptime(dateFilled, "%m/%d/%Y")

    actualDays = (daysOfMeds / weeklyCount) * 7

    newDate = start + timedelta(days=actualDays)

    newDate = newDate.strftime("%m/%d/%Y")

    return newDate

def PerscriptionRefillReminder(refillDate, refillsLeft ): #will have object with an attribute that is refill date etc.
    today = datetime.today()
    today = today.strftime("%m/%d/%Y")

    refillDate = datetime.strptime(refillDate, "%m/%d/%Y")

    start = datetime.strptime(today, "%m/%d/%Y")

    print('start', start)

    diff = refillDate.date() - start.date()

    print(diff.days)

    refillsLeft = 3


    # if diff.days < 30 and refillsLeft == 3: # how to handle this Sulsal CHANGE THESE, USED FOR SAKE OF DEMO
    #     mySTR = "You need to refill your perscription in 10 days, but you dont have any refills left. Contact your physician if you need more medicine."
    #     Responce.speechandsay(mySTR)
    # elif diff.days < 2:
    #     print("its time to fill your perscription")

    # would usually remind user if their perscription was empty and needed refilled, but removing for now for sake of demo.

# new reminder function, actually reminding. check the time and date from the table.

conn = psycopg2.connect(
    host="localhost",
    database="EVA",
    user="postgres",
    password="alex"
)

cur = conn.cursor()

def notification(medID, curID, reportID):
    medID = medID

    pgmedNameCom = "SELECT medname FROM medicine1 where id = " + medID + ";"
    pgdateFilledCom = "SELECT datefilled FROM medicine1 where id = " + medID + ";"
    pgQuanCom = "SELECT quantity FROM medicine1 where id = " + medID + ";"
    pgRefillCom = "SELECT refillsleft FROM medicine1 where id = " + medID + ";"
    pgrefillDatecom ="SELECT refilldate FROM medicine1 where id = " + medID + ";"

    dateFilled = getfromTable(pgdateFilledCom)
    medName = getfromTable(pgmedNameCom)
    quantity = getfromTable(pgQuanCom)
    refillsLeft = getfromTable(pgRefillCom)

    if getfromTable(pgrefillDatecom) == "hiya":
        insertVal = computedRefilDate(dateFilled, quantity, 1, 7)
        print(insertVal)
        pgrefillDateInsert = "update medicine1 set refilldate='" + insertVal + "' WHERE id=" + medID + ";"
        cur.execute(pgrefillDateInsert)

    refillDate = getfromTable(pgrefillDatecom)

    notificationString = "It's time to take your "+ medName + " medicine. "
    Responce.speechandsay(notificationString)
    print("refilsLeft " + refillsLeft)

    PerscriptionRefillReminder(refillDate, refillsLeft)
    #takenMedsConfirmaiton(medID, curID, reportID)


def convertTuple(tup):
    try:
        myStr = ''.join(tup)
        return myStr
    except TypeError:
        myStr = ','.join(str(tu) for tu in tup)
        return myStr

def checkTriggerNotification(reminderTime, reminderFinalDate, medID, curID, reportID):
    today = datetime.today()
    today = today.strftime("%m/%d/%Y")
    now = time.strftime('%H:%M')
    print(now)
    if now > reminderTime and reminderFinalDate > today:
        alert()
        notification(medID, curID, reportID)
    else:
        print("not time yet")


def getfromTable(command):
    cur.execute(command)
    myVal = cur.fetchone()

    try:
        myresult = all(elem is None for elem in myVal)
        if "refilldate" in command and myresult:
            myvalue = "hiya"
            return myvalue

        myValtoString = convertTuple(myVal)
        return myValtoString
    # dont alwasy need to handle it this above way...

    except TypeError:
        print("db error")
        dbError = True

def getfromTableNotTime(com):
    cur.execute(com)
    myVal = cur.fetchone()
    return myVal




def checkRunThrough():
    check = True
    curID = 0

    today = datetime.today()
    today = today.strftime("%m/%d/%Y")
    while check:
        curID +=1
        if curID > 20:
            break
        curID = str(curID)
        postgresTimeCommand = "SELECT remindertime FROM reminders where id = " + curID + ";"
        postgresDateCommand = "SELECT finalreminderdate FROM reminders where id = " + curID + ";"

        postgresmedIDCommand = "SELECT medid FROM reminders where id = " + curID + ";"

        alreadyTriggredCommand = "select id from reportMetrics where medid = " + curID + " and date = '" + today + "' and timetaken is NULL;"

        #Davison need to resolve this but for sake of demo, will add stuff needed


        reminderTime = getfromTable(postgresTimeCommand)
        reminderFinalDate = getfromTable(postgresDateCommand)
        medID = getfromTable(postgresmedIDCommand)
        reportID = getfromTable(alreadyTriggredCommand)
        print(reportID)

        isNoneTime = isinstance(reminderTime, str)
        isNoneDate = isinstance(reminderFinalDate, str)
        isAlreadyTriggered = isinstance(reportID, int) #DAVISON Need to add check to see if already triggered, i guess we do up top
        print(isAlreadyTriggered)
        isNoneMedID = isinstance(medID,str)

        print(isAlreadyTriggered)
        print()

        if isNoneTime and isNoneDate:
            checkTriggerNotification(reminderTime, reminderFinalDate, medID, curID, reportID)
        else:
            print("you got an error or are at end of db")
        curID = int(curID)







# I need something that checks the db, specifically the time of day and compares it to the db. THen when the time comes it needs to trigger the notification
# THen I need something to run in the back ground. It will listen constantly. When someone prompts it and sayd Eva, it will say, what can I help you with?
# then the user will ask about their meds, if they've taken them yet, etc.
# so theres 2 parts, theres the