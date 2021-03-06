################################################################### SUDOKU SOLVER PROGRAM ############################################################################################

# importing necessary libraries - opencv,numpy,pillow and tessarect
import cv2
import numpy as np
from PIL import Image
import pytesseract

k = 1

#############################################################################################################################################################################################################

#creating 9x9 sudoku grid with all element zero
board = []
for i in range(0, 9):
    board.append([])
    for j in range(0, 9):
        board[i].append(0)

#############################################################################################################################################################################################################

# function to check the order of points
#this prevent rotation of image in homography transition


def order(ar):
    ar1 = [[0, 0], [0, 0], [0, 0], [0, 0]]
    max = 0
    ymax = 0
    min = 99999
    for i in range(len(ar)):
        if (ar[i][0][0] + ar[i][0][1]) > max:
            max = ar[i][0][0] + ar[i][0][1]
            ar1[2][0] = ar[i][0][0]
            ar1[2][1] = ar[i][0][1]
        if (ar[i][0][0] + ar[i][0][1]) < min:
            min = ar[i][0][0] + ar[i][0][1]
            ar1[0][0] = ar[i][0][0]
            ar1[0][1] = ar[i][0][1]

    for i in range(len(ar)):
        if (ar[i][0][0] + ar[i][0][1]) < max and (
                ar[i][0][0] + ar[i][0][1]) > min and ar[i][0][1] > ymax:
            ar1[1][0] = ar[i][0][0]
            ar1[1][1] = ar[i][0][1]
            ymax = ar[i][0][1]
    for i in range(len(ar)):
        if (ar[i][0][0] + ar[i][0][1]) < max and (
                ar[i][0][0] + ar[i][0][1]) > min and ar[i][0][1] < ymax:
            ar1[3][0] = ar[i][0][0]
            ar1[3][1] = ar[i][0][1]

    return ar1


############################################################################# SUDOKU SOLVING CODE ####################################################################################

#sudoku solving algoritm

size = 9

#function to print solved sudoku grid


def print_grid(arr):
    for i in range(9):
        print(arr[i])


# checking empty location that means 0 position in grid


