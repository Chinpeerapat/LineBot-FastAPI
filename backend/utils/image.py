import base64

def encode_image(image_data: bytes) -> str:
    """
    Encode binary image data to a base64 string.
    
    :param image_data: Binary data of the image
    :return: Base64 encoded string of the image
    """
    return base64.b64encode(image_data).decode('utf-8')
