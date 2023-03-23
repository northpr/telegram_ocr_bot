import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import random

def img_preprocess(img:np): 
    """Preprocess image to make letters clearer while removing background

    Args:
        img (np): Image file

    Returns:
        img_bin (np): Binary image with clearer letters and removed background
    """
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to obtain a binary mask of the black letters
    _, img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert the binary mask to obtain a mask of the background
    img_bg = cv2.bitwise_not(img_bin)

    # Apply color thresholding to the image to remove the background
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([179, 255, 150])
    img_mask = cv2.inRange(img_hsv, lower, upper)

    # Apply the background mask to the color thresholded image
    img_masked = cv2.bitwise_and(img_mask, img_mask, mask=img_bg)

    # Invert the binary mask again to obtain the final binary image
    img_bin_final = cv2.bitwise_not(img_masked)

    # Apply erosion to remove small details and noise from the background
    kernel = np.ones((2, 2), np.uint8)
    img_erode = cv2.erode(img_bin_final, kernel, iterations=1)

    # Apply dilation to make the letters thicker
    # img_dilate = cv2.dilate(img_erode, kernel, iterations=1)

    return img_erode

def random_image(directory: str)->str : 
    # Get a list of all subdirectories in the given directory
    subdirectories = [os.path.join(directory, name) for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

    # If there are no subdirectories, return None
    if not subdirectories:
        return None

    # Pick a random subdirectory
    random_subdirectory = random.choice(subdirectories)

    # Get a list of all image files in the random subdirectory and its subdirectories
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    image_files = []
    for root, dirs, files in os.walk(random_subdirectory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(os.path.join(root, file))

    # If there are no image files, return None
    if not image_files:
        return None

    # Pick a random image file and return its path
    random_image_path = random.choice(image_files)
    return random_image_path


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


