from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Node, BonusSettings, BonusType, Bonus, PropertyValueSettings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.db.models import Sum


def index(request):
    return render(request, 'account/login.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('account:home')
        else:
            return render(request, 'account/login.html', {'alert': "Неверный логин или пароль"})
    else:
        return render(request, 'account/login.html')


def signup(request):
    if request.method == "POST":
        inviter = request.POST.get('inviter')
        email_phone = request.POST.get('email_phone')
        tree_parent = request.POST.get('parent_id')
        username = request.POST.get('username')
        password = request.POST.get('user_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        city = request.POST.get('city')
        country = request.POST.get('country')
        address = request.POST.get('address')

        if '@' in email_phone:
            email = email_phone
            phone = ''
        else:
            email = ''
            phone = email_phone

        if inviter == '':
            return render(request, 'account/signup.html', {'alert': "Регистрируйтесь по реферальной ссылке",
                                                           'inviter': inviter})

        inviter_node = get_object_or_404(Node, pk=int(inviter))
        if inviter_node.status == 0:
            return render(request, 'account/signup.html', {'alert': "Реферальная ссылка неактивна",
                                                           'inviter': inviter})

        username_exists = User.objects.filter(username__iexact=username).exists()
        if username_exists:
            return render(request, 'account/signup.html', {'alert': "Такой логин существует в системе",
                                                           'inviter': inviter})

        if tree_parent == '':
            return render(request, 'account/signup.html', {'alert': "Укажите parent id",
                                                           'inviter': inviter})
            # auto define node
            # node = get_object_or_404(Node, inviter=inviter_node)
            # left_node, left_count = get_tree_parent_node(node, False, 0)
            # right_node, right_count = get_tree_parent_node(node, True, 0)
            # if left_count > right_count:
            #    parent_node = right_node
            #    is_right = True
            # else:
            #    parent_node = left_node
            #    is_right = False
        else:
            parent_node = get_object_or_404(Node, pk=int(tree_parent))
            if parent_node.children.count() > 5:
                return render(request, 'account/signup.html',
                              {'alert': "Данный tree parent занят", 'inviter': inviter})

        try:
            with transaction.atomic():
                node, user, user_profile = save_registration(address, city, country, username, email, first_name,
                                                             last_name, middle_name, parent_node, password, phone, inviter_node)
        except IntegrityError:
            return render(request, 'account/signup.html', {'alert': "Ошибка при регистрации",
                                                           'inviter': inviter})

        if user and user_profile and node:
            login(request, user)
            return redirect('account:home')
        else:
            return render(request, 'account/signup.html', {'alert': "Ошибка регистрации",
                                                           'inviter': inviter})
    else:
        inviter = ''
        if request.GET.get('inviter'):
            inviter = request.GET.get('inviter')
        return render(request, 'account/signup.html', {'inviter': inviter})


def get_tree_parent_node(node, is_right, count):
    try:
        child = Node.objects.get(parent=node, is_right=is_right)
    except Node.DoesNotExist:
        return node, count
    count = count + 1
    return get_tree_parent_node(child, is_right, count)


def save_registration(address, city, country, username, email, first_name, last_name, middle_name,
                      parent_node, password, phone, inviter):

    user = User(username=username, email=email, first_name=first_name, last_name=last_name, is_staff=1)
    user.set_password(password)
    user.save()

    node = Node.objects.create(user=user, address=address, country=country, city=city, middle_name=middle_name, phone=phone, parent=parent_node,
                               inviter=inviter)

    # calculate_bonus(node, inviter)

    return node, user


def calculate_bonus():
    value_settings = get_object_or_404(PropertyValueSettings, name='pv_som')
    pv_value_som = int(value_settings.value)
    # nodes = Node.objects.filter(pk__gt=int(value_settings.value)).order_by('id')
    nodes = Node.objects.filter(status=1, is_processed=0).order_by('id')
    bonus_settings = BonusSettings.objects.all()
    bonus_types = BonusType.objects.all()
    recommendation_type = bonus_types.get(code=1)
    cycle_type = bonus_types.get(code=3)
    cycle_bonus_value = bonus_settings.get(bonus_type=cycle_type, level=1).bonus_value
    # last_node_id = 0
    for node in nodes:
        # last_node_id = node.pk
        calculate_recommendation_bonus(node, recommendation_type)
        calculate_parent_bonus(cycle_type, node, node, cycle_bonus_value, pv_value_som)
        node.is_processed = 1
        node.save()
    # if last_node_id > 0:
    #    value_settings.value = last_node_id
    #    value_settings.save()


def calculate_recommendation_bonus(node, recommendation_type):
    inviter = node.inviter
    recommendation_bonus_value = node.package.recommendation_bonus_usd
    if inviter is None:
        return
    if inviter.status == 1:
        Bonus.objects.create(node=inviter, value=recommendation_bonus_value, partner=node, type=recommendation_type.name, currency='usd')
        if inviter.bonus is None:
            inviter.bonus = recommendation_bonus_value
        else:
            inviter.bonus = inviter.bonus + recommendation_bonus_value
        inviter.save()


def calculate_parent_bonus(cycle_type, node, partner, cycle_bonus_value, pv_value_som):
    price_som = node.package.price_som
    is_right = node.is_right
    parent = node.parent
    if parent is None:
        return
    if parent.status == 1:
        if is_right:
            parent.right_point = parent.right_point + (parent.package.percent * price_som)/(100 * pv_value_som)
        else:
            parent.left_point = parent.left_point + (parent.package.percent * price_som)/(100 * pv_value_som)
        pv_bonus = 0
        if parent.right_point > parent.left_point:
            pv_bonus = parent.left_point
        elif parent.right_point < parent.left_point:
            pv_bonus = parent.right_point
        else:
            pv_bonus = parent.right_point
        if pv_bonus > 0:
            if parent.right_point is None:
                parent.right_point = 0
            if parent.left_point is None:
                parent.left_point = 0
            if parent.bonus is None:
                parent.bonus = 0
            parent.right_point = parent.right_point - pv_bonus
            parent.left_point = parent.left_point - pv_bonus
            bonus = pv_bonus * cycle_bonus_value
            parent.bonus = parent.bonus + bonus
            Bonus.objects.create(node=parent, value=bonus, partner=partner, type=cycle_type.name, currency='usd')
        parent.save()
    return calculate_parent_bonus(cycle_type, parent, partner, cycle_bonus_value, pv_value_som)


def validate_username_ajax(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Такой логин существует в системе'
    return JsonResponse(data)


@login_required
def user_logout(request):
    logout(request)
    return redirect('account:user_login')


@login_required
def home(request):
    user = request.user
    return render(request, 'account/home.html', {'node': user.node, 'user': user, 'profile': user.userprofile})


@login_required
def structure(request):
    user = request.user
    node = user.node
    nodes = node.get_descendants(include_self=True)
    return render(request, 'account/structure.html', {'node': node, 'nodes': nodes})


@login_required
def invited(request):
    user = request.user
    node = user.node
    nodes = Node.objects.filter(inviter=node)
    return render(request, 'account/invited.html', {'node': node, 'nodes': nodes})


@login_required
def invited_ajax(request):
    user = request.user
    level = int(request.GET.get('level'))
    s = 1
    ids = Node.objects.filter(inviter=user.node).values_list('inviter_id', flat=True)
    while s < level:
        s = s + 1
        ids = Node.objects.filter(inviter__pk__in=ids).values_list('inviter_id', flat=True)
    nodes = Node.objects.filter(inviter__pk__in=ids)
    return render(request, 'account/invited_ajax.html', {'nodes': nodes})


@login_required
def bonus_history(request):
    user = request.user
    node = user.node
    history = Bonus.objects.filter(node=node).order_by('-created_date')
    total_sum = Bonus.objects.filter(node=node).aggregate(Sum('value'))['value__sum'] or 0.00
    return render(request, 'account/bonus_history.html', {'node': node, 'total_sum': total_sum, 'history': history})


@login_required
def documentation(request):
    user = request.user
    return render(request, 'account/documentation.html', {'node': user.node})


@login_required
def notifications(request):
    user = request.user
    return render(request, 'account/notifications.html', {'node': user.node})
