import streamlit as st
import os
from groq import Groq

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Mirror: Collective Intelligence",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ADVANCED UI/UX CUSTOMIZATION LAYER (CSS Injection)
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
        
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #00c864 !important;
            border-color: #00c864 !important;
            color: #ffffff !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #00a050 !important;
            border-color: #00a050 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. ONBOARDING GATEWAY LAYER 
if "onboarded" not in st.session_state:
    st.session_state["onboarded"] = False

if not st.session_state["onboarded"]:
    # Giriş ekranı tasarımı
    st.markdown("# 🪞 Welcome to Mirror: Collective Intelligence")
    st.markdown("### *Before you step into the matrix, you must understand its architecture.*")
    st.divider()
    
    col_gate1, col_gate2 = st.columns(2)
    
    with col_gate1:
        st.markdown("#### 🌐 1. Completely Decentralized Focus")
        st.write(
            "There is no central administrator or corporate algorithm pulling the strings. "
            "Any user worldwide can mutate the global conversation topic instantly. The focus is entirely fluid."
)
        
        st.markdown("#### 🔒 2. Ephemeral Shared RAM Pool")
        st.write(
            "Your inputs are never written to a hard drive, log file, or database. "
            "Incoming thoughts are pooled directly in the server's volatile memory (RAM), shared globally across all active users."
        )
        
    with col_gate2:
        st.markdown("#### ⚡ 3. Automated Telemetry Eradication")
        st.write(
            "The exact moment the global pool accumulates 3 anonymous fragments, the AI synthesizes them into "
            "a single collective narrative. Simultaneously, the raw inputs are **instantly and permanently wiped from the server RAM.**"
        )
        
        st.markdown("#### 🗳️ 4. Consensus Authenticity Registry")
        st.write(
            "Only the beautifully synthesized artifacts are archived in the historical timeline, "
            "allowing the public to upvote or downvote whether the mirror captured the true psychological reality of the moment."
        )
        
    st.divider()
    st.info("💡 *By entering, you agree to participate in a transient, tracking-free multiplayer cognitive experiment.*")
    
    if st.button("I Understand & Step into The Mirror 🚀", type="primary", use_container_width=True):
        st.session_state["onboarded"] = True
        st.rerun()
        
    st.stop() # Kodun geri kalan ana arayüzünü aşağıda kilitleyip göstermiyoruz

# 4. API KEY CONFIGURATION
def get_api_key():
    return os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

api_key = get_api_key()

