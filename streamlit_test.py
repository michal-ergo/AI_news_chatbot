#>>> streamlit run main.py
streamlit.title("Zpravodaj")

with streamlit.form(key="user_input_form"):
    topic_input = streamlit.text_input("Vlož téma, které tě zajímá:")
    submit_button = streamlit.form_submit_button(label="Potvrdit")

    if submit_button:
        news_client = NewsAPIClient(news_key)
        formatted_articles = news_client.fetch_news(topic=topic_input)

        streamlit.write(formatted_articles)
