import pandas as pd
import datetime
import smtplib
import time
import requests
from win10toast import ToastNotifier
GMAIL_ID = 'your_email_here'
GMAIL_PWD = 'your_passoword_here'
toast = ToastNotifier()
name = 'Anderson Rodrigues'
'www.fast2sms.com'

def sendEmail(to, sub, msg):
    gmail_obj = smtplib.SMTP('smtp.gmail.com', 587)
    gmail_obj.starttls()
    gmail_obj.login(GMAIL_PWD, GMAIL_PWD)
    gmail_obj.sendmail(GMAIL_ID, to, f'Subject: {sub}\n\n{msg}')
    gmail_obj.quit()
    print("Email sent to " + str(to) + "with subject" + str(sub) + "and message: " + str(msg))
    toast.show_toast("Email Sent!", f'{name} was sent e-mail ', threaded=True, icon_path=True, duration=6)

    while toast.notification_active():
        time.sleep(0.1)
def sendsms(to, msg, name, sub):
    url = "https://www.fast2sms.com/dev/bulk"
    payload = f"sender_id=FSTSMS&message={msg}&language=english&route=p&numbers={to}"
    headers = {
        'authorization': "API_KEY_HERE",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
    response_obj = requests.request("POST", url,
                                    data=payload,
                                    headers=headers)
    print(response_obj.text)
    print("SMS sent to " + str(to) + " with subject :" +
          str(sub) + " and message :" + str(msg))

    toast.show_toast("SMS Sent!",
                     f"{name} was sent message",
                     threaded=True,
                     icon_path=None,
                     duration=6)

    while toast.notification_active():
        time.sleep(0.1)


if __name__ == "__main__":

    dataframe = pd.read_excel("excelsheet.xlsx")

    today = datetime.datetime.now().strftime("%d-%m")

    yearNow = datetime.datetime.now().strftime("%Y")

    writeInd = []

    for index, item in dataframe.iterrows():
        msg = "Many Many Happy Returns of the day dear " + str(item['NAME'])

        bday = item['Birthday'].strftime("%d-%m")

        if (today == bday) and yearNow not in str(item['Year']):
            sendEmail(item['Email'], "Happy Birthday",
                      msg)
            sendsms(item['Contact'], msg, item['NAME'],
                    "Happy Birthday")
        writeInd.append(index)

for i in writeInd:
    yr = dataframe.loc[i, 'Year']

    dataframe.loc[i, 'Year'] = str(yr) + ',' + str(yearNow)

dataframe.to_excel('excelsheet.xlsx',
                   index=False)

