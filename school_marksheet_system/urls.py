# school_marksheet_system/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marksheet.urls')),
    path('captcha/', include('captcha.urls')),  # Add this line to include captcha URLs

]
