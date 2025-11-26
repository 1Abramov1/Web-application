from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import CustomUserCreationForm, UserUpdateForm


def register(request):
    """
    Контроллер регистрации пользователя
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Отправка приветственного письма
            send_welcome_email(user)

            # Автоматический вход после регистрации
            # Аутентифицируем пользователя перед логином
            authenticated_user = authenticate(
                request,
                username=user.email,
                password=form.cleaned_data['password1']
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, f'Добро пожаловать, {user.first_name or user.email}! Регистрация прошла успешно!')
                return redirect('catalog:home')
            else:
                messages.error(request, 'Ошибка автоматического входа. Пожалуйста, войдите вручную.')
                return redirect('users:login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def send_welcome_email(user):
    """
    Отправка приветственного письма после регистрации
    """
    try:
        subject = 'Добро пожаловать в Skystore!'

        # HTML версия письма
        html_message = render_to_string('users/emails/welcome_email.html', {
            'user': user,
            'first_name': user.first_name or 'пользователь',
        })

        # Текстовая версия письма
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=None,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True

    except Exception as e:
        print(f"❌ Ошибка отправки письма: {e}")
        return False


def login_view(request):
    """
    Контроллер авторизации пользователя
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name or user.email}!')
            return redirect('catalog:home')
        else:
            messages.error(request, 'Неверный email или пароль. Пожалуйста, попробуйте снова.')

    return render(request, 'users/login.html')


def logout_view(request):
    """
    Контроллер выхода пользователя
    """
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('catalog:home')


@login_required
def profile(request):
    """
    Контроллер профиля пользователя
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})