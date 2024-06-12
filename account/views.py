from django.contrib import messages, auth
from django.shortcuts import render, redirect
from account.models import User


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(
            username=username,
            password=password
        )

        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Здравствуйте {request.user.first_name}")
            return redirect('home')
    return render(request, 'account/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        second_name = request.POST.get('second_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if len(password1) >= 6:
                if User.objects.filter(phone=phone).exists():
                    messages.error(request, "Данный номер уже зарегистрирован!")
                    return redirect('register')
                else:
                    if phone[0] == '+' and len(phone) > 9:
                        if User.objects.filter(email=email).exists():
                            messages.error(request, "Данная почта уже зарегистрирована!")
                        else:
                            user = User.objects.create_user(
                                first_name=first_name,
                                last_name=last_name,
                                second_name=second_name,
                                email=email,
                                phone=phone,
                                password=password1,
                            )
                            user.save()

                            messages.success(request, "Успешная регистрация!")

                            return redirect("login")
                    else:
                        messages.error(request, "Некорректный формат номера!")
            else:
                messages.error(request, "Длина пароля должно быть больше либо равно 6!")
                return redirect('register')
        else:
            messages.error(request, "Пароли должны совпадать!")
            return redirect('register')

    return render(request, 'account/register.html')


def logout(request):
    auth.logout(request)
    messages.success(request, "Вы вышли из аккаунта")

    return redirect("home")


def dashboard(request):
    pass
