# Modern Dictionary

Modern Dictionary is a web application that allows users to search for word definitions using an online dictionary. It utilizes the Streamlit framework for the user interface and Selenium for web scraping.

## Features

- Search for word definitions
- Display word type, level, and phonetic form
- Play audio pronunciation (if available)
- Show multiple definitions

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/modern-dictionary.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Download and install the appropriate version of ChromeDriver for your Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Make sure to place the `chromedriver` executable in your system's PATH.

## Usage

1. Run the following command to start the web application:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and go to the displayed URL (usually http://localhost:8501).

3. Enter a word in the search box and click the "Search" button.

4. The definitions, word type, level, and phonetic form will be displayed. If available, you can also listen to the audio pronunciation.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
