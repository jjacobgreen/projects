from PIL import Image
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

img = Image.open('images/ascii-pineapple.jpg')
img_array = np.array(img)
gray_array = np.mean(img_array, 2)
# ascii_array = np.empty([img_array.shape[0], img_array.shape[1]])
ascii_array = np.chararray([img_array.shape[0], img_array.shape[1]])
print(img_array.shape)


ascii_chars = "`^,:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# Normalise to length of ascii chars
gray_array = np.floor(len(ascii_chars) * gray_array / 255)

for x in range(0, gray_array.shape[0]):
    for y in range(0, gray_array.shape[1]):
        ascii_array[x, y] = str(ascii_chars[int(gray_array[x, y])])

print(ascii_array.shape)
# ascii_array = np.array([['hello', 'hi'], ['hi there', 'oh hi']])
np.savetxt('images/ascii_art_output', ascii_array, fmt='%s', delimiter='')#, newline='\n')
# (fname, X, fmt='%.18e', delimiter=' ', newline='n', header='', footer='', comments='# ', encoding=None)
