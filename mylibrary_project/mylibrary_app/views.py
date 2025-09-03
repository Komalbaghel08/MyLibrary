from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StudentSignupForm, StudentLoginForm, BookForm, StudentForm,IssueBookForm
from .models import Student, Book, IssueBook
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
# -------------------
# Landing Page
# -------------------
def landing_page(request):
    return render(request, "landing.html")


# -------------------
# Signup Student
# -------------------
def student_signup(request):
    if request.method == "POST":
        form = StudentSignupForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect("student_login")
    else:
        form = StudentSignupForm()
    return render(request, "signup_login.html", {"form": form, "sign_up": True})


# -------------------
# Login (Student + Admin)
def login_view(request):
    msg = None
    form = StudentLoginForm()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if admin credentials
        if email == "admin@gmail.com" and password == "admin123":
            request.session["admin_email"] = email
            return redirect("admin_dashboard")

        # Otherwise check student credentials
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            student = Student.objects.filter(email=email, password=password).first()
            if student:
                request.session["student_id"] = student.id
                return redirect("student_dashboard")
            else:
                msg = "Invalid credentials!"
        else:
            msg = "Please correct the errors below."

    return render(
        request,
        "signup_login.html",
        {"form": form, "log_in": "log_in", "admin": False, "msg": msg}
    )

# -------------------
# Logout
# -------------------
def logout_view(request):
    if "student_id" in request.session:
        del request.session["student_id"]
    if "admin_email" in request.session:
        del request.session["admin_email"]
    return redirect("landing_page")

# -------------------
# Student Dashboard
# -------------------
def student_dashboard(request):
    user_id = request.session.get('student_id')   
    if not user_id:
        return redirect("student_login")

    student = Student.objects.get(id=user_id)

    # Currently issued books (sirf jo return nahi hui)
    issued_books = IssueBook.objects.filter(student=student, is_returned=False)

    # Pending returns (sirf jo due date cross kar gayi aur abhi return nahi hui)
    from django.utils import timezone
    today = timezone.now().date()
    pending_returns = IssueBook.objects.filter(
        student=student, 
        is_returned=False, 
        return_date__lt=today
    )

    return render(request, "student_dashboard.html", {
        "student": student,
        "issued_books": issued_books.count(),   # sirf active issued books ka count aayega
        "pending_returns": pending_returns.count(),
        "Dashboard": True,
    })


