from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pagina_inicial/', views.pagina_inicial, name='pagina_inicial'),
    path('cadastrar_cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('deletar_cliente/<int:id>/',
         views.deletar_cliente, name='deletar_cliente'),
    path('realizar_emprestimo/<int:id>/',
         views.realizar_emprestimo, name='realizar_emprestimo'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('get_cliente_data/<int:id>/',
         views.get_cliente_data, name='get_cliente_data'),
    path('cadastrar_cartao_de_credito/<int:id>/',
         views.cadastrar_cartao_de_credito, name='cadastrar_cartao_de_credito'),
]