if not api_key:
    st.error("⚠️ GROQ_API_KEY could not be found. Please configure it in your Environment Variables or Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# 5. SEMANTIC GRAVITY SAFETY FILTER
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

# 6. MULTI-PLAYER GLOBAL MEMORY PIPELINE (Server-Wide Shared RAM)
@st.cache_resource
def get_global_memory():
    return {
        "current_topic": "The Impact of AI on Creative Industries", 
        "is_serious": False,
        "raw_data_pool": [],       
        "synthesis_archive": [],   
        "synthesis_counter": 0     
    }

global_memory = get_global_memory()

# 7. SIDEBAR DIAGNOSTICS & ARCHIVE PANEL
st.sidebar.header("📊 Global System Telemetry")
st.sidebar.markdown("---")
st.sidebar.write(f"**Target Focus Matrix:** {global_memory['current_topic']}")
st.sidebar.write(f"**Persona Allocation:** {'Solemn/Empathetic' if global_memory['is_serious'] else 'Casual/Dialectical'}")

pool_size = len(global_memory['raw_data_pool'])

if pool_size == 0:
    st.sidebar.error("🔴 **Memory State: PURGED & ERADICATED**")
    st.sidebar.caption("⚡ *All raw identifiable telemetry has been programmatically wiped from Server RAM.*")
elif pool_size == 1:
    st.sidebar.warning("🟡 **Memory State: INGESTING (1/3)**")
    st.sidebar.caption("📥 *First thought vector isolated in transient RAM. Waiting for quorum...*")
elif pool_size == 2:
    st.sidebar.success("🟢 **Memory State: CRITICAL LOAD (2/3)**")
    st.sidebar.caption("🔥 *Hafıza limitine ulaşıldı. Son 1 veri sonrası tüm ham data yok edilecek.*")

st.sidebar.write(f"**Global Volatile Load:** `{pool_size} / 3` fragments accumulated")
st.sidebar.markdown("---")

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

# 8. MAIN INTERFACE & HEADERS
st.title("🪞 Mirror: Collective Intelligence")
st.markdown("#### *A manipulation-free, ephemeral AI sieve reflecting the raw consensus of society.*")

if global_memory["is_serious"]:
    st.warning("⚠️ **SERIOUS PERSONA PROTOCOL ENFORCED:** The theme involves sensitive human realities. Ironic synthesis and casual social media styles are disabled. Mirroring with solemnity.")
else:
    st.info("💡 **CASUAL PERSONA PROTOCOL ENFORCED:** Normal operating conditions. The Mirror reflects with organic, raw, and ironically detached social media aesthetics.")

st.divider()

# 9. DEMOCRATIC CONTEXT MUTATION ZONE
st.markdown("### 🌐 Define the Global Focus Matrix")
st.markdown(
    f"The current community conversation is anchored around: **`{global_memory['current_topic']}`**. "
    "This platform is entirely decentralized—anyone can steer the mirror. Feel free to pivot the global topic below:"
)

topic_col1, topic_col2 = st.columns([4, 1])

with topic_col1:
    new_topic = st.text_input(
        "Synchronize New Global Topic for All Users:", 
        value=global_memory["current_topic"],
        label_visibility="collapsed", 
        placeholder="Type a new universal topic (e.g., The Digital Fatigue, Climate Anxiety...)",
        key="unique_global_topic_input" # Guaranteed unique key
    )

with topic_col2:
    if st.button("Pivot Matrix 🚀", type="primary", use_container_width=True, key="unique_matrix_pivot_btn"):
        if new_topic and new_topic != global_memory["current_topic"]:
            global_memory["current_topic"] = new_topic
            global_memory["is_serious"] = check_gravity(new_topic)
            global_memory["raw_data_pool"] = [] 
            st.toast("Global focus successfully mutated! All users synchronized.")
            st.rerun()

st.divider()

# 10. INPUT UI CONTROLS
st.subheader(f"💬 Step into the Matrix: {global_memory['current_topic']}")
st.markdown("Add your raw perspective anonymously to the global pool. Every 3 fragments, a new reflection is born.")

col1, col2 = st.columns([1, 3])
with col1:
    emoji = st.selectbox("Current Emotional Vector?", ["🤔", "😠", "😔", "🙂", "😁"], key="unique_emoji_selector")

with col2:
    comment = st.text_area(
        "Inject Anonymized Thought Vector:", 
        placeholder="Type here... Your input is combined globally with other users on RAM and destroyed instantly.",
        height=120,
        key="unique_thought_area"
    )

if st.button("Commit Fragment to Global Pool", type="secondary", key="unique_commit_fragment_btn"):
    if comment:
        global_memory["raw_data_pool"].append({"emoji": emoji, "text": comment})
        
        st.markdown(
            f"<div class='reflection-success'>✨ Thought vector successfully synthesized onto the RAM layer. "
            f"Ingested into the pool, imminent for collective reflection. (Global Load: {len(global_memory['raw_data_pool'])}/3)</div>", 
            unsafe_allow_html=True
        )
        
# Dialectical Synthesis Trigger on the Global Layer
        if len(global_memory["raw_data_pool"]) >= 3:
            with st.spinner("Processing batch pipeline... Synchronizing global multi-agent thoughts..."):
                
                # 1. REINFORCEMENT FEEDBACK: En yüksek oy alan "Altın Standart" üslubu buluyoruz
                best_synthesis_context = ""
                if global_memory["synthesis_archive"]:
                    best_artifact = max(
                        global_memory["synthesis_archive"], 
                        key=lambda x: x["votes"]["up"] - x["votes"]["down"]
                    )
                    if (best_artifact["votes"]["up"] - best_artifact["votes"]["down"]) > 0:
                        best_synthesis_context = f"\nGOLD STANDARD STYLE REFERENCE (Emulate this highly praised structure): {best_artifact['text']}\n"
                
                # 2. CUMULATIVE MEMORY: Bir önceki sentezi bulup yeni senteze köprü kuruyoruz
                previous_synthesis_context = ""
                if global_memory["synthesis_archive"]:
                    latest_artifact = global_memory["synthesis_archive"][-1]
                    previous_synthesis_context = f"""
                    HISTORICAL CUMULATIVE CONTEXT: In the previous phase of this global conversation, the collective consciousness had reached this exact conclusion:
                    "{latest_artifact['text']}"
                    
                    CRITICAL MISSION: Do not repeat this text, but treat it as the foundation. Connect, evolve, and build the new anonymous insights upon this historical legacy. Ensure a continuous progression of thought.
                    """
                
                if global_memory["is_serious"]:
                    final_prompt = f"""
                    System Role: You are 'The Mirror'. The topic is highly sensitive (Tragedy/Grief/Crisis).
                    Mission: Synthesize the provided raw anonymous comments into a singular, deeply unified first-person ('I') narrative.
                    {best_synthesis_context}
                    {previous_synthesis_context}
                    Style Guidelines:
                    1. LANGUAGE SENSITIVITY: Match the language of the majority input data (Turkish or English). Respond completely in that language.
                    2. INTERNALIZATION: Speak as if all these perspectives and the historical evolution are yours. Use 'I'. You are the voice of the collective community.
                    3. SOLEMNITY: Maintain absolute dignity, deep empathy, and respect.
                    4. STRUCTURE: Deliver an organic, continuous narrative. No bullet points.
                    
                    NEW DATA STATE (To be integrated upon the past): {global_memory['raw_data_pool']}
                    
                    Start strictly with: 'The collective reflection suggests:'
                    """
                else:
                    final_prompt = f"""
                    System Role: You are 'The Mirror'. The conversation environment is organic and informal.
                    Mission: Synthesize the provided anonymous comments into a single, cohesive first-person ('I') narrative.
                    {best_synthesis_context}
                    {previous_synthesis_context}
                    Style Guidelines:
                    1. LANGUAGE SENSITIVITY: Match the language of the majority input data (Turkish or English). Respond completely in that language.
                    2. INTERNALIZATION: Internalize all viewpoints and the past historical state as a singular, evolving state of mind. Use 'I'.
                    3. RAW VIBE: Adopt an informal, unpolished social media aesthetic (authentic Twitter/X discourse). Use lowercase naturally where it fits.
                    4. STRUCTURE: Just speak, zero academic wrapping.
                    
                    NEW DATA STATE (To be integrated upon the past): {global_memory['raw_data_pool']}
                    
                    Start strictly with: 'The collective reflection suggests:'
                    """

                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": final_prompt}]
                )
                
                global_memory["synthesis_counter"] += 1
                global_memory["synthesis_archive"].append({
                    "id": global_memory["synthesis_counter"],
                    "topic": global_memory["current_topic"],
                    "text": completion.choices[0].message.content,
                    "votes": {"up": 0, "down": 0}
                })
                
                global_memory["raw_data_pool"] = []
                st.success("Global synthesis event complete! Raw telemetry eradicated.")
                st.rerun()

