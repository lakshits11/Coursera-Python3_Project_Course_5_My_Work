import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!

# define a function to get (name, image, text) from a zip file
def zip_images_extraction(name):
    """
    get all the information (name, image, text) from a zip file

    :input: the name of a zip file
    :output: a list of dictoionaries. Each dictionary contains the all the information
    (name, image, text) of a image object.

    """
    # zip name
    zip_name = 'readonly/' + name

    # output
    out = []

    # index out all the information
    with zipfile.ZipFile(zip_name) as myzip:
        zip_infos = myzip.infolist()

        for ele in zip_infos:
            # name
            name = ele.filename
            # image
            img = Image.open(myzip.open(name))
            # text
            img_strs = pytesseract.image_to_string(img.convert('L'))

            # test if "Christopher" or "Mark" are in the text
            if ("Christopher" in img_strs) or ("Mark" in img_strs):
                 # example of dictionary
                my_dic = {"name":name, "img":img, "text":img_strs}
                out.append(my_dic)
    return out
# extract all the information related to small_img.zip and images.zip
small_imgs = zip_images_extraction("small_img.zip")

# big_imgs will be here latter
#big_imgs = zip_images_extraction("images.zip")
# big_imgs will be here latter
big_imgs = zip_images_extraction("images.zip")
# define a function to extract a list of faces
# create a contact sheet for these faces
def extract_faces(img, scale_factor):
    """
    gray is in array form
    """
    # extract the retangle of the faces
    gray = np.array(img.convert("L"))
    faces = face_cascade.detectMultiScale(gray, scale_factor)

    # if no faces are detected
    if (len(faces) == 0):
        return None

    # extract faces into the list imgs
    faces_imgs = []

    for x,y,w,h in faces:
        faces_imgs.append(img.crop((x,y,x+w,y+h)))

    # compute nrows and ncols
    ncols = 5
    nrows = math.ceil(len(faces) / ncols)

    # contact sheet
    contact_sheet=Image.new(img.mode, (550, 110*nrows))
    x, y = (0, 0)

    for face in faces_imgs:
        face.thumbnail((110,110))
        contact_sheet.paste(face, (x,y))

        if x+110 == contact_sheet.width:
            x = 0
            y += 110
        else:
            x += 110

    return contact_sheet
# define the search function
def value_search(value, zip_name, scale_factor):
    if zip_name == "small_img.zip":
        ref_imgs = small_imgs
    else:
        ref_imgs = big_imgs

    for ele in ref_imgs:
        # test if value is in the text
        if value in ele["text"]:
            # print out the name of the figure
            print("Results found in file {}".format(ele["name"]))

            # index out the faces
            img = ele["img"]
            contact_sheet = extract_faces(img, scale_factor)
            if contact_sheet is not None:
                display(contact_sheet)
            else:
                print("But there were no faces in that file")

###########################################################################################
# NEW CELL
# reproduce the search for "Christopher"
value = "Christopher"
zip_name = "small_img.zip"
value_search(value, zip_name, scale_factor = 1.4)

############################################################################################
#NEW CELL
# reproduce the search for "Mark"
value = "Mark"
zip_name = "images.zip"
value_search(value, zip_name, scale_factor = 1.5)
