from os.path import isdir,join,normpath
from os import listdir

import sys

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import Image

from numpy import asfarray,dot,argmin,zeros, array
from numpy import average,sort,trace,argsort
import numpy as np
from numpy.linalg import svd,eigh
from numpy import concatenate, reshape, vstack
from math import sqrt

import Tkinter
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

def convertImgToNumpyData(img):
    imgList = list()
    imgList.append(img)

    numpyList = convertImgListToNumpyData(imgList)
    return numpyList[0]


def calculateEigenfaces(adjfaces, width, height, K):
    # calulate the quadratic matrix MxM
    CV = dot(adjfaces, adjfaces.transpose())

    # Calculate Eigenvalues and Eigenvectors
    eigenValues, eigenVectors = eigh(CV)

    # get sortindices for reverse sorting
    sortIndices = argsort(eigenValues)[::-1]

    # apply indices to arrays
    eigenValues = eigenValues[sortIndices]
    eigenVectors = eigenVectors[sortIndices]

    # calculate Eigenfaces from Eigenvectors
    Eigenfaces = dot(adjfaces.transpose(), eigenVectors).transpose()

    # restrict to K faces
    return Eigenfaces[:K]


def subtractAverageImage(ArrayOfFaces, AverageImage):
    # remove average image from all images
    NormedArrayOfFaces = ArrayOfFaces.copy()
    for image in NormedArrayOfFaces:
        image = image - AverageImage

    return NormedArrayOfFaces

def calculateEigenfaceCoordinates(NormedArrayOfFaces, Usub):
    EigenfaceCoordinates = np.zeros((Usub.shape[0], NormedArrayOfFaces.shape[0]))

    # go through each of the normed images
    for i in range(NormedArrayOfFaces.shape[0]):
        
        # go through each of the eigenvectors of the eigenface
        for k in range(Usub.shape[0]):

            # calculate eingeface-coordinate of that image by multiplying it with the eigenvector
            EigenfaceCoordinates[k,i] = dot(Usub[k,:], NormedArrayOfFaces[i, :])

    return EigenfaceCoordinates.transpose()


def calculateEigenfaceCoordinatesForTestimage(NormedTestFace, Usub):
    TestfaceCoordinates = np.zeros((Usub.shape[0])) #calculateEigenfaceCoordinates(NormedTestFace, Usub)

    # go through each of the eigenvectors of the eigenface
    for k in range(Usub.shape[0]):
        # calculate eingeface-coordinate of that image by multiplying it with the eigenvector
        TestfaceCoordinates[k] = dot(Usub[k,:], NormedTestFace)

    return TestfaceCoordinates


# easy way to calculate euclidean distance between two arrays
def euclideanDist(A, B):
    return np.linalg.norm(A-B)

def getNearestImage(TestfaceCoordinates, EigenfaceCoordinates):
    dist = sys.float_info.max
    nearestImageIdx = 0
    for idx, faceCoordinates in enumerate(EigenfaceCoordinates):
        newDist = euclideanDist(TestfaceCoordinates, faceCoordinates)
        if dist > newDist:
            nearestImageIdx = idx
            dist = newDist

    return nearestImageIdx, dist


####################################################################################
#Start of main programm

#Choose Directory which contains all training images
root = Tkinter.Tk()
root.withdraw()
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
#Choose the file extension of the image files
Extension='png' 
#Choose the image which shall be recognized
testImageDirAndFilename=tkFileDialog.askopenfilename(title="Choose Image to detect")
root.destroy()

####################################################################################
# Implement required functionality of the main programm here

# global height/width
g_width = 167
g_height = 250

# store all training-images in a list
trainImages = generateListOfImgs(parseDirectory(TrainDir, Extension))

# get numpyArray
ArrayOfFaces = convertImgListToNumpyData(trainImages)

# get the normed image
AverageImage = average(ArrayOfFaces, axis=0)

# remove average image from all images
NormedArrayOfFaces = subtractAverageImage(ArrayOfFaces, AverageImage)

# Calulate Eigenfaces with K = 6
Usub = calculateEigenfaces(NormedArrayOfFaces, g_width, g_height, 6)

### Show all Eigenfaces as Images
eigenfaceFig = plt.figure()
for i in range(Usub.shape[0]):
        picture = Usub[i, :]
        PicCopy = np.reshape(picture, (g_height, g_width) )
        ax = eigenfaceFig.add_subplot(2,3,i)
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        ax.imshow(PicCopy, cmap=plt.cm.gray)

plt.show()

# calculate coordinates of the Normed Images in the Eigenface-Room
EigenfaceCoordinates = calculateEigenfaceCoordinates(NormedArrayOfFaces, Usub)


# 3 Phase Erkennung
# store the test-image
testImage = Image.open(testImageDirAndFilename)

# convert to grayscale
testImage = testImage.convert('L')

# get NumpyArray of test-image
testImageAsNumpy = convertImgToNumpyData(testImage)

# remove average from testImage
NormedTestFace = subtractAverageImage(array(testImageAsNumpy), AverageImage)

# Calculate Eigenface-Coordinates of TestImage
TestfaceCoordinates = calculateEigenfaceCoordinatesForTestimage(NormedTestFace, Usub)

# Get nearest testimage and the distance
NearestImageIndex, dist = getNearestImage(TestfaceCoordinates, EigenfaceCoordinates)

print "NearestImageIndex: %d , dist: %.3f" % (NearestImageIndex, dist)


### Show all Eigenfaces as Images
resultFig = plt.figure()
resultFig.suptitle("Euclidean Distance %.3f" % (dist))

ax = resultFig.add_subplot(1,2,1)
ax.yaxis.set_visible(False)
ax.xaxis.set_visible(False)
ax.imshow(testImage, cmap=plt.cm.gray)

ax2 = resultFig.add_subplot(1,2,2)
ax2.yaxis.set_visible(False)
ax2.xaxis.set_visible(False)
ax2.imshow(trainImages[NearestImageIndex], cmap=plt.cm.gray)

plt.show()













