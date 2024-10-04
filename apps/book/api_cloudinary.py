import cloudinary
from decouple import config 

def api_cloudinary(): 
    return cloudinary.config(
        cloud_name=config('CLOUD_NAME'),
        api_key=config('API_KEY'),
        api_secret=config('API_SECRET'),
        secure=config('SECURE', cast=bool) 
    )
