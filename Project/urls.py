
from django.contrib import admin
from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/' , views.home, name='home'),
    path('', views.auth_login, name="login"),
    path('signup/', views.signup, name='signup'),
    path('feeling/', views.feeling, name='feeling'),
    path('calendar/', views.calendar, name='calendar'),
    path('journal/', views.create_entry, name='create_entry'),
    path('entries/', views.entries, name='entries'),
    path('logout/', views.dologout, name='logout'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('tags/', views.tags, name='tags'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
