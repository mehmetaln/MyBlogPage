from django.shortcuts import render
from appMy.models import *
from django.db.models import Count # count import etmek için 

# Create your views here.


def indexPage(request):
    # blogs = Comment.objects.values("blog__title").annotate(comments= Count('blog'))
    # print(blogs)
    
    blog_list =Blog.objects.all().order_by('-id')
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
      "comment_list":comment_list

   }
   return render(request, "detail.html", context)