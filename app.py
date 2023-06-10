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


#Custom CSS styling to make the app look better

with open("./css/style.css") as f:
    style=f.read()

st.markdown(f"""{style}""", unsafe_allow_html=True)


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
    st.title(":blue[Modern] :red[Dictionary] :books:",anchor=None)

# Input box for search word
search_word = st.text_input("Enter a word")

# Search button
if st.button("Search"):
    if search_word:
        with st.spinner("Searching..."):
            try:
                level, phonetic_form, definitions, audio_url, wordtype = get_word_definition(search_word)

                # Displaying the results
                st.markdown(f"""
                            <div class="text-left py-4 sm:px-4 rounded-lg font-extrabold text-3xl" style="font-family: 'Righteous', cursive; background-color:#F9BF8F;">
                            {search_word}
                            </div> 
                            """, unsafe_allow_html=True)
                st.markdown(f"""
                            <br>
                            <div class="p-2 text-center bg-indigo-600 items-center text-indigo-100 leading-none lg:rounded-full sm:rounder-full md:rounded-full flex lg:inline-flex" role="alert">
                            <span class="font-semibold mr-2 text-left flex-auto">{wordtype}</span>
                        </div>
                        <br>
                        <br>
                            """,unsafe_allow_html=True)
                col1,col2=st.columns(2)
                st.markdown("---")
                with col1:
                    st.markdown("---")
                    st.markdown(f"**Level:** :star: :red[{level}]".replace(
                    "This shows grade level based on the word's complexity.",
                    " 📈 "
                ))     
                with col1:
                    st.markdown(f"##### Phonetic Form: :speaking_head_in_silhouette: {phonetic_form}".replace("SHOW IPA", ""))
                with col2:
                    st.markdown("---")
                    if audio_url:
                        st.audio(audio_url, format='audio/mp3')
                formatted_definitions = "".join([f"🔘{definition}<br>" for definition in definitions])
                st.markdown("""<h1 class="text-xl text-gray-600">Example:</h1>""",unsafe_allow_html=True)
                st.markdown(f"""
                            <div class="container mx-auto border rounded-lg px-2 py-2" style="border-color: #E2434B;">
                            {formatted_definitions}
                            </div>
                            """,unsafe_allow_html=True)
                

            except:
                warn="""
                <div class="bg-brown-100 text-center py-4 lg:px-4 rounded-lg">
                <div class="p-2 bg-brown-100 items-center text-indigo-100 leading-none lg:rounded-full flex lg:inline-flex" role="alert">
                    <span class="flex rounded-full bg-brown-100 uppercase px-2 py-1 text-xs font-bold mr-3">Oops..</span>
                    <span class="font-semibold mr-2 text-left flex-auto">No result found!. Are you sure you have typed it correctly?</span>
                </div>
                </div>
                """
                # st.warning("No result found!. Are you sure you have typed it correctly?")
                st.markdown(f"""{warn}""", unsafe_allow_html=True)
    else:
        st.warning("Please enter a word to search!")
st.markdown(
        """
        <div class="bg-gray-100 py-4 text-gray-700 text-center mx-2 rounded-xl shadow m-4 custom-footer">
            <p class="text-sm text-gray-600">© 2023 Modern Dictionary 💓. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
