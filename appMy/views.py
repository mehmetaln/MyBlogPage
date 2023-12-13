from django.shortcuts import render
from appMy.models import *
from django.db.models import Count # count import etmek için 

# Create your views here.


def indexPage(request):
    
    blog_list =Blog.objects.all()
    blog_likes = Blog.objects.annotate(q_count = Count('likes')).order_by('-q_count') #annotate sayaç göevi görür # orderby ise neye göre ssıralamamız istiyorsaé 
    
    print(blog_likes)
    context={
        "blog_list": blog_list,
        "blog_likes": blog_likes[:5],
    }
    
    return render(request,"index.html",context)
