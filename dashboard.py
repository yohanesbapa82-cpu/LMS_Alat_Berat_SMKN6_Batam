"""dashboard.py — Dashboard modern untuk guru dan siswa"""
import streamlit as st
import pandas as pd
from database import (
    get_total_siswa, get_total_materi, get_total_soal,
    get_total_ujian, get_total_praktik,
    get_all_siswa, get_nilai_akhir,
    get_rata_nilai_teori, get_rata_nilai_praktik,
    get_siswa_ranking, get_aktivitas_terbaru,
    get_all_nilai_teori, get_all_nilai_praktik,
)
from utils import (
    page_header, bar_chart_nilai, get_predikat, get_grade_letter,
    format_tanggal, score_badge, format_tanggal_short
)


def render_dashboard():
    if st.session_state.role == "guru":
        render_dashboard_guru()
    else:
        render_dashboard_siswa()


# ─── GURU DASHBOARD ──────────────────────────────────────────────────────────

def render_dashboard_guru():
    page_header(
        "Dashboard Guru",
        f"Selamat datang, {st.session_state.nama_lengkap} | SMK Negeri 6 Batam — Teknik Alat Berat",
        "📊"
    )

    # ── KPI Cards ──
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        (c1, "👷 Total Siswa",    get_total_siswa(),   "siswa terdaftar"),
        (c2, "📚 Total Materi",   get_total_materi(),  "materi tersedia"),
        (c3, "❓ Bank Soal",      get_total_soal(),    "soal pilihan ganda"),
        (c4, "📝 Ujian Selesai",  get_total_ujian(),   "sesi ujian"),
        (c5, "🔧 Nilai Praktik",  get_total_praktik(), "penilaian praktik"),
    ]
    for col, label, val, sub in metrics:
        with col:
            st.metric(label, val, sub)

    st.divider()

    # ── Ranking & Aktivitas ──
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### 🏆 Ranking Nilai Akhir Siswa")
        ranking = get_siswa_ranking()
        if not ranking:
            st.info("Belum ada data nilai.")
        else:
            # Chart
            chart_data = {r["nama"].split()[0] + " " + (r["nama"].split()[1][:1] + ".") if len(r["nama"].split()) > 1 else r["nama"]: r["nilai_akhir"] for r in ranking}
            bar_chart_nilai(chart_data, "Nilai Akhir per Siswa")

            # Tabel ranking
            st.markdown("#### 📋 Detail Ranking")
            for i, r in enumerate(ranking, 1):
                na = r["nilai_akhir"]
                medal = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else f"#{i}"))
                col_a, col_b, col_c, col_d = st.columns([0.5, 2.5, 1.5, 1.5])
                with col_a: st.markdown(f"**{medal}**")
                with col_b: st.markdown(f"**{r['nama']}** <br><small style='color:#718096'>{r.get('kelas','')}</small>", unsafe_allow_html=True)
                with col_c: st.progress(min(na/100, 1.0))
                with col_d: st.markdown(score_badge(na), unsafe_allow_html=True)

    with col_right:
        st.markdown("### 🕐 Aktivitas Terbaru")
        aktivitas = get_aktivitas_terbaru(8)
        if not aktivitas:
            st.info("Belum ada aktivitas.")
        else:
            for a in aktivitas:
                icon = "📝" if a["tipe"] == "Ujian" else "🔧"
                nilai = a["nilai"] or 0
                tgl = format_tanggal_short(a.get("tanggal",""))
                with st.container():
                    st.markdown(f"""
                    <div style="background:white;border-radius:10px;padding:10px 14px;
                                margin-bottom:8px;border-left:3px solid {'#3182CE' if a['tipe']=='Ujian' else '#38A169'};
                                box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div>
                                <span style="font-size:0.75rem;font-weight:600;
                                      color:{'#3182CE' if a['tipe']=='Ujian' else '#38A169'};">
                                    {icon} {a['tipe']}
                                </span><br>
                                <b style="font-size:0.85rem;">{a['nama_lengkap']}</b><br>
                                <span style="font-size:0.75rem;color:#718096;">{a['keterangan'][:40]}</span>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:1.2rem;font-weight:700;color:#FF6B35;">{nilai:.1f}</div>
                                <div style="font-size:0.7rem;color:#A0AEC0;">{tgl}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Summary Stats ──
    st.divider()
    st.markdown("### 📈 Ringkasan Performa Kelas")
    siswa_list = get_all_siswa()
    if siswa_list:
        data = []
        for s in siswa_list:
            rt = get_rata_nilai_teori(s["id"])
            rp = get_rata_nilai_praktik(s["id"])
            na = get_nilai_akhir(s["id"])
            data.append({
                "Nama": s["nama_lengkap"],
                "Kelas": s.get("kelas",""),
                "Teori": round(rt,1),
                "Praktik": round(rp,1),
                "Nilai Akhir": round(na,1),
                "Grade": get_grade_letter(na),
                "Predikat": get_predikat(na),
                "Status": "✅ Lulus" if na >= 75 else ("⚠️ Perlu Remedial" if na > 0 else "⏳ Belum Dinilai"),
            })
        df = pd.DataFrame(data).sort_values("Nilai Akhir", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Export
        st.download_button(
            "📥 Export ke CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            "nilai_siswa.csv", "text/csv"
        )


# ─── SISWA DASHBOARD ─────────────────────────────────────────────────────────

def render_dashboard_siswa():
    page_header(
        f"Dashboard — {st.session_state.nama_lengkap}",
        "Pantau perkembangan belajarmu di sini",
        "📊"
    )

    siswa_id = st.session_state.user_id
    rt  = get_rata_nilai_teori(siswa_id)
    rp  = get_rata_nilai_praktik(siswa_id)
    na  = get_nilai_akhir(siswa_id)

    # ── KPI ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📝 Nilai Teori", f"{rt:.1f}", f"({get_grade_letter(rt)})")
    with c2:
        st.metric("🔧 Nilai Praktik", f"{rp:.1f}", f"({get_grade_letter(rp)})")
    with c3:
        st.metric("🎯 Nilai Akhir", f"{na:.1f}", f"({get_grade_letter(na)})")
    with c4:
        status = "✅ LULUS" if na >= 75 else ("⚠️ REMEDIAL" if na > 0 else "⏳ BELUM")
        st.metric("📋 Status", status)

    # ── Visual progress ──
    st.divider()
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown("### 📈 Progres Nilai")
        st.markdown("**Teori (30%)**")
        st.progress(min(rt/100, 1.0))
        st.caption(f"{rt:.1f}/100 — {get_predikat(rt)}")

        st.markdown("**Praktik (70%)**")
        st.progress(min(rp/100, 1.0))
        st.caption(f"{rp:.1f}/100 — {get_predikat(rp)}")

        st.markdown("**Nilai Akhir**")
        st.progress(min(na/100, 1.0))
        st.caption(f"{na:.1f}/100 — {get_predikat(na)}")

        # Status box
        if na >= 75:
            st.success("🎉 **Selamat!** Nilai Anda sudah memenuhi KKM (75). Pertahankan!")
        elif na >= 60:
            st.warning("⚠️ Nilai sudah cukup, tapi masih perlu ditingkatkan untuk mencapai KKM.")
        elif na > 0:
            st.error("❌ Nilai belum memenuhi KKM. Pelajari lagi materi dan hubungi guru.")
        else:
            st.info("ℹ️ Kerjakan ujian dan ikuti penilaian praktik untuk melihat nilaimu!")

    with col_b:
        st.markdown("### 🧮 Kalkulasi Nilai")
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:1.2rem;
                    box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <table style="width:100%;font-size:0.85rem;">
                <tr style="border-bottom:1px solid #E2E8F0;">
                    <td style="padding:6px 0;color:#4A5568;">Teori × 30%</td>
                    <td style="text-align:right;font-weight:600;color:#3182CE;">{rt*0.3:.1f}</td>
                </tr>
                <tr style="border-bottom:1px solid #E2E8F0;">
                    <td style="padding:6px 0;color:#4A5568;">Praktik × 70%</td>
                    <td style="text-align:right;font-weight:600;color:#38A169;">{rp*0.7:.1f}</td>
                </tr>
                <tr>
                    <td style="padding:8px 0;font-weight:700;color:#1A365D;">Nilai Akhir</td>
                    <td style="text-align:right;font-size:1.3rem;font-weight:700;color:#FF6B35;">{na:.1f}</td>
                </tr>
            </table>
            <div style="text-align:center;margin-top:0.8rem;padding:6px;
                        background:{'#C6F6D5' if na>=75 else '#FED7D7'};border-radius:6px;">
                <b style="color:{'#276749' if na>=75 else '#822727'};">
                    {'✅ LULUS' if na >= 75 else '❌ BELUM LULUS'} — KKM: 75
                </b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏅 Grade")
        grade = get_grade_letter(na)
        color_map = {"A":"#276749","B":"#2C5282","C":"#7B341E","D":"#7B341E","E":"#822727"}
        bg_map    = {"A":"#C6F6D5","B":"#BEE3F8","C":"#FEEBC8","D":"#FEB2B2","E":"#FED7D7"}
        st.markdown(f"""
        <div style="text-align:center;background:{bg_map.get(grade,'#F7FAFC')};
                    border-radius:12px;padding:1.5rem;">
            <div style="font-size:4rem;font-weight:800;color:{color_map.get(grade,'#1A365D')};">{grade}</div>
            <div style="color:{color_map.get(grade,'#718096')};font-weight:500;">{get_predikat(na)}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Riwayat ──
    st.divider()
    st.markdown("### 📋 Riwayat Ujian Terakhir")
    nilai_teori = get_all_nilai_teori()
    nilai_siswa = [n for n in nilai_teori if n.get("siswa_id") == siswa_id][:5]

    if not nilai_siswa:
        st.info("📝 Belum ada riwayat ujian. Kerjakan ujian di menu **Ujian**!")
    else:
        for n in nilai_siswa:
            s = n["skor"]
            icon = "✅" if s >= 75 else ("⚠️" if s >= 60 else "❌")
            st.markdown(f"""
            <div style="background:white;border-radius:8px;padding:10px 16px;margin-bottom:6px;
                        display:flex;justify-content:space-between;
                        box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                <span>📚 {n.get('materi_judul','')[:45]}</span>
                <span>{icon} <b>{s:.1f}</b> &nbsp;|&nbsp; <small style='color:#718096'>{format_tanggal_short(n.get('tanggal',''))}</small></span>
            </div>
            """, unsafe_allow_html=True)


# ─── STATISTIK PAGE ──────────────────────────────────────────────────────────

def render_statistik_page():
    page_header("Statistik Kelas", "Analisis performa seluruh siswa", "📈")

    siswa_list = get_all_siswa()
    if not siswa_list:
        st.info("Belum ada siswa.")
        return

    # Hitung data semua siswa
    data = []
    for s in siswa_list:
        rt, rp, na = get_rata_nilai_teori(s["id"]), get_rata_nilai_praktik(s["id"]), get_nilai_akhir(s["id"])
        data.append({"Nama": s["nama_lengkap"], "Kelas": s.get("kelas",""),
                     "Teori": round(rt,1), "Praktik": round(rp,1), "Nilai Akhir": round(na,1),
                     "Grade": get_grade_letter(na), "Status": "Lulus" if na >= 75 else ("Remedial" if na > 0 else "Belum")})
    df = pd.DataFrame(data).sort_values("Nilai Akhir", ascending=False)

    # Stats
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Total Siswa", len(df))
    with c2: st.metric("Rata-rata Nilai Akhir", f"{df['Nilai Akhir'].mean():.1f}")
    with c3: st.metric("Siswa Lulus", len(df[df['Status']=='Lulus']))
    with c4: st.metric("Nilai Tertinggi", f"{df['Nilai Akhir'].max():.1f}")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 Grafik","📋 Tabel","📥 Export"])

    with tab1:
        chart_data = dict(zip([n.split()[0] for n in df["Nama"]], df["Nilai Akhir"]))
        bar_chart_nilai(chart_data, "Distribusi Nilai Akhir Siswa")

        # Grafik perbandingan teori vs praktik
        st.markdown("#### ⚖️ Teori vs Praktik")
        import matplotlib.pyplot as plt, matplotlib
        matplotlib.use("Agg")
        fig, ax = plt.subplots(figsize=(10,4))
        x = range(len(df))
        w = 0.35
        ax.bar([i-w/2 for i in x], df["Teori"],   w, label="Teori (30%)",   color="#3182CE", alpha=0.85)
        ax.bar([i+w/2 for i in x], df["Praktik"], w, label="Praktik (70%)", color="#38A169", alpha=0.85)
        ax.axhline(75, color="#E53E3E", linestyle="--", linewidth=1.5, label="KKM 75")
        ax.set_xticks(list(x))
        ax.set_xticklabels([n.split()[0] for n in df["Nama"]], rotation=30, ha="right")
        ax.set_ylim(0, 105)
        ax.legend()
        ax.spines[["top","right"]].set_visible(False)
        ax.set_title("Perbandingan Nilai Teori vs Praktik", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tab2:
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Download CSV", df.to_csv(index=False).encode("utf-8-sig"),
                               "statistik_kelas.csv", "text/csv", use_container_width=True)
        with col2:
            try:
                import openpyxl, io
                buf = io.BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="Nilai Siswa")
                st.download_button("📊 Download Excel", buf.getvalue(),
                                   "statistik_kelas.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)
            except ImportError:
                st.info("Install openpyxl untuk export Excel.")
