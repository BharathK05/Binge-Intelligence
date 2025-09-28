# Binge-Intelligence


# 🎥 YouTube Time Analyzer & Next-Binge Predictor

**App live at: https://binge-intelligence.streamlit.app/**

---
A web app that analyzes your personal YouTube watch history and predicts your next binge session per genre using lightweight machine learning.

![App Screenshot](https://github.com/BharathK05/Binge-Intelligence/blob/main/Screenshots/Screenshot%201.png) 
![App Screenshot 2](https://github.com/BharathK05/Binge-Intelligence/blob/main/Screenshots/Screenshot%202.png)
---

## 🚀 Features

- **Upload YouTube History**: Drop in the JSON file you download from Google Takeout.
- **Genre Classification**: Automatically groups your watched videos into genres (Movies, Gaming, Tech, Music, Cooking, News, Other).
- **Watch Time Analytics**: Interactive bar charts of your daily watch time per genre.
- **Machine-Learning Prediction**: Uses a simple linear regression model per genre to forecast your next session’s watch duration.
- **Modern UI**: Built with Streamlit — responsive, clean, and deployed online.

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Streamlit** for UI & deployment  
- **Pandas / NumPy** for data wrangling  
- **Scikit-learn** for linear regression prediction  

---

## 📊 How It Works

- Upload your YouTube history JSON file (downloaded from Google Takeout).
- The app parses your watch history, extracts channels, timestamps, and classifies videos into genres.
- For each genre, it aggregates daily watch minutes and trains a small Linear Regression model to forecast the next day’s expected watch time.
- Results are displayed in an interactive dashboard.

---

## 🤝 Contributing

- Pull requests and feature suggestions are welcome. Please open an issue first to discuss any major changes.

---

## 📄 License

- This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---