# -------------------
# Admin Dashboard
# -------------------
def admin_dashboard(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")

    books = Book.objects.all()
    total_books = books.count()
    total_students = Student.objects.all().count()
    total_issued_books = IssueBook.objects.all().count()
    return render(request, "admin_dashboard.html", {"books": books,"dashboard":"dashboard","total_books":total_books,"total_students":total_students,"total_issued_books":total_issued_books})

# student crud
def manage_students(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    query = request.GET.get("q", "")
    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(phone__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'admin_dashboard.html', {
        'students': students,
        "manage_studnts": "manage_studnts",
        "query": query
    })


def add_student(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('manage_students')
    else:
        form = StudentForm()
    return render(request, 'admin_dashboard.html', {'add_new_student': True, 'form': form})

# edit student by ADMIN
def edit_student(request, id):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    student = Student.objects.get(id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student) 
        if form.is_valid():
            form.save()
            return redirect('manage_students')
    else:
        form = StudentForm(instance=student)
    return render(request, 'admin_dashboard.html', {'edit_student': True, 'form': form, 'student': student})

# del studen by admin
def delete_student(request, id):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    student = Student.objects.get(id=id)
    student.delete()
    return redirect('manage_students')


# manage books for admin
def manage_books(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    query = request.GET.get("q")  # search query li hai
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(category__icontains=query)
        )
    else:
        books = Book.objects.all()

    return render(request, 'admin_dashboard.html', {
        'manage_books': True,
        'books': books,
        'query': query,
    })

# add book for admin
def add_book(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm()
    return render(request, 'admin_dashboard.html', {'add_new_book': True, 'form': form})

# edit book for admin
def edit_book(request, id):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    book = Book.objects.get(id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'admin_dashboard.html', {'edit_book': True, 'form': form, 'book': book})

# del book by admin
def delete_book(request, id):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    book = Book.objects.get(id=id)
    book.delete()
    return redirect('manage_books')

#  ISSUE BOOKS  for admin
def manage_issued_books(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    issued_books = IssueBook.objects.select_related('student', 'book').all()
    return render(request, 'admin_dashboard.html', {'manage_issued_books': True, 'issued_books': issued_books})

# Admin: Add a new issue record isme admin kisi stuent ka issue book manage karega
def add_issue_book(request):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_issued_books')
    else:
        form = IssueBookForm()
    return render(request, 'admin_dashboard.html', {'add_new_issue': True, 'form': form})

# Admin: Edit issued book
def edit_issue_book(request, id):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    issue = IssueBook.objects.get(id=id)
    if request.method == 'POST':
        form = IssueBookForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('manage_issued_books')
    else:
        form = IssueBookForm(instance=issue)
    return render(request, 'admin_dashboard.html', {'edit_issue': "edit_issue", 'form': form, 'issue': issue})

# Admin: Delete issued book record
def delete_issue_book(request, id):
    admin_email = request.session.get('admin_email')
    if not admin_email:
        return redirect("student_login")


    issue = IssueBook.objects.get(id=id)
    issue.delete()
    return redirect('manage_issued_books')

# Student: View their issued books (read-only)
def student_issued_books(request, student_id):


    student = Student.objects.get(id=student_id)
    issued_books = IssueBook.objects.filter(student=student).select_related('book')
    return render(request, 'student_dashboard.html', {'issued_books': issued_books, 'student': student}) 


# -------------------
# Student Profile (View Only)
# -------------------
def my_profile(request):
    user_id = request.session.get("student_id")   
    if not user_id:
        return redirect("student_login")

    student = Student.objects.get(id=user_id)
    return render(request, "student_dashboard.html", {"student": student, "my_profile": "my_profile"})


# -------------------
# Student Profile (Edit)
# -------------------
def edit_profile(request):
    if "student_id" not in request.session:
        return redirect("student_login")

    student = Student.objects.get(id=request.session["student_id"])

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("my_profile")
    else:
        form = StudentForm(instance=student)

    return render(request, "student_dashboard.html", {"student": student, "form": form, "edit_profile": True})





#  All Books (search books page bhi yehi hai)
def all_books(request):
    user_id = request.session.get("student_id")   
    if not user_id:
        return redirect("student_login")


    student = Student.objects.get(id=user_id)

    query = request.GET.get("q")  # search query
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()

    return render(request, "student_dashboard.html", {
        "Dashboard": False,
        "my_profile": False,
        "edit_profile": False,
        "my_books": False,
        "all_books": True,
        "student": student,
        "books": books,
        "query": query,
        "quantity": books.count()
    })


#  My Books (Issued Books)
def my_books(request):
    user_id = request.session.get("student_id")   
    if not user_id:
        return redirect("student_login")


    student = Student.objects.get(id=user_id)
    issued_books = IssueBook.objects.filter(student=student)  # sabhi show karo (returned + issued)

    return render(request, "student_dashboard.html", {
        "Dashboard": False,
        "my_profile": False,
        "edit_profile": False,
        "my_books": True,
        "student": student,
        "issued_books": issued_books
    })

# from django.http import HttpResponse

# Issue Book Action
def issue_book(request, book_id):
    user_id = request.session.get("student_id")   
    if not user_id:
        return redirect("student_login")

    student = Student.objects.get(id=user_id)
    book = Book.objects.get(id=book_id)

    if book.quantity > 0:
        IssueBook.objects.create(
            student=student,
            book=book,
            issue_date=timezone.now().date(),   # only date
            return_date=timezone.now().date() + timedelta(days=15),
            is_returned=False
        )
        book.quantity -= 1
        book.save()
        return redirect("my_books")

    # agar quantity 0 ho toh simple HttpResponse bhejo
    return HttpResponse("<h3>Sorry, this book is not available right now.</h3>")


# Return Book Action
def return_book(request, issue_id):
    user_id = request.session.get("student_id")   
    if not user_id:
        return redirect("student_login")


    issue = IssueBook.objects.get(id=issue_id, student_id=user_id, is_returned=False)

    issue.is_returned = True
    issue.return_date = timezone.now().date()
    issue.save()

    # quantity wapas increase karo
    issue.book.quantity += 1
    issue.book.save()

    return HttpResponse("<h3>Book returned successfully.</h3>")
