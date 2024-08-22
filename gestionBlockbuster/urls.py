from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'director', views.DirectorViewSet)
#router.register(r'categoria', views.CategoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categorias/', views.CategoriaView.as_view()),
    path('peliculas/', views.getPeliculaAll),
    path('peliculas/create/', views.createPelicula),
    path('peliculas/edit/<int:pk>/', views.editPelicula),
    path('prestamos/', views.getPrestamoAll),
    path('prestamos/create/', views.createPrestamo),
    path('prestamos/edit/<int:pk>/', views.editPrestamo),
    path('prestamos/devolucion/<int:pk>/', views.devolucion),
]
