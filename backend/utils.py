from pypdf import PdfReader
from docx import Document
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# read pdf data
def read_pdf(file):
    # print("pdf file in utils file: ", file)
    reader = PdfReader(file.file)
    # pages
    extracted_text = ""
    for page in reader.pages:
        extracted_text = extracted_text + page.extract_text()
    return extracted_text


# read document data
def read_docs(file):
    reader = Document(file.file)
    extracted_data = ""
    for para in reader.paragraphs:
        extracted_data = extracted_data + para.text
    return extracted_data


# read txt file data
def read_txt_file(file):
    data = file.file.read()
    return data

# create chunks
def create_chunks(data):
    chunk_size = 25
    chunk_data = []
    for index in range(0, len(data), chunk_size ):
        # print( 'index: ', index )
        # test = f" {index} :{index + chunk_size} "
        # print(test)
        chunk_data.append( data[index: index + chunk_size ] )
    return chunk_data
    

# scrape website
# requests beautifulsoup4  
def scrape_server_rendered_website(url):
    response = requests.get(url)
    print( response.status_code )
    if response.status_code == 200:
        soap_response = BeautifulSoup(response.text, "html.parser")
        return soap_response.get_text()
    else:
        return "unable to scrape your website"


def scrape_ui_side_websites(url):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            text = page.inner_text("body")
            browser.close()
            return text
        except Exception as ex:
            return "Unable to scrape your website. Please provide knowledge through files or manual entry"




















