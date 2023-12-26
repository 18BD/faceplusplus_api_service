from io import BytesIO
from PIL import Image, ImageDraw

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status, parsers, mixins, viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import ComparisonSerializer, ComparisonConfidenceSerializer, ListFaceSerializer, ImageSerializer, FaceQuerySerializer
from .models import Face
from .services import upload_image_to_faceplusplus, compare_faces


class FaceViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Face.objects.all()
    serializer_class = ListFaceSerializer
    parser_classes = (parsers.MultiPartParser,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('face_tokens', openapi.IN_QUERY,
                              type=openapi.TYPE_ARRAY, items=openapi.Items(
                                  type=openapi.TYPE_STRING),
                              required=False, collection_format='multi'),
            openapi.Parameter('color', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            '200': openapi.Response('File Attachment', schema=openapi.Schema(type=openapi.TYPE_FILE)),
        },
        produces='image/jpeg',
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Обработчик для извлечения и визуализации информации о лице на основе предоставленных токенов лиц.

        :param request: Запрос, содержащий параметры для извлечения информации.
        :return: Ответ с изображением, на котором отмечены лица.
        """

        # Валидация параметров запроса с использованием сериализатора.
        serializer = FaceQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        # Извлечение токенов лиц и цвета из валидированных данных.
        face_tokens = serializer.validated_data.get('face_tokens')
        color = serializer.validated_data.get('color')
        
        # Получение экземпляра лица из базы данных.
        instance = self.get_object()
        
        # Загрузка изображения из экземпляра лица.
        image = Image.open(instance.image_file)

        # Создание контекста для рисования на изображении.
        draw = ImageDraw.Draw(image)

        # Фильтрация лиц на основе предоставленных токенов лиц и отрисовка рамок вокруг них.
        faces = [face for face in instance.face_tokens if face['face_token'] in face_tokens] if face_tokens else instance.face_tokens
        for face in faces:
            face_rect = face["face_rectangle"]
            top_left = (face_rect["left"], face_rect["top"])
            bottom_right = (
                face_rect["left"] + face_rect["width"], face_rect["top"] + face_rect["height"])
            draw.rectangle([top_left, bottom_right], outline=color, width=2)

        # Сохранение изображения в байтовый поток в формате JPEG.
        byte_stream = BytesIO()
        image.save(byte_stream, format='JPEG')
        byte_stream.seek(0)

        # Возврат байтового потока в ответе.
        return HttpResponse(byte_stream, content_type='image/jpeg')

    @swagger_auto_schema(
        request_body=ImageSerializer(),
        responses={status.HTTP_200_OK: ListFaceSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Обработчик для создания новой записи лица на основе загруженного изображения.

        :param request: Запрос, содержащий загруженное изображение.
        :return: Ответ с данными созданной записи лица.
        """

        # 1. Получение загруженного изображения из данных запроса.
        uploaded_image = request.FILES.get('image')

        # Проверка наличия загруженного изображения.
        if not uploaded_image:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Отправка изображения на Face++ API для обнаружения лиц.
        face_tokens = upload_image_to_faceplusplus(uploaded_image)

        # 3. Создание записи лица в базе данных с использованием полученных токенов лиц и загруженного изображения.
        face = Face.objects.create(
            face_tokens=face_tokens, image_file=uploaded_image)

        # Получение сериализатора для созданной записи лица и возврат данных в ответе.
        serializer = self.get_serializer(instance=face)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ComparisonSerializer(),
        responses={status.HTTP_200_OK: ComparisonConfidenceSerializer}
    )
    @action(methods=['POST'], detail=False, url_path='comparison-faces')
    def comparison_faces(self, request, *args, **kwargs):
        """
        Эндпоинт для сравнения двух лиц с использованием Face++ API.

        :param request: Запрос, содержащий данные для сравнения двух лиц.
        :return: Результат сравнения лиц.
        """

        # Валидация данных запроса с использованием сериализатора.
        query_serializer = ComparisonSerializer(data=request.data)
        query_serializer.is_valid(raise_exception=True)
        
        # Получение токенов лиц из валидированных данных.
        face_token1 = query_serializer.validated_data.get('face_token1')
        face_token2 = query_serializer.validated_data.get('face_token2')
        
        # Сравнение двух лиц с помощью функции compare_faces.
        data = compare_faces(face_token1, face_token2)
        
        # Сериализация результата с использованием сериализатора для ответа.
        serializer = ComparisonConfidenceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Возврат результата сравнения лиц в ответе.
        return Response(serializer.data)
        
