#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

make install && make collectstatic && make migrate

# Создаем суперпользователя, если его нет
uv run python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
"
