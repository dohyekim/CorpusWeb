import smtplib

def send_email(to, subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        pwd = 'pwd'
        pwd.encode('utf-8')
        email = 'idid'
        email.encode('utf-8')
        server.login(email, pwd)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        message.encode('utf-8')
        server.sendmail(email, to, message)
        server.quit()

    except Exception as err:
        print("Email failed to send.", err)

# def confirm_email(token):
#     try:
#         email = s.loads(token, salt= 'email_confirm', max_age = 100)
#     except SignatureExpired:
#         return '<h1>유효기간이 만료되었습니다. 다시 가입해주세요. </h1>'
#     return redirect('/login')
