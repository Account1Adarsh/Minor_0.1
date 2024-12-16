from django.urls import path
from . import views

urlpatterns = [
    path('', views.firstpage, name='firstpage'),
    path('home/', views.Home, name='home'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),

    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),

    path('issued-books/', views.user_issued_books, name='user_issued_books'),

    # Login streak
    path('login-streak/', views.daily_login, name='login_streak'),

    path('return-book/<int:issue_id>/', views.return_book, name='return_book'),


    # Issue book
    path('issue-book/', views.issue_book, name='issue_book'),

    # Book list
    path('books/', views.book_list, name='book_list'),

    # Issued books
    path('issued-books-list/', views.issued_books, name='issued_books'),  # Renamed to avoid conflict
]
