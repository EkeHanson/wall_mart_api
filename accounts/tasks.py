# from celery import shared_task
# from django.utils import timezone
# from .models import CustomUser

# @shared_task
# def update_commissions():
#     now = timezone.now()
#     users = CustomUser.objects.all()
#     for user in users:
#         user.commission1 = user.commission2
#         user.commission2 = 0
#         user.save()


# # celery -A  core worker --loglevel=info
# # celery -A core beat --loglevel=info