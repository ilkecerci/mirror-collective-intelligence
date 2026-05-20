import streamlit as st
import os
from groq import Groq

st.set_page_config(
    page_title="Mirror: Collective Intelligence",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        html, body, [data-testid="stWidgetLabel"] p, .stMarkdown p {
            font-family: 'Inter', sans-serif !important;
        }
        h1 {
            font-size: 2.2rem !important;
            font-weight: 600 !important;
            letter-spacing: -0.05rem;
            padding-bottom: 0.5rem !important;
        }
        
        h4 {
            font-size: 1.1rem !important;
            font-weight: 400 !important;
            color: #888888 !important;
        }
        
        .reflection-success {
            padding: 12px;
            background-color: rgba(0, 200, 100, 0.1);
            border-left: 4px solid #00c864;
            border-radius: 4px;
            color: #e0e0e0;
            font-size: 0.95rem;
            margin-top: 10px;
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

def get_api_key():
    return os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

api_key = get_api_key()

if not api_key:
    st.error("⚠️ GROQ_API_KEY could not be found. Please configure it in your Environment Variables or Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

def check_gravity(topic: str) -> bool:
    try:
        check_prompt = (
            f"Is the following topic about a human tragedy, violence, loss of life, or a serious natural disaster? "
            f"Respond strictly with only 'True' or 'False'. Topic: {topic}"
        )
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": check_prompt}],
            max_tokens=5,
            temperature=0.0
        )
        return "true" in response.choices[0].message.content.lower()
    except Exception:
        return False

# --- MULTI-PLAYER GLOBAL MEMORY PIPELINE (Server-Wide Shared RAM) ---
@st.cache_resource
def get_global_memory():
    """
    Creates a centralized, server-wide volatile memory pipeline using Streamlit's resource cache.
    This replaces individual user session isolation, allowing true multi-agent global collaboration.
    Data stored here lives strictly in the server's ephemeral RAM.
    """
    return {
        "current_topic": "The Impact of AI on Creative Industries", 
        "is_serious": False,
        "raw_data_pool": [],       
        "synthesis_archive": [],   
        "synthesis_counter": 0     
    }

# Connect this runtime instance to the global server memory
global_memory = get_global_memory()

# --- SIDEBAR DIAGNOSTICS & GLOBAL ARCHIVE PANEL ---
st.sidebar.header("📊 Global System Telemetry")
st.sidebar.markdown("---")
st.sidebar.write(f"**Target Focus Matrix:** {global_memory['current_topic']}")
st.sidebar.write(f"**Persona Allocation:** {'Solemn/Empathetic' if global_memory['is_serious'] else 'Casual/Dialectical'}")
st.sidebar.write(f"**Global Volatile Load:** `{len(global_memory['raw_data_pool'])} / 3` fragments accumulated")
st.sidebar.markdown("---")

# Global Synthesis Archive Sidebar Display
st.sidebar.subheader("📚 Collective Memory History")
if not global_memory["synthesis_archive"]:
    st.sidebar.info("The global archive is currently empty. Be the first to trigger a synthesis event!")
else:
    for item in reversed(global_memory["synthesis_archive"]):
        with st.sidebar.expander(f"📍 Context: {item['topic']}"):
            st.write(item["text"])
            st.caption(f"👍 Consensus Score: **{item['votes']['up'] - item['votes']['down']}** (Up: {item['votes']['up']} | Down: {item['votes']['down']})")

st.sidebar.markdown("---")
st.sidebar.info(
    "**Multiplayer Privacy Framework:** Incoming vectors are aggregated globally in transient server RAM. "
    "Raw data is programmatically destroyed every 3 inputs. Only synthesized collective artifacts are archived."
)

# --- ADMIN MATRIX RE-CONFIGURATION LAYER ---
with st.expander("🛠️ System Configuration Panel (Matrix Control)"):
    st.markdown("### *Update the baseline focus for all users globally.*")
    new_topic = st.text_input("Declare New Global Topic Context:", value=global_memory["current_topic"])
    if st.button("Mutate Global Matrix Focus", type="primary"):
        if new_topic and new_topic != global_memory["current_topic"]:
            global_memory["current_topic"] = new_topic
            global_memory["is_serious"] = check_gravity(new_topic)
            global_memory["raw_data_pool"] = [] 
            st.success("Global matrix successfully mutated. All users are now synchronized.")
            st.rerun()

# --- MAIN PRODUCTION MIRROR INTERFACE ---
st.title("🪞 Mirror: Collective Intelligence")
st.markdown("#### *A manipulation-free, ephemeral AI sieve reflecting the raw consensus of society.*")

if global_memory["is_serious"]:
    st.warning("⚠️ **SERIOUS PERSONA PROTOCOL ENFORCED:** The theme involves sensitive human realities. Ironic synthesis and casual social media styles are disabled. Mirroring with solemnity.")
else:
    st.info("💡 **CASUAL PERSONA PROTOCOL ENFORCED:** Normal operating conditions. The Mirror reflects with organic, raw, and ironically detached social media aesthetics.")

st.subheader(f"Current Global Focus Matrix: {global_memory['current_topic']}")
st.divider()

# Input UI Controls
col1, col2 = st.columns([1, 3])
with col1:
    emoji = st.selectbox("Current Emotional Vector?", ["🤔", "😠", "😔", "🙂", "😁"])

with col2:
    comment = st.text_area(
        "Inject Anonymized Thought Vector:", 
        placeholder="Type here... Your input is combined globally with other users on RAM and destroyed instantly.",
        height=120
    )

if st.button("Commit Fragment to Global Pool", type="secondary"):
    if comment:
        # Push the user fragment into the global shared memory pool
        global_memory["raw_data_pool"].append({"emoji": emoji, "text": comment})
        
        # Render the custom CSS fade-in notification correctly inside the scope
        st.markdown(
            f"<div class='reflection-success'>✨ Thought vector successfully synthesized onto the RAM layer. "
            f"Ingested into the pool, imminent for collective reflection. (Global Load: {len(global_memory['raw_data_pool'])}/3)</div>", 
            unsafe_allow_html=True
        )
        
        # Dialectical Synthesis Trigger on the Global Layer
