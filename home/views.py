from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UpdateForm
from django.contrib.auth import logout as lt
from django.contrib import messages
from django.contrib.auth.models import User

class HomeView(TemplateView):

    template_name = 'home/home.html'

class AboutView(TemplateView):

    template_name = 'home/about.html'

class ContactView(TemplateView):
 
    template_name = 'home/contact.html' 

def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)

def error_500(request):
        data = {}
        return render(request,'500.html', data)

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "home/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="home/password/password_reset.html", context={"password_reset_form":password_reset_form})


def signup(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("home:update_profile")
    context.update({
        "form":form, 
        "title": "Signup",
    })
    return render(request, "registration/signup.html", context)

def signin(request):
    context = {}
    form = AuthenticationForm(request, data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    context.update({
        "form": form,
        "title": "Signin",
    })
    return render(request, "registration/signin.html", context)

@login_required
def update_profile(request):
    context = {}
    user = request.user 
    form = UpdateForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.user = user
            update_profile.save()
            return redirect("home:home")

    context.update({
        "form": form,
        "title": "Update Profile",
    })
    return render(request, "registration/update.html", context)

@login_required
def logout(request):
    lt(request)
    return redirect("home:home")