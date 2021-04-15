from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo, Category, Permisions, MainPermisions
from django.http import HttpResponseRedirect
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

# from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.db import connection


def home(request):
    # s = SessionStore()
    # s['userid'] = 

    category2 = Todo.objects.filter(userId=1)
    todos = Todo.objects.all() #Fetch Models data
    todoscount = Todo.objects.count()
    completetodos = Todo.objects.filter(isCompleted=1).count()
    incompletetodos = Todo.objects.filter(isCompleted=0).count()
    category = Category.objects.all()


    return render(request, 'home.html', {'todos': todos , 'todoscount': todoscount, 'completetodos': completetodos, 'incompletetodos':incompletetodos, 'category':category })

def lhome(request):
    userid = request.user.id
    todos = Todo.objects.filter(userId=userid) #Fetch Models data
    todoscount = Todo.objects.filter(userId=userid).count()
    completetodos = Todo.objects.filter(isCompleted=1, userId=userid).count()
    incompletetodos = Todo.objects.filter(isCompleted=0, userId=userid).count()
    category = Category.objects.filter(userId=userid)


    return render(request, 'index.html', {'todos': todos , 'todoscount': todoscount, 'completetodos': completetodos, 'incompletetodos':incompletetodos, 'category':category })


def add(request):
    userid = request.user.id
    title = request.POST['title']
    description = request.POST['description']
    category = request.POST['category']
    compdate = request.POST['compdate']
    Todo.objects.create(title=title, description=description, category=category, compdate=compdate, userId=userid)

    return HttpResponseRedirect('/index')

def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('/index')

def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    
    todo.isCompleted = isCompleted

    todo.save()
    return redirect('/index')

def addcategory(request):
    userid = request.user.id
    name = request.POST['name']
    Category.objects.create(name=name, userId=userid)

    print(name)
    return HttpResponseRedirect('/index')

def deletecategory(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id)
    category.delete()

    return redirect('/index')

def permisions(request):
    userid = request.user.id
    # permisions = Permisions.objects.all()
    # permisions = Permisions.objects.filter(user_id=userid)
    # return render(request, 'permisions.html', {'permisions': permisions, 'userid':userid})

    # cursor = connection.cursor()
    # cursor.execute('SELECT name,user_id FROM `todoapp_mainpermisions` JOIN todoapp_permisions on todoapp_permisions.permisions_id=todoapp_mainpermisions.id WHERE user_id=userid')
    # cursor.execute('call whereclaused')
    # result = cursor.fetchall()
    # return render(request, 'permisions.html', {'permisions': result})
    allpermisions = MainPermisions.objects.all()
    for allpermision in allpermisions:
        print (allpermision)

    permisions = Permisions.objects.all().select_related('permisions_id').filter(user_id=userid)
    print (permisions)

    # for permision in permisions:
    #     print (permision.id, permision.permisions_id, permision.user_id)
    return render(request, 'permisions.html', {'permisions':permisions, 'allpermisions':allpermisions})

def addpermision(request):
    userid = request.user.id
    permisionid = request.POST['permision']
    # Permisions.objects.create(permisions_id=permisionid, userId=userid)

    print('you')
    print(id)
    print('user_id')
    print(userid)
    print('permision_id')
    print(permisionid)
    
    # Permisions.objects.create(permisions_id=id, user_id=userid)

    return HttpResponseRedirect('/permisions')

def filtertodos(request):
    userid = request.user.id
    name = request.GET['category']
    todos = Todo.objects.filter(category=name, userId=userid) #Fetch Models data
    todoscount = Todo.objects.count()
    completetodos = Todo.objects.filter(isCompleted=1).count()
    incompletetodos = Todo.objects.filter(isCompleted=0).count()
    category = Category.objects.filter(userId=userid)

    return render(request, 'index.html', {'todos': todos , 'todoscount': todoscount, 'completetodos': completetodos, 'incompletetodos':incompletetodos, 'category':category })

def filtertodosdate(request):

    userid = request.user.id
    datefilter = request.GET['date']
    todos = Todo.objects.filter(created_at=datefilter, userId=userid) #Fetch Models data
    todoscount = Todo.objects.count()
    completetodos = Todo.objects.filter(isCompleted=1).count()
    incompletetodos = Todo.objects.filter(isCompleted=0).count()
    category = Category.objects.filter(userId=userid)

    return render(request, 'index.html', {'todos': todos , 'todoscount': todoscount, 'completetodos': completetodos, 'incompletetodos':incompletetodos, 'category':category })

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['sname']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Usename Taken')
                return redirect ('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect ('register')

            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
        else:
            messages.info(request,'Passwords Donot Match')
            return redirect ('register')
        return redirect('/')

    else:
        return render(request,'register.html')

def userloginurl(request):
    return render(request,'login.html')
    
# Create your views here.
def logind(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print(request.user)

    if user is not None:
        login(request, user)
        print(login)
        # data = serializers.serialize(Todo.objects.all(), cls=login)
            # print(data)

        return redirect('/index')
        

        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
    # return render(request, 'register.html')

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')
