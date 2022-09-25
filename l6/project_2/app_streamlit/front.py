import streamlit as st
import requests
st.title("Modele Reddit")

select = st.selectbox("Wybierz model", ("Regresja liniowa", "Regresja logistyczna", "Drzewo decyzyjne"))
st.write('Wybrałeś:', select)

if select == "Regresja liniowa":
    endpoint = "/linearregression"
    subreddit_name = st.selectbox(
        'Subreddit:',
        ("AskReddit", "politics", "funny", "news", "memes")
    )

    post_text = st.text_input('Tekst:', '')
    is_nsfw = st.selectbox(
        'Kategoria NSFW:',
        ('Tak', 'Nie')
    )
    if is_nsfw == 'Tak':
        is_nsfw = True
    else:
        is_nsfw = False

    num_votes = st.text_input('Liczba polubień:', '')
    num_comments = st.text_input('Liczba komentarzy:', '')

    params = {
        'subreddit': subreddit_name,
        'number_votes': num_votes,
        'belongs_to_NSFW_ind': is_nsfw,
        'num_of_comments': num_comments,
        'text': post_text
    }
    st.write('Przewidziana długość postu:')

elif select == "Regresja logistyczna":
    endpoint = "/binary"
    subreddit_name = st.selectbox(
        'Subreddit:',
        ("AskReddit", "politics", "funny", "news", "memes")
    )
    post_text = st.text_input('Tekst:', '')

    num_votes = st.text_input('Liczba polubień:', '')
    num_comments = st.text_input('Liczba komentarzy:', '')

    params = {
        'subreddit': subreddit_name,
        'number_votes': num_votes,
        'num_of_comments': num_comments,
        'text': post_text
    }
    st.write('Czy należy do NSFW:')

elif select == "Drzewo decyzyjne":
    endpoint = "/multiclass"
    post_text = st.text_input('Tekst:', '')
    is_nsfw = st.selectbox(
        'Kategoria NSFW:',
        ('Tak', 'Nie')
    )
    if is_nsfw == 'Tak':
        is_nsfw = True
    else:
        is_nsfw = False
    num_votes = st.text_input('Liczba polubień:', '')
    num_comments = st.text_input('Liczba komentarzy:', '')

    params = {
        'number_votes': num_votes,
        'belongs_to_NSFW_ind': is_nsfw,
        'num_of_comments': num_comments,
        'text': post_text
    }
    st.write('Należy do subreddita:')

submit = st.button('Poznaj odpowiedź')
if submit:
    model_url = 'http://app_flask:8080' + endpoint
    requests_out = requests.get(model_url, params=params)
    st.write(requests_out.text)