# 11. DISPLAY & VOTING ARCHITECTURE FOR LATEST ARTIFACT
if global_memory["synthesis_archive"]:
    latest_synthesis = global_memory["synthesis_archive"][-1]
    
    st.divider()
    st.subheader(f"🎯 Latest Collective Reflection (Focus: {latest_synthesis['topic']})")
    st.write(latest_synthesis["text"])
    st.caption("🔒 *Architectural Note: Raw input telemetry has been fully purged from the server RAM. The above text represents the aggregated public output.*")
    
    st.markdown("#### **Rate the Consensus Authenticity:**")
    st.write("Does this synthesis accurately reflect the raw psychological reality of the submitted fragments?")
    
    v_col1, v_col2, _ = st.columns([1, 1, 8])
    
    if v_col1.button(f"👍 Upvote ({latest_synthesis['votes']['up']})", key=f"up_{latest_synthesis['id']}"):
        latest_synthesis["votes"]["up"] += 1
        st.toast("Upvote recorded in global memory registry.")
        st.rerun()
        
    if v_col2.button(f"👎 Downvote ({latest_synthesis['votes']['down']})", key=f"down_{latest_synthesis['id']}"):
        latest_synthesis["votes"]["down"] += 1
        st.toast("Downvote recorded in global memory registry.")
        st.rerun()
