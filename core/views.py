from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count  # Remove the 'models' import as it's incorrect
from social_app.models import Post, PostComment, PostLike, Reel, ReelComment, ReelLike, Follower


def index(request):
    """Renderiza a página inicial com links para os endpoints da API."""
    return render(request, 'core/index.html')


def usuarios_que_curtiram_reels(request):
    """Retorna todos os usuários que curtiram pelo menos um reel."""
    usuarios = User.objects.filter(reel_likes__isnull=False).distinct().values('id', 'username')
    
    # Para cada usuário, obter os reels que ele curtiu
    resultado = []
    for usuario in usuarios:
        reels_curtidos = ReelLike.objects.filter(user_id=usuario['id']).values_list('reel__id', flat=True)
        resultado.append({
            'usuario': usuario['username'],
            'reels_curtidos': list(reels_curtidos)
        })
    
    return JsonResponse(resultado, safe=False)


def usuarios_que_comentaram_em_postagens(request):
    """Retorna todos os usuários que comentaram em pelo menos uma postagem, junto com seus comentários."""
    comentarios = PostComment.objects.select_related('user', 'post').all()
    
    resultado = []
    for comentario in comentarios:
        resultado.append({
            'usuario': comentario.user.username,
            'texto': comentario.text,
            'postagem_id': comentario.post.id
        })
    
    return JsonResponse(resultado, safe=False)


def quem_segue_quem(request):
    """Retorna todas as relações de seguidores."""
    seguidores = Follower.objects.select_related('follower', 'following').all()
    
    resultado = []
    for seguidor in seguidores:
        resultado.append({
            'seguidor': seguidor.follower.username,
            'seguindo': seguidor.following.username
        })
    
    return JsonResponse(resultado, safe=False)


def comentarios_em_reels(request, nome_usuario=None):
    """Retorna comentários em reels, opcionalmente filtrados por usuário."""
    if nome_usuario:
        comentarios = ReelComment.objects.filter(user__username=nome_usuario).select_related('user', 'reel')
    else:
        comentarios = ReelComment.objects.select_related('user', 'reel').all()
    
    resultado = []
    for comentario in comentarios:
        resultado.append({
            'usuario': comentario.user.username,
            'texto': comentario.text,
            'reel_id': comentario.reel.id,
            'reel_descricao': comentario.reel.description
        })
    
    return JsonResponse(resultado, safe=False)


def estatisticas_usuario(request, username):
    """Retorna estatísticas detalhadas de um usuário específico."""
    try:
        usuario = User.objects.get(username=username)
        
        # Contagens
        posts_count = Post.objects.filter(user=usuario).count()
        reels_count = Reel.objects.filter(user=usuario).count()
        likes_recebidos = PostLike.objects.filter(post__user=usuario).count() + ReelLike.objects.filter(reel__user=usuario).count()
        comentarios_recebidos = PostComment.objects.filter(post__user=usuario).count() + ReelComment.objects.filter(reel__user=usuario).count()
        seguidores_count = Follower.objects.filter(following=usuario).count()
        seguindo_count = Follower.objects.filter(follower=usuario).count()
        
        # Posts mais curtidos
        posts_mais_curtidos = Post.objects.filter(user=usuario).annotate(
            likes_count=Count('likes')
        ).order_by('-likes_count')[:5].values('id', 'content', 'likes_count')
        
        # Reels mais curtidos
        reels_mais_curtidos = Reel.objects.filter(user=usuario).annotate(
            likes_count=Count('likes')
        ).order_by('-likes_count')[:5].values('id', 'description', 'likes_count')
        
        resultado = {
            'username': username,
            'posts_count': posts_count,
            'reels_count': reels_count,
            'likes_recebidos': likes_recebidos,
            'comentarios_recebidos': comentarios_recebidos,
            'seguidores': seguidores_count,
            'seguindo': seguindo_count,
            'posts_mais_curtidos': list(posts_mais_curtidos),
            'reels_mais_curtidos': list(reels_mais_curtidos)
        }
        
        return JsonResponse(resultado)
    
    except User.DoesNotExist:
        return JsonResponse({'erro': f'Usuário {username} não encontrado'}, status=404)
