"""
URL configuration for mylibrary_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mylibrary_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Landing Page
    path('', views.landing_page, name="landing_page"),

    # Student
    path('signup/', views.student_signup, name="student_signup"),
    path('login/', views.login_view, name="student_login"),
    path('dashboard/', views.student_dashboard, name="student_dashboard"),

    # Logout
    path('logout/', views.logout_view, name="logout"),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name="admin_dashboard"),

    # student crud
    path('admin_dashboard/students/', views.manage_students, name='manage_students'),
    path('admin_dashboard/students/add/', views.add_student, name='add_student'),
    path('admin_dashboard/students/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('admin_dashboard/students/delete/<int:id>/', views.delete_student, name='delete_student'),

    path('admin_dashboard/manage_issue_books/', views.manage_issued_books, name='manage_issue_books'),

    # Admin Book Management
    path('admin_dashboard/books/', views.manage_books, name='manage_books'),        # View all books
    path('admin_dashboard/books/add/', views.add_book, name='add_book'),            # Add new book
    path('admin_dashboard/books/edit/<int:id>/', views.edit_book, name='edit_book'), # Edit existing book
    path('admin_dashboard/books/delete/<int:id>/', views.delete_book, name='delete_book'), # Delete book

    # Admin IssueBook CRUD
    path('dashboard/issued-books/', views.manage_issued_books, name='manage_issued_books'),
    path('dashboard/issued-books/add/', views.add_issue_book, name='add_issue_book'),
    path('dashboard/issued-books/edit/<int:id>/', views.edit_issue_book, name='edit_issue_book'),
    path('dashboard/issued-books/delete/<int:id>/', views.delete_issue_book, name='delete_issue_book'),

    # Student issued books (read-only)
    path('student/<int:student_id>/issued-books/', views.student_issued_books, name='student_issued_books'),

    # profile 
    path("student/profile/", views.my_profile, name="my_profile"),
    path("student/profile/edit/", views.edit_profile, name="edit_profile"),

    # books
    path("student/all_books/", views.all_books, name="all_books"),
    path("student/issue-book/<int:book_id>/", views.issue_book, name="issue_book"),
    path("student/my_books/", views.my_books, name="my_books"),
    path("student/return-book/<int:issue_id>/", views.return_book, name="return_book"),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
