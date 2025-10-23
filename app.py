import streamlit as st
import pandas as pd
from pyserini.search.lucene import LuceneSearcher
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import string
import json

factory = StemmerFactory()
stemmer = factory.create_stemmer()

istilah_kesehatan = {
    # Tekanan Darah
    "hipertensi": "tekanan darah tinggi",
    "hipotensi": "tekanan darah rendah",

    # Gula Darah
    "hiperglikemia": "kadar gula darah tinggi",
    "hipoglikemia": "kadar gula darah rendah",
    "diabetes melitus": "penyakit kencing manis",

    # Pernapasan
    "dispnea": "sesak napas",
    "rinorea": "pilek atau ingusan",
    "epistaksis": "mimisan",
    "faringitis": "radang tenggorokan",
    "laringitis": "radang pita suara",
    "asma": "bengek",

    # Pencernaan
    "dispepsia": "mag atau gangguan pencernaan",
    "konstipasi": "sembelit atau susah buang air besar",
    "diare": "mencret",
    "hemoroid": "wasir atau ambeien",
    "apendisitis": "radang usus buntu",
    "gastritis": "radang lambung",

    # Kulit dan Alergi
    "urtikaria": "biduran atau kaligata",
    "dermatitis": "eksim atau radang kulit",
    "varisela": "cacar air",
    "morbili": "campak atau tampek",
    "veruka": "kutil",
    "tinea pedis": "kutu air",
    "lotion": "losion",

    # Kepala dan Saraf
    "sefalgia": "sakit kepala atau pusing",
    "insomnia": "susah tidur",
    "sinkop": "pingsan",
    "konvulsi": "kejang",

    # Umum
    "pireksia": "demam",
    "hipertermia": "suhu tubuh sangat tinggi",
    "hipotermia": "suhu tubuh sangat rendah",
    "mialgia": "nyeri otot",
    "artralgia": "nyeri sendi",
    "fatik": "kelelahan atau rasa capai",
    "edema": "bengkak",
    "pruritus": "gatal-gatal",
    "anemia": "kurang darah",
    "karsinoma": "kanker",
    "neoplasma": "tumor",
    "halitosis": "bau mulut",
    "kalkulus renal": "batu ginjal",
    "moisturizing": "moisturizer"
}

# --- Page Configuration ---
st.set_page_config(
    page_title="Information Retrieval System",
    page_icon="🔎",
    layout="wide",
)

# --- Load Data and Model ---
@st.cache_resource
def normalize_text(text, dictionary):
    tokens = text.split()

    normalized_tokens = []
    for token in tokens:
        normalized_token = dictionary.get(token, token)
        normalized_tokens.append(normalized_token)

    return " ".join(normalized_tokens)

def stem_tokens(tokens):
    lemmas = [stemmer.stem(token) for token in tokens]
    return lemmas

def preprocess_query(text):
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords.words('indonesian')])
    text = ''.join([char for char in text if char not in string.punctuation])
    text = normalize_text(text, istilah_kesehatan)
    tokens = text.split()
    stemmed_tokens = stem_tokens(tokens)
    
    return ' '.join(stemmed_tokens)

def load_data_and_searcher():
    """Loads the dataset and initializes the Pyserini searcher."""
    try:
        # Load the article data from the CSV file
        df = pd.read_csv('artikel/raw_health_articles.csv')
        # Initialize the Pyserini searcher with the specified index
        searcher = LuceneSearcher('indexing/indexes/title_content_jsonl/')
        return df, searcher
    except Exception as e:
        st.error(f"Error loading data or searcher: {e}")
        return None, None

df, searcher = load_data_and_searcher()

# --- Main Application ---
if df is not None and searcher is not None:
    st.title("🔎 Health Information Retrieval")
    st.markdown("Enter a keyword below to search for relevant health articles.")

    # --- Search Form ---
    with st.form(key="search_form"):
        keyword = st.text_input("Keyword", placeholder="e.g., 'diabetes symptoms'")
        keyword = preprocess_query(keyword)
        submit_button = st.form_submit_button(label="Search")

    # --- Search and Display Results ---
    if submit_button and keyword:
        with st.spinner("Searching..."):
            # Perform the search using Pyserini
            hits = searcher.search(keyword.lower(), k=10)

            if hits:
                st.subheader(f"Found {len(hits)} results for '{keyword}'")

                # Display each result
                for i, hit in enumerate(hits):
                    try:
                        doc_id = int(hit.docid)
                        # Retrieve article information from the DataFrame
                        article = df[df['article_index'] == doc_id].iloc[0]
                        title = article['title']
                        source = article['source']
                        date = article['date']
                        description = article['description']
                        link = article['link']

                        st.markdown(f"### [{title}]({link})")
                        st.write(f"**Source:** {source}")
                        st.write(f"**Date:** {date}")
                        st.write(description)
                        st.markdown("---")

                    except (ValueError, IndexError) as e:
                        st.warning(f"Could not retrieve article for document ID: {hit.docid}. Error: {e}")
            else:
                st.warning("No articles found matching your keyword.")