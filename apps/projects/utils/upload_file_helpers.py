import os
from rest_framework import serializers


def is_extension(value):
    return value.split('.')[-1] in ['pdf', 'csv', 'doc', 'xlsx', 'py']

def validate_extension(file):
    if file.name.split('.')[-1] not in ['pdf', 'csv', 'doc', 'xlsx', 'py', 'txt']:
        raise serializers.ValidationError('This extension is not allowed!')
    return file

def validate_size(path):
    return os.path.getsize(path) / 1024 / 1024 < 2

def validate_file_size(file):
    if file.size / 1024 / 1024 > 2:
        raise serializers.ValidationError('File size too big')

def create_path(value):
    os.makedirs(value, exist_ok=True)

def save_file(path, data_chunks):
    with open(path, 'w', encoding='utf-8') as file:
        for chuck in data_chunks:
            file.write(chuck)

