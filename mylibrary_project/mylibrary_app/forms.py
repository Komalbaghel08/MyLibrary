from django import forms
from .models import Student, Book, IssueBook
import re
from django.utils import timezone

# ===========================
# Student Signup Form
# ===========================
class StudentSignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'roll_number', 'profile_image','password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Roll Number'}),
        }

    # Name validation
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError("Name should only contain alphabets and spaces.")
        return name.strip()

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    # Phone validation
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\d{10,15}$', phone.strip()):
            raise forms.ValidationError("Phone must contain 10-15 digits.")
        return phone.strip() if phone else phone

    # Roll number validation
    def clean_roll_number(self):
        roll = self.cleaned_data.get('roll_number')
        if Student.objects.exclude(pk=self.instance.pk).filter(roll_number=roll).exists():
            raise forms.ValidationError("Roll number already exists.")
        if not re.match(r'^[A-Za-z0-9-]+$', roll):
            raise forms.ValidationError("Roll number should only contain letters, numbers, and dashes.")
        return roll.strip()

    # Password validation
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if not pwd or len(pwd) < 4:
            raise forms.ValidationError("Password must be at least 4 characters long.")
        return pwd

    # Confirm password validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

# ===========================
# Student Login Form
# ===========================
class StudentLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError("Invalid Email Address.")
        return email

    # Password validation
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 4:
            raise forms.ValidationError("Password must be at least 4 characters long.")
        return password

# ===========================
# Student Admin Form (Profile update)
# ===========================
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'roll_number', 'password', 'profile_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Roll Number'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

    # Name validation
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not re.match(r'^[A-Za-z ]+$', name.strip()):
            raise forms.ValidationError("Name should only contain alphabets and spaces.")
        return name.strip()

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    # Phone validation
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\d{10,15}$', phone.strip()):
            raise forms.ValidationError("Phone must contain 10-15 digits.")
        return phone.strip() if phone else phone

    # Roll number validation
    def clean_roll_number(self):
        roll = self.cleaned_data.get('roll_number')
        if Student.objects.exclude(pk=self.instance.pk).filter(roll_number=roll).exists():
            raise forms.ValidationError("Roll number already exists.")
        if not re.match(r'^[A-Za-z0-9-]+$', roll):
            raise forms.ValidationError("Roll number should only contain letters, numbers, and dashes.")
        return roll.strip()

    # Password validation
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if not pwd or len(pwd) < 4:
            raise forms.ValidationError("Password must be at least 4 characters long.")
        return pwd

# ===========================
# Book Form
# ===========================
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'quantity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title.strip()

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if not author or not re.match(r'^[A-Za-z ]+$', author.strip()):
            raise forms.ValidationError("Author name should only contain alphabets and spaces.")
        return author.strip()

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category and not re.match(r'^[A-Za-z ]+$', category.strip()):
            raise forms.ValidationError("Category should only contain alphabets and spaces.")
        return category.strip() if category else ''

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return qty

# ===========================
# Issue Book Form
# ===========================
class IssueBookForm(forms.ModelForm):
    class Meta:
        model = IssueBook
        fields = ['student', 'book', 'issue_date', 'return_date', 'is_returned']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'book': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_returned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_issue_date(self):
        issue_date = self.cleaned_data.get('issue_date')
        if issue_date > timezone.now().date():
            raise forms.ValidationError("Issue date cannot be in the future.")
        return issue_date

    def clean_return_date(self):
        issue_date = self.cleaned_data.get('issue_date')
        return_date = self.cleaned_data.get('return_date')
        if return_date and return_date < issue_date:
            raise forms.ValidationError("Return date cannot be before issue date.")
        return return_date
