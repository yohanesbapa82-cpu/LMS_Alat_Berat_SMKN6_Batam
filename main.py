"""
main.py — Entry Point LMS Alat Berat
SMK Negeri 6 Batam — Teknik Alat Berat
Jalankan: streamlit run main.py
"""
import streamlit as st

# ── Page config HARUS di baris pertama ──────────────────────────────────────
st.set_page_config(
    page_title="LMS Alat Berat — SMK N 6 Batam",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Import setelah set_page_config ──────────────────────────────────────────
from database import init_database
from auth import (
    init_session_state, show_login_page, isLoggedIn, isGuru, isSiswa,
    render_user_info, render_logout_button, render_user_management
)
from utils import apply_custom_style
from dashboard import render_dashboard, render_statistik_page
from materi import render_materi_page, render_materi_siswa
from soal import render_soal_page
from ujian import render_ujian_page
from praktik import render_praktik_page
from nilai import render_nilai_page

# ── Bootstrap ────────────────────────────────────────────────────────────────
init_database()
init_session_state()
apply_custom_style()

# ── Gate: tampilkan login jika belum login ───────────────────────────────────
if not isLoggedIn():
    show_login_page()
    st.stop()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2.5rem;">⚙️</div>
        <h2>LMS Alat Berat</h2>
        <p>SMK Negeri 6 Batam</p>
    </div>
    """, unsafe_allow_html=True)

    render_user_info()
    st.markdown("")

    # ── Navigasi berdasarkan role ──
    if isGuru():
        st.markdown('<p style="color:#90CDF4;font-size:0.7rem;font-weight:600;letter-spacing:1px;margin:0 0 4px;">MENU UTAMA</p>', unsafe_allow_html=True)
        page = st.radio("", [
            "🏠  Dashboard",
            "📚  Materi",
            "❓  Bank Soal",
            "📝  Hasil Ujian",
            "🔧  Penilaian Praktik",
            "📊  Nilai Akhir",
            "📈  Statistik",
            "👥  Manajemen User",
        ], label_visibility="collapsed")
    else:
        st.markdown('<p style="color:#90CDF4;font-size:0.7rem;font-weight:600;letter-spacing:1px;margin:0 0 4px;">MENU SISWA</p>', unsafe_allow_html=True)
        page = st.radio("", [
            "🏠  Dashboard",
            "📚  Materi",
            "✏️  Ujian Online",
            "🔧  Nilai Praktik",
            "📊  Nilai Akhir",
        ], label_visibility="collapsed")

    st.markdown("---")
    render_logout_button()

    # Info versi
    st.markdown("""
    <div style="text-align:center;padding:0.5rem 0;color:#4A5568;font-size:0.7rem;">
        v2.0 · Offline Ready · SMK N 6 Batam<br>
        <span style="color:#2d4a7c;">Program Keahlian Teknik Alat Berat</span>
    </div>
    """, unsafe_allow_html=True)

# ── Main content router ──────────────────────────────────────────────────────
page_clean = page.strip()

if isGuru():
    if   "Dashboard"        in page_clean: render_dashboard()
    elif "Materi"           in page_clean: render_materi_page()
    elif "Bank Soal"        in page_clean: render_soal_page()
    elif "Hasil Ujian"      in page_clean: render_ujian_page()
    elif "Penilaian Praktik"in page_clean: render_praktik_page()
    elif "Nilai Akhir"      in page_clean: render_nilai_page()
    elif "Statistik"        in page_clean: render_statistik_page()
    elif "Manajemen User"   in page_clean: render_user_management()
else:
    if   "Dashboard"        in page_clean: render_dashboard()
    elif "Materi"           in page_clean: render_materi_siswa()
    elif "Ujian Online"     in page_clean: render_ujian_page()
    elif "Nilai Praktik"    in page_clean: render_praktik_page()
    elif "Nilai Akhir"      in page_clean: render_nilai_page()
