"""auth.py — login, logout, session management"""
import streamlit as st
from database import verify_password, get_user_by_username, create_user

def init_session_state():
    defaults = {"user_id":None,"username":None,"nama_lengkap":None,"role":None,"logged_in":False}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def login_user(username, password):
    user = get_user_by_username(username)
    if user and verify_password(password, user["password"]):
        st.session_state.user_id      = user["id"]
        st.session_state.username     = user["username"]
        st.session_state.nama_lengkap = user["nama_lengkap"]
        st.session_state.role         = user["role"]
        st.session_state.logged_in    = True
        return True
    return False

def logout_user():
    for k in ["user_id","username","nama_lengkap","role","logged_in",
              "ujian_in_progress","ujian_soal_list","ujian_jawaban","ujian_materi_id"]:
        st.session_state[k] = None if k != "logged_in" else False
        if k in ["ujian_soal_list","ujian_jawaban"]:
            st.session_state[k] = [] if k == "ujian_soal_list" else {}

def isLoggedIn():   return st.session_state.get("logged_in", False)
def isGuru():       return st.session_state.get("role") == "guru"
def isSiswa():      return st.session_state.get("role") == "siswa"

def get_current_user():
    if isLoggedIn():
        return {k: st.session_state.get(k) for k in ["user_id","username","nama_lengkap","role"]}
    return None

def require_login():
    if not isLoggedIn():
        show_login_page()
        st.stop()

def require_role(required_role):
    require_login()
    if st.session_state.role != required_role:
        st.error("⛔ Anda tidak memiliki akses ke halaman ini!")
        st.stop()

def show_login_page():
    from utils import apply_custom_style
    apply_custom_style()

    # Hero section
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0F1F3D 0%,#1A365D 50%,#243B6E 100%);
                padding:3rem 2rem;border-radius:16px;text-align:center;margin-bottom:2rem;
                box-shadow:0 8px 32px rgba(15,31,61,0.4);">
        <div style="font-size:64px;margin-bottom:8px;">⚙️</div>
        <h1 style="color:#FF6B35;margin:0;font-size:2.2rem;font-weight:800;letter-spacing:-0.5px;">
            LMS Alat Berat
        </h1>
        <p style="color:#90CDF4;margin:8px 0 0;font-size:1rem;">
            Learning Management System<br>
            <b style="color:#FFB627;">SMK Negeri 6 Batam</b> — Teknik Alat Berat
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        with st.container():
            st.markdown("""
            <div style="background:white;border-radius:16px;padding:2rem;
                        box-shadow:0 4px 24px rgba(0,0,0,0.1);border:1px solid #E2E8F0;">
                <h3 style="text-align:center;color:#1A365D;margin-top:0;">🔐 Masuk ke Sistem</h3>
            </div>
            """, unsafe_allow_html=True)

            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("👤 Username", placeholder="Masukkan username Anda")
                password = st.text_input("🔒 Password", type="password", placeholder="Masukkan password")
                submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")

                if submitted:
                    if not username or not password:
                        st.warning("⚠️ Isi username dan password!")
                    elif login_user(username.strip(), password):
                        st.success(f"✅ Selamat datang, {st.session_state.nama_lengkap}!")
                        st.rerun()
                    else:
                        st.error("❌ Username atau password salah!")

        st.markdown("""
        <div style="background:#EBF8FF;border-radius:10px;padding:1rem;margin-top:1rem;
                    border-left:4px solid #3182CE;font-size:0.85rem;">
            <b>🔑 Cara Login:</b><br>
            👨‍🏫 <b>Guru</b> → username: nama depan (cth: <code>yohanes</code>, <code>andrew</code>)<br>
            👷 <b>Siswa</b> → username: NIS tanpa titik (cth: <code>244464</code>)<br>
            🔒 Password default: <code>guru123</code> (guru) / <code>siswa123</code> (siswa)
        </div>
        """, unsafe_allow_html=True)

def render_logout_button():
    if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
        logout_user()
        st.rerun()

def render_user_info():
    if not isLoggedIn(): return
    from database import get_user_by_id
    user_db = get_user_by_id(st.session_state.user_id) or {}
    role_label = "👨‍🏫 Guru" if st.session_state.role == "guru" else "👷 Siswa"
    nis_line   = f'<div style="font-size:0.72rem;color:#FFD700;">NIS: {user_db.get("nis","")}</div>' if st.session_state.role == "siswa" and user_db.get("nis") else ""
    kelas_line = f'<div style="font-size:0.72rem;color:#90CDF4;">{user_db.get("kelas","")}</div>' if user_db.get("kelas") else ""
    st.sidebar.markdown(f"""
    <div class="user-info-box">
        <div style="font-size:0.72rem;color:#90CDF4;margin-bottom:2px;">Logged in as</div>
        <div style="font-weight:600;font-size:0.88rem;line-height:1.3;">{st.session_state.nama_lengkap}</div>
        {nis_line}
        {kelas_line}
        <div style="font-size:0.72rem;color:#FFB627;margin-top:2px;">{role_label}</div>
    </div>
    """, unsafe_allow_html=True)

