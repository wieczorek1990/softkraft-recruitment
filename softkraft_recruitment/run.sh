#!/bin/sh

function manage() {
  python manage.py $@
}

manage collectstatic --noinput &&
 manage migrate --noinput &&
 manage runserver 0.0.0.0:8000
