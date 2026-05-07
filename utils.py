"""utils.py — styling, helpers, konstanta untuk LMS Alat Berat"""
import streamlit as st
from datetime import datetime

KATEGORI_OPTIONS = ["Engine", "Hydraulic", "Kelistrikan", "Unit Spesifik"]

MODUL_PRAKTIK_OPTIONS = [
    "Inspeksi Harian (10 Jam)",
    "Start-Up & Shut-Down Procedure",
    "Perawatan Sistem Hidrolik",
    "Perawatan Mesin Diesel",
    "Pengoperasian Excavator PC200",
    "Pengoperasian Forklift",
    "Pengoperasian Backhoe Loader 428",
    "Troubleshooting Engine",
    "Troubleshooting Hydraulic",
    "Pemeliharaan Sistem Kelistrikan",
    "Pemeriksaan Undercarriage",
]

# ─── CSS MODERN ──────────────────────────────────────────────────────────────

def apply_custom_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F1F3D 0%, #1A365D 60%, #243B6E 100%);
        border-right: 1px solid #2d4a7c;
    }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #CBD5E0 !important; }
    [data-testid="stSidebar"] hr { border-color: #2d4a7c !important; }

    /* ── Main Background ── */
    .stApp { background: #F0F4F8; }
    .main .block-container { padding: 1.5rem 2rem; max-width: 1200px; }

    /* ── Metric Cards ── */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-left: 4px solid #FF6B35;
        transition: transform .2s, box-shadow .2s;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    [data-testid="stMetricValue"] { font-size: 2rem !important; color: #FF6B35 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #4A5568 !important; font-weight: 500 !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35, #E55A2B);
        color: white !important; border: none;
        border-radius: 8px; font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: all .2s; box-shadow: 0 2px 6px rgba(255,107,53,0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #E55A2B, #CC4A1B);
        box-shadow: 0 4px 12px rgba(255,107,53,0.4);
        transform: translateY(-1px);
    }
    .stButton > button[kind="secondary"] {
        background: white !important; color: #FF6B35 !important;
        border: 2px solid #FF6B35 !important;
        box-shadow: none;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: white; border-radius: 10px;
        padding: 4px; gap: 4px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; padding: 0.5rem 1.2rem;
        color: #4A5568; font-weight: 500;
        transition: all .2s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B35, #E55A2B) !important;
        color: white !important;
    }

    /* ── Cards ── */
    .lms-card {
        background: white; border-radius: 12px;
        padding: 1.5rem; margin-bottom: 1rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.08);
        border: 1px solid #E2E8F0;
        transition: box-shadow .2s;
    }
    .lms-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }

    /* ── Stat Cards ── */
    .stat-card {
        background: white; border-radius: 14px;
        padding: 1.2rem 1.5rem; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #FF6B35;
    }
    .stat-number { font-size: 2.5rem; font-weight: 700; color: #FF6B35; line-height: 1; }
    .stat-label  { color: #718096; font-size: 0.85rem; font-weight: 500; margin-top: 4px; }

    /* ── Score Badge ── */
    .score-excellent { color: #276749; background: #C6F6D5; padding: 3px 10px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .score-good      { color: #7B341E; background: #FEEBC8; padding: 3px 10px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .score-fail      { color: #822727; background: #FED7D7; padding: 3px 10px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }

    /* ── Page Header ── */
    .page-header {
        background: linear-gradient(135deg, #1A365D 0%, #2D5A9E 100%);
        color: white; padding: 1.5rem 2rem; border-radius: 14px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(26,54,93,0.3);
    }
    .page-header h1 { color: white !important; margin: 0; font-size: 1.6rem; }
    .page-header p  { color: #BEE3F8; margin: 0; font-size: 0.9rem; }

    /* ── Form ── */
    .stTextInput input, .stTextArea textarea, .stSelectbox > div {
        border-radius: 8px !important; border-color: #CBD5E0 !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #FF6B35 !important; box-shadow: 0 0 0 3px rgba(255,107,53,0.15) !important;
    }

    /* ── Dataframe ── */
    .stDataFrame { border-radius: 10px; overflow: hidden; }

    /* ── Progress Bar ── */
    .stProgress .st-bo { background: linear-gradient(90deg, #FF6B35, #FFB627); border-radius: 99px; }

    /* ── Sidebar Nav ── */
    .sidebar-logo {
        text-align: center; padding: 1rem 0;
        border-bottom: 1px solid #2d4a7c; margin-bottom: 1rem;
    }
    .sidebar-logo h2 { color: #FF6B35 !important; font-size: 1.1rem; margin: 4px 0 0; }
    .sidebar-logo p  { color: #90CDF4 !important; font-size: 0.75rem; margin: 0; }

    .user-info-box {
        background: rgba(255,255,255,0.06); border-radius: 10px;
        padding: 0.8rem; margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: white !important; border-radius: 10px !important;
        font-weight: 600 !important; color: #1A365D !important;
    }

    /* ── Alert custom ── */
    div[data-baseweb="notification"] { border-radius: 10px !important; }

    /* ── Divider ── */
    hr { border-color: #E2E8F0 !important; }
    </style>
    """, unsafe_allow_html=True)


# ─── HELPERS ────────────────────────────────────────────────────────────────

def page_header(title, subtitle="", icon="⚙️"):
    st.markdown(f"""
    <div class="page-header">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def score_badge(nilai):
    if nilai >= 75:
        return f'<span class="score-excellent">✅ {nilai:.1f}</span>'
    elif nilai >= 60:
        return f'<span class="score-good">⚠️ {nilai:.1f}</span>'
    else:
        return f'<span class="score-fail">❌ {nilai:.1f}</span>'

def get_kategori_emoji(k):
    return {"Engine":"⚙️","Hydraulic":"🔧","Kelistrikan":"⚡","Unit Spesifik":"🚜"}.get(k,"📚")

def get_kategori_color(k):
    return {"Engine":"#FF6B35","Hydraulic":"#3182CE","Kelistrikan":"#D69E2E","Unit Spesifik":"#38A169"}.get(k,"#1A365D")

def format_tanggal_short(ts):
    if not ts: return "-"
    try:
        s = str(ts)
        dt = datetime.fromisoformat(s.replace("Z","+00:00").split(".")[0])
        return dt.strftime("%d/%m/%Y")
    except:
        return str(ts)[:10]

def format_tanggal(ts):
    if not ts: return "-"
    try:
        s = str(ts)
        dt = datetime.fromisoformat(s.replace("Z","+00:00").split(".")[0])
        return dt.strftime("%d %b %Y %H:%M")
    except:
        return str(ts)

def hitung_nilai_praktik(safety, prosedur, hasil):
    return round((safety * 0.30) + (prosedur * 0.30) + (hasil * 0.40), 2)

def hitung_nilai_akhir(teori, praktik):
    if teori == 0 and praktik == 0: return 0.0
    if teori == 0: return praktik
    if praktik == 0: return teori
    return round((teori * 0.30) + (praktik * 0.70), 2)

def get_predikat(nilai):
    if nilai >= 90: return "Sangat Baik"
    elif nilai >= 80: return "Baik"
    elif nilai >= 70: return "Cukup"
    elif nilai >= 60: return "Kurang"
    else: return "Sangat Kurang"

def get_grade_letter(nilai):
    if nilai >= 90: return "A"
    elif nilai >= 80: return "B"
    elif nilai >= 70: return "C"
    elif nilai >= 60: return "D"
    else: return "E"

def show_success(msg): st.success(f"✅ {msg}")
def show_error(msg):   st.error(f"❌ {msg}")
def show_warning(msg): st.warning(f"⚠️ {msg}")
def show_info(msg):    st.info(f"ℹ️ {msg}")

def bar_chart_nilai(data_dict, title="Grafik Nilai"):
    """Render simple bar chart dengan matplotlib."""
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use("Agg")
    if not data_dict: return
    fig, ax = plt.subplots(figsize=(max(6, len(data_dict)*1.2), 4))
    names  = list(data_dict.keys())
    values = list(data_dict.values())
    colors = ["#2ecc71" if v >= 75 else ("#f39c12" if v >= 60 else "#e74c3c") for v in values]
    bars = ax.bar(names, values, color=colors, edgecolor="white", linewidth=1.5, width=0.6)
    ax.axhline(y=75, color="#e74c3c", linestyle="--", linewidth=1.5, alpha=0.7, label="KKM (75)")
    ax.set_ylim(0, 105)
    ax.set_title(title, fontsize=13, fontweight="bold", color="#1A365D")
    ax.set_ylabel("Nilai")
    ax.legend(fontsize=9)
    ax.spines[["top","right"]].set_visible(False)
    ax.set_facecolor("#FAFAFA")
    fig.patch.set_facecolor("white")
    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f"{val:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    plt.xticks(rotation=30, ha="right", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
