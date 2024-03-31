```html
{% load static %}
```

### Цикл _for_
```html
{% for tag in tags %}
    <span class="badge text-{{ tag.color }}">{{ tag.title }}</span>
{% endfor %}
```

### Именнованная ссылка
```html
<a href="{% url "settings" param %}">settings</a>
```

### Файлы из _css_ и _templates_
```
"{% static 'img/avatar.jpg' %}"
```

### Включение шаблона 
```html
{% block auth %}
    {% include 'layouts/auth_block.html' %}
{% endblock %}
```
^ Нужно исправить ссылки

### Наследование шаблона
```html
{% extends "layouts/base.html" %}
```
^ Нужно исправить ссылки

