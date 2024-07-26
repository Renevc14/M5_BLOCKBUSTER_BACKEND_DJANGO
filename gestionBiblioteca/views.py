from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import AutorSerializer, CategoriaSerializer, LibroSerializer, PrestamoSerializer
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Autor, Categoria, Libro, Prestamo
from rest_framework.decorators import api_view

# Create your views here.
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

############### Categoria #########################

class CategoriaView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

################# libros #########################

@api_view(['GET'])
def getLibroAll(request):
    try:
        librosAll = Libro.objects.all()
        print(librosAll)
        return JsonResponse(
            LibroSerializer(librosAll, many=True).data,
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
def createLibro(request):
    try:
        create = LibroSerializer(data=request.data)
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
def editLibro(request, pk):
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return Response(
            {"error": "Libro no encontrado."},
            safe=False,
            status=404
        )
    try:
        serializer = LibroSerializer(libro, data=request.data, partial=(request.method == 'PUT'))
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
            libro_id = create.validated_data['libro'].id
            libro = Libro.objects.get(pk=libro_id)
            if not libro.disponible:
                return JsonResponse(
                    {"error": "El libro no está disponible para préstamo."},
                    safe=False,
                    status=400
                )
            create.save()
            libro.disponible = False
            libro.save()
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
            libro_id = prestamo.libro.id
            print(libro_id)
            libro = Libro.objects.get(pk=libro_id)
            serializer.save()
            libro.disponible = True
            libro.save()
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