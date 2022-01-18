from PIL import Image
import glob


max_width = 0
total_height = 0

image_list = []
for filename in glob.glob('xCombine\*.jpg'):
    image_list.append(filename)

open_images = []
for img in image_list:
    im = Image.open(img)
    temp_size = im.size
    if temp_size[0] > max_width:
        divisor = 1
        if temp_size[0] > 3000:
            divisor = 2
        max_width = int(temp_size[0]/divisor)
    total_height += int(max_width/temp_size[0] * temp_size[1])
    im = im.resize((max_width, int(max_width/temp_size[0] * temp_size[1])))
    open_images.append(im)
      
new = Image.new("RGBA", (max_width, total_height))

running_height = 0
for open_image in open_images:
    new.paste(open_image, (0, running_height))
    running_height += open_image.size[1]
    
new.save('auto_cobined.png', 'PNG', optimize=True, quality=95)