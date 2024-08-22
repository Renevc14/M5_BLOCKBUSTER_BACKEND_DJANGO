from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import DirectorSerializer, CategoriaSerializer, PeliculaSerializer, PrestamoSerializer
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Director, Categoria, Pelicula, Prestamo
from rest_framework.decorators import api_view

# Create your views here.
class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

############### Categoria #########################

class CategoriaView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

################# peliculas #########################

@api_view(['GET'])
def getPeliculaAll(request):
    try:
        peliculasAll = Pelicula.objects.all()
        print(peliculasAll)
        return JsonResponse(
            PeliculaSerializer(peliculasAll, many=True).data,
            safe=False,
            status=200,
        )
    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )


@api_view(['POST'])
def createPelicula(request):
    try:
        create = PeliculaSerializer(data=request.data)
        if create.is_valid():
            create.save()
            return JsonResponse(
                create.data,
                safe=False,
                status=201
            )
        return JsonResponse(
            create.errors,
            safe=False,
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )

@api_view(['PUT'])
def editPelicula(request, pk):
    try:
        pelicula = Pelicula.objects.get(pk=pk)
    except Pelicula.DoesNotExist:
        return Response(
            {"error": "Pelicula no encontrado."},
            safe=False,
            status=404
        )
    try:
        serializer = PeliculaSerializer(pelicula, data=request.data, partial=(request.method == 'PUT'))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data,
                safe=False,
                status=201
                )
        return JsonResponse(
            serializer.errors,
            safe=False,
            status=400
            )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )

############### prestamos #########################

@api_view(['GET'])
def getPrestamoAll(request):
    try:
        prestamoAll = Prestamo.objects.all()
        return JsonResponse(
            PrestamoSerializer(prestamoAll, many=True).data,
            safe=False,
            status=200,
        )
    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )


@api_view(['POST'])
def createPrestamo(request):
    try:
        create = PrestamoSerializer(data=request.data)
        if create.is_valid():
            pelicula_id = create.validated_data['pelicula'].id
            pelicula = Pelicula.objects.get(pk=pelicula_id)
            if not pelicula.disponible:
                return JsonResponse(
                    {"error": "El pelicula no está disponible para préstamo."},
                    safe=False,
                    status=400
                )
            create.save()
            pelicula.disponible = False
            pelicula.save()
            return JsonResponse(
                create.data,
                safe=False,
                status=201
            )
        return JsonResponse(
            create.errors,
            safe=False,
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )

@api_view(['PUT'])
def editPrestamo(request, pk):
    try:
        prestamo = Prestamo.objects.get(pk=pk)
    except Prestamo.DoesNotExist:
        return Response(
            {"error": "Prestamo no encontrado."},
            safe=False,
            status=404
        )
    try:
        serializer = PrestamoSerializer(prestamo, data=request.data, partial=(request.method == 'PUT'))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data,
                safe=False,
                status=201
                )
        return JsonResponse(
            serializer.errors,
            safe=False,
            status=400
            )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )

@api_view(['PUT'])
def devolucion(request, pk):
    try:
        prestamo = Prestamo.objects.get(pk=pk)
    except Prestamo.DoesNotExist:
        return Response(
            {"error": "Prestamo no encontrado."},
            safe=False,
            status=404
        )
    try:
        serializer = PrestamoSerializer(prestamo, data=request.data, partial=(request.method == 'PUT'))
        if serializer.is_valid():
            pelicula_id = prestamo.pelicula.id
            print(pelicula_id)
            pelicula = Pelicula.objects.get(pk=pelicula_id)
            serializer.save()
            pelicula.disponible = True
            pelicula.save()
            return JsonResponse(
                serializer.data,
                safe=False,
                status=201
                )
        return JsonResponse(
            serializer.errors,
            safe=False,
            status=400
            )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )