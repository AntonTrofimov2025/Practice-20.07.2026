import os


def validate_extension(value):
    return value.split('.')[-1] in ['pdf', 'csv', 'doc', 'xlsx']

def validate_size(path):
    return os.path.getsize(path) / 1024 / 1024 < 2

def create_path(value):
    os.makedirs(value, exist_ok=True)

def save_file(path, data_chunks):
    with open(path, 'w', encoding='utf-8') as file:
        for chuck in data_chunks:
            file.write(chuck)

