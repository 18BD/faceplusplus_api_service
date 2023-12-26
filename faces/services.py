import requests

from django.conf import settings


def upload_image_to_faceplusplus(image_file):
    """
    Загрузка изображения на Face++ для обнаружения лиц.
    
    :param image_file: Файл изображения для загрузки.
    :return: Список обнаруженных лиц.
    """
    url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    
    # Параметры API-ключа и секрета из настроек Django.
    params = {
        'api_key': settings.FACEPLUSPLUS_API_KEY,
        'api_secret': settings.FACEPLUSPLUS_API_SECRET
    }
    
    # Отправка POST-запроса на API Face++ для обнаружения лиц.
    response = requests.post(url, files={'image_file': image_file}, params=params)
    data = response.json()
    return data['faces']


def compare_faces(face_token1, face_token2):
    """
    Сравнение двух лиц с помощью Face++.
    
    :param face_token1: Токен первого лица для сравнения.
    :param face_token2: Токен второго лица для сравнения.
    :return: Результат сравнения лиц.
    """
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"
    
    # Параметры API-ключа и секрета из настроек Django.
    params = {
        'api_key': settings.FACEPLUSPLUS_API_KEY,
        'api_secret': settings.FACEPLUSPLUS_API_SECRET
    }
    
    # Подготовка данных для сравнения двух лиц.
    payload = {
        'face_token1': face_token1,
        'face_token2': face_token2
    }
    
    # Отправка POST-запроса на API Face++ для сравнения лиц.
    response = requests.post(url, data=payload, params=params)
    data = response.json()
    
    return data
