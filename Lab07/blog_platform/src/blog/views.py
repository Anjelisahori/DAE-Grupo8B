from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from .models import Post, Category, Tag, Comment


class PostListView(ListView):
    """Vista para listar todas las publicaciones de blog publicadas"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Devuelve todas las publicaciones publicadas"""
        return Post.blog_objects.published()
    
    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            posts_count=Count('posts')
        )
        context['tags'] = Tag.objects.annotate(
            posts_count=Count('posts')
        ).order_by('-posts_count')[:10]
        context['recent_posts'] = Post.blog_objects.recent_posts()
        return context


class PostDetailView(DetailView):
    """Vista para mostrar una publicación individual con comentarios"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Asegura que solo mostramos publicaciones publicadas"""
        return Post.blog_objects.published()
    
    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto"""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.annotate(
            posts_count=Count('posts')
        ).order_by('-posts_count')[:10]
        context['recent_posts'] = Post.blog_objects.recent_posts().exclude(
            id=self.object.id
        )
        return context


class CategoryPostListView(ListView):
    """Vista para listar publicaciones en una categoría específica"""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Obtiene publicaciones para la categoría especificada"""
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        return Post.blog_objects.by_category(self.category.slug)
    
    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto"""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.annotate(
            posts_count=Count('posts')
        )
        context['tags'] = Tag.objects.annotate(
            posts_count=Count('posts')
        ).order_by('-posts_count')[:10]
        return context


class TagPostListView(ListView):
    """Vista para listar publicaciones con una etiqueta específica"""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Obtiene publicaciones para la etiqueta especificada"""
        self.tag = Tag.objects.get(slug=self.kwargs['slug'])
        return Post.blog_objects.by_tag(self.tag.slug)
    
    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto"""
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.annotate(
            posts_count=Count('posts')
        ).order_by('-posts_count')[:10]
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear un nuevo comentario en una publicación"""
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['content']  # Campos que queremos que el usuario complete

    def form_valid(self, form):
        """Asocia el comentario con la publicación y el usuario actual"""
        form.instance.author = self.request.user  # El autor es el usuario actual
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])  # Asociamos el comentario con la publicación correcta
        return super().form_valid(form)

    def get_success_url(self):
        """Redirige a la página de detalle de la publicación después de agregar el comentario"""
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        """Agrega la publicación al contexto"""
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(slug=self.kwargs['slug'])  # Agregamos la publicación a contexto para mostrarla en el formulario
        return context
