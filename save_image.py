import os,urllib.request

def save_the_images_in_local(img_id,img_url, user_id):
    filepath = os.getcwd()+"\\"+user_id

    if not(os.path.exists(filepath)):
        os.mkdir(user_id)

    fullfilename = os.path.join(filepath+"\\"+img_id+".jpg")
    if not(os.path.exists(fullfilename)):
        urllib.request.urlretrieve(img_url, fullfilename)
        print("Saved:::::::::"+img_id+".jpg")
