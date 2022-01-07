#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # curPath = os.getcwd()
    # path = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    # print(path)
    # # print(os.listdir(path))
    # path = os.path.join(path, 'atoOCR')
    # print(path)
    # sys.path.append(path)
    # import demo_modifed_for_one_image_processing as ocr
    #
    # os.chdir(path)
    # craftModel, model, opt = ocr.setModel()
    # imgPath = path + "/curImage.jpg"
    # img, points = ocr.craftOperation(imgPath, craftModel, dirPath=opt.image_folder)
    # os.chdir(curPath)



    main()
