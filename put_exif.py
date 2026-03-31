import sys
import os
import re
import shutil
import piexif


def get_creation_date(filename):
    match = re.match(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', os.path.splitext(filename)[0])
    if match is None:
        return "0000:00:00 00:00:00"

    return match.group(1).replace("_", " ").replace("-", ":")


def add_exif(image_filename, source_directory, store_directory):
    saved_image = os.path.join(store_directory, image_filename)
    if os.path.exists(saved_image):
        return
    path = os.path.join(source_directory, image_filename)
    try:
        shutil.copyfile(path, saved_image)
        exif_dict = piexif.load(saved_image)
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = get_creation_date(image_filename)
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, saved_image)
        print('Saved file: {}'.format(saved_image))
    except Exception as e:
        print('Problem converting image: {} in {}'.format(image_filename, source_directory))
        print(e)


def addexif_images_in_directory(source_dir, target_dir):
    source_dir = os.path.abspath(source_dir)
    target_dir = os.path.abspath(target_dir)
    os.makedirs(target_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir, topdown=True):
        dirs[:] = [
            dir_name for dir_name in dirs
            if os.path.abspath(os.path.join(root, dir_name)) != target_dir
        ]
        relative_root = os.path.relpath(root, source_dir)
        if relative_root == '.':
            store_directory = target_dir
        else:
            store_directory = os.path.join(target_dir, relative_root)
        os.makedirs(store_directory, exist_ok=True)
        for dir_name in dirs:
            directory = os.path.join(store_directory, dir_name)
            os.makedirs(directory, exist_ok=True)
        for file_name in files:
            # Ignore hidden directories
            if file_name[0] != '.':
                add_exif(file_name, root, store_directory)



if __name__ == '__main__':
    addexif_images_in_directory(sys.argv[1], sys.argv[2])
