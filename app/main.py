from concurrent.futures import ThreadPoolExecutor, as_completed
from settings import FRONTEND_DIR
from logger import logger
import requests
from utils import (
    generate_animal_url_adjective,
    get_no_of_cpu_cores,
    get_wiki_animal_images,
    prepare_json_array_of_objects,
    write_json_to_file,
)
from exceptions import CollateralAdjectivesError
from bs4 import BeautifulSoup
WIKI_URL = "https://en.wikipedia.org"
def get_parsed_html():
    try:
        logger.info("Started Scraping wiki animal page")
        html = requests.get("https://en.wikipedia.org/wiki/List_of_animal_names",timeout=3)
        soup = BeautifulSoup(html.text, "html.parser")
        logger.info("Ended Scraping wiki animal page")
    #TODO need to add more exceptions 
    except Exception as e:        
        logger.exception("Did not start scraping wikipedia page to bs4")
        raise Exception("Error getting parsed html")
    return soup




# find all rows in the table
def generate_colateral_adjectives(tables):
    try:
        table_cursor = 0
        collateral_adjectives_animals = {}
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
            # get tds in each row
                tds = row.find_all("td")
                if len(tds) > 6:
                    if table_cursor == 0:
                        collateral_adjectives = tds[-1].children
                        for animal, animal_url, adjective in generate_animal_url_adjective(
                        tds, collateral_adjectives
                    ):
                            if isinstance(adjective, str):
                                collateral_adjectives_animals.setdefault(adjective, []).append(
                                (animal, animal_url)
                            )
                    if table_cursor == 1:
                        collateral_adjectives = tds[-2].children
                        for animal, animal_url, adjective in generate_animal_url_adjective(
                        tds, collateral_adjectives
                    ):
                            if isinstance(adjective, str):
                                collateral_adjectives_animals.setdefault(adjective, []).append(
                                (animal, animal_url)
                            )

            table_cursor += 1
    except Exception as e:
        logger.exception("Generating Colateral Adjectives")  
        raise CollateralAdjectivesError()  
    return collateral_adjectives_animals
# start the thread pool
def image_scraping_futures(WIKI_URL, executor, animals):
    image_futures = []
    for animal, animal_url in animals:        
        image_futures.append(
            executor.submit(
                get_wiki_animal_images, url=WIKI_URL + animal_url, animal=animal
            )
        )
    return image_futures
if __name__ == "__main__":
    soup = get_parsed_html()
    tables = soup.find_all(
    "table", {"class": ["wikitable", "sortable", "jquery-tablesorter"]}
    )

    collateral_adjectives_animals = generate_colateral_adjectives(tables)


    write_json_to_file(FRONTEND_DIR+"/collateral_adjectives_animals.json", collateral_adjectives_animals)
    # better json representation
    array_of_animals = prepare_json_array_of_objects(collateral_adjectives_animals)
    write_json_to_file(FRONTEND_DIR+"/array_of_animals.json", array_of_animals)

    with ThreadPoolExecutor(max_workers=get_no_of_cpu_cores()) as executor:
        # create futures
        logger.info("Image_futures collection started")
        for adjective, animals in collateral_adjectives_animals.items():
            logger.info("Image_futures collection started for adjective: {}".format(adjective))
            image_futures = image_scraping_futures(WIKI_URL, executor, animals)
        logger.info("Image_futures collected")
        try:
            for future in as_completed(image_futures,timeout=4.5):
                result = future.result()
        except TimeoutError:
            logger.exception("Task timed out")
        
        except Exception as e:
            logger.exception("Thread Pool Error")
            
