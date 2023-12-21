from django.shortcuts import render, redirect # yönlendirme redirect istediğimiz sayfada kullanabiliyoruz 
from appMy.models import *
from django.db.models import Count # count import etmek için count sayma işlemlerinde işimze yarıyor
from django.db.models import Q     # veya (|) baglacını kullanmamız ayarayan  kütüphane
from django.contrib.auth import authenticate, login, logout    # auth tüm kullancı işlemlerini çekmemize yarayan kütüphane
from django.contrib.auth.models import User    # Django kullanıcı için
from django.contrib import messages # Hata mesajı gibi şeyleri almamıza ayarayan kütüphane kullanıcıya mesaj göndermemize yarar 


# Create your views here.


def indexPage(request):
    # blogs = Comment.objects.values("blog__title").annotate(comments= Count('blog'))
    # print(blogs)
    
    blog_list =Blog.objects.all().order_by('-id')
    
    # Sidenav ile alakalı bölüm
    blog_likes = Blog.objects.annotate(q_count = Count('likes')).order_by('-q_count') #annotate sayaç göevi görür # orderby ise neye göre ssıralamamız istiyorsa
    blog_random_list =Blog.objects.all().order_by('?')                            # buradaki soru işareti bize rastgele bir blog yazısı çekmesini söylüyor
    blog_comments = Blog.objects.all().order_by('-comment_num')
    
    print(blog_likes)
    context={
        "blog_list": blog_list,
        "blog_likes": blog_likes[:5],
        "blog_random_list" : blog_random_list[:4], # rastgele en fazla kaç tane çekebileceğimizi gösteriyor
        "blog_comments":blog_comments[:4],
    }
    
    return render(request,"index.html",context)

def detailPage(request, bid):

    
    blog = Blog.objects.get(id=bid)
    comment_list = Comment.objects.filter(blog=blog)
   
   
    if request.method == "POST":
        text = request.POST.get("text")
       #request.user girişli olan kullanıcı 
        comment = Comment(text=text, blog=blog, user= request.user)    
        comment.save()
        
        blog.comment_num +=1
        blog.save()
        
                                             
    context = {
      "blog":blog,
      "comment_list":comment_list,
      "blog_likes" : Blog.objects.annotate(q_count = Count('likes')).order_by('-q_count')[:5], #annotate sayaç göevi görür # orderby ise neye göre ssıralamamız istiyorsa
      "blog_random_list" : Blog.objects.all().order_by('?')[:4],                            # buradaki soru işareti bize rastgele bir blog yazısı çekmesini söylüyor
      "blog_comments" : Blog.objects.all().order_by('-comment_num')[:4],

   }
    return render(request, "detail.html", context)



def contactPage(request):
    
    if  request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        text = request.POST.get("text")
        
        
        contact = Contact(fullname=fullname, email= email, title=subject, text=text)
        contact.save()
    
    context = {}
    return render(request, "contact.html",context)



def blogallPage(request, cslug=None):
    
    if cslug:
        blog_list =Blog.objects.filter(category__slug = cslug).order_by('-id')
    else:
            
        blog_list =Blog.objects.all().order_by('-id')
    
    query = request.GET.get("query") 
    # formu GET methodu   ile çkeiyoruz ve içerisinden get ile name = query çekiyoruz   
    if query:
        blog_list=Blog.objects.filter(  Q(title__icontains = query) | Q(text__icontains = query))  
        # icontains buradaki işlevi title içerisindeki kelimlerden veya harflerden birini yazsak bile bulunur      Q veya bağlacını kullanmamıza yarar
        
    
    category_list = Category.objects.all()
    
    context = {
         "blog_list": blog_list,
         "category_list": category_list
    }
    return render(request, "blogall.html",context)  



# USER VİEVS

def loginPage(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user =authenticate(username =username, password=password) #Kullanıcın adı ve şifresi dogrumu degil kontrol etmemize yarar yanlışsa None döndürür
        if user:
            login(request, user)
        # else:           hata mesajı olacak elsede şimdilik yok
            return redirect ("indexPage")
        
        else: 
           messages.error(request,"Kullanıcı adı veya Şifre yanlış")
             # [] message bir listedir ve html? sayfasında for ile döndürülmelidir.
             
        
    
    context= {}
    return render(request,"User/login.html",context)


def logoutUser(request):
    logout(request) # Çıkış fonksiyonumuz
    return redirect("loginPage")

def registerPage(request):
    
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        # Böyle bir kullanıcı yoksa kaydet var mı diye kontrol et
        boolup =boolmum =False 
        boolchar = True
        if password1 == password2:
            nonchar = ["*;:@?.,"]
            for i in password1:
                if i.isupper():
                    boolup = True
                if i.isnumeric():
                    boolmum = True
                if i in nonchar:
                    boolchar = False
            if boolup and boolmum and boolchar and le(password1)>=6:
                if not User.objects.filter(username=username).exists(): # Exists bize içerisinde bir kullanıcı varmı yokmu dşye kontrol ediyor varsa True dönderiri yoksa False
                    if not User.objects.filter(email=email).exists():   # Not burada True degerini false çevirmemize yarıyor yani bölyel bir mail veya kullanıcı olmadığı için kayıt yaoamay ahazır demke istiyor bize
                        # Kaydetme işlemleri
                        # Kullanıcı kaydederken bu şekilde yazıyoruz tğm şartlar sağlanırsa kayıt oluşur 
                        user = User.objects.create_user(first_name = fname, last_name = lname, email=email, username=username, password = password1 )   
                        user.save()
                        return redirect("loginPage")
                    else:
                        messages.error(request,"Bu email zaten kullanılıyor!!")
                else:
                    messages.error(request,"Bu Kullanıcı adı  zaten kullanılıyor!!")
            else: 
                messages.error(request, "Şifrenizde büyük harf ,rakam ve en az 6 karekterden oluşmalı")
                messages.error(request, f"{nonchar} bu karekterleri kullanmayınız")
        else:
            messages.error(request,"Şifreler Uyuşmuyor!!")
    
    
    
    
    
    
    
    
    context={}
    return render(request, "user/register.html", context)