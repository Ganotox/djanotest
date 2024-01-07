from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProgramUploadForm, CommentForm, ComplaintForm, EditProfileForm
from .models import Program, Comment, Complaint, User, Program, Category, Genre

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def upload_program(request):
    if request.method == 'POST':
        form = ProgramUploadForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save(commit=False)
            program.uploaded_by = request.user
            program.save()
            return redirect('program_detail', program_id=program.id)
    else:
        form = ProgramUploadForm()
    return render(request, 'upload_program.html', {'form': form})

def program_detail(request, program_id):
    program = Program.objects.get(id=program_id)
    comments = Comment.objects.filter(program=program)
    complaints = Complaint.objects.filter(program=program)
    return render(request, 'program_detail.html', {'program': program, 'comments': comments, 'complaints': complaints})

def add_comment(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.program = program
            comment.author = request.user
            comment.save()
            return redirect('program_detail', program_id=program.id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

def submit_complaint(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.program = program
            complaint.author = request.user
            complaint.save()
            return redirect('program_detail', program_id=program.id)
    else:
        form = ComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form})


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Your Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except Exception as e:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def about_us(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact.html')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправлення на URL-шлях 'profile_view'
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

def home(request):
    programs = Program.objects.all()
    return render(request, 'home.html', {'programs': programs})

def filter_programs(request):
    category_id = request.GET.get('category')
    genre_id = request.GET.get('genre')
    if category_id:
        programs = Program.objects.filter(category_id=category_id)
    elif genre_id:
        programs = Program.objects.filter(genre_id=genre_id)
    else:
        programs = Program.objects.all()
    return render(request, 'home.html', {'programs': programs})

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
def manage_programs(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden()
    programs = Program.objects.all()
    return render(request, 'manage_programs.html', {'programs': programs})

@login_required
def view_complaints(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden()
    complaints = Complaint.objects.all()
    return render(request, 'view_complaints.html', {'complaints': complaints})


@login_required
def edit_program(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.user != program.uploaded_by and not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ProgramUploadForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            return redirect('program_detail', program_id=program.id)
    else:
        form = ProgramUploadForm(instance=program)
    return render(request, 'edit_program.html', {'form': form, 'program': program})


@login_required
def delete_program(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.user != program.uploaded_by and not request.user.is_superuser:
        return HttpResponseForbidden()

    program.delete()
    return redirect('home')


@login_required
def resolve_complaint(request, complaint_id):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden()

    complaint = Complaint.objects.get(id=complaint_id)
    complaint.resolved = True
    complaint.save()
    return redirect('view_complaints')


@login_required
def manage_moderators(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    # Логіка для керування статусами модераторів
    return render(request, 'manage_moderators.html')


@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    user_programs = Program.objects.filter(uploaded_by=user)
    return render(request, 'user_profile.html', {'user': user, 'programs': user_programs})


def search(request):
    query = request.GET.get('q', '')
    if query:
        programs = Program.objects.filter(title__icontains=query)
        users = User.objects.filter(username__icontains=query)
    else:
        programs = Program.objects.all()
        users = User.objects.none()
    return render(request, 'search.html', {'programs': programs})


@login_required
def block_user(request, user_id):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden()

    user_to_block = User.objects.get(id=user_id)
    return redirect('manage_users')


def rules(request):
    return render(request, 'rules.html')


def change_theme(request):
    # Логіка для зміни теми сайту (світла/темна)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def logout_view(request):
    logout(request)
    return redirect('home')

def user_programs(request, username):
    programs = Program.objects.filter(uploaded_by__username=username)
    return render(request, 'user_programs.html', {'programs': programs})