import sys
import os
import shutil
import piexif


def get_creation_date(filename):
    if not ("_" in filename and "-" in filename):
        return "0000:00:00 00:00:00"

    return filename.split('.')[0].replace("_", " ").replace("-", ":")


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
    if target_dir[-1] != os.sep:
        target_dir += os.sep

    for root, dirs, files in os.walk(source_dir, topdown=True):
        store_directory = root.replace(source_dir, target_dir)
        for dir_name in dirs:
            directory = os.path.join(store_directory, dir_name)
            os.makedirs(directory, exist_ok=True)
        for file_name in files:
            # Ignore hidden directories
            if file_name[0] != '.':
                add_exif(file_name, root, store_directory)



if __name__ == '__main__':
    addexif_images_in_directory(sys.argv[1], sys.argv[2])