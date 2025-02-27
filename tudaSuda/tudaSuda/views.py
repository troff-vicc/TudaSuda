from django.http import HttpResponseRedirect
from django.shortcuts import render
from .sqlite import DateBase
from .forms import LoginForm, RegistrationForm, AddForm, EditForm
import json


def index(request):
    dateBase = DateBase()
    login = 'Войти'
    if request.COOKIES.get('id'):
        id = request.COOKIES.get('id')
        user_name = dateBase.execute(f"SELECT username FROM users WHERE id = '{id}'").fetchone()[0]
        login = user_name
    
    routes = dateBase.execute(
        f'''SELECT id, name, description, autor, img
        FROM route ORDER BY RANDOM() LIMIT 5'''
    ).fetchall()
    for i in range(len(routes)):
        img = json.loads(routes[i][-1])[0]
        autor = json.loads(routes[i][-2])[0]
        img = dateBase.execute(
            f'''SELECT img FROM images WHERE id = {img}'''
        ).fetchone()[0]
        autor = dateBase.execute(
            f'''SELECT username FROM users WHERE id = {autor}'''
        ).fetchone()[0]
        routes[i] = list(routes[i][:-2])+[autor]+[img[2:-1]]
    dateBase.close()
    return render(request, 'home.html', {'login': login, 'routes': routes})


def login(request):
    dateBase = DateBase()
    out = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            cur = dateBase.execute(f'''SELECT id, password from users WHERE username = "{name}" ''').fetchone()
            passwordTrue = cur
            if passwordTrue == []:
                dateBase.close()
                return HttpResponseRedirect('/registration')
            id = passwordTrue[0]
            if passwordTrue[1] == password:
                outt = HttpResponseRedirect('/')
                outt.set_cookie("id", id, max_age=7 * 24 * 60 * 60)
                return outt
            else:
                out = 'Неверный пароль'
    else:
        form = LoginForm()
    dateBase.close()
    return render(request, 'login.html', {'form': form, 'out': out})


def registration(request):
    dateBase = DateBase()
    def checkString(x):
        s = 'abcdefghijklmnopqrstuvwxyz_1234567890'
        x = x.lower()
        t = True
        for i in x:
            if not (i in s):
                t = False
        return t
    
    def checkName():
        cur = dateBase.execute(f'''SELECT username from users WHERE username = "{name}" ''').fetchone()
        if cur == []:
            if checkString(name):
                return [True, '']
            else:
                return [False, 'Логин может состоять из латиницы, чисел или нижнего подчёркивания ']
        else:
            return [False, 'Логин уже занят']
    
    out = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']
            if len(password) >= 8 and password1 == password:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                # email = email.replace('@', '|')
                checkName = checkName()
                if checkName[0]:
                    cur = dateBase.execute(f'''SELECT username from users;''').fetchall()
                    dateBase.execute(f"""INSERT INTO users VALUES({len(cur)}, {name}, {email}, {password}, NONE, NONE, NONE);""")
                    dateBase.commit()
                    dateBase.close()
                    return HttpResponseRedirect('/login')
                else:
                    out = checkName[1]
            else:
                if password1 != password:
                    out = 'Пароли не совпадают'
                else:
                    out = 'Пароль должен быть длинее 8 символов'
    else:
        form = RegistrationForm()
    dateBase.close()
    return render(request, 'registration.html', {'form': form, 'out': out})


def profile(request):
    if request.COOKIES.get('id'):
        id = request.COOKIES.get('id')
    else:
        return HttpResponseRedirect('/')
    
    dateBase = DateBase()
    userList = list(dateBase.execute(f"SELECT username, description, img, route, id, email FROM users WHERE id = '{id}'").fetchone())
    img = json.loads(userList[2])[0]
    img = dateBase.execute(
        f'''SELECT img FROM images WHERE id = {img}'''
    ).fetchone()[0]
    userList[2] = img[2:-1]
    routesID = json.loads(userList[3])
    routesS = []
    for ID in routesID:
        routes = dateBase.execute(
            f'''SELECT id, name, description, autor, img
                    FROM route WHERE id="{ID}" '''
        ).fetchone()
        img = json.loads(routes[-1])[0]
        autor = json.loads(routes[-2])[0]
        img = dateBase.execute(
            f'''SELECT img FROM images WHERE id = {img}'''
        ).fetchone()[0]
        autor = dateBase.execute(
            f'''SELECT username FROM users WHERE id = {autor}'''
        ).fetchone()[0]
        routes = list(routes[:-2]) + [autor] + [img[2:-1]]
        routesS.append(routes)
    dateBase.close()
    return render(request, 'profile.html', {'userList': userList, "routes": routesS})


def add(request):
    if request.COOKIES.get('id'):
        id = request.COOKIES.get('id')
    else:
        return HttpResponseRedirect('/')
    
    dateBase = DateBase()
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            cur = dateBase.execute(f'''SELECT id from route;''').fetchall()
            dateBase.execute(
                f"""INSERT INTO route (name, description, private)
                VALUES("{form.name}", "{form.description}", "{form.private}");""")
            dateBase.commit()
            dateBase.close()
    else:
        form = AddForm()
    return render(request, 'add.html', {'form': form})


def edit(request, id):
    if request.COOKIES.get('id') != str(id):
        return HttpResponseRedirect('/')
    
    dateBase = DateBase()
    
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            import base64, json
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            img_file = form.cleaned_data['img_file']
            image_64_encode = base64.b64encode(img_file.read())
            imgLen = int(dateBase.execute("""SELECT id FROM images ORDER BY id DESC LIMIT 1;""").fetchone()[0])+1
            dateBase.execute(
                f"""INSERT INTO images (id, img, autor)
                                        VALUES({imgLen}, "{image_64_encode}", "{id}");""")
            dataJson = json.dumps([f'{imgLen}'])
            dateBase.execute(f"""UPDATE users
                SET email = '{email}',
                    description = '{description}',
                    img = '{dataJson}'
                WHERE id = {id}; """
                             )
            dateBase.commit()
            dateBase.close()
            return HttpResponseRedirect('/profile')
        else:
            return HttpResponseRedirect('/profile')
    else:
        userList = list(
            dateBase.execute(f"SELECT username, description, email FROM users WHERE id = '{id}'").fetchone()
        )
        form = EditForm(my_arg=userList[1:])
    
    return render(request, 'edit.html', {'form': form, 'userList': userList})
    


def map(request):
    return render(request, 'map.html')