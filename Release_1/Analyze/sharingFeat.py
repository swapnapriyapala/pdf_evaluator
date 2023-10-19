import smtplib
import json
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dataLogics.AnalyzeImage import image_analysis
from dataLogics.AnalyzeFont import TextAnalyze
from dataLogics.AnalyzeHeadFoot import AnalyzeHeadFooter

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Root@12345',
    database='pdfelv'
)

def pdf_analysis_mail(receiver_email, user_name, filename, userid, pdfid):
    cur = db.cursor()
    cur.execute(f"select pu.filename, pa.imagestyle, pa.fontstyles, pa.authorname from pdfanalysis pa join pdfupload pu where pu.filename='{filename}' and pu.userid={userid} and pu.pdfid={pdfid};")
    pdf_data = cur.fetchall()
    #print("Pdf DATA Starts")
    #print(pdf_data)
    #print("PDF DATA ENDS")
    sender_email = 'tejeshvenna@gmail.com'
    receiver_email = f'{receiver_email}'
    subject = 'PDF Analysis Report'

 
    image_str = pdf_data[0][1].replace("'", '"')
    font_json_str = pdf_data[0][2].replace("'", '"')


    pdf_data[0] = (pdf_data[0][0], image_str, font_json_str)

    pdf_data_str = ''
    pdf_data_str += f'Analyzed PDF Name: {pdf_data[0][0]}\n\n'


    image_data = json.loads(pdf_data[0][1])

    font_data = json.loads(pdf_data[0][2])

    pdf_data_str += 'Image Data:\n\n'
    for key, value in image_data.items():
        pdf_data_str += f'Image Name: {key}\n'
        pdf_data_str += f'Page Number: {value["Page Number"]}\n'
        pdf_data_str += f'Width: {value["width"]}\n'
        pdf_data_str += f'Height: {value["Height"]}\n'
        pdf_data_str += f'Color Space: {value["Color Space"]}\n\n'

    pdf_data_str += 'Font Styles:\n\n'
    for key, value in font_data.items():
        pdf_data_str += f'Font Name: {key}\n'
        pdf_data_str += f'Font Sizes: {", ".join(map(str, value))}\n\n'

    # Email message body
    message = f'''
<html>
<body>
    <p>Hi {user_name},</p>
    <p>Your PDF Analysis is Ready:</p>
    <pre>
    {pdf_data_str}
    </pre>
</body>
</html>
'''

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'tejeshvenna@gmail.com'
    smtp_password = 'ejypitgoawfizqnf'

    email_body = MIMEText(message, 'html')

    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject

    email_message.attach(email_body)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, email_message.as_string())
        server.quit()
        return f'{receiver_email} Email sent successfully!'
    except Exception as e:
        return f"An error occurred: {str(e)}"