def render_user_management():
    """Manajemen user untuk guru."""
    if not isGuru():
        st.error("⛔ Hanya guru yang dapat mengakses fitur ini.")
        return
    from utils import page_header, show_success, show_error
    from database import get_all_users, delete_user, update_user_password
    page_header("Manajemen Pengguna", "Kelola akun guru & siswa SMK Negeri 6 Batam", "👥")

    tab1, tab2, tab3 = st.tabs(["📋 Daftar Pengguna", "➕ Tambah Pengguna", "🔑 Reset Password"])

    # ── Tab 1: Daftar ──────────────────────────────────────────────────────
    with tab1:
        import pandas as pd
        users = get_all_users()
        if not users:
            st.info("Belum ada data pengguna.")
        else:
            # Split guru & siswa
            guru_list  = [u for u in users if u["role"] == "guru"]
            siswa_list = [u for u in users if u["role"] == "siswa"]

            # Guru
            st.markdown(f"### 👨‍🏫 Daftar Guru ({len(guru_list)} orang)")
            df_guru = pd.DataFrame(guru_list)[["username","nama_lengkap","created_at"]]
            df_guru.columns = ["Username","Nama Lengkap","Tgl Daftar"]
            df_guru["Tgl Daftar"] = df_guru["Tgl Daftar"].apply(lambda x: str(x)[:10])
            st.dataframe(df_guru, use_container_width=True, hide_index=True)

            st.markdown(f"### 👷 Daftar Siswa ({len(siswa_list)} orang) — Kelas XI TAB")
            df_siswa = pd.DataFrame(siswa_list)[["nis","nama_lengkap","username","kelas","created_at"]]
            df_siswa.columns = ["NIS","Nama Lengkap","Username","Kelas","Tgl Daftar"]
            df_siswa["Tgl Daftar"] = df_siswa["Tgl Daftar"].apply(lambda x: str(x)[:10])
            st.dataframe(df_siswa, use_container_width=True, hide_index=True)

            # Export
            st.download_button(
                "📥 Export Daftar Siswa CSV",
                df_siswa.to_csv(index=False).encode("utf-8-sig"),
                "daftar_siswa_xi_tab.csv", "text/csv"
            )

    # ── Tab 2: Tambah ──────────────────────────────────────────────────────
    with tab2:
        with st.form("form_tambah_user", clear_on_submit=True):
            st.subheader("➕ Tambah Pengguna Baru")
            c1, c2 = st.columns(2)
            with c1:
                nama     = st.text_input("Nama Lengkap *")
                username = st.text_input("Username *", help="Untuk siswa gunakan NIS tanpa titik (contoh: 244464)")
                role     = st.selectbox("Role *", ["siswa", "guru"])
            with c2:
                nis      = st.text_input("NIS", placeholder="Contoh: 24.4.464 (kosongkan untuk guru)")
                kelas    = st.text_input("Kelas", placeholder="XI TAB")
                password = st.text_input("Password *", type="password", value="siswa123")
                konfirm  = st.text_input("Konfirmasi Password *", type="password", value="siswa123")
            save = st.form_submit_button("💾 Simpan", type="primary", use_container_width=True)
            if save:
                errs = []
                if not nama:     errs.append("Nama wajib diisi")
                if not username: errs.append("Username wajib diisi")
                if not password: errs.append("Password wajib diisi")
                if len(password) < 6: errs.append("Password min. 6 karakter")
                if password != konfirm: errs.append("Password tidak cocok")
                if errs:
                    for e in errs: st.error(f"❌ {e}")
                elif get_user_by_username(username):
                    st.error("❌ Username sudah digunakan!")
                else:
                    create_user(username.strip(), password, nama.strip(), role, kelas.strip(), nis.strip())
                    show_success(f"Pengguna **{nama}** berhasil ditambahkan! Username: `{username}` | Password: `{password}`")
                    st.rerun()

    # ── Tab 3: Reset Password ───────────────────────────────────────────────
    with tab3:
        st.subheader("🔑 Reset Password Pengguna")
        st.info("Gunakan fitur ini jika siswa/guru lupa password.")
        users = get_all_users()
        user_map = {f"[{u['role'].upper()}] {u['nama_lengkap']} ({u['username']})": u["id"]
                    for u in users}
        with st.form("form_reset_pw", clear_on_submit=True):
            selected = st.selectbox("Pilih Pengguna *", list(user_map.keys()))
            new_pw   = st.text_input("Password Baru *", type="password", placeholder="Min. 6 karakter")
            konfirm2 = st.text_input("Konfirmasi Password *", type="password")
            reset_btn = st.form_submit_button("🔄 Reset Password", type="primary", use_container_width=True)
            if reset_btn:
                if not new_pw or len(new_pw) < 6:
                    st.error("❌ Password minimal 6 karakter!")
                elif new_pw != konfirm2:
                    st.error("❌ Password tidak cocok!")
                else:
                    uid = user_map[selected]
                    if update_user_password(uid, new_pw):
                        show_success(f"Password berhasil direset! Password baru: `{new_pw}`")
                    else:
                        show_error("Gagal reset password.")
