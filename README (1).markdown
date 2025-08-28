# ✈️ Flight Price Prediction App 💸

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0+-red.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-1.6+-green.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Welcome to the **Flight Price Prediction App**, a sleek and interactive web application built with **Streamlit** to predict flight ticket prices! Powered by an **XGBoost** model trained on 10,000+ flight records from 2019, this project combines in-depth data analysis from a **Jupyter Notebook** with a modern, black-themed UI. Featuring animated inputs, a dynamic progress bar, and optional confetti animations, it’s designed to make price predictions both accurate and fun! 🎉

This project includes a Jupyter notebook (`EDA Feature Engineering Flight Price Prediction.ipynb`) for exploratory data analysis (EDA), feature engineering, and model training, alongside a Streamlit app (`flight_app.py`) for user-friendly predictions.

## 📸 Screenshots
*Coming soon! Add screenshots of the app’s sleek UI, animated buttons, and confetti effect in `/screenshots`.*

## 🌟 Features
- 🎯 **Accurate Predictions**: Uses an XGBoost model (R² ~0.85) trained on features like `Total_Stops`, `Duration`, and one-hot encoded `Airline`, `Source`, and `Destination`.
- 📓 **Jupyter Notebook**:
  - Comprehensive EDA on `flight_price.xlsx` (10,683 records, 2019, 6 Indian cities).
  - Feature engineering: Extracts `Date`, `Month`, `Duration_hour`, `Duration_minute`, and one-hot encodes categorical variables.
  - Trains an XGBoost Regressor, saved as `flight_rf_model.pkl`.
- 🎨 **Modern & Interactive UI**:
  - Bold black background (`#000000`) with a dark gray sidebar (`#1a1a1a`) for a premium, futuristic vibe.
  - Poppins font, animated inputs (scale/glow on hover), and gradient buttons with pulse animations.
  - Dynamic progress bar during predictions and optional confetti animation (via `streamlit-lottie`).
- 🛠️ **Robust & Reliable**:
  - Fixed a typo (`Airline_SpicJet` → `Airline_SpiceJet`) for seamless predictions.
  - Feature validation prevents mismatches with the model’s expected inputs.
  - Streamlined sidebar by removing redundant "Tips" section for a cleaner interface.
- 📱 **Responsive Design**: Optimized for mobile and desktop with a card-based layout.
- 🔍 **Debugging**: Expander to inspect input features for troubleshooting.

## 🛠️ Tech Stack
- **Python**: 3.8+ for core development
- **Jupyter Notebook**: For EDA, feature engineering, and model training
- **Streamlit**: 1.25.0+ for the web interface
- **XGBoost**: 1.6+ for the prediction model
- **Pandas & NumPy**: Data processing
- **streamlit-lottie & requests**: Optional for confetti animation

## 📋 Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/flight-price-prediction.git
   cd flight-price-prediction
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Core Dependencies**:
   ```bash
   pip install streamlit pandas numpy xgboost jupyter
   ```
   Optional (for confetti animation):
   ```bash
   pip install streamlit-lottie requests
   ```

4. **Ensure Model File**:
   - Place `flight_rf_model.pkl` in the project root. If unavailable, run `EDA Feature Engineering Flight Price Prediction.ipynb` to train the model and generate it.
   - Dataset (`flight_price.xlsx`) is required for the notebook and should be in the `/data` folder.

## 🚀 Running the App
1. **Start the Streamlit Server**:
   ```bash
   streamlit run flight_app.py
   ```
2. **Access the App**:
   - Open your browser at `http://localhost:8501`.

3. **Run the Jupyter Notebook** (optional, for EDA/model training):
   ```bash
   jupyter notebook "EDA Feature Engineering Flight Price Prediction.ipynb"
   ```
   - Follow the notebook to explore data, engineer features, and train the model.

## 🎮 How to Use
1. **Explore the Data (Optional)**:
   - Open `EDA Feature Engineering Flight Price Prediction.ipynb` in Jupyter to understand the dataset, visualize trends, and train the XGBoost model.
   - Outputs `flight_rf_model.pkl` for use in the Streamlit app.

2. **Enter Flight Details in the App**:
   - Select **Airline** (e.g., IndiGo), **Source City** (e.g., Bangalore), **Destination City** (e.g., New Delhi), **Journey Date**, **Departure Time**, **Arrival Time**, and **Total Stops**.
   - Example: IndiGo, Bangalore → New Delhi, non-stop, August 28, 2025, 22:20 departure, 01:10 arrival.
3. **Predict Price**:
   - Click the "🚀 Predict Price" button to see the estimated price (e.g., ~₹3,897 for sample input) and flight duration (e.g., 2h 50m).
   - Enjoy the progress bar and (if installed) confetti animation on success!
4. **Debug**:
   - Use the "🔍 Debug: Input Features" expander to verify the input DataFrame.

## 📊 Model Details
- **Dataset**: 10,683 flight records from 2019 (`flight_price.xlsx`), covering 6 Indian cities (Bangalore, Chennai, Delhi, Kolkata, Mumbai, New Delhi).
- **Features**: `Total_Stops`, `Date`, `Month`, `Year` (fixed to 2019), `Arrival_hour`, `Arrival_minute`, `Departure_hour`, `Departure_minute`, `Duration_hour`, `Duration_minute`, and one-hot encoded `Airline`, `Source`, `Destination`.
- **Model**: XGBoost Regressor (n_estimators=300, learning_rate=0.1, max_depth=6).
- **Performance**: R² ~0.855, MAE ~1125.18, RMSE ~1754.72 (from notebook).

## 🐛 Troubleshooting
- **ModuleNotFoundError: No module named 'streamlit_lottie'**:
  - Install: `pip install streamlit-lottie requests`.
  - The app skips the confetti animation if not installed, with a warning.
- **Prediction Failed: Feature Mismatch**:
  - Check the debug expander for missing/extra features.
  - Ensure `flight_rf_model.pkl` aligns with `model_columns` (includes `Airline_SpiceJet`).
  - Re-run the notebook to regenerate the model if needed.
- **Environment Issues**:
  - Use Streamlit 1.25.0+ and XGBoost 1.6+.
  - Verify dependencies:
    ```bash
    pip list | findstr "streamlit pandas numpy xgboost streamlit-lottie requests jupyter"
    ```
- **Notebook Errors**:
  - Ensure `flight_price.xlsx` is in the `/data` folder.
  - Check Python version compatibility (3.8+ recommended).
- **Time Zone**: Uses IST (e.g., 09:18 PM IST, August 28, 2025). Ensure system time is correct for `st.date_input`.

## 🔮 Future Enhancements
- Add a flight route map using `streamlit-folium`.
- Include a reset button to clear inputs in the app.
- Support dynamic `Year` input (currently fixed to 2019).
- Deploy to Streamlit Cloud for public access.
- Enhance the notebook with additional visualizations (e.g., price trends by airline).

## 🤝 Contributing
Love the project? Contributions are welcome!
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/YourFeature`.
3. Commit changes: `git commit -m 'Add YourFeature'`.
4. Push: `git push origin feature/YourFeature`.
5. Open a pull request.

## 📜 License
Licensed under the [MIT License](LICENSE).

## 📬 Contact
Questions or ideas? Connect with me on [LinkedIn](https://www.linkedin.com/in/your-profile) or open an issue on GitHub.

---

*Built with 💻 and ☕ on August 28, 2025, in India.*