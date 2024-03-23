# Image resizer

Image resizer is a small python script to resize all images in a directory and compress them at the same time. It is useful for generating compressed images from digital cameras that look just "ok" to put on the web or in a small gallery while also saving space.

## Installation

This script supports Python 3 (>= 3.6).

```sh
$ pip install -r requirements.txt
```

## Usage

```sh
$ python image_resizer.py source output
```

It will take all files and directories from `source` directory and map them to `output`.
A size option may be given using `-size WxH`, default is `2048x1536`, proportions are kept.

Example usage:
```sh
$ python image_resizer.py some_images compressed_images --size=2048x1536
```

