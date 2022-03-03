import smtplib
from email.message import EmailMessage
from string import Template


class SendEmail:
    def __init__(self, loan, password, my_email, to_email):
        self.loan = loan
        self.MY_EMAIL = password
        self.PASSWORD = my_email
        self.TO_EMAIL = to_email
        self.email = EmailMessage()
        self.send()

    def send(self):

        print(round(sum(self.loan.total_interests), 2))
        with open('email_template.html', 'r', encoding='UTF-8') as f:
            html = f.read()

        template = Template(html)

        self.email['from'] = 'Grean Loans'
        self.email['to'] = self.TO_EMAIL
        self.email['subject'] = 'Loan Table'

        self.email.set_content(html, "html")
        self.email.set_content(template.substitute({'amount': f'{self.loan.amount}', "period": f'{round(self.loan.period)}',
                                           "percentages": f'{self.loan.interest}',
                                           "total_interests": f'{round(sum(self.loan.total_interests), 2)}',
                                           "sum": f'{self.loan.amount + round(sum(self.loan.total_interests), 2)}'
                                           }), 'html')

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(user=self.MY_EMAIL, password=self.PASSWORD)
            smtp.send_message(self.email)



