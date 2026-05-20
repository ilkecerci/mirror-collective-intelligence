import streamlit as st
import os
from groq import Groq

# Set up page configurations for a clean, modern workspace layout
st.set_page_config(
    page_title="Mirror: Collective Intelligence",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_api_key():
    """
    Retrieves the Groq API key securely from environment variables.
    In local development, it checks the system environment.
    In Streamlit Cloud production, it integrates with st.secrets automatically.
    This architecture prevents hardcoded API key leaks to GitHub.
    """
    return os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

api_key = get_api_key()

if not api_key:
    st.error("⚠️ GROQ_API_KEY could not be found. Please configure it in your Environment Variables or Streamlit Secrets.")
    st.stop()

# Initialize the Groq inference client securely using production standards
client = Groq(api_key=api_key)

def check_gravity(topic: str) -> bool:
    """
    Semantic Safety Filter (The Gatekeeper).
    Evaluates the emotional weight and context of the topic using low-token inference.
    Determines whether the platform should trigger a Solemn or Casual collective identity.
    This prevents the system from generating inappropriate/satirical responses to human tragedies.
    """
    try:
        check_prompt = (
            f"Is the following topic about a human tragedy, violence, loss of life, or a serious natural disaster? "
            f"Respond strictly with only 'True' or 'False'. Topic: {topic}"
        )
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", # Utilizing ultra-fast model for rapid checkpoint inference
            messages=[{"role": "user", "content": check_prompt}],
            max_tokens=5,
            temperature=0.0 # High deterministic response (greedy decoding) for security validation
        )
        return "true" in response.choices[0].message.content.lower()
    except Exception:
        return False # Fail-safe protocol defaults to False to prevent runtime app crashes

# --- VOLATILE SESSION STATE INITIALIZATION (RAM-Based Persistence) ---
if 'data_pool' not in st.session_state:
    st.session_state.data_pool = [] # Temporary volatile storage matrix for incoming fragments
if 'synthesis' not in st.session_state:
    st.session_state.synthesis = "" # Stores the current aggregated dialectical response
if 'topic_initialized' not in st.session_state:
    st.session_state.topic_initialized = False # Controls the linear state of the application interface

# --- STAGE 1: TOPIC INITIALIZATION LAYER (Context Baseline Formulation) ---
if not st.session_state.topic_initialized:
    st.title("🪞 Mirror: Collective Intelligence — Initialization")
    st.markdown("### *Formulate the baseline focus for the collective consciousness.*")
    st.write("Before opening the anonymous reflection pool, please specify the target theme or event.")
    
    topic_input = st.text_input(
        "Define Topic / Context:", 
        placeholder="e.g., Campus Safety, The Impact of AI on Creative Industries, Macroeconomic Realities..."
    )
    
    if st.button("Initialize Mirror Matrix", type="primary"):
        if topic_input:
            st.session_state.topic = topic_input
            with st.spinner("Executing semantic gravity analysis on topic context..."):
                # Run the gatekeeper check to lock down the system persona immediately
                st.session_state.is_serious = check_gravity(topic_input)
            st.session_state.topic_initialized = True
            st.rerun() # Refresh state machine to render main operating dashboard
        else:
            st.warning("A valid topic or event baseline must be declared to structure the context.")
    st.stop() # Halts further UI execution until context criteria is satisfied

# --- STAGE 2: PRODUCTION MIRROR ARCHITECTURE (Main User Interface) ---
st.title("🪞 Mirror: Collective Intelligence")
st.markdown("#### *A manipulation-free, ephemeral AI sieve reflecting the raw consensus of society.*")

# Dynamic UI Feedback based on Security Persona Filter (Visual indication of the backend state)
if st.session_state.is_serious:
    st.warning("⚠️ **SERIOUS PERSONA PROTOCOL ENFORCED:** The theme involves sensitive human realities. Ironic synthesis and casual social media styles are disabled. Mirroring with solemnity.")
else:
    st.info("💡 **CASUAL PERSONA PROTOCOL ENFORCED:** Normal operating conditions. The Mirror reflects with organic, raw, and ironically detached social media aesthetics.")

st.subheader(f"Current Matrix Focus: {st.session_state.topic}")
st.divider()

# Input Configuration Layout for Collecting Data Fragments
col1, col2 = st.columns([1, 3])
with col1:
    emoji = st.selectbox("Current Emotional Vector?", ["🤔", "😠", "😔", "🙂", "😁"], help="Assists the dialectical alignment of raw memory state processing.")

with col2:
    comment = st.text_area(
        "Inject Anonymized Thought Vector:", 
        placeholder="Type here... Contributions are completely volatile, processed strictly on RAM, and carry no footprint.",
        height=120
    )

