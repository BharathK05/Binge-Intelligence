import streamlit as st
import pandas as pd
import json
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

st.set_page_config(page_title="YouTube Analyzer", page_icon="🎥", layout="centered")

# Title with style
st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>🎥 YouTube Time Analyzer & Next-Binge Predictor</h1>",
    unsafe_allow_html=True,
)

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

    # Average durations
    avg_duration = {'Movies':90,'Tech':10,'Music':4,'Gaming':30,'News':5,'Cooking':15,'Other':8}
    df['duration_min'] = df['genre'].map(avg_duration).fillna(8)

    daily = df.groupby(['date','genre'])['duration_min'].sum().reset_index()
    daily['date'] = pd.to_datetime(daily['date'])

    # --- Machine Learning: Linear Regression per genre ---
    predictions = {}
    for genre in daily['genre'].unique():
        genre_data = daily[daily['genre']==genre].sort_values('date')
        y = genre_data['duration_min'].values
        X = np.arange(len(y)).reshape(-1,1)  # time index as feature
        if len(X) > 3:  # only fit if enough data
            model = LinearRegression().fit(X, y)
            next_day_index = np.array([[len(y)+1]])
            pred = model.predict(next_day_index)[0]
            predictions[genre] = round(pred,1)
        else:
            predictions[genre] = round(y.mean(),1)

    # --- Display ---
    st.subheader("🔮 Predicted Next Binge Session (minutes)")
    for genre, mins in predictions.items():
        st.write(f"**{genre}**: {mins} minutes")

    st.subheader("📊 Daily Watch Time per Genre")
    st.bar_chart(daily.pivot(index='date', columns='genre', values='duration_min'))

    # Footer
    st.markdown(
        """
        <hr>
        <div style='text-align: center; color: gray; font-size: small;'>
        © 2025 Bharath Kalimuthu
        </div>
        """,
        unsafe_allow_html=True,
    )