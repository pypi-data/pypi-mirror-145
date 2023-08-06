import matplotlib.image as mpimg

def read_image(path):
    image = mpimg.imread(path)
    return image