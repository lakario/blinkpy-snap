import time
import os.path
import sys
from session import BlinkSession
import argparse


def get_camera_image(camera_name, image_path, auth_file, no_prompt=False):
    blink = BlinkSession(auth_file).get(no_prompt=no_prompt)
    camera = blink.cameras[camera_name]
    before_thumb = camera.attributes['thumbnail']

    print(f"Snapping image from camera: '{camera_name}'... ", end='')
    camera.snap_picture()
    time.sleep(5)

    blink.refresh(force=True)

    retry_count = 0
    max_retries = 3

    while before_thumb == camera.attributes['thumbnail'] and retry_count < max_retries:
        print('ERROR')
        print('Failed to retrieve updated thumbnail. Retrying.')
        time.sleep(2)
        blink.refresh(force=True)
        retry_count += 1

    if before_thumb == camera.attributes['thumbnail']:
        print('ERROR')
        print('Thumbnail was not updated. Aborting.')
        exit(1)
    else:
        image_name = image_path + '/save-' + str(time.time()) + '.jpg'

        if not os.path.exists(image_path):
            os.makedirs(image_path, exist_ok=True)

        camera.image_to_file(image_name)

        if os.path.exists(image_name):
            print('OK')
            print('Image saved to: ' + os.path.abspath(image_name))
        else:
            print('ERROR')
            print('Something went wrong. Image was not found at expected path.')
            exit(1)


def setup_logger():
    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s [%(asctime)s] [%(name)s] %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='run.log')


if __name__ == '__main__':
    setup_logger()
    target_camera = os.environ.get('Snap_Camera')
    output_path = os.environ.get('Snap_OutputPath') or f'/images'
    auth_file_path = os.environ.get('Snap_AuthPath') or BlinkSession.DEFAULT_AUTH_FILE
    quiet = False

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--Camera", help="Camera name")
    parser.add_argument("-o", "--Output", help="Output path")
    parser.add_argument("-a", "--Auth", help="Auth path")
    parser.add_argument("-q", "--Quiet", default=True, action=argparse.BooleanOptionalAction,
                        help="Quiet mode. Disables authentication prompts.")

    if len(sys.argv) > 1:
        args = parser.parse_args()

        if args.Camera is not None:
            target_camera = args.Camera
        if args.Output is not None:
            output_path = args.Output
        if args.Auth is not None:
            auth_file_path = args.Auth
        if args.Quiet is not None:
            quiet = args.Quiet

    if target_camera is not None and output_path is not None and auth_file_path is not None:
        get_camera_image(target_camera, output_path, auth_file_path, no_prompt=quiet)
    else:
        parser.print_help()
