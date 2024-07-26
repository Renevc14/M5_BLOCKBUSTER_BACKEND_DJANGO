from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'autor', views.AutorViewSet)
#router.register(r'categoria', views.CategoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categorias/', views.CategoriaView.as_view()),
    path('libros/', views.getLibroAll),
    path('libros/create/', views.createLibro),
    path('libros/edit/<int:pk>/', views.editLibro),
    path('prestamos/', views.getPrestamoAll),
    path('prestamos/create/', views.createPrestamo),
    path('prestamos/edit/<int:pk>/', views.editPrestamo),
    path('prestamos/devolucion/<int:pk>/', views.devolucion),
]
