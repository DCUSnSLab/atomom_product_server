# atomom_product_server

## Overview
This repository contains the code for the Deep Learning system for text detection and recognition in Cosmetic images. 

our system is OCR models locate Text, recognition them, the product name is detected from the recognized characters, and the most similar product is searched for in the product database.

If you use our code, please use it after installation through the .yaml file we uploaded




## Getting Started
### Dependency
- This work was tested with PyTorch 1.10.1, CUDA 11.2, python 3.7, django 3.2.11, djangorestframework 3.13.1, django-extensions 3.1.5 and Ubuntu 18.04.3 LTS. 

```
You must need `conda env create --file environment.yaml`.
```

### Demo instruction using pre-trained model
- Download the trained models
 
 *Model name* | *Languages* | *Purpose* | *Model Link* |
 | :-: | :-: | :-: | :-: |
craft_mlt_25k | Eng + MLT | Text detection | [Click](https://drive.google.com/file/d/1-0ssNWhmsHD3H_oelg6OMH7aLaKDfJak/view?usp=sharing)
best_accuracy | Eng + Kor | Text recognition | [Click](https://drive.google.com/file/d/1m0b-kTVvcvWiHXqlnnEK_sklXc85YM-P/view?usp=sharing)

* Run with pretrained model
``` (with python 3.7)
1. Download pretrained model craft_mlt_25k and best_accuracy
2. Move craft_mlt_25k into `atoOCR/craftPytorch/`
3. Move best_accuracy into `atoOCR/`
4. Modify database path name, user, passwd and etc in `demo/config/settings.py`.
5. python ./jsonToDB/demo/manage.py runserver [your ip:port]
```

* Test with cosmetics image(This work is a test method at [Postman](https://www.postman.com/). 
``` (with python 3.7)
Launch Postman by clicking on the logo. After it completely loads the ㅣmain screen follow these steps to create your collection of requests:
1. On the “collections” tab click on the “+” button to create a new collection. A new collection will appear and you will be able to edit its name, description, and many other settings.
2. Then right click on that new collection and select “add request” to create your first request.
3. Select the recently created request and enter the API endpoint(ex. http://your ip :port/api) where it says ‘Enter request URL’ and select the method (the action type POST ) on the left of that field. 
4. Enter a POST body(key is 'media' and Value is 'cosmetic image')
5. If you execute this API now, hit the ‘Send’ button, which is located to the right of the API request field. You can also click on the ‘Save’ button beside it to save that API request to your library.
```
### Sample Results

| *demo images* | *json results* | *cosmetics matching <br/>success in database* |
| :-:         |     :-:      |     :-:      |
|   <img src="https://user-images.githubusercontent.com/48535768/178191129-9a5e6a67-1aba-49e0-a32b-c4145ec959fa.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-1_9axXrKwiWfqtr3UXuWaeKR77vhSbU/view?usp=sharing)   |  O   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191156-5ef67b92-b1c4-4b0e-82f0-8d590122419b.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-5GxYKBNivQChSDPH0bed6PB7gqN0DUn/view?usp=sharing)   |  O   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191246-13eb699b-7b59-410a-b0d4-e2b23832b15b.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-Kh_OJth8tL4orZOLyoZbmjVFSvYwbV9/view?usp=sharing)   |  O   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191306-9c74ff44-cb62-4977-8b28-75e28910ca21.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-PvKIz3TxHukOwKJMndMNJEYJtErGOH4/view?usp=sharing)   |  X   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191325-ceca8555-1d1f-483e-97ee-cb8058c414b2.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-SlYZz-6U3UYwaLHOuyMMXXRHBt5-YKD/view?usp=sharing)   |  O   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191330-180f2551-8674-42b1-a51a-8d2a2602704a.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-MgCOAZ854OCp7YV9ecEUHnA7tExOL8J/view?usp=sharing)   |  O   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191359-4eafacd2-ccc5-43c2-9492-033c3e603835.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-LXpaSMfJsWdcI08en6wUdhHERQ99xLE/view?usp=sharing)   |  O   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191366-490779a1-194a-46a7-bc6f-2550f2e4283b.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-91ukYUSi3haVoqUnlZoIhy_ZtLKVlX3/view?usp=sharing)   |  O   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191369-f4332e42-9659-4a48-863b-32238fca2e7a.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-FL2SazxHrtd0DiJYBuL9yMVvrw7xgaU/view?usp=sharing)   |  X   |
|   <img src="https://user-images.githubusercontent.com/48535768/178191377-e2764418-22fa-4fff-9c92-478eae869b66.jpg" width="196" height="50">   |  [Json_File](https://drive.google.com/file/d/1-Gt-7VBxA9zvknNarvoCi50gujVprPe4/view?usp=sharing)   |  O   |

## Acknowledgements
This implementation has been based on these repository [CRAFT-pytorch](https://github.com/clovaai/CRAFT-pytorch), [
deep-text-recognition-benchmark](https://github.com/clovaai/deep-text-recognition-benchmark).


