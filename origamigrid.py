from __future__ import print_function
from collections import namedtuple
from math import sqrt
import numpy as np
import random
try:
    import Image
except ImportError:
    from PIL import Image

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(filename, n=3):
    img = Image.open(filename)
    # img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def colorzFromMatrix(matrix, n=3):
    img = Image.fromarray(matrix, 'RGB')
    # img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbCustomOps = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters

print(list(colorz("butterfly.jpg", 2)))

#1 millimeter = 4 pixels
# WIDTH_MILLI = 6
# HEIGHT_MILLI = 6
# img = Image.open("butterfly.jpg")
# # img.load()
# # data = np.asarray(img, dtype="int32")
# # data = np.array(img)
# # data = img.load()
# data = np.array(img)
# # print(data)
# colt = data[150:200, 150:200]
#
# print(colt)
# print(list(colorzFromMatrix(colt, 1)))
# hex = list(colorzFromMatrix(colt, 1))[0]
# hex = hex.lstrip('#')
# hex_to_rgb = tuple(int(hex[i:i+2], 16) for i in (0,2,4))
# print(hex + " => " + str(hex_to_rgb))
#
# w, h = img.size
# # print(w + " " + h)


def put_into_matrix(matrix, start_x, start_y, step_x, step_y, value):

    for i in range(start_x, start_x + step_x):
        for j in range(start_y, start_y + step_y):
            if i == start_x + step_x or j == start_y + step_y\
                    or i == start_x + step_x - 1 or j == start_y + step_y - 1:
                matrix[i, j] = (0, 0, 0)
            else:
                matrix[i, j] = value
    return matrix


def generate_grid(data, h, w, height, width):
    for step, i in enumerate(range(0, h, height*4)):
        offset = 0
        if step % 2 == 1:
            offset = width // 2 * 4

        for j in range(0 + offset, w, width*4):

            colt = data[i:i + height * 4, j:j + width * 4]
            hex = list(colorzFromMatrix(colt, 1))[0]
            hex = hex.lstrip('#')
            hex_to_rgb = tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))

            if h - i < height * 4 or w - j < width * 4:
                data = put_into_matrix(data, i, j, h-i, w-j, hex_to_rgb)
            else:
                data = put_into_matrix(data, i, j, height * 4, width * 4, hex_to_rgb)
    return data

# # data[150:200, 150:200] = hex_to_rgb
# img = Image.fromarray(data)
# img.save("output.png")
# print(data)

# for i in range(h):
#     for j in range(w):

# m = np.ma.masked_where(y>2, y)
