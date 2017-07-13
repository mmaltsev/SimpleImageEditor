# Simple Image Editor

Simple app for transparenting, resizing, cuting and whitening images.

# Usage

```
$ image_editor.py --path path/to/file [-t | -r | -c | -w | -s | -b]

Options:
  -p, --path TEXT   Path to image.
  -t                Make image backgound transparent.
  -r                Resize image.
  -c                Resize image canvas.
  -w                Make image outline white.
  -s                Make image square with edges equal to longest side.
  -b                Make image beautiful.
  --width INTEGER   Width of image. Specified only for croping, resizing and
                    beautifier. Default = 100px.
  --height INTEGER  Height of image. Specified only for croping, resizing and
                    beautifier. Default = 100px.
  --help            Show this message and exit.
```

# License
MIT License. Copyright (c) 2017 Maxim Maltsev.
