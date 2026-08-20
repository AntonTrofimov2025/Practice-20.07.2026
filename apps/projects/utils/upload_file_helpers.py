import os
from rest_framework import serializers


def is_extension(value):
    return value.split('.')[-1] in ['pdf', 'csv', 'doc', 'xlsx', 'py', 'txt', 'png', 'jpeg', 'jpg']

def validate_extension(file):
    if file.name.split('.')[-1] not in ['pdf', 'csv', 'doc', 'xlsx', 'py', 'txt', 'png', 'jpeg', 'jpg']:
        raise serializers.ValidationError('This extension is not allowed!')
    return file

def is_size_acceptable(path):
    return os.path.getsize(path) / 1024 / 1024 < 2

def validate_file_size(file):
    if file.size / 1024 / 1024 > 2:
        raise serializers.ValidationError('File size too big')
    return file


# Both functions are not necessary to implement due to Django's internal validations.
# They both are already on board and had been implemented by Django devs.
def create_path(path):
    os.makedirs(path, exist_ok=True)

def save_file(path, data_chunks):
    with open(path, 'wb') as file: # wb instead of w, because of the nature of binary files
        for chuck in data_chunks:
            file.write(chuck)
####################################################################################