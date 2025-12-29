from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.conf import settings
from .models import Post, Category, Tag


@cache_page(60 * 15)
def blog_list_view(request):
    posts = Post.objects.filter(is_published=True).select_related('category', 'author').prefetch_related('tags')
    
    category_slug = request.GET.get('categoria')
    tag_slug = request.GET.get('etiqueta')
    
    selected_category = None
    selected_tag = None
    
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=selected_category)
    
    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=selected_tag)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    popular_tags = Tag.objects.all()[:10]
    
    context = {
        'meta_title': f'Blog - {settings.SITE_NAME}',
        'meta_description': 'Noticias, consejos y novedades sobre construcción, reformas y el sector inmobiliario.',
        'page_obj': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'selected_category': selected_category,
        'selected_tag': selected_tag,
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    
    post.views += 1
    post.save(update_fields=['views'])
    
    related_posts = post.get_related_posts()
    
    context = {
        'meta_title': post.get_meta_title(),
        'meta_description': post.get_meta_description(),
        'post': post,
        'related_posts': related_posts,
        'og_image': post.featured_image.url if post.featured_image else None,
    }
    return render(request, 'blog/blog_detail.html', context)
