from PIL import Image
import numpy as np
import matplotlib.pyplot as plt




def read_img(in_file, offset):
    in_file = open(in_file, "rb")
    in_file.seek(offset)
    lines = in_file.read(784)
    l = list(lines)
    return l

def convert_matrix(in_file, offset):
    img = read_img(in_file, offset)
    for i in range(len(img)):
        img[i] = img[i]
    arr = np.array(img)
    arr.resize(28,28)
    return arr

def convert_array(in_file, offset):
        img = read_img(in_file, offset)
        for i in range(len(img)):
            img[i] = ord(img[i])
        arr = np.array(img)
        return arr

def list_labelled_images(image_file, label_file, nbr, number_offset, mode):
    image_list = []
    label_list = []
    image = open(image_file, "rb")
    label = open(label_file, "rb")
    image.seek(16 + 784*number_offset)
    label.seek(8+number_offset)
    for i in range(nbr):
        lines_im = list(image.read(784))
        for j in range(len(lines_im)):
            lines_im[j] = lines_im[j]/float(255)
        image_list.append(lines_im)
        if(mode == 'letters'):
            label_list.append(np.zeros(26))
            a = ord(label.read(1))
            label_list[-1][a-1] = 1
        if(mode == 'digits'):
            label_list.append(np.zeros(10))
            a = ord(label.read(1))
            label_list[-1][a] = 1
        #print (i/(float(nbr)))
    return (image_list, label_list)

def list_labelled_images2D(image_file, label_file, nbr, number_offset, mode):
    image_list = []
    label_list = []
    image = open(image_file, "rb")
    label = open(label_file, "rb")
    image.seek(16 + 784*number_offset)
    label.seek(8+number_offset)
    for i in range(nbr):
        lines_im = np.array(list(image.read(784)))
        lines_im = lines_im/float(255)
        lines_im = np.reshape(lines_im, (1,28,28))
        image_list.append(lines_im)
        if(mode == 'letters'):
            label_list.append(np.zeros(26))
            a = ord(label.read(1))
            label_list[-1][a-1] = 1
        if(mode == 'digits'):
            label_list.append(np.zeros(10))
            a = ord(label.read(1))
            label_list[-1][a] = 1
        #print (i/(float(nbr)))
    return (image_list, label_list)

def list_labelled_images2Dnew(image_file, label_file, nbr, number_offset, mode):
    image_list = []
    image = open(image_file, "rb")
    label = open(label_file, "rb")
    image.seek(16 + 784*number_offset)
    label.seek(8+number_offset)
    for i in range(nbr):
        lines_im = np.array(list(image.read(784)))
        lines_im = lines_im/float(255)
        lines_im = np.reshape(lines_im, (1,28,28))
        if(mode == 'letters'):
            zeros = np.zeros(26)
            a = ord(label.read(1))
            zeros[a-1] = 1
            image_list.append( (lines_im, zeros) )
        if(mode == 'digits'):
            zeros = np.zeros(10)
            a = ord(label.read(1))
            zeros[a-1] = 1
            image_list.append( (lines_im, zeros) )
        #print (i/(float(nbr)))
    return image_list


def print_grey(in_file, offset):
    arr = convert_matrix(in_file, offset)
    plt.imshow(arr,cmap=plt.get_cmap('gray'))

def read_label(in_file, offset):
    in_file = open(in_file, "rb")
    in_file.seek(offset)
    lines = in_file.read(1)
    return ord(lines)

#a = list_labelled_images('train-images-idx3-ubyte', 'train-labels-idx1-ubyte', 10, 0)
#print a
def print_multiple_images(nb, sizeim, offset, input_file):
    fig = plt.figure(figsize=(sizeim,sizeim))
    col = nb/10
    row = nb/col
    print (col,row)
    for i in range(col*row):
        img = convert_matrix(input_file,16+784*(i+offset))
        img = np.flipud(img)
        img = np.rot90(img, 3   )
        fig.add_subplot(row,col,i+1)
        a = plt.imshow(img, cmap=plt.get_cmap('gray'))
        a.axes.get_xaxis().set_visible(False)
        a.axes.get_yaxis().set_visible(False)
    plt.show()

"""a = list_labelled_images('emnist-letters-train-images-idx3-ubyte', 'emnist-letters-train-labels-idx1-ubyte', 10, 50, 52)
print_multiple_images(10, 10, 50, 'emnist-letters-train-images-idx3-ubyte')"""

#a = print_grey('train-images-idx3-ubyte',16)





def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def get_data(file):
    labelled_images = unpickle(file)
    print('getting data from file', file, '... ', end = '')
    X = np.asarray(labelled_images[b'data']).astype("uint8")
    X = np.reshape(X, (10000,3,32,32))
    # X = X.transpose([0, 2, 3, 1])
    X = X/float(255)
    Yraw = np.asarray(labelled_images[b'labels'])
    Y = np.zeros((10000,10))
    for i in range(10000):
        Y[i,Yraw[i]] = 1
    print('done')
    return X,Y
