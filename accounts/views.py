from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import View
from django.shortcuts import redirect
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        
        user = form.save()
        login(self.request, user)
        
        return super().form_valid(form) 
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        return render(request, self.template_name, {'form': form})
    


class UserPasswordView(PasswordChangeView):
    template_name = 'accounts/pass_change.html'
    title = 'Password Change'
    def form_valid(self, form):
        acc_no = self.request.user.account.account_no
        form.save()
        messages.success(
            self.request,
            f'Password changed Successfully'
        )
        send_transaction_email(self.request.user,acc_no,"Password Changed","accounts/pass_change_email.html")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('pass_change')



    
    
    