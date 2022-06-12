# **SuppleTime**

     Корпоративный трекер времени и планирования времени.

# 1. Цель проекта

Цель проекта - создать сервис для удобного планирования и трекинга времени и гибкого управления проектами и командами. Пользователь может создавать команды, планы, задачи, проекты, и в удобной форме собирать статистику для выставления счетов заказчику.

# 2. Описание сервиса

Основные функциональные блоки проекта:

* Регистрация, аутентификация и авторизация
* Планирование задач
* Отслеживание рабочего времени
* Сбор и визуализация статистики
* Функционал управления проектами
* Функционал управления команд
* Система тегов

## 2.1 Регистрация

При регистрации пользователя необходимо указать следующие поля:

* login — обязательное поле
* email — обязательное поле
* пароль — обязательное поле (? возможно сделаем без пароля)

После отправки формы регистрации пользователю на email прийдёт ссылка для подтверждения email. После чего пользователь будет зарегистрирован.

## 2.2 Планирование задач

В системе присутствует интерактивный календарь, где пользователь может создавать, редактировать задачи. Так же фильтровать задачи по тегам, командам, проектам, исполнителям и т.д.

### 2.2.1 Задачи

При создании задачи пользователю предлагается заполнить информацию о задаче:

* теги
* команда / проект
* исполнитель (если пользователь лидер команды по умолчанию пользователь - исполнитель)
* клиент
* промежуток времени исполнения

Так же по ходу взаимодействие с задачей пользователь может оставлять коментарии к задаче.

## 2.3 Отслеживание рабочего времени

## 2.4 Сбор и визуализация статистики

## 2.5 Функционал управления проектами

## 2.6 Функционал управления команд

## 2.7 Система тегов


В системе при создании любого объекта (команда, проект, задача и т.д.) пользователю будет предлагаться добавить теги, чтобы в будущем легко ориентироваться и проводить поиск по всем записям.

# 3. Предлагаемый стек технологий

Для реализации сервиса предлагается следующий стек технологий:

* Бэкенд:
    * Python
    * Flask
    * SQLAlchemy
* Фронтенд:
    * HTML
    * CSS
    * JavaScript