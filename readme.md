## Требования

Убедитесь, что у вас установлены следующие компоненты:

- Python 3.10
- PostgreSQL
- Утилита `pip` (для установки зависимостей из `requirements.txt`)

## Установка

1. **Создание виртуального окружения** (рекомендуется, но не обязательно):

   ```bash
   python -m venv myenv
   source myenv/bin/activate   # Для Linux/macOS
   myenv\Scripts\activate      # Для Windows
   ```

2. **Установка зависимостей** из `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка базы данных PostgreSQL**:

- Создайте новую базу данных для вашего проекта.
- Обновите настройки в файле `app/settings.py` вашего Django проекта, чтобы использовать соответствующие параметры подключения к вашей базе данных.

4. **Примените миграции**:

   ```bash
   python manage.py migrate
   ```

5. **Запуск сервера**:

   ```bash
   python manage.py runserver
   ```

## Структура проекта

- `face++/` - основная директория вашего Django проекта.
- `faces/` - ваше Django приложение.
- `app/` - основа.
- `static/` - статические файлы (CSS, JS, изображения).

## Документация

- [Faces app документация](http://127.0.0.1:8000/api/docs/)
