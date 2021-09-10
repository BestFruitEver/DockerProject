#!/bin/bash

echo "waiting for database..."

while ! nc -z db 3306
do
  sleep 0.5
done

echo database found

python3 main.py