from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
print(dotenv_path)
load_dotenv(dotenv_path)
