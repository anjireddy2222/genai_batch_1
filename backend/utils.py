from pypdf import PdfReader
from docx import Document

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
    






#  2, 3,

# chunk_size = 2
# a b c d e f g h i j k  l  m
# 0 1 2 3 4 5 6 7 8 9 10 11 12 
# 0:2
# 2:


# a b -> 0 to 2 char
# c d
# e f g h
# gh


# [ ab, cd, ef, gh, kl, m]


















