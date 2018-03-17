import subprocess
import urllib.request
import os

c = "ls; ls; mkdir test"
d = 30
images = []
bash_command = "cd /home/nick/myproject \nmkdir tester \n"

for i in range(d):
    img_location = "static/images/curiosity/curiosity_{}.jpg".format(i)
    # urllib.request.urlretrieve(url_images[i], img_location)
    images.append("static/images/curiosity/curiosity_{}.jpg".format(i))
    if os.name == 'posix':
        bash_command += "convert static/images/curiosity/curiosity_{}.jpg -sampling-factor 4:2:0 -strip " \
                       "-quality 85 -interlace JPEG -colorspace RGB static/images/curiosity/curiosity_{}" \
                       ".jpg \n".format(i, i)

print("test.py")
process = subprocess.Popen(bash_command, shell=True)