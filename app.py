import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# Ensure src path is accessible
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from smart_grocery_optimizer.data_loader import load_data
from smart_grocery_optimizer.recommender import recommend_many

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="OptimisedDeals | Fresh Groceries", 
    page_icon="🛒", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Custom CSS for Modern UI ---
st.markdown("""
<style>
    /* Clean up default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main typography and headers */
    .title-h1 {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    /* Enhance metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #16a34a;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #475569;
        font-weight: 600;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        background-color: #16a34a;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.65rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #15803d;
        color: white;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgb(0 0 0 / 0.1) 0%, rgb(0 0 0 / 0.1) 100%);
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    .sidebar-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 0.9rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }
    .sidebar-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.25rem;
    }
    .sidebar-text {
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.4;
    }
    .deploy-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 0.9rem;
        color: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Header Section ---
st.markdown('<h1 class="title-h1">🛒 OptimisedDeals</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your smart companion for finding the best local grocery deals based on budget, distance, and real-time stock.</p>', unsafe_allow_html=True)
st.markdown("---")

# --- 4. Data Loading (Cached for performance) ---
@st.cache_data
def get_data():
    return load_data()

families, shops, inventory = get_data()

# Process unique lists
locality_name = sorted(families["area_name"].unique().tolist())
item_names = sorted(inventory["item_name"].dropna().unique().tolist())

# --- 5. Sidebar Navigation & Inputs ---
with st.sidebar:
    st.markdown('<div class="sidebar-card"><div class="sidebar-title">🛍️ Build Your Cart</div><div class="sidebar-text">Pick a locality and item to discover the best nearby grocery option.</div></div>', unsafe_allow_html=True)

    locality = st.selectbox("📍 Select Locality", locality_name)
    item_name = st.selectbox("🍎 Search Item", item_names)

    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input("📦 Quantity", min_value=1, max_value=50, value=5, step=1)
    with col2:
        top_n = st.number_input("🏆 Matches", min_value=1, max_value=10, value=3, step=1)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Find Best Stores"):
        st.session_state["run_recommendation"] = True

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card"><div class="sidebar-title">🚀 Deploy This App</div><div class="sidebar-text">Share it online with Streamlit Community Cloud or any container platform.</div></div>', unsafe_allow_html=True)
    st.link_button("☁️ Deploy on Streamlit Cloud", "https://streamlit.io/cloud")
    st.markdown('<div class="deploy-box">Run locally:<br><code>streamlit run app.py</code></div>', unsafe_allow_html=True)

# --- 6. Main Content & Results ---
if st.session_state.get("run_recommendation"):
    with st.spinner("Analyzing real-time stock, pricing, and travel distances..."):
        # Fetching the first family ID associated with the selected locality
        family_id = families[families["area_name"] == locality].iloc[0].family_id
        
        ranked_results = recommend_many(
            family_id,
            item_name,
            quantity,
            families,
            shops,
            inventory,
            top_n=top_n,
        )

    if not ranked_results:
        st.error("⚠️ We couldn't find a store matching your budget and item availability. Try adjusting your preferences in the sidebar.")
    else:
        df = pd.DataFrame(ranked_results)
        selected = df.iloc[0]

        # Hero highlight for the absolute best match
        st.success("✨ Found the perfect match for you!")
        st.markdown(f"### 🏆 Top Recommendation: **{selected['shop_name']}**")
        
        # Display key metrics side-by-side
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(label="Estimated Cost", value=f"₹{selected['total_cost']:.2f}")
        with m2:
            st.metric(label="Distance", value=f"{selected['distance']:.2f} km")
        with m3:
            st.metric(label="Store Rating", value=f"{selected['rating']:.1f} ⭐")
        with m4:
            st.metric(label="Match Score", value=f"{selected['final_score']:.2f}")

        st.markdown("---")
        st.markdown("### 📋 Alternative Options")
        
        # Enhanced Dataframe styling
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "shop_name": st.column_config.TextColumn("Store Name", width="medium"),
                "total_cost": st.column_config.NumberColumn("Estimated Cost (₹)", format="₹%.2f"),
                "distance": st.column_config.NumberColumn("Distance (km)", format="%.2f km"),
                "rating": st.column_config.NumberColumn("Rating", format="%.1f ⭐"),
                "final_score": st.column_config.ProgressColumn("Match Score", min_value=0, max_value=max(1, df['final_score'].max()), format="%.2f"),
            }
        )

else:
    # Empty State Landing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("👈 **Start by selecting your locality and items from the menu on the left.**")
        st.markdown("""
            ### Why use OptimisedDeals?
            * 💰 **Save Money:** We calculate the lowest basket totals.
            * 🚗 **Save Time:** Recommendations are optimized for nearby stores.
            * ⭐ **Quality Assured:** We factor in historical store ratings.
        """)