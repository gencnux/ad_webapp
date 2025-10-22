from . import views
from django.urls import path
from .views import login_view, logout_view, run_script
from .views import view_logs

urlpatterns = [
    path("manage-users/", views.manage_users, name="manage_users"),
    path("my-logs/", views.my_logs, name="my_logs"),
    path("logs/", view_logs, name="logs"),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", run_script, name="dashboard"),
]
