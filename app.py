import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")  # Set log level to minimize output
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)

def get_word_definition(search_word):
    url = f"https://www.dictionary.com/browse/{search_word}"
    driver.get(url)
    time.sleep(2)  # Adding a delay to allow the page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extracting the elements from the HTML
    level = soup.find(class_="css-1t9sqkg e1wg9v5m1").text.strip()
    phonetic_form = soup.find(class_="pron-spell-container css-eivff4 evh0tcl2").text.strip()
    definition_section = soup.find(class_="css-109x55k e1hk9ate4")
    wordtype = soup.find(class_="css-69s207 e1hk9ate3").text.strip()
    audio_element = soup.find("div", class_="audio-wrapper")

    # Formatting the definitions
    formatted_definitions = []
    if definition_section:
        definition_items = definition_section.find_all(class_="one-click-content css-nnyc96 e1q3nk1v1")
        for item in definition_items:
            formatted_definitions.append(item.text.strip())

    audio_url = None
    if audio_element:
        audio_source = audio_element.find("source")
        if audio_source:
            audio_url = audio_source["src"]

    return level, phonetic_form, formatted_definitions, audio_url, wordtype


# Streamlit app
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title(":blue[Word] :red[Dictionary] :books:")

# Input box for search word
search_word = st.text_input("Enter a word")

# Search button
if st.button("Search"):
    if search_word:
        with st.spinner("Searching..."):
            try:
                level, phonetic_form, definitions, audio_url, wordtype = get_word_definition(search_word)

                # Displaying the results
                st.markdown(f"> ##  {search_word}")
                st.markdown(f"#### *:blue[{wordtype}]*")
                st.markdown(f"**Level:** :red[{level}]".replace(
                    "This shows grade level based on the word's complexity.",
                    " 📈  :blue[``` This shows grade level based on the word's complexity.``` ] "
                ))
                st.markdown(f"##### Phonetic Form: :speaking_head_in_silhouette: {phonetic_form}".replace("SHOW IPA", ""))

                col1, col2 = st.columns(2)
                with col1:
                    if audio_url:
                        st.audio(audio_url, format='audio/mp3')

                st.markdown("### Definitions: :books:")
                formatted_definitions = "".join([f"🔘{definition}<br>" for definition in definitions])
                st.markdown(formatted_definitions, unsafe_allow_html=True)

            except:
                st.warning("No result found!. Are you sure you have typed it correctly?")
    else:
        st.warning("Please enter a word to search!")

driver.quit()
