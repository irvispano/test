import os
import requests
from logger import logger
from bs4 import BeautifulSoup
import json
from settings import IMAGE_SAVE_FOLDER


def makedirs(filename_path):
    path="/".join(filename_path.split("/")[:-1])
    os.makedirs(path, exist_ok=True)


def write_file(filename_path,filename, content):
    makedirs(filename_path)
    with open(filename_path+filename, "wb") as f:
        f.write(content)


def generate_animal_url_adjective(tds, collateral_adjectives):
    animal_url = tds[0].find("a")["href"]
    animal = tds[0].text
    for adjective in collateral_adjectives:
        if adjective is not None and isinstance(adjective, str):
            adjective = adjective.strip("\n")
            yield (animal, animal_url, adjective)


def get_no_of_cpu_cores():
    return os.cpu_count()


def get_wiki_animal_images(animal: str, url: str):
    logger.info(f"animal image download started {animal}")
    try:
        html = requests.get(url,timeout=3)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, "html.parser")
            animal_image_link = soup.select_one("table.biota img").get("src", None)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
            }
            image_file = requests.get("https:" + animal_image_link, headers=headers)
            if image_file.status_code == 200:
                logger.info(f"Image animal download success {animal}")
                # TODO make ENV var
                write_file(IMAGE_SAVE_FOLDER, animal + ".jpg", image_file.content)
            else:
                logger.info(f"Image animal download failed {animal}")
    except requests.exceptions.RequestException as e:
        logger.exception("Image animal download request exeption", extra=animal)
    except Exception as exp:
        logger.exception("Image animal download  exeption", extra=animal)
    return {
        "success": True}
        





def write_json_to_file(filename_path, data):
    makedirs(filename_path)
    with open(filename_path, "w") as f:
        json.dump(data, f)


def prepare_json_array_of_objects(collateral_adjectives_animals):
    animals_array = []
    for (
        colateral_adj,
        array_of_animal_and_link_pairs,
    ) in collateral_adjectives_animals.items():
        for animal, animal_link in array_of_animal_and_link_pairs:
            animal_object = {
                "colateral_adjective": colateral_adj,
                "animal": animal,
                "animal_link": animal_link,
            }
            animals_array.append(animal_object)
    return animals_array