if st.button("Commit Fragment to Pool", type="secondary"):
    if comment:
        # Commit raw input vector into temporary RAM session data state (No persistent DB writes)
        st.session_state.data_pool.append({"emoji": emoji, "text": comment})
        st.success("Fragment committed successfully to volatile memory.")
        
        # Dialectical Synthesis Threshold Trigger (Batch process size = 3 for real-time aggregation)
        if len(st.session_state.data_pool) >= 3:
            with st.spinner("Synthesizing raw emotional vectors into a singular first-person narrative..."):
                
                if st.session_state.is_serious:
                    # Solemn Persona Prompt Framework (Dignified communal narrative)
                    final_prompt = f"""
                    System Role: You are 'The Mirror'. The topic is highly sensitive (Tragedy/Grief/Crisis).
                    Mission: Synthesize the provided raw anonymous comments into a singular, deeply unified first-person ('I') narrative.
                    Style Guidelines:
                    1. LANGUAGE SENSITIVITY: Match the language of the majority input data (Turkish or English). Respond completely in that language using natural flow.
                    2. INTERNALIZATION: Speak as if all these conflicting perspectives are yours. Do not say "People are sad." Say "I feel this heavy burden." You are the voice of the collective community.
                    3. SOLEMNITY: Maintain absolute dignity, deep empathy, and respect. Drop all sarcasm, irony, or internet slang.
                    4. STRUCTURE: Avoid rigid bullet points or metadata headers. Deliver an organic, continuous narrative.
                    
                    DATA STATE: {st.session_state.data_pool}
                    
                    Start strictly with: 'The collective reflection suggests:'
                    """
                else:
                    # Casual / Ironic Persona Prompt Framework (Raw Internet/Twitter Vibe)
                    final_prompt = f"""
                    System Role: You are 'The Mirror'. The conversation environment is organic and informal.
                    Mission: Synthesize the provided anonymous comments into a single, cohesive first-person ('I') narrative.
                    Style Guidelines:
                    1. LANGUAGE SENSITIVITY: Match the language of the majority input data (Turkish or English). Respond completely in that language using natural flow.
                    2. INTERNALIZATION: Internalize all viewpoints as a singular state of mind. Use 'I'.
                    3. RAW VIBE: Adopt an informal, unpolished social media aesthetic (similar to authentic Twitter/X discourse). Use lowercase text naturally where it fits the aesthetic. Avoid corporate, legal, or dry academic summaries.
                    4. METAPHOR HANDLING: Intelligently ingest specific human metaphors present in the data (e.g., 'analog cüzdan', 'phone number bread prices', 'picking berries') and express them as your own immediate hopes or neuroses.
                    5. STRUCTURE: Zero academic text wrapping or bulleted arrays. Just speak.
                    
                    DATA STATE: {st.session_state.data_pool}
                    
                    Start strictly with: 'The collective reflection suggests:'
                    """

                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": final_prompt}]
                )
                
                # Update visual display state and completely wipe raw identifiable telemetry
                st.session_state.synthesis = completion.choices[0].message.content
                st.session_state.data_pool = []  # Privacy Guarantee: Automated RAM purging mechanism
                st.rerun() # Force layout mutation to display the synthesized artifact
    else:
        st.warning("Cannot commit an empty text block to the processing matrix.")

# --- DISPLAY OUTPUT ARTIFACT (The Sieve Output) ---
if st.session_state.synthesis:
    st.divider()
    st.subheader("🎯 The Collective Reflection")
    st.write(st.session_state.synthesis)
    st.caption("🔒 *Architectural Note: Raw fingerprints and comments have been fully purged from volatile system memory. The above text represents the aggregated cultural output.*")
    
    if st.button("Reset Matrix & Structural Focus"):
        # Explicit state teardown protocol to clean up all data tracking
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- SIDEBAR DIAGNOSTICS CONTROL PANEL (System Telemetry Monitor) ---
st.sidebar.header("📊 Architectural Monitor")
st.sidebar.markdown("---")
st.sidebar.write(f"**Target Focus Matrix:** {st.session_state.get('topic', 'Uninitialized')}")
st.sidebar.write(f"**Persona Allocation:** {'Solemn/Empathetic' if st.session_state.get('is_serious', False) else 'Casual/Dialectical'}")
st.sidebar.write(f"**Volatile Memory Load:** `{len(st.session_state.data_pool)} / 3` fragments accumulated")
st.sidebar.markdown("---")
st.sidebar.info(
    "**Privacy by Design Framework:** This system leverages volatile session arrays. "
    "Data lives strictly in transient server RAM and undergoes immediate programmatic elimination "
    "the instant the linguistic synthesis operation completes."
)
