from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .tokens import account_activation_token
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User


class ProfileSignUp(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('profiles:account_activation_sent')
    success_message = 'Пользователь %(username)s успешно зарегистрирован. Необходимо активировать почтовый адрес'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your RealCryptopia Account'
        message = render_to_string('registration/account_activation_email.html', {
            'user': self.object,
            'domain': current_site.domain,
            'uid': force_text(urlsafe_base64_encode(force_bytes(self.object.pk))),
            'token': account_activation_token.make_token(self.object),
        })
        self.object.email_user(subject, message)
        return super().form_valid(form)

class ProfilePasswordResetView(views.PasswordResetView):
    success_url = reverse_lazy('profiles:password_reset_done')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend=['django.contrib.auth.backends.ModelBackend'])
        messages.success(request, 'Ваш профиль %s успешно активирован' % user.username)
        return redirect('index')
    else:
        return render(request, 'registration/account_activation_invalid.html')
