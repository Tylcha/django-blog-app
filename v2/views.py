from django.shortcuts import render, get_object_or_404, HttpResponseRedirect,redirect
#from django.views.generic import TemplateView #classlarda
from v2.models import Post, Category, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #paginator icin
from django.db.models import Q #arama cubugu icin
from v2.forms import CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

#from django.http import HttpResponse
#def anasayfa(request):
#    return HttpResponse(request,'templates/index.html')

def anasayfa(request):
    context = dict() #  dict olarak tanimladik 
    post_list = Post.objects.all() #butun postlari atadik

    #arama cubugu
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(user__first_name__icontains=query)
        ).distinct() #butun sonuclari gonder postlistle title content ve usera gore arama yapma
    
    
    paginator = Paginator(post_list, 6) #bir sayfada 6 tane
    
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.page_number)

    context['posts'] = posts #butun postlari atadik 'posts' olarak deger soldaki templatede bakmak icin    
    context['cat'] = Category.objects.all()
    return render(request, 'index.html', context) #requeste(gelen istege)indexe postu gonderdik

def post_detail(request, slug): 
    post = get_object_or_404(Post, slug=slug) #hazir modul
    form = CommentForm(request.POST or None)

    if form.is_valid(): #formun gecerliligini sorguladik
        comment = form.save(commit=False)
        comment.post = post
        comment.save() #save edilio
        return HttpResponseRedirect(post.get_absolute_url())#sayfayi tekrar dondurmemiz gerekio

    context = {
        'post':post, #  tek post gostermek icin
        'posts':Post.objects.all(), #post hepsi kayanbar icin
        'cat':Category.objects.all(),
        'form':form,
    }
    return render(request, 'partials/detailpost.html', context) #request tek post detail gonderdik

def category_show(request, category_slug):
    context = dict()
    context['category'] = get_object_or_404(
        Category, slug=category_slug,
    )
    context['items'] = Post.objects.filter(
        category=context['category']   
    )
    return render(request,'partials/categori.html',context)


def add_comment_to_post(request,pk): #post pk
    post=Post.get_object_or_404(Post, pk=pk)

    if request.POST == "POST": #Post olup olmadigini sorguluyoruz
        form =CommentForm(request.POST) #eslescegi yer
        if form.is_valid(): #formun gecerliligini sorguladik
            comment = form.save(comit=False)
            comment.post = post
            comment.save()
            return redirect('detail',pk=post.pk)

    else:
        form = CommentForm()
        
        return render(request,'partials/forms.html',{'form':form})

@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('detail', pk=comment.post.pk)

@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.delete()
    return redirect('detail', pk=comment.post.pk)
