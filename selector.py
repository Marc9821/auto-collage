from tkinter import *  
from PIL import ImageTk, Image


def draw(image_name, width, height):    
    img_max_width = 520
    img_max_height = 652

    root = Tk()  
    canvas = Canvas(root, width=width*1.1, height=height*1.1)  
    canvas.pack()
    
    img = Image.open(image_name)
    
    w, h = img.size
    w_ratio, h_ratio = img_max_width/w, img_max_height/h
            
    if w_ratio > h_ratio:
        img = img.resize((int(w * w_ratio), int(h * w_ratio)))
    else:
        img = img.resize((int(w * h_ratio), int(h * h_ratio)))
    
    img_size = img.size
    img = ImageTk.PhotoImage(img)
    border_w = int(img_max_width*0.05)
    border_h = int(img_max_height*0.05)
    
    i1 = canvas.create_image(border_w, border_h, anchor=NW, image=img)
    
    create_rectangle(root, canvas, border_w, border_h, border_w + img_max_width, border_h + img_max_height, fill='red', alpha=.2)
    
    global last_coords
    last_coords = [(border_w, border_h, border_w + img_max_width, border_h + img_max_height)]
    
    my_label = Label(root, text="")
    my_label.pack(pady=10)
    
    data = {'canvas': canvas, 'border_w': border_w, 'border_h': border_h, 'img_size': img_size, 'root': root, 'my_label': my_label}
    
    root.bind("<Key>", lambda event, arg=data: keypress(event, arg))
    root.bind("<B1-Motion>", lambda event, arg=data: mouse_move(event, arg))
    root.bind("<MouseWheel>", lambda event, arg=data: mouse_zoom(event, arg))
    root.bind("<Return>", lambda e: root.destroy())
    root.state('zoomed')
    root.grab_set()
    root.focus()
    root.mainloop()
    
    x, y, x1, y1 = calc_coords(last_coords, border_w, border_h)
    
    return x, y, x1, y1
    
images=[]
def create_rectangle(root, canvas, x,y,a,b,**options):
    if 'alpha' in options:
        alpha = int(options.pop('alpha') * 255)
        fill = options.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (a-x, b-y), fill)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x, y, image=images[-1], anchor='nw', tag='rect')
        return
        
def keypress(event, arg):
    canvas = arg['canvas']
    
    # do not allow rectangle to move outside of selectable area
    border_w = arg['border_w']
    border_h = arg['border_h']
    img_size = arg['img_size']
    current_position = canvas.bbox('rect')
    c_x_min = border_w
    c_x_max = border_w + img_size[0]
    c_y_min = border_h
    c_y_max = border_h + img_size[1]
    
    if event.char == '+' or event.char == '-':
        zoomer(event, arg, current_position)
    
    if len(last_coords) > 1:
        last_coords.pop(0)
    x = y = 0
    if event.char == "a": 
        x = -10
        if current_position[0] + x < c_x_min:
            x = 0
    elif event.char == "d": 
        x = 10
        if current_position[2] + x > c_x_max:
            x = 0
    elif event.char == "w": 
        y = -10
        if current_position[1] + y < c_y_min:
            y = 0
    elif event.char == "s": 
        y = 10
        if current_position[3] + y > c_y_max:
            y = 0
    canvas.move('rect', x, y)
    last_coords.append(canvas.bbox('rect'))

def zoomer(event, arg, current_position):
    scaling_factor = 0.95
    canvas = arg['canvas']
    root = arg['root']
    max_width, max_height = arg['img_size']
    x1, y1, x2, y2 = current_position
    width = x2 - x1
    height = y2 - y1
    
    mode = ''
    if event.char == '-':
        mode = 'out'
    elif event.char == '+':
        mode = 'in'
    elif event.delta >= 0:
        mode = 'out'
    else:
        mode = 'in'
    
    #do not allow rectangle to be bigger than image or smaller than 20% of original image width
    if mode == 'out':
        if width/scaling_factor > max_width or height/scaling_factor > max_height:
            return
    elif width/max_width < 0.2 or height/max_height < 0.2:
        return
    #initiate new rectangle creation
    if mode == 'in':
        w_n = int(width * scaling_factor)
        h_n = int(height * scaling_factor)
    else:
        w_n = int(width / scaling_factor)
        h_n = int(height / scaling_factor)
    border_w = arg['border_w']
    border_h = arg['border_h']
    #delete old rectangle
    canvas.delete('rect')
    #create new rectangle
    create_rectangle(root, canvas, border_w, border_h, border_w + w_n, border_h + h_n, fill='red', alpha=.2)

def mouse_move(event, arg):
    my_label = arg['my_label']
    my_label.config(text=f'Coordinates: x={event.x} y={event.y}')

def mouse_zoom(event, arg):
    canvas = arg['canvas']
    current_position = canvas.bbox('rect')
    zoomer(event, arg, current_position)

def calc_coords(coordinates, border_w, border_h):
    x = coordinates[0][0]-border_w
    y = coordinates[0][1]-border_h
    x1 = coordinates[0][2]-border_w
    y1 = coordinates[0][3]-border_h
    return x, y, x1, y1