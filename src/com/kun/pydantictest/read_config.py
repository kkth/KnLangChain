import os

from config import get_settings


if __name__ == "__main__":
   theSetting = get_settings(os.getenv("ENV","dev"))
   #print(theSetting.__dict__)
   print(theSetting.dict())
