from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



# STEP 1. Load raw pdf
DATA_PATH = 'data/'
def load_pdf_files(data):
    loader = DirectoryLoader(data,
                              glob='*.pdf',
                              loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

documents = load_pdf_files(data=DATA_PATH)
print("Length of pdf pages: ",len(documents))