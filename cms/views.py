import datetime
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .forms import DeclarationForm
from .models import Fruit, Bank, Logging, Declaration
from users.forms import UserLoginForm
from django.contrib.auth import authenticate, login
from users.models import Chat
from cms.tasks import task_check_warehouse, task_buy_fruits, task_sell_fruits
from django.core.cache import cache
from django.contrib import messages


class MainPage(View):
    form = UserLoginForm
    file_form = DeclarationForm
    room_name = 'warehouse'

    def post(self, request):
        form = self.form(request.POST)
        file_form = self.file_form(request.POST, request.FILES)
        if request.FILES:
            if file_form.is_valid():
                file_form.save()
                messages.success(request, 'Файл успешно загружен')
            else:
                messages.error(request, file_form.error_messages.get('error_file'))
                return HttpResponseRedirect(reverse_lazy('home'))
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('home'))
            messages.error(request, 'Не верный логин или пароль')
            return HttpResponseRedirect(reverse_lazy('home'))
        return HttpResponseRedirect(reverse_lazy('home'))

    def get(self, request):
        context = {
            'form': self.form(),
            'file_form': self.file_form(),
            'fruits': Fruit.objects.all(),
            'bank': Bank.objects.first(),
            'history_chat': Chat.objects.select_related('user').order_by('-id')[:40],
            'room_name': self.room_name,
            'current_data': datetime.datetime.now(),
            'history_logging': Logging.objects.select_related('fruit').order_by('-id')[:100],
            'yesterday': datetime.datetime.now() - datetime.timedelta(days=1),
            'declaration_count': Declaration.objects.filter(date=datetime.datetime.now()).count()
        }

        return render(request, 'cms/layout.html', context)


def transactions(request):
    if request.is_ajax():
        balance = None  # noqa
        value = request.GET.get('value')
        flag = True if request.GET.get('flag') == 'true' else False
        if flag and value:
            bank = Bank.objects.first()
            bank.balance += int(value)
            bank.save()
            balance = bank.balance
        elif value:
            bank = Bank.objects.first()
            if bank.balance >= int(value):
                bank.balance -= int(value)
                bank.save()
                balance = bank.balance
            else:
                return JsonResponse({'message': 'Недостаточно средств', 'status': 400})

        else:
            return JsonResponse({'message': 'Ошибка транзакции', 'status': 400})
        return JsonResponse({'message': 'Операция успешна', 'balance': balance, 'status': 200})


def audit(request):
    if request.is_ajax():
        if cache.get(request.user.id):
            return JsonResponse({'status': 202})
        else:
            task = task_check_warehouse.delay(request.user.id)
            cache.set(request.user.id, task)
            return JsonResponse({'message': 'success', 'task_id': task.task_id, 'status': 200})


def warehouse(request):
    if request.is_ajax():
        try:
            value = request.GET.get('value')
            types = request.GET.get('type')
            count = request.GET.get('count')
            if types == "buy":
                task_buy_fruits.delay(value, count)
            if types == "sell":
                task_sell_fruits.delay(value, count)
            else:
                return JsonResponse({'status': 400})
            return JsonResponse({'status': 200})
        except Exception as exp:
            print(exp)
            return JsonResponse({'status': 400})
