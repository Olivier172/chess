

import cv2
import os
import glob
folder = 'data\games'

# Get a list of all the images in the folder
images = glob.glob(os.path.join(folder, '*.jpg'))


for image in images:
    # Load the image
    img = cv2.imread(image)
    h,w,_ = img.shape
    
    # Resize the image
    img_resized = cv2.resize(img, (w // 4, h // 4), interpolation=cv2.INTER_AREA)

    # Save the resized image
    new_file = image.replace('.jpg', '_small.jpg')
    cv2.imwrite(new_file, img_resized)