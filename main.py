# Name: Nigel Jacob
# Date: 26/07/2021

import config
import cv2 as cv
import RPi.GPIO as GPIO
from threading import Thread


def analyse() -> None:
    print("Press 'q' to exit.")

    while not cv.waitKey(1) & 0xFF == ord("q"):
        try:
            (success, img) = config.cap.read()
            (class_ids, confs, bbox) = config.net.detect(img, confThreshold=config.ACCURACY)

        except cv.error as e:
            print(e)
            break

        if len(class_ids) != 0:
            for (classId, confidence, box) in zip(
                    class_ids.flatten(), confs.flatten(), bbox
            ):
                object_identified = config.classNames[classId - 1].upper()
                prob_correct = round(confidence * 100, 2)

                if object_identified == "PERSON":
                    color = config.RED
                    # Start alarm if there isn't noise already
                    if config.firstRun:
                        alarm = Thread(target=config.alert)
                        config.firstRun = False
                    if not alarm.is_alive():
                        alarm = Thread(target=config.alert)
                        alarm.start()
                else:
                    color = config.GREEN
                # Draw box around image and label object identified
                cv.rectangle(img, box, color=color, thickness=2)
                cv.putText(
                    img,
                    "%s %d%%" % (object_identified, prob_correct),
                    (box[0] + 5, box[1] + 20),
                    cv.FONT_HERSHEY_COMPLEX_SMALL,
                    1,
                    color,
                    2,
                )

        cv.imshow("Security Camera Feed", img)

        if config.button.is_pressed:
            break

    cv.destroyAllWindows()
    GPIO.cleanup()


if __name__ == "__main__":
    analyse()
