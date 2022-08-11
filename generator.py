from epslab import IslandingGenerator

DATASET_PATH = ""
islanding_generator = IslandingGenerator(DATASET_PATH)

islanding_generator.greeting()
islanding_generator.prompt_user()
islanding_generator.generate()