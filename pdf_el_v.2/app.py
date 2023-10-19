from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dataLogics.AnalyzeImage import image_analysis
from dataLogics.AnalyzeFont import TextAnalyze
from dataLogics.AnalyzeHeadFoot import AnalyzeHeadFooter
from dataLogics.sharingFeat import pdf_analysis_mail



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'




# # Connect to the railway database
# db = mysql.connector.connect(user='root', password='XISE5fvcij9kwCmTw0bu',
#                               host='containers-us-west-208.railway.app', database='railway')

db = mysql.connector.connect(
    host='containers-us-west-208.railway.app',
    user='root',
    password='XISE5fvcij9kwCmTw0bu',
    database='railway'
)
  

# # Configure MySQL
# db = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='Root@12345',
#     database='pdfelv'
# )

# Set a secret key for session management
app.secret_key = 'hello'

# Signup Page
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cpassword=request.form['cpassword']
        pnnumber=request.form['pnnumber']
        email=request.form['email']
        hyu=request.form['who']
        if password == cpassword:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username,email,pnnumber,hcdu,password) VALUES (%s, %s,%s,%s,%s)", (username,email,pnnumber,hyu,password))
            db.commit()
            cursor.close()
            flash('1')
            
        else:
            flash('2')
            
        return render_template('./signup.html')
    return render_template('./signup.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password ='{password}'")
        user = cursor.fetchall()
        ##print(user[0][1])
        cursor.close()  # Close the cursor after fetching the result
        if user:
            session['username'] = user[0][1]
            session['userid'] = user[0][0]
            session['email']=user[0][2]
            receiver_email=session['email']
            user_name=session['username']
            send_mail(receiver_email,user_name)
            flash('Login successful!')
            return render_template('pdf_upload.html',username=username,pdfimage={},pdffont={})
        else:
            flash('wrong')
    return render_template('login.html')




@app.route('/pdf_upload', methods=['GET', 'POST'])
def pdf_upload():
    pdf_image_result={}
    pdf_font_result={}
    pdf_head_foot_result={}
    username = session['username'] 
    if 'username' in session:
        username = session['username'] 
        
        userid=session['userid']
        if request.method == 'POST':
            pdf_file = request.files['pdf_file']
            if 'sharereport' in request.form:
                #if pdf_file and pdf_file.filename.endswith('.pdf'):
                filename = request.form['file_sharing']
                cur = db.cursor()
                cur.execute(f"SELECT * FROM pdfupload WHERE filename = '{filename}' and userid={userid}")
                pdf_data = cur.fetchall()
                sahrefile_id=pdf_data[0][0]
                pdfid=sahrefile_id
                email_share=request.form['email_sharing']
                #print("Email Sent to the user ")
                pdf_analysis_mail(email_share,username,filename,userid,pdfid)

            if 'pdfanalysis' in request.form:
                if pdf_file and pdf_file.filename.endswith('.pdf'):
                    filename = pdf_file.filename
                    pdf_image_result={}
                    pdf_font_result={}
                    pdf_head_foot_result={}
                    # Save the PDF file to the uploads folder
                    pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    output_dir = f'''static/{username}/{filename}'''
                    filename_path=f'''static/uploads/{filename}'''
                    #pdf_image_result=image_analysis(filename_path,output_dir)
                    pdf_font_result=TextAnalyze(filename_path)
                    pdf_head_foot_result=AnalyzeHeadFooter(filename_path)
                
                    #print(pdf_image_result)
                    #print(pdf_font_result)
        
                    #print(pdf_head_foot_result)

                    authorName=pdf_head_foot_result[1]
                    phf=pdf_head_foot_result[0]
                    user_ui_filpath=f'{username}/{filename}'
                    # Save the PDF file info to the database
                    cur = db.cursor()
                    cur.execute("INSERT INTO pdfupload (filename,userid) VALUES (%s,%s)", (filename,userid))
                    db.commit()

                    #return [pdf_image_result,pdf_image_result,pdf_head_foot_result]

                    return render_template('pdf_upload.html', pdf_filename=filename,username=username,pdfimage=pdf_image_result,pdffont=pdf_font_result,userfile=user_ui_filpath,pdfh=phf,an=authorName)
                return render_template('pdf_upload.html', pdf_filename=None,pdfimage={},pdffont={},username=username)

            if 'pdfanalysisfull' in request.form:
                if pdf_file and pdf_file.filename.endswith('.pdf'):
                    filename = pdf_file.filename
                    pdf_image_result={}
                    pdf_font_result={}
                    pdf_head_foot_result={}
                    # Save the PDF file to the uploads folder
                    pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    output_dir = f'''static/{username}/{filename}'''
                    filename_path=f'''static/uploads/{filename}'''
                    pdf_image_result=image_analysis(filename_path,output_dir)
                    pdf_font_result=TextAnalyze(filename_path)
                    pdf_head_foot_result=AnalyzeHeadFooter(filename_path)
                
                    #print(pdf_image_result)
                    #print(pdf_font_result)
        
                    #print(pdf_head_foot_result)

                    authorName=pdf_head_foot_result[1]
                    phf=pdf_head_foot_result[0]
                    user_ui_filpath=f'{username}/{filename}'
                    # Save the PDF file info to the database
                    cur = db.cursor()
                    cur.execute("INSERT INTO pdfupload (filename,userid) VALUES (%s,%s)", (filename,userid))
                    db.commit()
                    
                    #return [pdf_image_result,pdf_image_result,pdf_head_foot_result]

                    cur.execute(f"SELECT * FROM pdfupload WHERE filename = '{filename}' and userid={userid}")
                    pdf_data = cur.fetchall()
                    sahrefile_id=pdf_data[0][0]
                    sharefile_user=pdf_data[0][2]
                    
                    cur.execute("INSERT INTO pdfanalysis (pdfid,userid,imagestyle,fontstyles,authorname) VALUES (%s,%s,%s,%s,%s)", (sahrefile_id,sharefile_user,str(pdf_image_result),str(pdf_font_result),authorName))
                    db.commit()
                    cur.close()

                    return render_template('pdf_upload.html', pdf_filename=filename,username=username,pdfimage=pdf_image_result,pdffont=pdf_font_result,userfile=user_ui_filpath,pdfh=phf,an=authorName)
            return render_template('pdf_upload.html', pdf_filename=None,pdfimage={},pdffont={},username=username)
        return render_template('pdf_upload.html',username=username,pdfimage={},pdffont={})
    

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        username = session['username'] 
        userid=session['userid']
        cur = db.cursor()
        cur.execute(f"select * from pdfupload where userid={userid};")
        user = cur.fetchall()

        #print(user[0])
        return render_template('dash.html', userData=user)
    

@app.route('/pdf_delete', methods=['GET', 'POST'])
def pdf_delete():
    if 'username' in session:
        del_request=request.form['del_req']
        print(del_request)
        username = session['username'] 
        userid=session['userid']
        cur = db.cursor()

        cur.execute(f"select * from pdfupload where filename='{del_request}';")
        file_id = cur.fetchall()
        print(file_id[0])
        cur.execute(f"delete from pdfanalysis where pdfid={file_id[0][0]} and userid={userid};")
        cur.execute(f"delete from pdfupload where filename='{del_request}' and userid={userid};")
        db.commit()
        cur.execute(f"select * from pdfupload where  userid={userid};")
        user = cur.fetchall()
        cur.close()
        print(del_request)
        #print(user[0])
        return render_template('dash.html', userData=user)

@app.route('/account')  
def account():
    if 'username' in session:
        username = session['username'] 
        userid=session['userid']
        cur = db.cursor()
        cur.execute(f"select * from pdfupload where userid={userid};")
        user = cur.fetchall()
        #print(user[0])
        return render_template('account.html', userData=user)


@app.route('/help')  
def help():
    if 'username' in session:
        username = session['username'] 
        userid=session['userid']
        cur = db.cursor()
        cur.execute(f"select * from pdfupload where userid={userid};")
        user = cur.fetchall()
        #print(user[0])
        return render_template('help.html')
    

def send_mail(receiver_email,user_name):
    sender_email = 'tejeshvenna@gail.com' 
    receiver_email = f'{receiver_email}' 
    subject = 'Login Detected'
    message = f'''
<pre style="font-family: Arial, Helvetica, sans-serif;text-align: justify;">
Hi {user_name},

Login Detected

</pre>
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
        return (f'{receiver_email} Email sent successfully!')

    except Exception as e:
        return (f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
