from goprocam import GoProCamera, constants
from utils import log
from datetime import datetime
import threading 
import queue
import time 
log.setup_logging()
logger = log.get_logger(__name__)

RESP_OK = '{}\n'


logger.info('Init GoPro')
gopro = GoProCamera.GoPro(constants.gpcontrol)
time.sleep(1)

logger.info('Sync local time')
ret = gopro.syncTime()
assert(ret==RESP_OK)
time.sleep(0.5)

logger.info('Silence Mode, No Auto-OFF')
ret = gopro.gpControlSet(constants.Setup.VOICE_CONTROL, constants.Setup.VoiceControl.OFF)
assert(ret==RESP_OK)
time.sleep(0.5)
ret = gopro.gpControlSet(constants.Setup.AUTO_OFF, constants.Setup.AutoOff.Never)
assert(ret==RESP_OK)
time.sleep(0.5)

def nightlapse(start, end, thread_event):
    
    logger.info('State: waiting...')
    while (start > datetime.now()) & (not thread_event.is_set()):
        time.sleep(2)
    
    logger.info('Set config...')
    try:
        ret = gopro.mode(constants.Mode.MultiShotMode, constants.Mode.SubMode.MultiShot.NightLapse)
        assert(ret==RESP_OK)
        time.sleep(0.5)
        ret = gopro.gpControlSet(constants.Multishot.NightLapseExp, constants.Multishot.NightLapseExp.ExpAuto)
        assert(ret==RESP_OK)
        time.sleep(0.5)
        ret = gopro.gpControlSet(constants.Multishot.TIMELAPSE_INTERVAL, constants.Multishot.NightLapseInterval.I1m)
        assert(ret==RESP_OK)
        time.sleep(0.5)
    except Exception as e:
        logger.exception(e)
        thread_event.set()
        return

    try:
        ret = gopro.shutter(constants.start)
        assert(ret==RESP_OK)
        logger.info('State: Recording...')
        while (end > datetime.now()) & (not thread_event.is_set()) & (gopro.IsRecording()):
            time.sleep(2)
    except Exception as e:
        logger.exception(e)
        thread_event.set()
    
    finally:
        gopro.shutter(constants.stop)
        thread_event.set()
        logger.info('State: Stopped')

    



if __name__ == "__main__":
    try:
        start = datetime.strptime('2020-11-20 12:35:01', '%Y-%m-%d %H:%M:%S')
        stop = datetime.strptime('2020-11-20 12:36:01', '%Y-%m-%d %H:%M:%S')

        thread_event = threading.Event()
        thr = threading.Thread(target=nightlapse, args=(start, stop, thread_event,))
        thr.start()

        while not thread_event.is_set():
            time.sleep(1)


    except (KeyboardInterrupt, SystemExit):
        logger.exception('Keyboard Interrupt')
        logger.warning('Shutting down...')
        thread_event.set()

    except Exception as e:
        logger.error('Error in main thread')
        logger.error('Shutting down...')
        logger.exception(e)
        thread_event.set()

    finally:
        thr.join()
