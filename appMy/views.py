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
        # icontains buradaki işlevi title içerisindeki kelimlerden veya harflerden birini yazsak bile bulunur       
        
    
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