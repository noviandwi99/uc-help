from epslab import IslandingGenerator
import os

FOLDER_NAME = ''
DATASET_PATH = os.path.join(os.getcwd(), 'data', FOLDER_NAME)
FILENAME = ''

islanding_generator = IslandingGenerator(
    data_path=DATASET_PATH,
    filename=FILENAME,
)

islanding_generator.greeting()
islanding_generator.prompt_user()
islanding_generator.generate()