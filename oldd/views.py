from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


def home(request):
    bb = Category.objects.all()
    return render(request, 'tem/index.html', {'bb': bb})


def about_us(request):
    bb = Category.objects.all()
    return render(request, 'tem/about.html',{'bb':bb})


@login_required
def about_us_admin(request):
    bb = Category.objects.all()
    return render(request, 'tem/about_us_admin.html', {'bb': bb})


def new_arrivals(request):
    bb = Category.objects.all()
    zz = Product.objects.all().order_by('-id')[:1]
    return render(request, 'new_arrivals.html', {'bb': bb,'zz':zz})


def daily_needs(request):
    bb = Category.objects.all()
    return render(request, 'daily_needs.html', {'bb': bb})


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if w.user.email == email and w.user_role == 'user':
                messages.success(request, 'You have already registered. Please login')
                return redirect('register')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')

        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('register')

        user = User.objects.create_user(username=user_name, email=email, password=psw, first_name=first_name,last_name=last_name)
        user.save()

        reg = Registration()
        reg.password = psw
        reg.user_role = 'admin'
        reg.user = user
        reg.save()
        messages.success(request, 'You have successfully registered')
        return redirect('home')
    else:
        return render(request, 'register.html')


@login_required
def upd_pr_adm(request):
    bb1 = Registration.objects.get(user_role = 'admin')
    rtrk = bb1.user.pk
    um = User.objects.get(id=rtrk)
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        em = request.POST.get('em')
        psw = request.POST.get('psw')

        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username=um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'upd_pr_adm.html', {'bb1': bb1, 'um': um})

        passwor = make_password(psw)
        df = Registration.objects.get(id = request.session['logg'])
        kmk = df.user.pk
        kmk = User.objects.get(id=kmk)
        kmk.username = user_name
        kmk.first_name = first
        kmk.last_name = last
        kmk.password = passwor
        kmk.email = em
        kmk.save()

        user = auth.authenticate(username=user_name, password=psw)
        auth.login(request, user)

        dcd = Registration.objects.get(user_role='admin')
        b = dcd.id
        m = int(b)
        request.session['logg'] = m

        dcd = Registration.objects.get(id = request.session['logg'])
        dcd.password = psw
        dcd.user = kmk
        dcd.save()

        messages.success(request, 'You have successfully updated your profile')
        return redirect('admin_home')
    return render(request, 'upd_pr_adm.html', {'bb1': bb1, 'um': um})


def login(request):
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'Invalid credentials')
            return render(request, 'login.html')
        auth.login(request, user)
        if Registration.objects.filter(user = user, password = password).exists():
            logs = Registration.objects.filter(user = user, password = password)
            for value in logs:
                user_id = value.id
                usertype  = value.user_role
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    return redirect('admin_home')
                elif usertype == 'user':
                    request.session['logg'] = user_id
                    return redirect('user_home')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return redirect('login')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required
def admin_home(request):
    bb = Category.objects.all()
    return render(request,'admin_home.html',{'bb':bb})


@login_required
def cat_admin(request):
    mkk = Category.objects.all()
    return render(request,'cat_admin.html',{'mkk':mkk})


@login_required
def add_cat_admin(request):
    if request.method == 'POST':
        cat = request.POST.get('cat')
        if Category.objects.filter(category_title = cat).exists():
            messages.success(request, 'Category exists')
            return redirect('add_cat_admin')
        imgg = request.FILES['imgg']
        fs = FileSystemStorage()
        fs.save(imgg.name, imgg)
        gh = Category()
        gh.category_title = cat
        gh.photo = imgg
        gh.save()
        messages.success(request, 'Category added successfully')
        return redirect('cat_admin')
    return render(request,'add_cat_admin.html')


@login_required
def edit_cat_admin(request, id):
    gh = Category.objects.get(id = id)
    if request.method == 'POST':
        try:
            cat = request.POST.get('cat')
            imgg = request.FILES['imgg']
            fs = FileSystemStorage()
            fs.save(imgg.name, imgg)
            gh.category_title = cat
            gh.photo = imgg
            gh.save()
        except:
            cat = request.POST.get('cat')
            imgg1 = request.POST.get('imgg1')
            gh.category_title = cat
            gh.photo = imgg1
            gh.save()
        messages.success(request, 'Category edited successfully')
        return redirect('cat_admin')
    return render(request, 'edit_cat_admin.html', {'gh': gh})


@login_required
def delete_cat_admin(request, id):
    Category.objects.get(id = id).delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('cat_admin')


@login_required
def cat_product_admin(request, id):
    id = int(id)
    request.session['catt_adm'] = id
    hh = Product.objects.filter(prd_cat = id)
    return render(request, 'cat_product_admin.html', {'hh': hh})


@login_required
def add_prod_adm(request):
    kkp = Category.objects.get(id = request.session['catt_adm'])
    if request.method == 'POST':
        pro_nam = request.POST.get('pro_nam')
        imgg = request.FILES['imgg']
        fs = FileSystemStorage()
        fs.save(imgg.name, imgg)
        uni_pri = request.POST.get('uni_pri')
        disc = request.POST.get('disc')
        if Product.objects.filter(prd_cat = kkp, name = pro_nam).exists():
            messages.success(request, 'Product already exists')
            redd = '/cat_product_admin/' + str(kkp.id)
            return redirect(redd)

        cdt = Product()
        cdt.name = pro_nam
        cdt.discount = disc
        cdt.image = imgg
        cdt.unit_price = uni_pri
        cdt.prd_cat = kkp
        cdt.save()

        messages.success(request, 'Product added successfully')
        redd = '/cat_product_admin/' + str(kkp.id)
        return redirect(redd)
    return render(request,'add_prod_adm.html',{'kkp':kkp})