def empty(arr, l):
    for row in range(9):
        for col in range(9):
            if (arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return False
    return True


#checking possibilty of a no in a row


def checkrow(arr, row, num):
    for i in range(9):
        if (arr[row][i] == num):
            return False
    return True


#checking possibilty of no in column


def checkcol(arr, col, num):
    for i in range(9):
        if (arr[i][col] == num):
            return False
    return True


#checking possibilities of a no in 3x3 sudoku grid


def checkbox(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if (arr[i + row][j + col] == num):
                return False
    return True


# this check the possibilties of a no in a particular place by calling checkrow(),checkcol(),checkbox() functions
def safe(arr, row, col, num):

    return checkrow(arr, row, num) and checkcol(arr, col, num) and checkbox(
        arr, row - (row % 3), col - (col % 3), num)


#this function check the possibilties of all no and produce a solution
def solve_sudoku(arr):
    #use of recursive backtracking algorithm
    l = [0, 0]
    #calling function for free space
    if (empty(arr, l)):
        return True

    row = l[0]
    col = l[1]

    #checking possiblities of all digits
    for num in range(1, 10):
        if (safe(arr, row, col, num)):

            # if there is possibility we keep that no
            arr[row][col] = num

            #moving towards next grid
            if (solve_sudoku(arr)):
                return True

#if not possible it will backtrack
            arr[row][col] = 0

    return False


#ssolver function is check wheather a solution exist or not
def ssolver(board):

    #printing sudoku

    if (solve_sudoku(board)):
        print_grid(board)
    else:
        print("No solution exists")


#############################################################################################################################################################################################################


# function to get ocr no into matrix
def inputb(board, k, no):
    count = 1
    for i in range(9):
        for j in range(9):

            if count == k:
                #checking the no possibility at that position
                #this is to reduce errors
                if safe(board, i, j, no):
                    board[i][j] = no
            count += 1


############################################################################################################################################################################################################

# use of webcam to capture image of sudoku

# def read(self):
#   ret, frame = self.cam.read()
#   return cv2.flip(frame, 1)

# def update(self):
#   cv2.imshow('frame', self.read())

ar = None
count = 0
# webcam is open
cap = cv2.VideoCapture(0)
while (1):
    key = cv2.waitKey(1) & 0xFF
    #reading  frame from webcam
    ret, frame = cap.read()
    k = 0
    # converting image to grayscale and then applying blurs to remove noise
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.GaussianBlur(img, (55, 55), 3)
    #thresholding frame in binary by adaptive thresholding

    thresh = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    cv2.imshow('thresh', thresh)
    #finding contours in image to find sudoku grid
    contours, hie = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
    #max is variable for maximum area and maxc for maximum contours
    maxc = [0]
    max = 0
    #loop to find largest contour in given frame
    for i in range(len(contours)):
        # finding perimeter of contour and contour approximation
        peri = cv2.arcLength(contours[i], True)
        approx = cv2.approxPolyDP(contours[i], 0.011 * peri, True)

        if cv2.contourArea(contours[i]) > 10000 and cv2.contourArea(
                contours[i]) > max and len(approx) == 4:
            #checking maximum contours

            max = cv2.contourArea(contours[i])
            maxc = approx
    #if contour have four corners then saving that frame and drawing contours
    if len(maxc) == 4:
        count = count + 1
    else:
        count = 0
    if len(maxc) == 4:
        cv2.drawContours(frame, [maxc], -1, (255, 0, 2), 5)
        cv2.drawContours(frame, maxc, -1, (
            0,
            255,
        ), 8)

#displaying contous edges and corners

    cv2.imshow('all', cv2.flip(frame,1))
    # cv2.waitKey(1)
    # if count == 4:
    if key == ord('c'):
        cv2.imwrite("frame.jpg", frame)
        ar = maxc
        k = 1

    if k == 1:
        break

#############################################################################################################################################################################################################

cv2.destroyAllWindows()

#calling function for proper order of points
ar = order(ar)
cap.release()

#reading frame
frame = cv2.imread('frame.jpg', 1)

#homography transition of sudoku grid
#converting it into 28x3x3 grid
pts2 = np.float32([[0, 0], [0, 252], [252, 252], [252, 0]])
ar = np.float32(ar)

#applying perpective transformation for parallelism of lines using four corner points
M = cv2.getPerspectiveTransform(ar, pts2)
transform = cv2.warpPerspective(img, M, dsize=(252, 252))

cv2.imwrite('bin.jpg', transform)
cv2.imshow('transform', transform)

#cropping the image to every number grid
for i in range(9):
    for j in range(9):
        crop = transform[(i * 28):((i + 1) * 28), (j * 28):((j + 1) * 28)]
        cv2.imshow('crop', crop)
        crop = cv2.GaussianBlur(crop, (5, 5), 1)
        #storing the image

        cv2.imwrite('Img{}.png'.format(k), crop)
        k = k + 1

        cv2.waitKey(1)

############################################################################################################################################################################################################

#for creating list for spaces and number
sum = 0
count = 0
lst = list()
lst1 = list()

for k in range(1, 82):
    #reading each no grid
    crop = cv2.imread('Img{}.png'.format(k), 0)
    sum = 0
    crop = cv2.adaptiveThreshold(crop, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY, 3, 2)
    #appending list with its no and and image
    #checking the sum of pixels to differentiate between no and space
    lst.append([k, crop])
    for i in range(10, 19):
        for j in range(10, 19):
            sum = sum + crop[i, j]
    j = 81 - (sum / 255)
    #differentiating no and spaces
    if j >= 10:
        count += 1
        lst1.append(k)

#############################################################################################################################################################################################################

#array creation
image = np.empty([count, 28, 28, 1])
grid = cv2.imread('bin.jpg', 1)
for k in range(count):

    #reading each no grid
    crop = cv2.imread('Img{}.png'.format(lst1[k]), 0)

    #thresholding of each grid by adative thresholding and ostus binarisation
    crop = cv2.adaptiveThreshold(crop, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY, 3, 2)
    ret, crop = cv2.threshold(crop, 0, 255,
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    #max variable for maximum area and max2 for largest no of contour
    max2 = [0]
    max = 0
    crop1 = crop.copy()
    contours, hie = cv2.findContours(crop, cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):

        if cv2.contourArea(contours[i]) > max:
            #checking maximum contours

            max = cv2.contourArea(contours[i])
            max2 = contours[i]
#filling the largest contours and removing others by thresholding
    cv2.drawContours(crop, [max2], -1, (255, 255, 255), -1)
    ret, thresh = cv2.threshold(crop, 254, 255, cv2.THRESH_BINARY)
    #masking to remove edges
    crop = cv2.bitwise_and(crop1, crop1, mask=thresh)
    ret, crop = cv2.threshold(crop, 254, 255, cv2.THRESH_BINARY_INV)
    #again dilation and erosion for better result
    crop = cv2.erode(crop, kernel)
    crop = cv2.dilate(crop, kernel)
    #saving the binary iamges for ocr
    cv2.imwrite('s{}.png'.format(k), crop)

    if k == len(lst1):
        break
    #dilation and erosion of no for better sharp image
    crop = cv2.dilate(crop, kernel)
    crop = cv2.erode(crop, kernel)

    #finding contours to remove noise and edges


#############################################################################################################################################################################################################

#pytesseract OCR to recognise the no
    image = Image.open('s{}.png'.format(k))

    string = pytesseract.image_to_string(
        image,
        lang='eng',
        # boxes=False,
        config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    print(string)

    #checking wheather the give character is no or not
    if string[0] >= '1' and string[0] <= '9':

        # if the ocr identify a digit the it is passed to matrix by calling inputb() function
        inputb(board, lst1[k], int(string[0]))

#############################################################################################################################################################################################################

#sudoku solver function

print("\n\n")
ssolver(board)

##############################################################################################################################################################################################################

dst = cv2.imread('bin.jpg', 1)

#writing the answer on sudoku
# font type to write on no
font = cv2.FONT_HERSHEY_SIMPLEX
#loop to print no
for i in range(9):
    for j in range(9):
        if (board[j][i] != 0):
            #coordinate position in image
            x = (i * 28 + 8)
            y = ((j) * 28 + 20)
            #converion of no to string
            str1 = str(board[j][i])
            #using puttext function for printing no on image
            cv2.putText(dst, str1, (x, y), font, 0.8, (0, 255, 255), 2, 2)
            #increasing size of sudoku
            restext = cv2.resize(dst,
                                 None,
                                 fx=4,
                                 fy=4,
                                 interpolation=cv2.INTER_CUBIC)
            cv2.imshow('dst', restext)
            #large time lapse for printing no one by one
            cv2.waitKey(50)

cv2.imwrite('ans.jpg', restext)

cv2.waitKey(0)
cv2.destroyAllWindows()
