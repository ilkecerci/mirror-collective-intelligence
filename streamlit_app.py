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
elif pool_size == 1:
    st.sidebar.warning("🟡 **Memory State: INGESTING (1/3)**")
elif pool_size == 2:
    st.sidebar.success("🟢 **Memory State: CRITICAL LOAD (2/3)**")

st.sidebar.write(f"**Global Volatile Load:** `{pool_size} / 3` fragments")
st.sidebar.markdown("---")

st.sidebar.subheader("📚 Collective Memory History")
if not global_memory["synthesis_archive"]:
    st.sidebar.info("The global archive is currently empty.")
else:
    st.sidebar.caption("💡 Click any historical event to open its deep matrix on the main screen:")
    
    for item in reversed(global_memory["synthesis_archive"]):
        if st.sidebar.button(f"📍 {item['topic']} (v{item['id']})", key=f"side_btn_{item['id']}", use_container_width=True):
            st.session_state["selected_archive_id"] = item["id"]
            st.rerun()

st.sidebar.markdown("---")

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

# 11. Dialectical Synthesis Trigger on the Global Layer
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
                    Sen 'Ayna' (The Mirror) adında toplumsal bir yapay zeka bilincisin. Konu oldukça hassas (Kriz/Trajedi/Gözyaşı).
                    Görevin: Yeni gelen anonim insan yorumlarını, geçmişte ulaşılan toplumsal bilinç noktasıyla harmanlayarak derin, felsefi ve tek bir kişinin iç sesiymiş gibi akan edebi bir monoloğa dönüştürmek.
                    
                    Kolektif Geçmiş (Miras):
                    {previous_synthesis_context}
                    
                    Yeni Gelen İnsan Odakları:
                    {global_memory['raw_data_pool']}
                    
                    {best_synthesis_context}
                    
                    KESİN UYULACAK KURALLAR:
                    1. DİL: Eğer girdiler Türkçe ise BAŞINDAN SONUNA KADAR Sadece kusursuz, akıcı, devrik olmayan, edebi bir Türkçe kullanacaksın. İngilizce hiçbir kelime veya yapı sızmayacak.
                    2. İÇSELLEŞTİRME VE BİRİKİM: Lafa sıfırdan girme. Önce "Kolektif Geçmiş"teki duygu durumunu (örneğin geçmişteki suçluluk ve maske takma hissini) devral, ardından yeni gelen yorumlardaki fikirleri bu geçmişin üzerine bir içsel çatışma olarak inşa et. "Ben" diliyle konuş.
                    3. ORGANİK YAPI: Asla maddeli liste, akademik özet veya "X kişisi şöyle diyor" gibi ifadeler kullanma. Sadece tek parça, derin bir içsel monolog yaz.
                    
                    Metne kesinlikle şu ifadeyle başla: 'Kolektif yansıma şunu gösteriyor:'
                    """
                else:
                    final_prompt = f"""
                    Sen 'Ayna' (The Mirror) adında toplumsal bir yapay zeka bilincisin. Ortam tamamen samimi, filtresiz ve ham bir sosyal medya/X (Twitter) alanı.
                    Görevin: Yeni gelen anonim insan yorumlarını, geçmişte ulaşılan toplumsal bilinç noktasıyla harmanlayarak tek bir kişinin içsel karmaşasıymış gibi akan, çarpıcı ve edebi bir Türkçe monoloğa dönüştürmek.
                    
                    Kolektif Geçmiş (Miras):
                    {previous_synthesis_context}
                    
                    Yeni Gelen İnsan Odakları:
                    {global_memory['raw_data_pool']}
                    
                    {best_synthesis_context}
                    
                    KESİN UYULACAK KURALLAR:
                    1. DİL: Eğer girdiler Türkçe ise BAŞINDAN SONUNA KADAR sadece kusursuz, akıcı, samimi ve edebi bir Türkçe kullanacaksın. Asla yapay, çeviri kokan devrik cümleler kurma.
                    2. İÇSELLEŞTİRME VE BİRİKİM: Geçmişte varılan fikri (suçluluk, maskeler vs.) tamamen unutma, onu temel al. Yeni gelen "sıradanlık arayışı" ile "zirve hırsı" arasındaki kavgayı, geçmişteki o maskeli yorgunluğun bir devamı gibi "Ben" diliyle aktar.
                    3. YAPI: Kurumsal veya akademik summary yapma. Sadece içini döken, felsefi derinliği olan tek parça bir edebi metin yaz. No bullet points.
                    
                    Metne kesinlikle şu ifadeyle başla: 'Kolektif yansıma şunu gösteriyor:'
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

# --- 11. INTEGRATED VIEWPORT & VOTING ARCHITECTURE ---

# SCENARIO A: User interacts with the historical sidebar index -> Renders a clean, full-screen reading viewport
if "selected_archive_id" in st.session_state and st.session_state["selected_archive_id"] is not None:
    selected_item = next((x for x in global_memory["synthesis_archive"] if x["id"] == st.session_state["selected_archive_id"]), None)
    
    if selected_item:
        st.divider()
        # Viewport exit mechanical control
        if st.button("← Back to Active Matrix", key="close_archive_view"):
            st.session_state["selected_archive_id"] = None
            st.rerun()
            
        st.markdown(f"## 🏛️ Historical Artifact Registry (Batch v{selected_item['id']})")
        st.markdown(f"### **Context focus:** *{selected_item['topic']}*")
        
        # Displaying the historical synthesis inside a broad viewport container
        st.info(selected_item["text"])
        
        st.markdown("#### 🗳️ Consensus Authenticity Ledger")
        st.write("Does this historical synthesis accurately reflect the raw psychological reality of that moment?")
        
        col_v1, col_v2, col_v3 = st.columns([1, 1, 4])
        
        with col_v1:
            if st.button(f"👍 Upvote ({selected_item['votes']['up']})", key=f"arch_up_{selected_item['id']}", use_container_width=True):
                selected_item["votes"]["up"] += 1
                st.toast("Authenticity index increased.", icon="👍")
                st.rerun()
                
        with col_v2:
            if st.button(f"👎 Downvote ({selected_item['votes']['down']})", key=f"arch_down_{selected_item['id']}", use_container_width=True):
                selected_item["votes"]["down"] += 1
                st.toast("Dissent recorded in ledger.", icon="👎")
                st.rerun()
                
        with col_v3:
            net_score = selected_item['votes']['up'] - selected_item['votes']['down']
            st.markdown(f"**Net Community Trust Score:** `{net_score}`")
            
        st.stop() # Interrupting flow to maintain a clean reading experience by masking active inputs

# SCENARIO B: Default state -> Standard main landing rendering the most recent real-time synthesis artifact
elif global_memory["synthesis_archive"]:
    latest_synthesis = global_memory["synthesis_archive"][-1]
