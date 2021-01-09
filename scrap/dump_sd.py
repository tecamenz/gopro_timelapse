from goprocam import GoProCamera, constants
import time
import json
# gpCam = GoProCamera.GoPro()
gpCam = GoProCamera.GoPro(constants.gpcontrol)
## Downloads all of the SD card's contents and then formats the sd card.

# gpCam.downloadAll()
# gpCam.downloadMultiShot()
gpCam.delete("all")
time.sleep(30)


#path = gpCam.getMedia()
#print(path)
#InfoFromURL = gpCam.getInfoFromURL(path)
#print(InfoFromURL)
#folder = InfoFromURL[0]
#filename = InfoFromURL[1]
#arr = json.loads(gpCam.listMedia())

#with open("{}_{}_{}.json".format(path.replace('/', '-').replace(':', ''), folder, filename), "w") as outfile: 
#    json.dump(arr, outfile) 
