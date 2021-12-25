#!/bin/bash
set -e

# Заполнить директорию staticfiles статическими файлами, если она пуста
[ "$(ls -A staticfiles)" ] || python manage.py collectstatic


exec "$@"

