# 分页插件包
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Article, Category, Banner, Tag, Link


def hello(request):
    return HttpResponse('欢迎使用Django!')

def index_test(request):
    '''主页'''
    # 对Article进行声时并实例化,然后生成对象allarticle
    allarticle = Article.objects.all()
    print(allarticle)
    # 把查询到的对象,封装到一下文
    context = {
        'allarticle' : allarticle,
    }
    # 把上下文传到模板页面index.html里
    return render(request, 'index_test.html', context)

# 首页
def index(request):
    allcategory = Category.objects.all() # 通过Category表查出所有分类
    banner = Banner.objects.filter(is_active=True)[0:4] # 查询所有幻灯图数据,并进行切片
    tui = Article.objects.filter(tui__id=1)[:3] # 查询推荐位ID为1的文章
    allarticle = Article.objects.all().order_by('-id')[0:10] # order_by('-id')为数据排序方式，[0:10]为只获取10索引切片，只获取最新的10篇文章
    # hot = Article.objects.all().order_by('?')[:10]#随机推荐
    # hot = Article.objects.filter(tui__id=3)[:10]   #通过推荐进行查询，以推荐ID是3为例
    hot = Article.objects.all().order_by('views')[:10]  # 通过浏览数进行排序
    remen = Article.objects.filter(tui__id=2)[:6] # 右侧热门推荐
    tags = Tag.objects.all() # 右侧所有标签
    link = Link.objects.all() # 尾部的友情链接

    # 把查询出来的分类封装到上下文里
    context = {
        'allcategory' : allcategory,
        'banner' : banner,
        'tui' : tui,
        'allarticle' : allarticle, # 最新文章
        'hot' : hot,
        'remen' : remen,
        'tags' : tags,
        'link' : link,
    }
    return render(request, 'index.html', context) #把上下文传到index.html页面

# 列表页
def list(request, lid):
    list = Article.objects.filter(category_id=lid) # 获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid) # 获取当前文章的栏目名
    remen = Article.objects.filter(tui__id=2)[:6] # 右侧的热门推荐
    allcategory = Category.objects.all() # 导航所有分类
    tags = Tag.objects.all() # 右侧所有文章标签
    page = request.GET.get('page') # 在URL中获取当前页面数
    paginator = Paginator(list, 5) # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时，显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时，显示最后一页内容

    return render(request, 'list.html', locals()) # locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典

# 内容
def show(request, sid):
    '''
    代码里Article.objexts.get(id=sid), 因为获取的是单个对象,所以用get方法,id=sid查询URL传过来的指定id文章
    previous_blog和netx_blog是文章上一篇下一篇,我们通过发布文章时间来进行筛选文章的,比当肖文章发布的时间小就是上一
    篇,比当前文章发布时间大就是下一篇
    category=show.category.id,则是指定查询的文章为当前分类下的文章
    文章的浏览数,我们先通过show.views查询到当前浏览数,然后对这个数进行加1操作,意思是每访问一次页面(视图函数),
    就进行加1操作.然后通过show.save()进行保存.
    :param request:
    :param sid:
    :return:
    '''
    show = Article.objects.get(id=sid) # 查询指定ID的文章
    allcategory = Category.objects.all() # 导航上的分类
    tags = Tag.objects.all() # 右侧所有标签
    remen = Article.objects.filter(tui__id=2)[:6] # 右侧热门推荐
    hot = Article.objects.all().order_by('?')[:10] # 内容下面的您可能感兴趣的文章,随机推荐
    previous_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    netx_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals()) # locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典

# 标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag) # 获取通过URL传进来的tag，然后进行查询文章
    tname = Tag.objects.get(name=tag) # 获取当前搜索的标签名
    remen = Article.objects.filter(tui__id=2)[:6] # 右侧的热门推荐
    allcategory = Category.objects.all() # 导航所有分类
    tags = Tag.objects.all() # 右侧所有文章标签
    page = request.GET.get('page') # 在URL中获取当前页面数
    paginator = Paginator(list, 5) # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时，显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时，显示最后一页内容

    return render(request, 'list.html', locals()) # locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典


# 搜索页
def search(request):
    ss = request.GET.get('search')  # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配
    remen = Article.objects.filter(tui__id=2)[:6]
    allcategory = Category.objects.all()
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())

# 关于我们
def about(request):
    pass
