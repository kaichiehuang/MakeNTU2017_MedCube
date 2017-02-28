import smtplib
 
server = smtplib.SMTP('smtp.sendgrid.net')
server.starttls()
server.login("azure_cf73ba62b6d99c12217b5a52d1afae59@azure.com", "GGininder123")
 
FROM = 'mzure_cf73ba62b6d99c12217b5a52d1afae59@azure.com'

TO = ["b02507013@ntu.edu.tw"] # must be a list

SUBJECT = "Time to buy medicine!"

TEXT = """Your medicine is running out. Please follow the link to get some more!
http://shopping.friday.tw/item/新升級善存_銀寶善存50綜合維他命錠禮盒-S07573081"""


msg = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)


server.sendmail("azure_cf73ba62b6d99c12217b5a52d1afae59@azure.com", "b02507013@ntu.edu.tw", msg.encode("utf8"))
server.quit()