import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont

# from keras.preprocessing.image import ImageDataGenerator

characters = list('abcdefghijklmnopqrstuvwxyz')
result_dir = 'data'
font_path = "/Library/Fonts/"


def generate_clean_dataset():
    fonts = get_fonts()

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    for fontPath in fonts:
        for char in characters:
            yield generate_clean_character(char, fontPath)


def get_fonts():
    fonts = [os.path.join(dirpath, filename)
             for dirpath, dirnames, filenames in os.walk(font_path)
             for filename in filenames
             if filename.endswith(".ttf")]
    return fonts


def generate_clean_character(char, fontPath):
    font = ImageFont.truetype(fontPath, 20)

    img = Image.new("RGBA", (32, 32), "black")
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), char, "white", font=font)

    return img


def add_gaussian_noise_to_image(img, radius=1):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


imgs = generate_clean_dataset()

# img_name = '{}/{}_{}.png'.format(result_dir, char, fontPath.split('/')[-1][:-4])
#            img.save(img_name)

# def add_point_noise_to_image(draw):
#     for i in range(1, 100):
#         xL = randint(0, 32)
#         yL = randint(0, 32)
#         draw.point((xL, yL), fill=255)
#     return draw

# def rotate():
#     datagen = ImageDataGenerator(rotation_range=90)
#     ImageDataGenerator(rotation_range=40,
#                        width_shift_range=0.4,
#                        height_shift_range=0.4,
#                        zoom_range=0.3,
#                        fill_mode='nearest')
