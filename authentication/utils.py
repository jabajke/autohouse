from django.core.mail import send_mail
from django.utils.html import format_html


class Util:

    @staticmethod
    def send_email(data):
        link = format_html('<a href="{}">link</a>', data['link'])

        send_mail(subject=data['subject'],
           html_message=data['body'].format(link),
           from_email='a@a.com',
           recipient_list=[data['to']],
           message=None
        )
