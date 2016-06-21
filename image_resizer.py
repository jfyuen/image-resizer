import os
import sys
import argparse
from PIL import Image
from PIL.ExifTags import TAGS


def get_exif(f):
    exif_dict = {}
    image = Image.open(f)
    info = image._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exif_dict[decoded] = value
    return exif_dict


def get_image_name(image_filename, source_directory):
    ext = '.' + image_filename.split('.')[-1]
    exif_dict = {}
    try:
        exif_dict = get_exif(source_directory + os.sep + image_filename)
        creation_date = exif_dict['DateTimeOriginal'][0]
        if creation_date == '0000:00:00 00:00:00':
            raise Exception('Wrong exif data for {}'.format(image_filename))
        image_name = creation_date.replace(':', '-').replace(' ', '_')
    except:
        image_name = image_filename.split('.')[0]
    return exif_dict, image_name + ext


def get_image_new_size(original_size, width, height):
    x, y = original_size
    if x > y:
        height, width = width, height
    if x > width:
        y = max(y * width // x, 1)
        x = width
    elif y > height:
        x = max(x * height // y, 1)
        y = height
    return x, y


def resize_image(image_filename, source_directory, store_directory, width, height):
    exif, image_name = get_image_name(image_filename, source_directory)
    saved_image = os.path.join(store_directory, image_name)
    if os.path.exists(saved_image):
        return
    path = os.path.join(source_directory, image_filename)
    try:
        original_image = Image.open(path)
        if width is None or height is None:
            size = original_image.size
        else:
            size = get_image_new_size(original_image.size, width, height)
        orientation = exif.get('Orientation', 0)
        if orientation == 3: 
            original_image = original_image.rotate(180, expand=True)
        elif orientation == 6: 
            original_image = original_image.rotate(270, expand=True)
            size = (size[1], size[0])
        elif orientation == 8: 
            original_image = original_image.rotate(90, expand=True)
            size = (size[1], size[0])
        new_image = original_image.resize(size, Image.ANTIALIAS) # best down-sizing filter
        new_image.save(saved_image)
        print('Saved file: {}'.format(saved_image))
    except Exception as e:
        print('Problem converting image: {} in {}'.format(image_filename, source_directory))
        print(e)


def resize_images_in_directory(source_dir, target_dir, width, height):
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
                resize_image(file_name, root, store_directory, width, height)            


def parse_args():
    parser = argparse.ArgumentParser(description='Resize and compress images in a directory.')
    parser.add_argument('source', help='directory containing images to compress')
    parser.add_argument('output', help=' directory to save new images too')
    parser.add_argument('-s', '--size', help='resize to WIDTHxHEIGHT', default='2048x1536')
    parser.add_argument('-n', '--noresize', help='do not resize images, just compress', default=False, action='store_true')
    return parser.parse_args()


def parse_size(size):
    if size == '300dpiA4':
        return 2480, 3508
    elif size == '200dpiA4':
        return 1654, 2339
    elif size == '100dpiA4':
        return 827, 1170
    elif size == '72dpiA4':
        return 596, 842
    else:
        w, h = size.split('x')
        return int(w), int(h)


if __name__ == '__main__':
    args = parse_args()
    if args.noresize:
        width = None
        height = None
    else:
        width, height = parse_size(args.size)
    os.makedirs(args.output, exist_ok=True)
    resize_images_in_directory(args.source, args.output, width, height)
    
