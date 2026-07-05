from django.contrib import admin
from .models import (
    Question,
    Choice,
    Project,
    Employee,
    Comment,
    IdempotencyKey,
)

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(Comment)
admin.site.register(IdempotencyKey)