from dalle2 import Dalle2
import os
from PIL import Image
import run

BATCH_CNT = 0  # counter for times Dalle-2 was used. for naming the files in wanted order.


def dalle_outputs_care():
    """
    Dalle-2 doesn't let changes to default file names and format downloaded.
    This function changes the files name to have an order and changes to pic format to JPEG.
    Order is in format of #[Batch].#[image in batch].JPEG
    """
    directory = os.getcwd()
    global BATCH_CNT
    image_cnt = 1  # number of images within one session (each session generates 4 images)
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if filename.startswith('generation-'):
                im = Image.open(filename).convert("RGB")
                im.save(str(BATCH_CNT) + "." + str(image_cnt) + ".JPG", "jpeg")
                os.remove(filename)
                image_cnt += 1


def create_image(key, text):
    """
    Opens a Dalle_2 user session which generates an image out of text given
    :key = openAI user session token
    :text = input for text to image
    """
    dalle = Dalle2(key)
    dalle.generate_and_download(text)

    global BATCH_CNT
    BATCH_CNT += 1

    dalle_outputs_care()


def create_text(image_path):
    """ returns text caption of an image
    :image_path = directory path to an image saved in the computer
    :return: text caption
    """
    return run.image_to_text(image_path)


if __name__ == '__main__':
    """
    Instructions for generating a key: 
        1. To get the your unique session key you need to go to https://labs.openai.com/.
        2. Open the Network Tab in Developer Tools in your browser.
        3. Send an image request in the input box.
        4. In the network tab you'll find a POST request to https://labs.openai.com/api/labs/tasks.
        5. In the POST request headers you'll find your session key in the "Authorization" header,
           it'll look something like "sess-xxxxxxxxxxxxxxxxxxxxxxxxxxxx".
    """
    token = "sess-"

    dalle_outputs_care()
    iterations = 8
    image_dir = "/photos/first_pic.jpg"

    for i in range(iterations):
        text = run.image_to_text(image_dir)
        print(str(BATCH_CNT) + ": " + text)
        create_image(token, text)
        image_dir = "/" + str(BATCH_CNT) + ".1.jpg"

    print(run.image_to_text(image_dir))
