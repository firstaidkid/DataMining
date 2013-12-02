from os.path import isdir,join,normpath
from os import listdir

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import Image

from numpy import asfarray,dot,argmin,zeros, array
from numpy import average,sort,trace,argsort
from numpy.linalg import svd,eigh
from numpy import concatenate, reshape, vstack
from math import sqrt

import tkFileDialog

def parseDirectory(directoryName,extension):
    '''This method returns a list of all filenames in the Directory directoryName. 
    For each file the complete absolute path is given in a normalized manner (with 
    double backslashes). Moreover only files with the specified extension are returned in 
    the list.
    '''
    if not isdir(directoryName): return
    imagefilenameslist=sorted([
        normpath(join(directoryName, fname))
        for fname in listdir(directoryName)
        if fname.lower().endswith('.'+extension)            
        ])
    return imagefilenameslist

#####################################################################################
# Implement required functions here
#
#
#
def generateListOfImgs(listOfTrainFiles):
    result = list()
    # go through each file in the list
    for fileName in listOfTrainFiles:
        # open the image
        img = Image.open(fileName)

        # convert to grayscale
        img = img.convert('L')

        # get size
        g_width, g_height = img.size

        # print data
        #print "Grab Image (%s), w: %f, h:%f" % (img, g_width, g_height)

        # add to results-list
        result.append(img)
    return result


def convertImgListToNumpyData(imgList):
    imgArrays = list()

    for image in imgList:
        # save data into array
        npImage = asfarray(image)

        # reshape to one line
        npImage = npImage.reshape(1, image.size[0]*image.size[1])

        # get the maximum value for this images
        maxValue = npImage.max()

        # normalize
        npImage = npImage/maxValue

        # push into results
        imgArrays.append(npImage)

    return concatenate(imgArrays, axis=0)


def calculateEigenfaces(adjfaces, width, height):
    # number of relevant vectors
    K = 6

    # calulate the quadratic matrix MxM
    quadMatrix = dot(adjfaces, adjfaces.transpose())

    # Calculate Eigenvalues and Eigenvectors
    eigenValues, eigenVectors = eigh(quadMatrix)

    # get sortindices for reverse sorting
    sortIndices = argsort(eigenValues)[::-1]

    # apply indices to arrays
    #eigenValues = eigenValues[sortIndices][:K]
    eigenVectors = eigenVectors[sortIndices][:K]

    return eigenVectors





####################################################################################
#Start of main programm

#Choose Directory which contains all training images 
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
#Choose the file extension of the image files
Extension='png' 
#Choose the image which shall be recognized
testImageDirAndFilename=tkFileDialog.askopenfilename(title="Choose Image to detect")

####################################################################################
# Implement required functionality of the main programm here

# global height/width
g_width = 0
g_height = 0

# store all training-images in a list
trainImages = generateListOfImgs(parseDirectory(TrainDir, Extension))

# store the test-image
testImage = Image.open(testImageDirAndFilename)

# get numpyArray
NormedArrayOfFaces = convertImgListToNumpyData(trainImages)

# get the normed image
normedImage = average(NormedArrayOfFaces, axis=0)

# remove average image from all images
for image in NormedArrayOfFaces:
    image = image - normedImage

# Calulate Eigenfaces with K = 6
Usub = calculateEigenfaces(NormedArrayOfFaces, g_width, g_height)

# calculate coordinates of the Normed Images in the Eigenface-Room
NormedArrayOfFaces = dot(Usub, NormedArrayOfFaces)