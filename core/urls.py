from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('pessoas/', views.pessoa_lista, name='pessoa_lista'),
    path('pessoas/cadastro/', views.pessoa_cadastro, name='pessoa_cadastro'),
    path('pessoas/<int:pk>/', views.pessoa_detalhe, name='pessoa_detalhe'),
    path('pessoas/<int:pk>/editar/', views.pessoa_editar, name='pessoa_editar'),
    path('pessoas/<int:pk>/excluir/', views.pessoa_excluir, name='pessoa_excluir'),
    path('aniversariantes/', views.aniversariantes, name='aniversariantes'),
    path('aniversariantes/enviar-mensagem/<int:pk>/', views.enviar_mensagem_aniversario, name='enviar_mensagem_aniversario'),
    path('mensagens/', views.mensagem_lista, name='mensagem_lista'),
    path('mensagens/cadastro/', views.mensagem_cadastro, name='mensagem_cadastro'),
    path('mensagens/<int:pk>/editar/', views.mensagem_editar, name='mensagem_editar'),
    path('datas-comemorativas/', views.data_comemorativa_lista, name='data_comemorativa_lista'),
    path('datas-comemorativas/cadastro/', views.data_comemorativa_cadastro, name='data_comemorativa_cadastro'),
    path('datas-comemorativas/<int:pk>/editar/', views.data_comemorativa_editar, name='data_comemorativa_editar'),
    path('exportar/pessoas/csv/', views.exportar_pessoas_csv, name='exportar_pessoas_csv'),
    path('exportar/pessoas/pdf/', views.exportar_pessoas_pdf, name='exportar_pessoas_pdf'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
