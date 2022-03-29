import os
import glob
from tkinter import *
from PIL import Image
from selector import draw

def create_collage():

    #settings
    img_max_width, img_max_height = 520, 652
    n_rows = 6
    folders = ["O","B","L","A","A2","C"]
    row_dist, col_dist = 30, 30

    #read in all images
    image_list = []
    for folder in folders:
        temp_list = []
        for filename in glob.glob(folder + '\*.jpg'):
            temp_list.append(filename)
        for filename in glob.glob(folder + '\*.png'):
            temp_list.append(filename)
        for filename in glob.glob(folder + '\*.jpeg'):
            temp_list.append(filename)
        temp_list.sort()
        image_list.append(temp_list)
        
    n_cols = len(image_list[0])
    
    
    collage = (img_max_width * n_cols + col_dist * (n_cols - 1), img_max_height * n_rows + row_dist * (n_rows - 1))
    new = Image.new("RGBA", collage, "WHITE")
    
    #check if enough images available   
    for i, img_list in enumerate(image_list):
        if len(img_list) < n_cols:
            print(f'Please add {n_cols-len(img_list)} image(s) to the folder {folders[i]}!')
            return

    #create collage
    running_row = running_col = 0
    for row in range(n_rows):
        for col in range(n_cols):
            img = Image.open(image_list[row][col])
            w, h = img.size
            if img_max_width > 1.2 * w or img_max_height > 1.2 * h:
                print(f'Image {image_list[row][col]} is too small!')
                return
            w_ratio, h_ratio = img_max_width/w, img_max_height/h
            
            if w_ratio > h_ratio:
                img = img.resize((int(w * w_ratio), int(h * w_ratio)))
                x, y, x1, y1 = draw(image_list[row][col], int(w * w_ratio), int(h * w_ratio), img_max_width, img_max_height)
            else:
                img = img.resize((int(w * h_ratio), int(h * h_ratio)))
                x, y, x1, y1 = draw(image_list[row][col], int(w * h_ratio), int(h * h_ratio), img_max_width, img_max_height)
            
            img = img.crop((x, y, x1, y1))
            
            n_w, n_h = img.size
            
            n_w_ratio, n_h_ratio = img_max_width/n_w, img_max_height/n_h
            if n_w_ratio > n_h_ratio:
                img = img.resize((int(n_w * n_w_ratio), int(n_h * n_w_ratio)))
            else:
                img = img.resize((int(n_w * n_h_ratio), int(n_h * n_h_ratio)))
            
            new.paste(img, (running_col, running_row))
            running_col += img_max_width + col_dist
        running_row += img_max_height + row_dist
        running_col = 0

    #show image
    # new.show()
    #save image
    new.save('Finished_.png', 'PNG', optimize=True, quality=95)
    
    delete_images(folders)
    
def delete_images(folders):
    directory = os.getcwd()
    prompt = 'Delete files in folders? (y/n):\n   '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        return delete_images()
    if ans == 'y':
        for folder in folders:
            dir = directory.replace(r'/', '/') + '/' + folder
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
        return
    return
    
if __name__ == '__main__':
    create_collage()