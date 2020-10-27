import time
import os.path
from session import BlinkSession


def get_camera_image(camera_name, image_path='images'):
    blink_session = BlinkSession().get()

    camera = blink_session.cameras[camera_name]
    before_thumb = camera.attributes['thumbnail']

    print('Snap picture from \'' + camera_name + '\'...')
    camera.snap_picture()
    time.sleep(4)

    blink_session.refresh(force=True)

    if before_thumb == camera.attributes['thumbnail']:
        print('ERROR: Thumbnail was not updated. Aborting.')
        exit(1)
    else:
        image_name = image_path + '/save-' + str(time.time()) + '.jpg'

        if not os.path.exists(image_path):
            os.mkdir(image_path)

        camera.image_to_file(image_name)
        print('Image saved to: ' + image_name)


if __name__ == '__main__':
    get_camera_image('Farm', 'images')
