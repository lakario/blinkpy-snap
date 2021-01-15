import time
import os.path
import sys
from session import BlinkSession


def get_camera_image(camera_name, image_path='images'):
    blink_session = BlinkSession().get()

    camera = blink_session.cameras[camera_name]
    before_thumb = camera.attributes['thumbnail']

    print('Snap picture from \'' + camera_name + '\'...')
    camera.snap_picture()
    time.sleep(5)

    blink_session.refresh(force=True)

    retry_count = 0
    max_retries = 3

    while before_thumb == camera.attributes['thumbnail'] and retry_count < max_retries:
        print('ERROR getting updated thumbnail. Retrying.')
        time.sleep(2)
        blink_session.refresh(force=True)
        retry_count += 1

    if before_thumb == camera.attributes['thumbnail']:
        print('ERROR: Thumbnail was not updated. Aborting.')
        exit(1)
    else:
        image_name = image_path + '/save-' + str(time.time()) + '.jpg'

        if not os.path.exists(image_path):
            os.mkdir(image_path)

        camera.image_to_file(image_name)
        print('Image saved to: ' + image_name)


def setup_logger():
    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s [%(asctime)s] [%(name)s] %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='../run.log')


if __name__ == '__main__' and len(sys.argv) == 2:
    target_camera = sys.argv[1]

    setup_logger()
    get_camera_image(target_camera, 'images/' + str.lower(target_camera))
