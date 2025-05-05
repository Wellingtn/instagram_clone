from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/usuarios-que-curtiram-reels/', views.usuarios_que_curtiram_reels, name='usuarios_que_curtiram_reels'),
    path('api/usuarios-que-comentaram-em-postagens/', views.usuarios_que_comentaram_em_postagens, name='usuarios_que_comentaram_em_postagens'),
    path('api/quem-segue-quem/', views.quem_segue_quem, name='quem_segue_quem'),
    path('api/comentarios-em-reels/', views.comentarios_em_reels, name='comentarios_em_reels'),
    path('api/comentarios-em-reels/<str:nome_usuario>/', views.comentarios_em_reels, name='comentarios_em_reels_por_usuario'),
    path('api/estatisticas-usuario/<str:username>/', views.estatisticas_usuario, name='estatisticas_usuario'),
]
