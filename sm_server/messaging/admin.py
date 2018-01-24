from django.contrib import admin

from messaging.models import PendingMessage, ActiveChannel

admin.site.register(PendingMessage)
admin.site.register(ActiveChannel)
