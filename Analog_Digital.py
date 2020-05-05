import cv2
import numpy

# Digital Gauge Specification
# 45 deg = 0
# 315 deg = 100
# diff between readings = 27 deg

img = cv2.imread("gauge-2.jpg")
height, width, channel = img.shape
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Takes an average of all the circles for better accuaracy
def avg_circle(circle, n):
    x = 0
    y = 0
    r = 0
    for p in range(n):
        x = x + circle[0][p][0]
        y = y + circle[0][p][1]
        r = r + circle[0][p][2]
    x = int(x / n)
    y = int(y / n)
    r = int(r / n)
    return x, y, r


# Changes the value of the line in form of Degrees to Actual Value
def ang_val_convert(deg):
    value = 10/27 * deg - 16.67
    return value


th, gray2 = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
# Detection of the Gauge Centre and Gauge Circular Scale
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, 100, 50, minRadius=200, maxRadius=0)
a, b, c = circles.shape
x, y, z = avg_circle(circles, b)
x = int(x)
y = int(y)
z = int(z)
img = cv2.circle(img, (x, y), z, (0, 255, 0), 3, cv2.LINE_AA)
img = cv2.circle(img, (x, y), 2, (255, 0, 0), 2, cv2.LINE_AA)

# Dividing the Gauge Scale into Segments of 10 degrees difference
dx = 0
points1 = numpy.zeros((36, 2))
points2 = numpy.zeros((36, 2))
for i in range(0, 36):
    for j in range(0, 2):
        if j == 0:
            points1[i][j] = x + z * numpy.cos(dx * numpy.pi / 180)
            points2[i][j] = x + 0.9 * z * numpy.cos(dx * numpy.pi / 180)
        else:
            points1[i][j] = y + z * numpy.sin(dx * numpy.pi / 180)
            points2[i][j] = y + 0.9 * z * numpy.sin(dx * numpy.pi / 180)
    dx = dx + 10
    img = cv2.line(img, (int(points1[i][0]), int(points1[i][1])), (int(points2[i][0]), int(points2[i][1])), (0, 0, 255), 2)

# Detecting the Gauge needle
lines = cv2.HoughLinesP(gray2, rho=3, theta=numpy.pi/180, threshold=160, minLineLength=80)

# Filtering out the redundant lines
final_line = []
for i in range(0, len(lines)):
    for x1, y1, x2, y2 in lines[i]:
        t1 = (x1 > x and y1 > y) and (x2 > x and y2 > y)
        t2 = (x1 < x and y1 > y) and (x2 < x and y2 > y)
        t3 = (x1 > x and y1 < y) and (x2 > x and y2 < y)
        t4 = (x1 < x and y1 < y) and (x2 < x and y2 < y)
        if t1 or t2 or t3 or t4:
            dist1 = numpy.sqrt((x1-x)**2 + (y1 - y)**2)
            dist2 = numpy.sqrt((x2-x)**2 + (y2 - y)**2)
            dist_1 = min(dist1, dist2)
            dist_2 = max(dist1, dist2)
            if dist_2 < z - 10:
                final_line.append((x1, y1, x2, y2))
                img = cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

x1, y1, x2, y2 = final_line[0]

# print(x, y, z)
# print(final_line[0])
img = cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
theta = numpy.arctan(abs(y1 - y2)/abs(x1 - x2))
theta = numpy.rad2deg(theta)
angle = 0

# Converting the lines position (x1, x2, y1, y2) into degrees
if x2 > x and y2 < y:
    angle = 90 + theta
elif x2 < x and y2 < y:
    angle = 270 - theta
elif x2 < x and y2 > y:
    angle = 360 - theta
else:
    angle = 90 - theta

val = ang_val_convert(angle)

print("Value = ", val)
cv2.imshow("Gauge", img)
cv2.imshow("Binary Img", gray2)
cv2.waitKey(0)
cv2.destroyAllWindows()
