import pytest
from main import get_parsed_html
from bs4 import BeautifulSoup
from utils import get_wiki_animal_images
@pytest.fixture
def animal_url():
    return "https://en.wikipedia.org/wiki/Bovinae"
def test_get_parsed_html():
    soup=get_parsed_html()
    assert isinstance(soup,BeautifulSoup)

def test_get_wiki_animal_images(animal_url):
    animal_images_saved=get_wiki_animal_images(url=animal_url,animal="Bovinae")
    assert animal_images_saved.get("success") is True
    
    