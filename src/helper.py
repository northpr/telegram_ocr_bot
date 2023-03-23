import matplotlib.pyplot as plt
import numpy as np
import cv2

def img_load(bankname: str, filename: str):
    """Load image to variable

    Args:
        bankname: bkb, kbank, ksb, scb
        filename: name of img in the folder
    """
    full_dir = "../data/"+ bankname + "/" + filename + ".jpg"
    img = plt.imread(full_dir)
    return img

def img_show_high(img, x_ticks:int=30, y_ticks:int=30, x_lim:int=1000, y_lim:int=1000):
    """Show image in mode detailed of coordinates
    Example:
        bank_name, file_name = "kbank", "S__20307981"
        img_test = img_load(bankname=bank_name, filename=file_name)
        img_show_high(img_test)

    Args:
        img (_type_): fill the img in it
        x_ticks (int, optional): Show how detailed of coordinated should be on x axis. Defaults to 30.
        y_ticks (int, optional): Show how detailed of coordinated should be on y axis. Defaults to 30.
        x_lim (int, optional): Limit of x-axis. Defaults to 1000.
        y_lim (int, optional): Limit of y-axis. Defaults to 1000.
    """
    # Show more coordinates
    x = np.arange(0, x_lim, x_ticks)
    y = np.arange(0, y_lim, y_ticks)
    plt.figure(figsize=(14,10))
    plt.xticks(x)
    plt.yticks(y)
    plt.imshow(img);

def get_var_name(variable):
    """Print the name of variable

    Args:
        variable (_type_): _description_

    Returns:
        _type_: String
        
    Examples:
        apple = 3
        print(get_var_name(apple))
        -> "apple"
    """
    globals_dict = globals()
    name = [var_name for var_name in globals_dict if globals_dict[var_name] is variable]
    return name[0]

def show_images(list_of_images:list, rows:int, columns:int, size_x:int=20, size_y:int=20):
    """
    Show the list of images
    Example: show_images(img_list,rows=1,columns=2)
    """
    if len(list_of_images)>(rows*columns):
        return "Check the input"
    plt.figure(figsize=(size_x, size_y))
    for i in range(len(list_of_images)):
        y_shape = list_of_images[i].shape[0]
        x_shape = list_of_images[i].shape[1]
        plt.subplot(rows, columns, i+1);plt.imshow(list_of_images[i]);plt.title(f"{get_var_name(list_of_images[i])} | {x_shape}x{y_shape}");

def img_preprocess(img:np): 
    """Preprocess image to dialate the background of a photo

    Args:
        img (np): Image file

    Returns:
        img_bin (np): Return an image that has clearer letter
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Remove noise using erosion
    kernel = np.ones((2, 2), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    return img_bin
