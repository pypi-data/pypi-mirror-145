import matplotlib.pyplot as plt
from skimage.color import rgb2gray

def gray(image):
    
    grayscale = rgb2gray(image)
    fig, axes = plt.subplots(1, figsize=(16, 8))

    fig.tight_layout()
    plt.imshow(grayscale, cmap='gray')
    plt.axis('off')
    plt.savefig('image_gray.png', format='png')

    plt.show()

def red(image):
    
    red_multiplier = [1, 0, 0]
    fig, axes = plt.subplots(1, figsize=(16, 8))

    fig.tight_layout()
    plt.imshow(red_multiplier * image)
    plt.axis('off')
    plt.savefig('image_red.png', format='png')

    plt.show()

def yellow(image):
    
    yellow_multiplier = [1, 1, 0]
    fig, axes = plt.subplots(1, figsize=(16, 8))

    fig.tight_layout()
    plt.imshow(yellow_multiplier * image)
    plt.axis('off')
    plt.savefig('image_yellow.png', format='png')

    plt.show()

def blue(image):
    
    blue_multiplier = [0, 1, 1]
    fig, axes = plt.subplots(1, figsize=(16, 8))

    fig.tight_layout()
    plt.imshow(blue_multiplier * image)
    plt.axis('off')
    plt.savefig('image_blue.png', format='png')

    plt.show()

def green(image):
    
    green_multiplier = [0, 1, 0]
    fig, axes = plt.subplots(1, figsize=(16, 8))

    fig.tight_layout()
    plt.imshow(green_multiplier * image)
    plt.axis('off')
    plt.savefig('image_green.png', format='png')

    plt.show()