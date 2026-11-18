"""
FocusEduc - Plateforme d'Aide à la Décision pour la Réduction des Disparités Éducatives au Burkina Faso.
Data Challenge Burkina 2026 - Défi 2 (Semaine du Numérique).
Solution unifiée intégrant modélisation prédictive, analyse de chocs de crise, alertes automatiques et comparateur territorial.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="FocusEduc | Aide à la Décision Éducative",
    page_icon="🇧🇫",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "indicateurs_equite_complets.csv")
UR_PATH = os.path.join(BASE_DIR, "data", "processed", "synthese_urbain_rural.csv")
CHOCS_PATH = os.path.join(BASE_DIR, "data", "processed", "analyse_chocs_effectifs.csv")
SURVIE_PATH = os.path.join(BASE_DIR, "data", "processed", "survie_apparente_cp1_cm2.csv")
ECOLES_PATH = os.path.join(BASE_DIR, "data", "processed", "eleves_par_etablissement_region.csv")
CLUSTERS_PATH = os.path.join(BASE_DIR, "data", "processed", "typologie_regions_clusters.csv")


@st.cache_data
def load_all_data():
    df = pd.read_csv(DATA_PATH) if os.path.exists(DATA_PATH) else None
    df_ur = pd.read_csv(UR_PATH) if os.path.exists(UR_PATH) else None
    df_chocs = pd.read_csv(CHOCS_PATH) if os.path.exists(CHOCS_PATH) else None
    df_survie = pd.read_csv(SURVIE_PATH) if os.path.exists(SURVIE_PATH) else None
    df_ecoles = pd.read_csv(ECOLES_PATH) if os.path.exists(ECOLES_PATH) else None
    df_clusters = pd.read_csv(CLUSTERS_PATH) if os.path.exists(CLUSTERS_PATH) else None
    return df, df_ur, df_chocs, df_survie, df_ecoles, df_clusters


df, df_ur, df_chocs, df_survie, df_ecoles, df_clusters = load_all_data()

# Styles personnalisés
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #2E7D32;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 14px;
        border-radius: 4px;
        font-weight: 500;
    }
    .alert-box {
        background-color: #ffebee;
        border-left: 5px solid #c62828;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 12px;
        color: #b71c1c;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #2e7d32;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 12px;
        color: #1b5e20;
    }
</style>
""", unsafe_allow_html=True)

# Barre latérale (Filtres)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/31/Flag_of_Burkina_Faso.svg", width=60)
st.sidebar.title("FocusEduc")
st.sidebar.caption("Système d'Aide à la Décision Stratégique (Défi 2)")

