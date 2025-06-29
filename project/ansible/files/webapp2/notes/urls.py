from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'notes'

urlpatterns = [
    path('', login_required(views.NoteListView.as_view()), name='list'),
    path('add/', login_required(views.NoteCreateView.as_view()), name='add'),
    path('delete/<int:pk>/', login_required(views.NoteDeleteView.as_view()), name='delete'),
    path('<int:pk>/', login_required(views.NoteDetailView.as_view()), name='detail'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
]
