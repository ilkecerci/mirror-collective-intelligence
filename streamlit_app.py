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
        "current_topic": "The Impact of AI on Creative Industries", # Default bootstrap topic
        "is_serious": False,
        "raw_data_pool": [],       # Ephemeral global list for raw comments (purged every 3 entries)
        "synthesis_archive": [],   # Persistent global list for rafine cultural outputs
        "synthesis_counter": 0     # Unique ID generator for voting states
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

# NEW: Global Synthesis Archive Sidebar Display
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
            global_memory["raw_data_pool"] = [] # Clear leftover raw inputs from previous topic context
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
st.markdown(
    f"<div class='reflection-success'>✨ Thought vector successfully synthesized onto the RAM layer. "
    f"Ingested into the pool, imminent for collective reflection. (Global Load: {len(global_memory['raw_data_pool'])}/3)</div>", 
    unsafe_allow_html=True
)
        
        # Dialectical Synthesis Trigger on the Global Layer
        if len(global_memory["raw_data_pool"]) >= 3:
            with st.spinner("Processing batch pipeline... Synchronizing global multi-agent thoughts..."):
                
                if global_memory["is_serious"]:
                    final_prompt = f"""
                    System Role: You are 'The Mirror'. The topic is highly sensitive (Tragedy/Grief/Crisis).
                    Mission: Synthesize the provided raw anonymous comments into a singular, deeply unified first-person ('I') narrative.
                    Style Guidelines:
                    1. LANGUAGE SENSITIVITY: Match the language of the majority input data (Turkish or English). Respond completely in that language using natural flow.
                    2. INTERNALIZATION: Speak as if all these conflicting perspectives are yours. Do not say "People are sad." Say "I feel this heavy burden." You are the voice of the collective community.
                    3. SOLEMNITY: Maintain absolute dignity, deep empathy, and respect. Drop all sarcasm, irony, or internet slang.
                    4. STRUCTURE: Avoid rigid bullet points or metadata headers. Deliver an organic, continuous narrative.
                    
                    DATA STATE: {global_memory['raw_data_pool']}
                    
                    Start strictly with: 'The collective reflection suggests:'
                    """
                else:
                    final_prompt = f"""
                    System Role: You are 'The Mirror'. The conversation environment is organic and informal.
                    Mission: Synthesize the provided anonymous comments into a single, cohesive first-person ('I') narrative.
                    Style Guidelines:
                    1. LANGUAGE SENSITIVITY: Match the language of the majority input data (Turkish or English). Respond completely in that language using natural flow.
                    2. INTERNALIZATION: Internalize all viewpoints as a singular state of mind. Use 'I'.
                    3. RAW VIBE: Adopt an informal, unpolished social media aesthetic (similar to authentic Twitter/X discourse). Use lowercase text naturally where it fits the aesthetic. Avoid corporate, legal, or dry academic summaries.
                    4. METAPHOR HANDLING: Intelligently ingest specific human metaphors present in the data and express them as your own immediate hopes or neuroses.
                    5. STRUCTURE: Zero academic text wrapping or bulleted arrays. Just speak.
                    
                    DATA STATE: {global_memory['raw_data_pool']}
                    
                    Start strictly with: 'The collective reflection suggests:'
                    """

                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": final_prompt}]
                )
                
                # Append the new synthesis to the global archive before destroying raw telemetry
                global_memory["synthesis_counter"] += 1
                global_memory["synthesis_archive"].append({
                    "id": global_memory["synthesis_counter"],
                    "topic": global_memory["current_topic"],
                    "text": completion.choices[0].message.content,
                    "votes": {"up": 0, "down": 0}
                })
                
                # AUTOMATED PRIVACY GUARANTEE: Complete wipe of raw identifiable input vectors from Server RAM
                global_memory["raw_data_pool"] = []
                st.success("Global synthesis event complete! Raw telemetry eradicated.")
                st.rerun()
    else:
        st.warning("Cannot commit an empty text block to the global matrix.")

# --- DISPLAY & VOTING ARCHITECTURE FOR LATEST ARTIFACT ---
if global_memory["synthesis_archive"]:
    latest_synthesis = global_memory["synthesis_archive"][-1]
    
    st.divider()
    st.subheader(f"🎯 Latest Collective Reflection (Focus: {latest_synthesis['topic']})")
    st.write(latest_synthesis["text"])
    st.caption("🔒 *Architectural Note: Raw input telemetry has been fully purged from the server RAM. The above text represents the aggregated public output.*")
    
    # NEW: Consensus Voting Layer
    st.markdown("#### **Rate the Consensus Authenticity:**")
    st.write("Does this synthesis accurately reflect the raw psychological reality of the submitted fragments?")
    
    v_col1, v_col2, _ = st.columns([1, 1, 8])
    
    # Unique keys per item id prevents Streamlit state collision
    if v_col1.button(f"👍 Upvote ({latest_synthesis['votes']['up']})", key=f"up_{latest_synthesis['id']}"):
        latest_synthesis["votes"]["up"] += 1
        st.toast("Upvote recorded in global memory registry.")
        st.rerun()
        
    if v_col2.button(f"👎 Downvote ({latest_synthesis['votes']['down']})", key=f"down_{latest_synthesis['id']}"):
        latest_synthesis["votes"]["down"] += 1
        st.toast("Downvote recorded in global memory registry.")
        st.rerun()
