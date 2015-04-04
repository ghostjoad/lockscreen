import re
import os.path
from os import getenv
from urllib.request import urlopen,urlretrieve
from urllib.error import URLError
from subprocess import Popen, PIPE, call

HOME = getenv('HOME')

def internet_on():
    """
    Check the availability of Internet connection.
    """

    try:
        response=urlopen('http://74.125.228.100',timeout=5)
        return True
    except URLError as err: 
        pass
    return False


def find_front_picture():
    """
    Find the name of the picture on the front page of SMBC.
    """

    image_pattern = 'comics/\d*-\d*\.png'
    pattern = re.compile(image_pattern)

    html = urlopen('http://www.smbc-comics.com/index.php')
    html = html.readall().decode('utf-8')
    image_location = re.findall(pattern,html)[0]
    image_name = image_location.strip('comics/')

    return image_name

def get_front_picture(image_name):
    """
    Downloads the picture on the front page.
    """

    image_adress = 'http://www.smbc-comics.com/comics/' + \
                        image_name
    
    path_to_image = HOME + '/Pictures/smbc/' + image_name
    
    #urlretrieve(image_adress,filename=path_to_image)
    request = urlopen(image_adress)
    image = request.read()

    with open(path_to_image,'wb') as ofile:
        ofile.write(image)


def resize_image(image_name):
    """
    Scale the image so that is fits on the screen.
    """
    
    path_to_image = HOME + '/Pictures/smbc/' + image_name
    #resized = '/home/baptiste/Pictures/smbc/resized/' + image_name \
    #          + 'r'

    get_height = Popen('identify -format "%h" '+path_to_image, 
                      stdout=PIPE, shell=True)

    height = float(get_height.communicate()[0].decode('utf-8'))

    scale_fact = str(800 / height * 100) + "%"

    call(["mogrify","-resize",scale_fact,
          "-gravity","center",
          #"-extent","1280x800",
          #"-background","transparent",
          path_to_image])


def retrieve_image():
    """
    If Internet is availbale, and if the front picture has not been downloaded
    yet, download it.
    """

    if internet_on():

        image_name = find_front_picture()

        path_to_image = HOME + '/Pictures/smbc/' + image_name

        if not os.path.isfile(path_to_image):
            get_front_picture(image_name)
            resize_image(image_name)

    else :
        print('No Internet connection !')


def print_blur_screen(image):
    """
    Takes a screenshot, blur it ; then, superimpose the last SMBC picture on it.
    """

    path_to_save = '/tmp/screenshot.png'

    call(["scrot",path_to_save])
    call(["convert",path_to_save,"-blur","0x3","/tmp/blurred.png"])
    call(["rm",path_to_save])


    get_width = Popen('identify -format "%w" '+image, 
                      stdout=PIPE, shell=True)

    width = float(get_width.communicate()[0].decode('utf-8'))

    residual_size = 1280 - width

    x_offset = residual_size / 2

    offset = '+'+str(x_offset)+'+0'

    call(["convert","/tmp/blurred.png",
          "(",image,"-alpha","off","-channel","A",
             "-evaluate","set","100%",")",
          "-geometry",offset,
          "-composite",
          HOME+"/Pictures/lockscreen/lockscreen.png"
         ])
