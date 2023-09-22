
# QRKot Кошачий благотворительный фонд (0.1.0)

  

[Описание](#описание) /

  

[Запуск](#Запуск) /

  

## Описание

  

[QRKot](https://github.com/slavspart/cat_charity_fund) Учебный проект - приложение для создания API благотворительного фонда поддержки котиков QRKot.

Пользователи могут создавать целевые проекты помощи котикам, а также делать пожертвования для финансирования проектов.

В рамках реализации сервиса:

- Описаны модели создания таблиц CharityProject и Donation
- Настроены create, list, retrieve, update и delete эндпойнты для получения API
- Описаны pydantic схемы
- Внедрена система авторизации с помощь JWT - токенов
- Настроена система инвестирования проектов при помощи пожертвований


Сервис создан на базе фрэймворка FastAPI.

  

## Запуск

  

```

git clone

```

  

```

cd cat_charity_fund

```

  

Cоздать и активировать виртуальное окружение:

  

```

python3 -m venv venv

```

  

* Если у вас Linux/macOS

  

```

source venv/bin/activate

```

  

* Если у вас windows

  

```

source venv/scripts/activate

```

  

Установить зависимости из файла requirements.txt:

  

```

python3 -m pip install --upgrade pip

```

  

```

pip install -r requirements.txt

```

```

uvicorn app.main:app

```

## Документация
Документацию API можно посмотреть на сайте https://redocly.github.io/redoc/, загрузив файл
```

cat_charity_fund/openapi.json
