from goprocam import GoProCamera, constants
from astral import LocationInfo
from astral.sun import sun
from utils import log
from datetime import datetime, timezone
import threading 
import queue
import time 

log.setup_logging()
logger = log.get_logger(__name__)

RESP_OK = '{}\n'

city = LocationInfo('Lucerne', 'Swiss', 'Europe/Zurich', "47°3′N", "8°18′E")

logger.info('Init GoPro')
gopro = GoProCamera.GoPro(constants.gpcontrol)
time.sleep(1)

logger.info('Silence Mode, No Auto-OFF')
ret = gopro.gpControlSet(constants.Setup.VOICE_CONTROL, constants.Setup.VoiceControl.OFF)
assert(ret==RESP_OK)
time.sleep(0.5)
ret = gopro.gpControlSet(constants.Setup.AUTO_OFF, constants.Setup.AutoOff.Never)
assert(ret==RESP_OK)
time.sleep(0.5)

def daylapse(error_event, stop_event):    
    logger.info('Set config for Daytime Timelapse...')
    try:
        ret = gopro.mode(constants.Mode.MultiShotMode, constants.Mode.SubMode.MultiShot.TimeLapse)
        assert(ret==RESP_OK)
        time.sleep(0.5)
        ret = gopro.gpControlSet(constants.Multishot.TIMELAPSE_INTERVAL, constants.Multishot.TimeLapseInterval.I60)
        assert(ret==RESP_OK)
        time.sleep(0.5)
        ret = gopro.gpControlSet(constants.Multishot.WHITE_BALANCE, constants.Multishot.WhiteBalance.WBAuto)
        assert(ret==RESP_OK)
        time.sleep(0.5)
    except Exception as e:
        logger.exception(e)
        error_event.set()
        return

    try:
        ret = gopro.shutter(constants.start)
        assert(ret==RESP_OK)
        logger.info('State: Recording...')
        while (not stop_event.is_set()) & (not error_event.is_set()) & (gopro.IsRecording()):
            time.sleep(2)
    except Exception as e:
        logger.exception(e)
        logger.info('gopro.IsRecording returned: {}'.format(gopro.IsRecording()))
        error_event.set()
    
    finally:
        ret = gopro.shutter(constants.stop)
        assert(ret==RESP_OK)
        logger.info('State: Stopped')

def daylapse_hdr(interval, error_event, stop_event):
    assert (interval > 0), 'Intervall must be greater than 0'
    logger.info('Set config for HDR Daytime Timelapse ...')
    try:
        ret = gopro.mode(constants.Mode.PhotoMode, constants.Mode.SubMode.Photo.Single)
        assert(ret==RESP_OK)
        time.sleep(0.5)
        ret = gopro.gpControlSet(constants.Photo.SUPER_PHOTO, constants.Photo.SuperPhoto.HDROnly)
        assert(ret==RESP_OK)
        time.sleep(0.5)
    except Exception as e:
        logger.exception(e)
        error_event.set()
        return

    try:
        logger.info('State: Recording...')
        seconds = 0
        while (not stop_event.is_set()) & (not error_event.is_set()):
            if seconds == interval:
                ret = gopro.take_photo()
                if not (ret==RESP_OK):
                    logger.warning(ret)
                logger.info('Day photo taken!')
                seconds = 0
            else:
                seconds = seconds + 1
            time.sleep(1)

    except Exception as e: 
        logger.exception(e)
        error_event.set()
    
    finally:
        logger.info('State: Stopped')

def nightlapse(error_event, stop_event):   
    logger.info('Set config for nightlapse...')
    try:

        ret = gopro.mode(constants.Mode.MultiShotMode, constants.Mode.SubMode.MultiShot.NightLapse)
        assert(ret==RESP_OK)
        time.sleep(0.5)
        ret = gopro.gpControlSet(constants.Multishot.NIGHT_LAPSE_EXP, constants.Multishot.NightLapseExp.ExpAuto)
        assert(ret==RESP_OK)
        time.sleep(0.5)
        ret = gopro.gpControlSet(constants.Multishot.NIGHT_LAPSE_INTERVAL, constants.Multishot.NightLapseInterval.I1m)
        assert(ret==RESP_OK)
        time.sleep(0.5)
        ret = gopro.gpControlSet(constants.Multishot.WHITE_BALANCE, constants.Multishot.WhiteBalance.WB4000k)
        assert(ret==RESP_OK)
        time.sleep(0.5)
    except Exception as e:
        logger.exception(e)
        error_event.set()
        return

    try:
        ret = gopro.shutter(constants.start)
        assert(ret==RESP_OK)
        logger.info('State: Recording...')
        while (not stop_event.is_set()) & (not error_event.is_set()) & (gopro.IsRecording()):
            time.sleep(2)
    except Exception as e:
        logger.exception(e)
        logger.info('gopro.IsRecording returned: {}'.format(gopro.IsRecording()))
        error_event.set()
    
    finally:
        ret = gopro.shutter(constants.stop)
        assert(ret==RESP_OK)
        logger.info('State: Stopped')


    



if __name__ == "__main__":
    

    try:
        error_event = threading.Event()
        stop_event = threading.Event()
        while not error_event.is_set():
            stop_event.clear()

            now = datetime.now(timezone.utc)
            # now = datetime.strptime('2020-11-21 22:35:01', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

            s = sun(city.observer, date=now)
            day_start = s["sunrise"]
            day_end = s["sunset"]

            try:
                logger.info('Sync local time')
                ret = gopro.syncTime()
                assert(ret==RESP_OK)
                time.sleep(0.5) 
            except Exception as e:
                logger.error('Could not set time...')
                logger.exception(e)

            state = None
            if (now > day_start) & (now < day_end):
                logger.info('')
                logger.info('Start daytime logging')
                day_thread = threading.Thread(target=daylapse, args=(error_event, stop_event,))
                day_thread.start()
                state = 'Day'
            
            else:
                logger.info('')
                logger.info('Start nighttime logging')
                night_thread = threading.Thread(target=nightlapse, args=(error_event, stop_event,))
                night_thread.start()
                state = 'Night'


            while (not error_event.is_set()) & (not stop_event.is_set()):
                now = datetime.now(timezone.utc)
                # now = datetime.strptime('2020-11-21 22:35:01', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                # if not day_end.day == now.day:
                #     # calculate new sunrise and sunset times
                #     s = sun(city.observer, date=now)
                #     day_start = s["sunrise"]
                #     day_end = s["sunset"]
                
                if (state == 'Day') & (now > day_end):
                    logger.info('Transition to night...')
                    if day_thread.is_alive():
                        stop_event.set()
                        day_thread.join()
                        time.sleep(90)
                        break
                    else:
                        error_event.set()
                        raise Exception('Day-Thread is dead!')
                        

                if (state == 'Night'):
                    time.sleep(30)
                    if not now.day == day_end.day: # already past midnight?
                        s = sun(city.observer, date=now)
                        if (now > s["sunrise"]):
                            logger.info('Transition to daytime...')
                            if night_thread.is_alive():
                                stop_event.set()
                                night_thread.join()
                                time.sleep(90)
                                break
                            else:
                                error_event.set()
                                raise Exception('Night-Thread is dead!')
                               

                time.sleep(5)



    except (KeyboardInterrupt, SystemExit):
        logger.exception('Keyboard Interrupt')
        logger.warning('Shutting down...')
        error_event.set()

    except Exception as e:
        logger.error('Error in main thread')
        logger.error('Shutting down...')
        logger.exception(e)
        error_event.set()

    finally:
        pass
