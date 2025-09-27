import streamlit as st
import pandas as pd
import json

st.title("YouTube Time Analyzer & Next-Binge Predictor")

uploaded_file = st.file_uploader("Upload your YouTube history JSON", type="json")

if uploaded_file:
    data = json.load(uploaded_file)
    df = pd.json_normalize(data)

    # Clean & feature engineer
    df['time'] = pd.to_datetime(df['time'])
    df['date'] = df['time'].dt.date
    df['hour'] = df['time'].dt.hour

    def get_channel(subtitles):
        if isinstance(subtitles, list) and len(subtitles) > 0:
            return subtitles[0].get('name', '')
        return ''
    df['channel'] = df['subtitles'].apply(get_channel)

    def classify_genre(title, channel):
        text = (title + ' ' + channel).lower()
        if 'movie' in text or 'film' in text: return 'Movies'
        if 'tech' in text or 'python' in text or 'ai' in text or 'machine' in text: return 'Tech'
        if 'music' in text or 'song' in text or 'guitar' in text or 'acoustic' in text: return 'Music'
        if 'game' in text or 'gaming' in text or 'walkthrough' in text: return 'Gaming'
        if 'news' in text or 'headlines' in text: return 'News'
        if 'cook' in text or 'recipe' in text or 'baking' in text: return 'Cooking'
        return 'Other'
    df['genre'] = df.apply(lambda x: classify_genre(x['title'], x['channel']), axis=1)

    avg_duration = {'Movies':90,'Tech':10,'Music':4,'Gaming':30,'News':5,'Cooking':15,'Other':8}
    df['duration_min'] = df['genre'].map(avg_duration).fillna(8)

    daily = df.groupby(['date','genre'])['duration_min'].sum().reset_index()
    daily['date'] = pd.to_datetime(daily['date'])

    # Prediction
    predictions = {}
    for genre in daily['genre'].unique():
        genre_data = daily[daily['genre']==genre].sort_values('date')
        last_week = genre_data.tail(7)['duration_min'].mean()
        predictions[genre] = round(last_week,1)

    # Display
    st.subheader("Predicted Next Binge Session (minutes)")
    for genre, mins in predictions.items():
        st.write(f"{genre}: {mins} minutes")

    st.subheader("Daily Watch Time per Genre")
    st.bar_chart(daily.pivot(index='date', columns='genre', values='duration_min'))