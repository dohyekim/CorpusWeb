import smtplib


def send_email(subject, msg, to):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(from_address,pwd)
        server.sendmail(from_address, to ,msg)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")





def confirm_email(token):
    try:
        email = s.loads(token, salt= 'email_confirm', max_age = 100)
    except SignatureExpired:
        return '<h1>유효기간이 만료되었습니다. 다시 가입해주세요. </h1>'
    return redirect('/login')