from celery import shared_task
from django.core.mail import send_mail
from fundonotes import settings

@shared_task(bind=True)
def send_email(self, token, to, name):
    """
    to send the email to desired user
    :param to:
    :param token:
    :param name:
    :return:
    """
    print("-----------")
    send_mail(from_email=settings.EMAIL_HOST, recipient_list=[to],
              message="Hy {}\nWelcome to Fundonotes App ,Thanks for installing our software\nYour Activation url = "
                      "http://127.0.0.1:8000/user/validate/{}".format(name,
                                                                      token),
              subject="Link for Your Registration", fail_silently=False, )
