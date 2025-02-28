import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime

# ✅ Access API Key
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

# ✅ Function to fetch AI-generated travel options
def get_travel_options(source, destination, travel_date):
    system_prompt = SystemMessage(
        content="""
        You are an AI-powered travel assistant. Provide multiple travel options (cab, train, bus, flight) with estimated costs, duration, 
        and relevant travel tips. Consider the travel date for availability and price fluctuations. Additionally, suggest the best tourist 
        attractions with helpful tips.
        """
    )
    user_prompt = HumanMessage(
        content=f"I am traveling from {source} to {destination} on {travel_date}. Suggest travel options with estimated cost, duration, and important details."
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)

    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

# ✅ Streamlit UI Configuration
st.set_page_config(page_title="Smart Trip Planner", page_icon="✈️", layout="centered")

# ✅ Custom CSS Styling
st.markdown(
    """
    <style>
        body {
            background: url('https://cdn-uploads.huggingface.co/production/uploads/67445925102349e867c92342/5O0QYB7g7VHMvTvrtNREM.jpeg') no-repeat center center fixed;
            background-size: cover;
            color: white;
        }
        .container {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            background: rgba(0, 0, 0, 0.7);
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
            max-width: 600px;
            margin: auto;
        }
        .stButton > button {
            background: #ff9800 !important;
            color: white !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            padding: 6px 12px !important;
            width: 100%;
        }
        input, .stDateInput, textarea {
            border-radius: 5px !important;
            padding: 10px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ✅ UI Layout
st.markdown("<div class='container'>", unsafe_allow_html=True)

st.markdown("""
    <h2 style='text-align: center;'>🚀 Smart Trip Planner</h2>
    <p style='text-align: center; font-size:16px;'>Plan your journey with AI-powered recommendations!</p>
""", unsafe_allow_html=True)

# ✅ Input Section
source = st.text_input("📍 Source Location", placeholder="Enter departure point")
destination = st.text_input("🎯 Destination", placeholder="Enter destination")
travel_date = st.date_input("📅 Travel Date", min_value=datetime.today())

if st.button("🔍 Find Travel Options"):
    if source.strip() and destination.strip():
        with st.spinner("🔄 Fetching best travel routes..."):
            travel_info = get_travel_options(source, destination, travel_date)
            st.success("✅ Travel Recommendations:")
            st.markdown(travel_info)
    else:
        st.warning("⚠️ Please enter both source and destination locations.")

st.markdown("</div>", unsafe_allow_html=True)
