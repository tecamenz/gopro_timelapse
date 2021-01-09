from goprocam import GoProCamera, constants
import time

time.sleep(10)
gpCam = GoProCamera.GoPro()
time.sleep(3)
gpCam.delete("all")