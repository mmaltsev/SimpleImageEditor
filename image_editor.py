"""Image Editor."""
from PIL import Image
from ntpath import basename
import click
import time
import sys
from termcolor import colored


def image_name_extract(img_path):
    """Extracting and editing name of image."""
    full_name = basename(img_path)
    name_ind = full_name.find('.')
    name = full_name[0:name_ind]
    return name


def background_cut(img):
    """Cutting background from image."""
    print(colored('->', 'green') + ' transparenting...')
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        # if image already has a transparent background
        if not item[3]:
            new_data = data
            break
        if (item[0] in list(range(230, 256)) and
                item[1] in list(range(230, 256)) and
                item[2] in list(range(230, 256))):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def image_resize(data, size):
    """Resizing image."""
    print(colored('->', 'green') + ' resizing...')
    return data.resize(size, Image.BICUBIC)


def canvas_resize(data, size):
    """Resizing image canvas."""
    print(colored('->', 'green') + ' resizing canvas...')
    new_data = []
    # data = bg_cut(data)
    [width, height] = data.size

    horizontal_padding = (size[0] - width) / 2
    vertical_padding = (size[1] - height) / 2

    new_data = data.crop(
        (
            -horizontal_padding,
            -vertical_padding,
            width + horizontal_padding,
            height + vertical_padding
        )
    )
    return new_data


def whiten(img):
    """Inverting colors."""
    print(colored('->', 'green') + ' whitening...')
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        if item[0] < 255 and item[1] < 255 and item[2] < 255 and item[3] > 0:
            new_data.append((255, 255, 255, item[3]))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def square(data):
    """Squaring image."""
    size = [max(data.size), max(data.size)]
    print(colored('->', 'yellow') + ' new image size: ' + str(max(data.size)) + 'x' + str(max(data.size)) + '.')
    return canvas_resize(data, size)


@click.command()
@click.option('-p', '--path', help='Path to image.')
@click.option('-t', 'editing', flag_value='transparent', help='Make image backgound transparent.')
@click.option('-r', 'editing', flag_value='resize', help='Resize image.')
@click.option('-c', 'editing', flag_value='crop', help='Resize image canvas.')
@click.option('-w', 'editing', flag_value='whiten', help='Make image outline white.')
@click.option('-s', 'editing', flag_value='square', help='Make image square with edges equal to longest side.')
@click.option('-b', 'editing', flag_value='beautify', default=True, help='Make image beautiful.')
@click.option('--width', default=100, help='Width of image. Specified only for croping, resizing and beautifier. Default = 100px.')
@click.option('--height', default=100, help='Height of image. Specified only for croping, resizing and beautifier. Default = 100px.')


def main(path, editing, width, height):    
    """Image editor for transparenting, resizing, croping and changing colors of images."""
    print('')
    if path and editing:
        img = Image.open(path)
        img_name = image_name_extract(path)
        
        if editing == 'transparent':
            img = background_cut(img)
            
        elif editing == 'resize':
            img = image_resize(img, [width, height])
                
        elif editing == 'crop':
            img = canvas_resize(img, [width, height])

        elif editing == 'whiten':
            img = whiten(img)
            
        elif editing == 'square':
            img = square(img)
            
        elif editing == 'beautify':
            img = background_cut(img)
            img = whiten(img)
            img = square(img)

        time_stamp = int(time.time())
        img_name += str(time_stamp) + '.png'
        img.save(img_name, 'PNG')
        print(colored('->', 'yellow') + ' saved as ' + img_name + '.')
        print('')

    else:
        print(colored('->', 'red') + ' no image path specified.')
        print(colored('->', 'red') + ' usage: {} --path path/to/file [-t | -r | -c | -w | -s | -b]'.format(sys.argv[0]))
        print(colored('->', 'red') + ' for options type: {} --help'.format(sys.argv[0]))
        print('')
        

if __name__ == '__main__':
    main()
