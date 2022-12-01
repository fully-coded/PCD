import imutils
import cv2
import numpy as np
import matplotlib.pyplot as plt

# edge detection
image = cv2.imread('cataracts.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (5, 5), 0)
canny = cv2.Canny(image, 30, 150)

# circle detection
img = cv2.medianBlur(image, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

detected_circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, 1,
                                    param1=50,
                                    param2=30,
                                    minDist=100,
                                    minRadius=100,
                                    maxRadius=140)

if detected_circles is not None:
    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]

        # Draw the circumference of the circle.
        cv2.circle(img, (a, b), r, (0, 255, 0), 2)

        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

cv2.imshow("Detected circles", img)
cv2.waitKey(0)


plt.title('Circle Detected')
plt.xticks([])
plt.yticks([])
plt.imshow(cimg, cmap='gray')
plt.show()
