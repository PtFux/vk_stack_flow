 ## StackFlow для VK :3
 
###  ДЗ - 1
Выполненное дз находится в папке _public_ в корне проекта. Коммит - _Init_.
В рамках дз была сделана верстка, следующих страниц:
- _ask.html_ - страница одного вопроса 
- _index.html_ - главная страница (также общий вид страниц, идентично - _base.html_)
- _login.html_ - страница авторизации
- _question.html_ - страница одного вопроса
- _signup.html_ - страница регистрации

В качестве стиля использовался **bootstrap**. **Bootstrap** подключен через скачанные файлы в папку _static/css_.

Верстка шаблонами **django** не применялась.

### ДЗ - 2
####  Views и шаблоны для основных страниц

- **главная** (список новых вопросов) - http://127.0.0.1:8000/
- **страница вопроса** (список ответов) - http://127.0.0.1:8000/question/3
- страница **добавления вопроса** - http://127.0.0.1:8000/ask
- форма **регистрации** - http://127.0.0.1:8000/signup
- форма **входа** - http://127.0.0.1:8000/login
- форма **редактирования профиля** - http://127.0.0.1:8000/profile/edit

#### Постраничное отображение 

- **функция пагинации** - _app/default_data.py_ _paginate(...)_
- **шаблон для отрисовки пагинатора** - _templates/layouts/pagination.html_
- **корректная обработка “неправильных” параметров** - _app/default_data.py_ _paginate(...)_

### ДЗ - 3

- **fill_db** - команда наполнения базы данных
- **clear_db** - команда очищения базы данных

#### Пример использования

- ``` python manage.py fill_db -h``` - выводит справочную информацию о команде **fill_db**
- ``` python manage.py clear_db -m``` - удаляет всё содержимое бд

### ДЗ - 4
- форма **входа** - http://127.0.0.1:8000/login
- форма **редактирования профиля** - http://127.0.0.1:8000/profile/edit
- страница **добавления вопроса** - http://127.0.0.1:8000/ask
- форма **регистрации** - http://127.0.0.1:8000/signup

## HELP
- [Tasks](app/tasks.md) - Основные задачи, что нужно еще сделать
- [StartUp](start_up.md) - Мини инструкция, как поднимать проект на другом устройстве
- [Bootstrap help template](templates/help.md) - Некоторые часто используемые в шаблонах конструкции
- [Database help](app/models/about_database.md) - Шпаргалка по работе с посгтресом и пг админом в doker