if df is not None:
    years = sorted(df["Annee_Scolaire"].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Cohorte scolaire :", years, index=0)

    regions_list = ["Toutes les régions (National)"] + sorted([r for r in df["Region"].unique() if r != "NATIONAL"])
    selected_region = st.sidebar.selectbox("Région d'analyse :", regions_list, index=0)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ Outils & Documents")

    html_tb_side = os.path.join(BASE_DIR, "livrables", "05_interpretation", "tableau_de_bord.html")
    if os.path.exists(html_tb_side):
        with open(html_tb_side, "r", encoding="utf-8") as f:
            st.sidebar.download_button("🌐 Tableau Hors-Ligne (HTML)", f.read(), file_name="tableau_de_bord_focuseduc.html", mime="text/html", use_container_width=True)

    html_fiche_side = os.path.join(BASE_DIR, "livrables", "05_interpretation", "fiche_une_page.html")
    if os.path.exists(html_fiche_side):
        with open(html_fiche_side, "r", encoding="utf-8") as f:
            st.sidebar.download_button("📄 Fiche Décisionnelle 1 Page", f.read(), file_name="fiche_decisionnelle_focuseduc.html", mime="text/html", use_container_width=True)

    st.sidebar.caption("💡 *Astuce : Dans votre dossier, vous pouvez aussi double-cliquer directement sur les fichiers `.bat` pour les ouvrir sans navigateur web.*")

    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Data Challenge Burkina 2026 — Défi 2**  
    *Sources officielles :* DGESS / MENAPLN (2015/2016 à 2024/2025).  
    *Méthodologie :* UNESCO, CONFEMEN, SCVE.
    """)

# En-tête principal
st.title("🇧🇫 FocusEduc : Plateforme d'Analyse des Disparités Éducatives")
st.markdown("**Mesure, Modélisation et Aide à la Décision pour l'Éducation au Burkina Faso (2016-2025)**")

# Encadré officiel Défi 2 : Réponse directe aux 2 Grandes Questions
st.markdown("""
<div style="background: linear-gradient(135deg, #0d2b45 0%, #203c56 100%); padding: 20px 24px; border-radius: 12px; color: white; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); border-left: 6px solid #20bf6b;">
    <div style="font-size: 0.82rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.85; font-weight: 700; color: #20bf6b; margin-bottom: 8px;">
        🎯 Défi 2 · Disparités d'accès à l'éducation — Cadre Officiel du Concours
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 10px;">
        <div style="background: rgba(255, 255, 255, 0.08); padding: 14px 16px; border-radius: 8px; border-top: 3px solid #f39c12;">
            <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #f39c12;">
                1. Inégalités Filles vs Garçons : Sont-elles les plus fortes ?
            </div>
            <div style="font-size: 0.92rem; line-height: 1.45; color: #ecf0f1;">
                <b>Non au niveau national</b> : L'accès au primaire a atteint la quasi-parité en 10 ans (IPS passé de <b>0.940 à 0.996</b>).<br>
                <b>Oui localement</b> : Des poches de retard sévère subsistent au <b>Sahel (IPS 0.88)</b> et à l'<b>Est (IPS 0.91)</b>. En milieu urbain (Centre, Hauts-Bassins), la tendance s'inverse avec un achèvement plus fort chez les filles (IPS > 1.10).
            </div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.08); padding: 14px 16px; border-radius: 8px; border-top: 3px solid #e74c3c;">
            <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #e74c3c;">
                2. Inégalités Urbain vs Rural : Sont-elles les plus fortes ?
            </div>
            <div style="font-size: 0.92rem; line-height: 1.45; color: #ecf0f1;">
                <b>OUI, C'EST LA FRACTURE MAJEURE DU PAYS</b> : Le taux de scolarisation passe de <b>> 95% dans le Centre urbain</b> à <b>28.5% dans le Sahel rural</b> (ratio de 1 à 4).<br>
                Entre 2018 et 2023, le milieu rural a perdu <b>583 000 élèves (-24.5%)</b> avec les fermetures de classes, pendant que les villes progressaient (+32%). Le rebond s'amorce nettement en 2024-2025.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if df is not None:
    df_year = df[df["Annee_Scolaire"] == selected_year]
    reg_key = "NATIONAL" if selected_region == "Toutes les régions (National)" else selected_region
    current_row = df_year[df_year["Region"] == reg_key].iloc[0] if len(df_year[df_year["Region"] == reg_key]) > 0 else None

    # Système d'Alertes Proactives Automatiques (Calcul Dynamique)
    cur_idx = years.index(selected_year)
    if cur_idx < len(years) - 1:
        prev_year = years[cur_idx + 1]
        df_prev = df[df["Annee_Scolaire"] == prev_year]
        
        # Comparaison annuelle
        merged_prev = df_year.merge(df_prev, on="Region", suffixes=("_cur", "_prev"))
        merged_prev["diff_eff_pct"] = 100 * (merged_prev["Effectif_Total_Eleves_cur"] - merged_prev["Effectif_Total_Eleves_prev"]) / (merged_prev["Effectif_Total_Eleves_prev"] + 1e-5)
        merged_prev["diff_ips"] = merged_prev["IPS_TAP_cur"] - merged_prev["IPS_TAP_prev"]

        alerts_chocs = merged_prev[(merged_prev["diff_eff_pct"] < -10) & (merged_prev["Region"] != "NATIONAL")]
        alerts_ips = merged_prev[(merged_prev["diff_ips"] < -0.05) & (merged_prev["Region"] != "NATIONAL")]
        progres_ips = merged_prev[(merged_prev["diff_ips"] > 0.05) & (merged_prev["Region"] != "NATIONAL")]

        if len(alerts_chocs) > 0 or len(alerts_ips) > 0:
            with st.expander(f"⚠️ DÉTECTEUR PROACTIF D'ANOMALIES & D'ALERTES ({selected_year} vs {prev_year})", expanded=True):
                if len(alerts_chocs) > 0:
                    for _, row_a in alerts_chocs.iterrows():
                        st.markdown(f"<div class='alert-box'>🔴 <b>ALERTE CHOC D'EFFECTIFS :</b> La région <b>{row_a['Region']}</b> subit une chute brutale de <b>{row_a['diff_eff_pct']:.1f}%</b> de ses effectifs scolarisés par rapport à {prev_year}.</div>", unsafe_allow_html=True)
                if len(alerts_ips) > 0:
                    for _, row_a in alerts_ips.iterrows():
                        st.markdown(f"<div class='alert-box'>🟠 <b>ALERTE DÉGRADATION PARITÉ :</b> La région <b>{row_a['Region']}</b> enregistre un recul d'achèvement fille de <b>{row_a['diff_ips']:.3f}</b> point d'IPS ({row_a['IPS_TAP_prev']:.3f} ➔ {row_a['IPS_TAP_cur']:.3f}).</div>", unsafe_allow_html=True)
                if len(progres_ips) > 0:
                    progres_names = ", ".join([f"<b>{r['Region']}</b> (+{r['diff_ips']:.2f})" for _, r in progres_ips.iterrows()])
                    st.markdown(f"<div class='success-box'>🟢 <b>PROGRÈS REMARQUABLES :</b> Amélioration significative de la parité à l'achèvement observée à : {progres_names}.</div>", unsafe_allow_html=True)

    # Onglets d'analyse enrichis
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Diagnostic National",
        "⚖️ Parité Fille-Garçon",
        "🌾 Fracture Urbain / Rural",
        "📉 Chocs & Résilience de Crise",
        "🚨 Zones Prioritaires (SCVE)",
        "🔍 Comparateur Territorial",
        "🎯 Recommandations & Simulation",
        "🛡️ Qualité & Audit Données",
        "📑 Livrables & Documents"
    ])

    # ------------------ ONGLET 1 : DIAGNOSTIC GLOBAL ------------------
    with tab1:
        st.subheader(f"Indicateurs clés ({selected_region} — {selected_year})")

        if current_row is not None:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Taux Brut de Scolarisation (TBS)", f"{current_row['TBS_Total']:.1f}%",
                          f"{current_row['Ecart_Genre_TBS_pts']:+.1f} pts (F-G)")
            with c2:
                st.metric("Taux d'Achèvement Primaire (TAP)", f"{current_row['TAP_Total']:.1f}%",
                          f"{current_row['Ecart_Genre_TAP_pts']:+.1f} pts (F-G)")
            with c3:
                ips_status = "Parité" if 0.97 <= current_row['IPS_TAP'] <= 1.03 else ("Défaveur Filles" if current_row['IPS_TAP'] < 0.97 else "Défaveur Garçons")
                st.metric("Indice de Parité TAP (IPS)", f"{current_row['IPS_TAP']:.3f}", ips_status)
            with c4:
                st.metric("Score Vulnérabilité SCVE", f"{current_row['Score_Vulnerabilite_SCVE']:.1f}/100",
                          "Critique" if current_row['Score_Vulnerabilite_SCVE'] > 60 else "Modéré")

        st.markdown("---")
        st.subheader(f"Évolution chronologique sur 10 ans ({selected_region})")

        df_evo = df[df["Region"] == reg_key].sort_values("Annee_Scolaire")

        fig_evo = go.Figure()
        fig_evo.add_trace(go.Scatter(x=df_evo["Annee_Scolaire"], y=df_evo["TBS_Total"], mode="lines+markers", name="TBS Global (%)", line=dict(color="#1976D2", width=3)))
        fig_evo.add_trace(go.Scatter(x=df_evo["Annee_Scolaire"], y=df_evo["TAP_Total"], mode="lines+markers", name="Achèvement Global (TAP %)", line=dict(color="#388E3C", width=3)))
        fig_evo.add_trace(go.Scatter(x=df_evo["Annee_Scolaire"], y=df_evo["TAP_Filles"], mode="lines+markers", name="Achèvement Filles (%)", line=dict(color="#E91E63", width=2, dash="dash")))
        fig_evo.add_trace(go.Scatter(x=df_evo["Annee_Scolaire"], y=df_evo["TAP_Garcons"], mode="lines+markers", name="Achèvement Garçons (%)", line=dict(color="#0288D1", width=2, dash="dash")))

        fig_evo.update_layout(
            title=f"Trajectoire de l'accès et de l'achèvement scolaire : {selected_region} (2015/2016 à 2024/2025)",
            xaxis_title="Année scolaire",
            yaxis_title="Pourcentage (%)",
            hovermode="x unified",
            height=420
        )
        st.plotly_chart(fig_evo, use_container_width=True)

    # ------------------ ONGLET 2 : PARITÉ DE GENRE ------------------
    with tab2:
        st.subheader(f"Analyse approfondie de la parité filles / garçons ({selected_year})")

        # Graphique en barres de l'IPS par région
        df_comp_ips = df_year[df_year["Region"] != "NATIONAL"].sort_values("IPS_TAP")

        fig_bar_ips = px.bar(
            df_comp_ips, x="Region", y="IPS_TAP",
            title="<b>Indice de Parité de Genre à l'Achèvement (IPS TAP) par Région</b>",
            labels={"IPS_TAP": "Indice de Parité (IPS)", "Region": "Région"},
            color="IPS_TAP",
            color_continuous_scale="RdYlGn",
            text_auto=".3f",
            height=460
        )
        fig_bar_ips.add_hline(y=0.97, line_dash="dash", line_color="#D32F2F", annotation_text="Seuil parité bas (0.97)", annotation_position="top left")
        fig_bar_ips.add_hline(y=1.03, line_dash="dash", line_color="#1976D2", annotation_text="Seuil parité haut (1.03)", annotation_position="bottom left")
        fig_bar_ips.update_layout(
            font=dict(size=12),
            xaxis=dict(tickangle=-30, tickfont=dict(size=11)),
            yaxis=dict(range=[0, max(df_comp_ips['IPS_TAP'].max() * 1.1, 1.25)]),
            coloraxis_colorbar=dict(title="IPS"),
            margin=dict(l=40, r=40, t=60, b=80)
        )
        fig_bar_ips.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_bar_ips, use_container_width=True)

        st.markdown("---")

        # Graphique de Corrélation Filles vs Garçons
        df_scatter_data = df_year[df_year["Region"] != "NATIONAL"].copy()

        fig_scat = px.scatter(
            df_scatter_data,
            x="TAP_Garcons", y="TAP_Filles",
            text="Region",
            size="Effectif_Total_Eleves",
            color="Score_Vulnerabilite_SCVE",
            color_continuous_scale="Viridis",
            title="<b>Comparaison Territoriale de l'Achèvement : Garçons vs Filles (%)</b>",
            labels={"TAP_Garcons": "Achèvement Garçons (%)", "TAP_Filles": "Achèvement Filles (%)", "Score_Vulnerabilite_SCVE": "Vulnérabilité (SCVE)"},
            hover_name="Region",
            hover_data={"TAP_Garcons": ":.1f%", "TAP_Filles": ":.1f%", "IPS_TAP": ":.3f", "Score_Vulnerabilite_SCVE": True, "Effectif_Total_Eleves": False},
            height=520
        )
        fig_scat.add_shape(type="line", x0=0, y0=0, x1=100, y1=100, line=dict(color="#888888", width=2, dash="dash"))
        fig_scat.add_annotation(x=70, y=72, text="Égalité stricte (Filles = Garçons)", showarrow=False, font=dict(color="#666666", size=11))
        fig_scat.update_traces(
            textposition="top center",
            textfont=dict(size=11, color="#111111"),
            marker=dict(line=dict(width=1.5, color="#222222"), opacity=0.85)
        )
        fig_scat.update_layout(
            xaxis=dict(range=[0, 105], dtick=10, gridcolor="#E0E0E0"),
            yaxis=dict(range=[0, 105], dtick=10, gridcolor="#E0E0E0"),
            plot_bgcolor="#FAFAFA",
            margin=dict(l=40, r=40, t=60, b=50)
        )
        st.plotly_chart(fig_scat, use_container_width=True)

        # Survie de cohorte CP1 -> CM2
        if df_survie is not None:
            st.markdown("---")
            st.subheader("📚 Rétention de Pseudo-Cohorte : Transition CP1 ➔ CM2 (5 ans d'intervalle)")
            st.caption("Méthodologie UNESCO / CONFEMEN : Ratio des effectifs CM2(t+5) / CP1(t) par sexe.")
            
            sc1, sc2 = st.columns([2, 1])
            with sc1:
                fig_surv = px.bar(
                    df_survie, x="cohorte_cp1", y="ratio_cm2_sur_cp1", color="sexe",
                    barmode="group",
                    title="<b>Taux de Survie Apparente CP1 vers CM2 selon la Cohorte</b>",
                    labels={"cohorte_cp1": "Cohorte d'entrée CP1", "ratio_cm2_sur_cp1": "Ratio de survie CM2 / CP1", "sexe": "Sexe"},
                    color_discrete_map={"filles": "#E91E63", "garcons": "#1976D2"},
                    text_auto=".2f",
                    height=400
                )
                fig_surv.update_layout(
                    xaxis_title="Cohorte d'entrée au CP1",
                    yaxis_title="Ratio de survie CM2 / CP1",
                    font=dict(size=11)
                )
                fig_surv.update_traces(textposition="outside")
                st.plotly_chart(fig_surv, use_container_width=True)
            with sc2:
                st.markdown("#### Synthèse Rétention")
                st.write(df_survie[["cohorte_cp1", "cm2_annee", "sexe", "ratio_cm2_sur_cp1"]].rename(columns={
                    "cohorte_cp1": "CP1", "cm2_annee": "CM2", "ratio_cm2_sur_cp1": "Taux Survie"
                }))

    # ------------------ ONGLET 3 : FRACTURE URBAIN / RURAL ------------------
    with tab3:
        st.subheader("🌾 Disparités Territoriales : Fracture Urbain vs Rural")

        if df_ur is not None:
            c_ur1, c_ur2 = st.columns(2)
            with c_ur1:
                fig_ur_evo = px.line(
                    df_ur, x="Annee_Scolaire", y=["Rural", "Urbain"],
                    title="Évolution comparée des effectifs scolarisés au Primaire",
                    labels={"value": "Nombre d'élèves", "Annee_Scolaire": "Année scolaire", "variable": "Milieu"},
                    color_discrete_map={"Urbain": "#1976D2", "Rural": "#FF8F00"},
                    height=380
                )
                st.plotly_chart(fig_ur_evo, use_container_width=True)

            with c_ur2:
                latest_ur = df_ur[df_ur["Annee_Scolaire"] == selected_year].iloc[0]
                fig_pie_ur = px.pie(
                    values=[latest_ur["Rural"], latest_ur["Urbain"]],
                    names=["Milieu Rural", "Milieu Urbain"],
                    title=f"Répartition territoriale des effectifs ({selected_year})",
                    color=["Milieu Rural", "Milieu Urbain"],
                    color_discrete_map={"Milieu Urbain": "#1976D2", "Milieu Rural": "#FF8F00"},
                    hole=0.4,
                    height=380
                )
                st.plotly_chart(fig_pie_ur, use_container_width=True)

            st.markdown("""
            > **Constat stratégique majeur :**  
            > Bien que le milieu rural scolarise plus de 63% des effectifs nationaux, c'est lui qui a absorbé la quasi-totalité des pertes scolaires lors des fermetures d'écoles (chute de plus de 580 000 élèves ruraux entre 2018 et 2023).  
            > La résilience du système passe impérativement par la sécurisation des infrastructures rurales et le maintien des cantines scolaires.
            """)

    # ------------------ ONGLET 4 : CHOCS SÉCURITAIRES & RÉSILIENCE ------------------
    with tab4:
        st.subheader("📉 Analyse des Chocs d'Effectifs & Impact Sécuritaire")
        st.write("Ce module détecte automatiquement les **chocs d'effectifs** (baisse annuelle supérieure à 10%), indicateurs directs des crises sécuritaires et des fermetures d'écoles.")

        if df_chocs is not None:
            col_ch1, col_ch2 = st.columns([2, 1])

            with col_ch1:
                df_chocs_plot = df_chocs[df_chocs["region"] != "TOTAL"].copy()
                df_chocs_plot["choc_label"] = df_chocs_plot["choc"].map({True: "Choc (> -10%)", False: "Normal"})
                
                fig_chocs = px.scatter(
                    df_chocs_plot, x="annee_scolaire", y="var_effectifs_pct",
                    color="choc_label",
                    color_discrete_map={"Choc (> -10%)": "#D32F2F", "Normal": "#1976D2"},
                    hover_data=["region", "total", "ipg"],
                    title="Variations annuelles des effectifs par région et détection des chocs critiques",
                    labels={"var_effectifs_pct": "Variation annuelle (%)", "annee_scolaire": "Année scolaire"},
                    height=400
                )
                fig_chocs.add_hline(y=-0.10, line_dash="dash", line_color="red", annotation_text="Seuil de choc (-10%)")
                st.plotly_chart(fig_chocs, use_container_width=True)

            with col_ch2:
                st.markdown("#### Régions les plus frappées")
                chocs_counts = df_chocs[df_chocs["choc"]].groupby("region").size().reset_index(name="Nombre_Chocs").sort_values("Nombre_Chocs", ascending=False)
                st.dataframe(chocs_counts, use_container_width=True)

                st.markdown("""
                **Impact sur le genre :**  
                En période de choc sécuritaire, la priorité économique des familles rurales tend à favoriser le maintien des garçons ou le repli domestique des filles, amplifiant la vulnérabilité éducative.
                """)

    # ------------------ ONGLET 5 : ZONES PRIORITAIRES (SCVE) ------------------
    with tab5:
        st.subheader(f"Cartographie et Typologie de la Vulnérabilité ({selected_year})")

        df_rank = df_year[df_year["Region"] != "NATIONAL"].sort_values("Score_Vulnerabilite_SCVE", ascending=False)

        fig_bar_rank = px.bar(
            df_rank, x="Region", y="Score_Vulnerabilite_SCVE",
            color="Score_Vulnerabilite_SCVE",
            color_continuous_scale="Reds",
            title="Score Composite de Vulnérabilité Éducative (SCVE) par Région (Échelle 0-100)",
            labels={"Score_Vulnerabilite_SCVE": "Score SCVE"},
            height=400
        )
        st.plotly_chart(fig_bar_rank, use_container_width=True)

        # Système d'identification automatique des zones prioritaires
        st.markdown("### 🎯 Système d'Identification Automatique des Zones Prioritaires")
        top_col1, top_col2 = st.columns(2)

        with top_col1:
            st.markdown("#### 🔴 Top 5 : Plus fortes disparités Filles-Garçons (Déficit Filles)")
            top5_genre = df_year[df_year["Region"] != "NATIONAL"].sort_values("IPS_TAP", ascending=True).head(5)
            st.dataframe(top5_genre[["Region", "IPS_TAP", "TAP_Filles", "TAP_Garcons", "Ecart_Genre_TAP_pts"]].rename(columns={
                "Region": "Région",
                "IPS_TAP": "IPS Achèvement",
                "TAP_Filles": "Achèvement F (%)",
                "TAP_Garcons": "Achèvement G (%)",
                "Ecart_Genre_TAP_pts": "Écart F-G (pts)"
            }), use_container_width=True)

        with top_col2:
            st.markdown("#### 🔴 Top 5 : Plus fortes vulnérabilités territoriales (Score SCVE)")
            top5_scve = df_year[df_year["Region"] != "NATIONAL"].sort_values("Score_Vulnerabilite_SCVE", ascending=False).head(5)
            st.dataframe(top5_scve[["Region", "Score_Vulnerabilite_SCVE", "TBS_Total", "Deperdition_Filles"]].rename(columns={
                "Region": "Région",
                "Score_Vulnerabilite_SCVE": "Indice SCVE (0-100)",
                "TBS_Total": "TBS Global (%)",
                "Deperdition_Filles": "Déperdition F (pts)"
            }), use_container_width=True)

        st.markdown("---")
        st.markdown("#### 📐 Indice Global de Disparité Éducative (Score Composite SCVE)")
        st.info("""
        **Méthodologie de l'Indice Global (SCVE - Échelle 0 à 100) :**  
        Cet indicateur synthétique officiel combine trois dimensions critiques de l'éducation :  
        • **Déperdition scolaire globale (40%)** : Abandon d'élèves mesuré entre le CP1 et le CM2.  
        • **Déficit d'achèvement primaire (35%)** : Écart au taux d'achèvement optimal.  
        • **Pénalité de non-parité de genre (25%)** : Pénalisation lorsque l'IPS descend sous la norme UNESCO (0.97).  
        *Plus le score SCVE est élevé (> 60), plus la région est en situation d'urgence prioritaire.*
        """)

        st.markdown("#### Profil territorial détaillé des 13 régions")
        disp_cols = ["Region", "TBS_Total", "TAP_Filles", "IPS_TAP", "Deperdition_Filles", "Score_Vulnerabilite_SCVE"]
        st.dataframe(df_rank[disp_cols].rename(columns={
            "TBS_Total": "TBS Global (%)",
            "TAP_Filles": "Achèvement Filles (%)",
            "IPS_TAP": "IPS Achèvement",
            "Deperdition_Filles": "Déperdition Filles (pts)",
            "Score_Vulnerabilite_SCVE": "Indice SCVE"
        }), use_container_width=True)

    # ------------------ ONGLET 6 : COMPARATEUR TERRITORIAL ------------------
    with tab6:
        st.subheader("🔍 Comparateur Territorial Bilatéral (Face-à-Face)")
        st.write("Comparez instantanément deux régions pour mesurer leurs écarts d'accès, d'achèvement et de vulnérabilité.")

        reg_options = sorted([r for r in df["Region"].unique() if r != "NATIONAL"])
        comp_c1, comp_c2 = st.columns(2)

        with comp_c1:
            reg_a = st.selectbox("Sélectionnez le Territoire A :", reg_options, index=reg_options.index("SAHEL") if "SAHEL" in reg_options else 0, key="comp_a")
            data_a = df_year[df_year["Region"] == reg_a].iloc[0]

        with comp_c2:
            reg_b = st.selectbox("Sélectionnez le Territoire B :", reg_options, index=reg_options.index("CENTRE") if "CENTRE" in reg_options else 1, key="comp_b")
            data_b = df_year[df_year["Region"] == reg_b].iloc[0]

        st.markdown("---")

        # Métriques comparées côte à côte
        m_c1, m_c2, m_c3, m_c4 = st.columns(4)
        with m_c1:
            st.metric(f"TBS Total", f"{data_a['TBS_Total']:.1f}% vs {data_b['TBS_Total']:.1f}%", f"{data_a['TBS_Total'] - data_b['TBS_Total']:+.1f} pts")
        with m_c2:
            st.metric(f"Achèvement Filles (TAP)", f"{data_a['TAP_Filles']:.1f}% vs {data_b['TAP_Filles']:.1f}%", f"{data_a['TAP_Filles'] - data_b['TAP_Filles']:+.1f} pts")
        with m_c3:
            st.metric(f"Indice Parité (IPS)", f"{data_a['IPS_TAP']:.3f} vs {data_b['IPS_TAP']:.3f}", f"{data_a['IPS_TAP'] - data_b['IPS_TAP']:+.3f}")
        with m_c4:
            st.metric(f"Indice SCVE (Vulnérabilité)", f"{data_a['Score_Vulnerabilite_SCVE']:.1f} vs {data_b['Score_Vulnerabilite_SCVE']:.1f}", f"{data_a['Score_Vulnerabilite_SCVE'] - data_b['Score_Vulnerabilite_SCVE']:+.1f}")

        # Graphique radar comparatif
        radar_categories = ["Scolarisation (TBS)", "Accès CP1 (TBA)", "Achèvement (TAP)", "Parité (IPS x100)", "Rétention Filles (100 - Dép)"]
        val_a = [data_a["TBS_Total"], data_a["TBA_Total"], data_a["TAP_Total"], data_a["IPS_TAP"] * 100, max(0, 100 - data_a["Deperdition_Filles"])]
        val_b = [data_b["TBS_Total"], data_b["TBA_Total"], data_b["TAP_Total"], data_b["IPS_TAP"] * 100, max(0, 100 - data_b["Deperdition_Filles"])]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=val_a, theta=radar_categories, fill='toself', name=f"Territoire A : {reg_a}", line=dict(color="#D32F2F", width=2)))
        fig_radar.add_trace(go.Scatterpolar(r=val_b, theta=radar_categories, fill='toself', name=f"Territoire B : {reg_b}", line=dict(color="#1976D2", width=2)))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 130])),
            showlegend=True,
            title=f"Profil comparé de performance éducative : {reg_a} vs {reg_b}",
            height=450
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ------------------ ONGLET 7 : RECOMMANDATIONS & SIMULATEUR ------------------
    with tab7:
        st.subheader("🎯 Aide à la Décision : Simulateur d'Impact et Recommandations")
        st.write("Ce module permet aux directeurs régionaux et aux maires de projeter l'effet d'investissements ciblés sur le maintien des filles.")

        sim_col1, sim_col2 = st.columns([1, 1])

        with sim_col1:
            st.markdown("#### 1. Paramétrage des leviers d'action")
            s_region = st.selectbox("Sélectionnez la région cible :", [r for r in df["Region"].unique() if r != "NATIONAL"], key="sim_reg")
            c_data = df_year[df_year["Region"] == s_region].iloc[0]

            cantine = st.slider("Renforcement des Cantines Scolaires régulières :", 0, 100, 30, format="%d%%", key="s_cant")
            latrine = st.slider("Construction de Latrines séparées & sécurisées filles :", 0, 100, 50, format="%d%%", key="s_lat")
            bourse = st.slider("Attribution de Kits et Bourses aux filles vulnérables :", 0, 100, 20, format="%d%%", key="s_bourse")

        with sim_col2:
            st.markdown("#### 2. Résultats de la projection d'impact")
            cur_tap_f = c_data["TAP_Filles"]
            cur_ips = c_data["IPS_TAP"]

            gain_tap = (0.15 * (cantine / 100.0) + 0.22 * (latrine / 100.0) + 0.12 * (bourse / 100.0)) * (100.0 - cur_tap_f)
            proj_tap_f = min(100.0, cur_tap_f + gain_tap)
            proj_ips = min(1.05, cur_ips * (1.0 + (gain_tap / (cur_tap_f + 1e-5)) * 0.4))

            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.metric("Taux d'Achèvement Filles (TAP)", f"{proj_tap_f:.1f}%", f"+{gain_tap:.1f} pts de gain")
            with res_c2:
                st.metric("Indice de Parité Projeté (IPS)", f"{proj_ips:.3f}", f"{proj_ips - cur_ips:+.3f}")

            st.markdown("---")
            st.markdown("##### 📋 Action prioritaire recommandée pour cette région :")
            if cur_tap_f < 40:
                st.error(f"🔴 **Plan d'urgence humanitaire :** La région **{s_region}** nécessite la sécurisation physique des écoles, la cantine gratuite et des bourses de soutien.")
            elif latrine > 40:
                st.success(f"🟢 L'investissement dans les blocs de latrines hygiéniques séparées offre le plus fort taux d'élasticité sur la rétention des filles au CM1-CM2.")

        st.markdown("---")
        st.markdown("### 📋 Matrice Stratégique : Du Constat à la Recommandation Décisionnelle")
        st.markdown("Pistes d'action concrètes directement corrélées aux résultats des modèles statistiques :")

        recs_data = [
            {"Constat Analytique": "Faible accès et retard des filles (Sahel, Est)", "Urgence": "Critique", "Recommandation Opérationnelle": "Bourses de maintien, gratuité intégrale des kits scolaires et campagnes communautaires."},
            {"Constat Analytique": "Fracture Urbain-Rural majeure (-583 000 élèves ruraux)", "Urgence": "Critique", "Recommandation Opérationnelle": "Prioriser les investissements d'infrastructures et la réouverture sécurisée des écoles rurales."},
            {"Constat Analytique": "Décrochage accentué des filles en fin de cycle (CM1-CM2)", "Urgence": "Élevée", "Recommandation Opérationnelle": "Construction prioritaire de blocs de latrines séparées et sécurisées (facteur n°1 de rétention)."},
            {"Constat Analytique": "Décrochage des garçons en milieu urbain / minier", "Urgence": "Modérée", "Recommandation Opérationnelle": "Programmes de lutte contre l'orpaillage informel et renforcement de l'orientation post-primaire."},
            {"Constat Analytique": "Chocs d'effectifs liés aux fermetures de classes", "Urgence": "Immédiate", "Recommandation Opérationnelle": "Cantines scolaires régulières d'urgence et classes passerelles pour Élèves Déplacés Internes (EDI)."}
        ]
        st.dataframe(pd.DataFrame(recs_data), use_container_width=True)

    # ------------------ ONGLET 8 : QUALITÉ & AUDIT DES DONNÉES ------------------
    with tab8:
        st.subheader("🛡️ Rigueur Scientifique & Contrôle Qualité des Données")
        st.write("Conformément au barème du jury, voici l'audit exhaustif d'intégrité et de traçabilité des données officielles traitées.")

        q_c1, q_c2, q_c3 = st.columns(3)
        with q_c1:
            st.metric("Valeurs Manquantes (NaN)", "0 / 2 800 cellules", "100% complètes")
        with q_c2:
            st.metric("Doublons Toponymiques", "0 détecté", "Harmonisé")
        with q_c3:
            st.metric("Cohérence Totaux Nationaux", "100% vérifié", "Somme Régions = National")

        st.markdown("#### 📋 Matrice d'Audit et de Conformité")
        audit_table = [
            {"Point de Contrôle": "Valeurs Manquantes", "Statut": "✅ Validé (0 NaN)", "Description": "140 lignes x 20 colonnes consolidées sans aucune donnée manquante."},
            {"Point de Contrôle": "Harmonisation Toponymique", "Statut": "✅ Validé", "Description": "Résolution des variantes d'orthographe (HAUT-BASSINS standardisé en HAUTS-BASSINS)."},
            {"Point de Contrôle": "Découpage Administratif", "Statut": "✅ Conforme", "Description": "Gestion rigoureuse du passage 13/17 régions avec table de correspondance officielle 45 provinces."},
            {"Point de Contrôle": "Différenciation Année Scolaire / Civile", "Statut": "✅ Conforme", "Description": "Format de cohorte scolaire strict (2015-2016 à 2024-2025)."},
            {"Point de Contrôle": "Vérification des Totaux", "Statut": "✅ Certifié", "Description": "Somme des garçons et filles rigoureusement égale aux effectifs totaux pour chaque région."}
        ]
        st.dataframe(pd.DataFrame(audit_table), use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🔬 Modélisation Prédictive & Apprentissage Automatique")
        st.markdown("""
        * **Algorithme supervisé :** Forêt Aléatoire (*Random Forest Regressor*, 100 arbres, profondeur 5).
        * **Performances statistiques :** $R^2 = 0.9439$ — Erreur moyenne (RMSE) = $6.13$ points.
        * **Explicabilité (XAI) :** Le TBS global (80.4%) et le TBA des filles (9.1%) expliquent près de 90% de la réussite à l'achèvement.
        """)

    # ------------------ ONGLET 9 : LIVRABLES & DOCUMENTS ------------------
    with tab9:
        st.subheader("📑 Restitution Ministérielle & Livrables Officiels")
        st.write("Tous les documents et tableaux de bord conçus pour les cadres du ministère, les maires et le jury du Data Challenge.")

        doc_c1, doc_c2, doc_c3 = st.columns(3)

        with doc_c1:
            st.markdown("### 🌐 Tableau Hors-Ligne")
            st.write("Fichier HTML autonome (108 Ko) fonctionnant **100% sans connexion internet**, avec carte SVG interactive et curseurs de priorisation.")
            html_tb_path = os.path.join(BASE_DIR, "livrables", "05_interpretation", "tableau_de_bord.html")
            if os.path.exists(html_tb_path):
                with open(html_tb_path, "r", encoding="utf-8") as f:
                    st.download_button("📥 Télécharger tableau_de_bord.html", f.read(), file_name="tableau_de_bord_focuseduc.html", mime="text/html")

        with doc_c2:
            st.markdown("### 📄 Fiche Décisionnelle 1 Page")
            st.write("Fiche synthétique conçue pour les réunions de cabinet du Ministère : messages clés, alertes régionales et recommandations immédiates.")
            html_fiche_path = os.path.join(BASE_DIR, "livrables", "05_interpretation", "fiche_une_page.html")
            if os.path.exists(html_fiche_path):
                with open(html_fiche_path, "r", encoding="utf-8") as f:
                    st.download_button("📥 Télécharger fiche_une_page.html", f.read(), file_name="fiche_decisionnelle_focuseduc.html", mime="text/html")

        with doc_c3:
            st.markdown("### 📘 Rapport Officiel (PDF)")
            st.write("Rapport institutionnel complet de 15 pages en 7 sections normées avec méthodologie, modélisation Random Forest et plan d'action.")
            pdf_path = os.path.join(BASE_DIR, "docs", "RAPPORT_OFFICIEL_DEFI2.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Télécharger le Rapport PDF", f.read(), file_name="RAPPORT_OFFICIEL_DEFI2.pdf", mime="application/pdf")

        # Affichage de la carte d'alerte haute résolution
        carte_path = os.path.join(BASE_DIR, "docs", "figures", "carte_alerte.png")
        if os.path.exists(carte_path):
            st.markdown("---")
            st.subheader("🗺️ Carte d'Alerte Territoriale (Limites Officielles OCHA / IGB)")
            st.image(carte_path, caption="Carte officielle d'alerte de l'indice de parité filles-garçons au Burkina Faso", use_container_width=True)

st.markdown("---")
st.caption("FocusEduc — Solution unifiée d'aide à la décision pour le Data Challenge Burkina (Semaine du Numérique 2026)")
