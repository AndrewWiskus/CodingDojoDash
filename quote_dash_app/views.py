from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, QuotePost

def index(request):
    return render(request, "login.html")

def dash(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        'all_quotes':QuotePost.objects.all()
    }
    return render(request, "dash.html", context)

def edit_account(request, user_id):
    context={
        'user':User.objects.get(id=user_id)
    }
    return render(request, 'edit_account.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')


# CREATE A USER
def register(request):
    if request.method=='POST':
        # VALIDATE
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        # ENCRYPTING PASSWORD
        user_pw=request.POST['pw']
        # HASH PASSWORD
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"

        return redirect('/dash')
    return redirect('/')


# UPDATE USER
def update(request, user_id):
    user_account=User.objects.get(id=user_id)

    # VALIDATE
    errors=User.objects.validator(request.POST)
    if errors:
        for error in errors:
            if user_account.email != request.POST['email'] or (user_account.email == request.POST['email'] and errors[error] != 'duplicate_email'):
                messages.error(request, errors[error])

                context={
                    'user':User.objects.get(id=user_id)
                }
                return render(request, "edit_account.html", context)
            
    user_account.first_name=request.POST['f_n']
    user_account.last_name=request.POST['l_n']
    user_account.email=request.POST['email']
    user_account.save()
    user_account=User.objects.get(id=user_id)
    request.session['user_name']=f"{user_account.first_name} {user_account.last_name}"
    context={
        'user':User.objects.get(id=user_id)
    }
    return render(request, "edit_account.html", context)
    
def like(request, user_id, quote_id):
    user_account=User.objects.get(id=user_id)
    quote=QuotePost.objects.get(id=quote_id)
    quote.likes.add(user_account)
    # context={
    #     'all_quotes':QuotePost.objects.all()
    # }
    return redirect('/dash')


# LOG IN
def login(request): 
    if request.method=='POST':
        # QUERY
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            # COMPARE PASSWORDS
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/dash')
    return redirect('/')


# DASH FUNCTIONALITY
def create_quote(request):
    if request.method=='POST':
        errors=QuotePost.objects.quote_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/dash')
        QuotePost.objects.create(author=request.POST['author'], content=request.POST['content'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/dash')
    return redirect('/')


def user_quotes(request, user_id):
    context={
        'user':User.objects.get(id=user_id)
    }
    return render(request, 'user_quotes.html', context)


# DESTROY
def delete_quote(request, quote_id):
    QuotePost.objects.get(id=quote_id).delete()
    return redirect('/dash')
