from django.shortcuts import render
from .models import Post, Category, Tag
import markdown
import re
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest,HttpRequest
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})
    # return render(request, 'blog/markdown.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})

    # return render(request, 'blog/markdown.html', context={'post': post})



# 归档
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year = year,created_time__month = month).order_by('-created_time')
    return render(request, 'blog/index.html', context = {'post_list':post_list} )


# 种类
def category(request,pk):
    cate = get_object_or_404(Category, pk = pk)
    post_list = Post.objects.filter(category = cate).order_by('-created_time')
    return render(request , 'blog/index.html' , context = {'post_list':post_list})

# 标签
def tag(request , pk):
    tg = get_object_or_404(Tag , pk = pk)
    post_list = Post.objects.filter(tags = tg).order_by('-created_time')
    return render(request, 'blog/index.html' , context = {'post_list':post_list})




