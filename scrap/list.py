from goprocam import GoProCamera, constants
import time 
gpCam = GoProCamera.GoPro()
print('Set Photo Single Mode')
ret = gpCam.mode(constants.Mode.PhotoMode, constants.Mode.SubMode.Photo.Single)
print(ret)
time.sleep(1)
print('Set HDR ON')
ret = gpCam.gpControlSet(constants.Photo.HDR_PHOTO, constants.Photo.HDR.OFF)