@login_required
def edit_prod_adm(request, id):
    kkp = Category.objects.get(id = request.session['catt_adm'])
    gh = Product.objects.get(id = id)
    ghd = int(gh.id)
    if request.method == 'POST':
        try:
            pro_nam = request.POST.get('pro_nam')
            imgg = request.FILES['imgg']
            fs = FileSystemStorage()
            fs.save(imgg.name, imgg)
            uni_pri = request.POST.get('uni_pri')
            disc = request.POST.get('disc')
            filt_quer = Product.objects.filter(prd_cat=kkp, name=pro_nam).exclude(id = ghd)
            if filt_quer.exists():
                messages.success(request, 'Product already exists')
                redd = '/cat_product_admin/' + str(kkp.id)
                return redirect(redd)
            gh.name = pro_nam
            gh.discount = disc
            gh.image = imgg
            gh.unit_price = uni_pri
            gh.prd_cat = kkp
            gh.save()

        except:

            pro_nam = request.POST.get('pro_nam')
            imgg1 = request.POST.get('imgg1')
            uni_pri = request.POST.get('uni_pri')
            disc = request.POST.get('disc')
            filt_quer = Product.objects.filter(prd_cat=kkp, name=pro_nam).exclude(id=ghd)
            if filt_quer.exists():
                messages.success(request, 'Product already exists')
                redd = '/cat_product_admin/' + str(kkp.id)
                return redirect(redd)
            gh.name = pro_nam
            gh.discount = disc
            gh.image = imgg1
            gh.unit_price = uni_pri
            gh.prd_cat = kkp
            gh.save()


        messages.success(request, 'Product edited successfully')
        redd = '/cat_product_admin/' + str(kkp.id)
        return redirect(redd)
    return render(request,'edit_prod_adm.html',{'gh':gh,'kkp':kkp})


@login_required
def delete_prod_adm(request, id):
    kkp = Category.objects.get(id=request.session['catt_adm'])
    Product.objects.get(id=id).delete()
    messages.success(request, 'Product deleted successfully')
    redd = '/cat_product_admin/' + str(kkp.id)
    return redirect(redd)


def product_view(request, id):
    bb = Category.objects.all()
    catt = Category.objects.get(id = id)
    cdc = Product.objects.filter(prd_cat=id)
    return render(request, 'product_view.html', {'cdc': cdc,'catt':catt,'bb':bb})


def surgical_view(request):
    bb = Category.objects.all()
    return render(request, 'surgical_view.html',{'bb':bb})


def syrin_disp(request):
    bb = Category.objects.all()
    return render(request, 'syrin_disp.html', {'bb': bb})


def belts_and_supports(request):
    bb = Category.objects.all()
    return render(request, 'belts_and_supports.html', {'bb': bb})


def supports_products(request):
    bb = Category.objects.all()
    return render(request, 'supports_products.html', {'bb': bb})


def gloves(request):
    bb = Category.objects.all()
    return render(request, 'gloves.html', {'bb': bb})


def dressings_and_bandaids(request):
    bb = Category.objects.all()
    return render(request, 'dressings_and_bandaids.html', {'bb': bb})


def hot_water_bags(request):
    bb = Category.objects.all()
    return render(request, 'hot_water_bags.html', {'bb': bb})


def thermometers(request):
    bb = Category.objects.all()
    return render(request, 'thermometers.html', {'bb': bb})


def stethescopes(request):
    bb = Category.objects.all()
    return render(request, 'stethescopes.html', {'bb': bb})


def nebulizers(request):
    bb = Category.objects.all()
    return render(request, 'nebulizers.html', {'bb': bb})


def bp_apparatus(request):
    bb = Category.objects.all()
    return render(request, 'bp_apparatus.html', {'bb': bb})


def diapers(request):
    bb = Category.objects.all()
    return render(request, 'diapers.html', {'bb': bb})


def hygiene_products(request):
    bb = Category.objects.all()
    return render(request, 'hygiene_products.html', {'bb': bb})


def new_mother_and_baby_products(request):
    bb = Category.objects.all()
    return render(request, 'new_mother_and_baby_products.html', {'bb': bb})


def masks(request):
    bb = Category.objects.all()
    return render(request, 'masks.html', {'bb': bb})


def vaporizers(request):
    bb = Category.objects.all()
    return render(request, 'vaporizers.html', {'bb': bb})


def cotton(request):
    bb = Category.objects.all()
    return render(request, 'cotton.html', {'bb': bb})


def beauty_products(request):
    bb = Category.objects.all()
    return render(request, 'beauty_products.html', {'bb': bb})


def other_products(request):
    bb = Category.objects.all()
    return render(request, 'other_products.html', {'bb': bb})


def logout(request):
    auth.logout(request)
    return redirect('home')