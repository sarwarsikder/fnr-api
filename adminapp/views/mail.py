import os

from django.views import generic
from django.core.mail import EmailMultiAlternatives


class MailHelper(generic.View):
    def mail_send(context, subject, to, sender_mail):
        html_content = context
        # logger = logging.getLogger(__name__)
        # logger.debug("-----------------sender Email------------------------")
        # logger.debug(sender_mail)
        # logger.debug("-----------------receiver Email------------------------")
        # logger.debug(to)
        # logger.debug("-----------------subject------------------------")
        # logger.debug(subject)
        # live
        if os.environ['ENVIRONMENT_TYPE'] == 'master':
            msg = EmailMultiAlternatives(subject=subject, from_email=sender_mail,
                                         to=['workspaceinfotech@gmail.com',to], body=html_content)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:
            msg = EmailMultiAlternatives(subject=subject, from_email=sender_mail,
                                         to=['mahedi@workspaceit.com'], body=html_content)
            msg.attach_alternative(html_content, "text/html")
            msg.send()


