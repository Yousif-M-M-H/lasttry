from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NameForm
from .models import Myname
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def index(request):

    return render(request, "first/base.html")


def home(request):
    name = Myname.objects.all()
    return render(request, "first/home.html", {'names': name})


def delete(request, id):
    names = Myname.objects.get(id=id)
    names.delete()
    return redirect("home")


def update(request, id):
    mymember = Myname.objects.get(id=id)
    form = NameForm(request.POST or None, instance=mymember)
    if form.is_valid():
        form.save()
        return redirect('home')
    context = {
        'mymember': mymember,
        'form': form
    }
    return render(request, "first/update.html", context)


def add(request):
    form = NameForm()
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(
            request, 'You successfully added a name  to your table')
    return render(request, "first/add.html", {'form': form})


class ShowProfilePageView(DetailView):
    model = Myname
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Myname.objects.all()
        context = super(ShowProfilePageView,
                        self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(
            Myname, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class EditProfilePageView(UpdateView):
    model = Myname
    template_name = 'registration/edit_profile_page.html'
    fields = ['first_name', 'last_name', 'email']

    success_url = reverse_lazy('home')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                        messages.success(
                            request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="first/password/password_reset.html", context={"password_reset_form": password_reset_form})
