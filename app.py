import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="YouTube Analyzer", page_icon="", layout="wide")

# Stylish title
st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'>YouTube Time Analyzer & Next-Binge Predictor</h1>
    <p style='text-align: center; font-size:18px;'>Upload your YouTube Takeout JSON and discover your watch habits</p>
    """,
    unsafe_allow_html=True
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

    # Display predictions in a nice card-like view
    st.subheader("Predicted Next Binge Session (minutes)")
    pred_df = pd.DataFrame(list(predictions.items()), columns=['Genre','Predicted Minutes'])
    st.dataframe(pred_df, use_container_width=True)

    st.subheader("Daily Watch Time per Genre")

    # Interactive Plotly chart
    fig = px.bar(
        daily,
        x="date",
        y="duration_min",
        color="genre",
        title="Daily Watch Time per Genre",
        labels={"duration_min":"Minutes","date":"Date"},
        hover_data=["genre","duration_min"]
    )
    fig.update_layout(barmode='stack', xaxis_title="Date", yaxis_title="Minutes Watched")
    st.plotly_chart(fig, use_container_width=True)

# Footer with your name & copyright
st.markdown(
    """
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <p style='text-align: center; color: grey; font-size:14px;'>
    © 2025 Bharath Kalimuthu — All rights reserved.
    </p>
    """,
    unsafe_allow_html=True
)