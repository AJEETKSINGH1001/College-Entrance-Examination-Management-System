# marksheet/admin.py
from django.contrib import admin
from .models import Class, Student, Subject, Marks

admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Marks)
