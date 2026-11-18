"""
FocusEduc - Plateforme d'Aide à la Décision pour la Réduction des Disparités Éducatives au Burkina Faso.
Data Challenge Burkina 2026 - Défi 2 (Semaine du Numérique).
Solution unifiée intégrant modélisation prédictive, analyse de chocs de crise et restitution ministérielle.
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


@st.cache_data
def load_all_data():
    df = pd.read_csv(DATA_PATH) if os.path.exists(DATA_PATH) else None
    df_ur = pd.read_csv(UR_PATH) if os.path.exists(UR_PATH) else None
    df_chocs = pd.read_csv(CHOCS_PATH) if os.path.exists(CHOCS_PATH) else None
    df_survie = pd.read_csv(SURVIE_PATH) if os.path.exists(SURVIE_PATH) else None
    df_ecoles = pd.read_csv(ECOLES_PATH) if os.path.exists(ECOLES_PATH) else None
    return df, df_ur, df_chocs, df_survie, df_ecoles


df, df_ur, df_chocs, df_survie, df_ecoles = load_all_data()

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
        margin-bottom: 15px;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #2e7d32;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Barre latérale (Filtres)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/31/Flag_of_Burkina_Faso.svg", width=60)
st.sidebar.title("FocusEduc")
st.sidebar.caption("Système Décisionnel & Analytique Unifié (Défi 2)")

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
st.title("🇧🇫 FocusEduc : Système d'Aide à la Décision Éducative")
st.markdown("**Mesure, Modélisation et Réduction des Disparités Éducatives au Burkina Faso (2016-2025)**")

# Encadré officiel Défi 2 : Question centrale et Réponse directe dès l'entrée
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
    <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.85; font-weight: 600; margin-bottom: 6px;">
        🎯 Défi 2 · Disparités d'accès (Question officielle du concours)
    </div>
    <div style="font-size: 1.25rem; font-weight: 700; line-height: 1.4; margin-bottom: 12px;">
        « Où les écarts d'accès à l'école sont-ils les plus grands (filles-garçons, ville-campagne) et évoluent-ils ? »
    </div>
    <div style="background: rgba(255, 255, 255, 0.12); padding: 12px 16px; border-radius: 6px; font-size: 0.95rem; line-height: 1.5;">
        <b>Réponse synthétique issue des données officielles DGESS (2015-2025) :</b><br>
        • <b>Filles-Garçons :</b> Le retard d'accès des filles est maximal au <b>Sahel</b> (IPS = 0.88) et à l'<b>Est</b> (IPS = 0.91). À l'inverse, dans les pôles urbains (Centre, Hauts-Bassins), les filles complètent davantage le primaire que les garçons (IPS achèvement > 1.15). Au niveau national, l'écart s'est résorbé en 10 ans (IPS passé de 0.940 à 0.996).<br>
        • <b>Ville-Campagne :</b> C'est la fracture la plus profonde du pays. Le taux brut de scolarisation passe de <b>> 95% dans le Centre urbain</b> à <b>28.5% dans le Sahel rural</b> (ratio de 1 à 4). Entre 2018 et 2023, la crise a fait chuter les effectifs ruraux de <b>583 000 élèves (-24.5%)</b> pendant que les villes progressaient (+32%), avant un net rebond amorcé en 2024-2025.
    </div>
</div>
""", unsafe_allow_html=True)

if df is not None:
    df_year = df[df["Annee_Scolaire"] == selected_year]
    reg_key = "NATIONAL" if selected_region == "Toutes les régions (National)" else selected_region
    current_row = df_year[df_year["Region"] == reg_key].iloc[0] if len(df_year[df_year["Region"] == reg_key]) > 0 else None

    # Onglets d'analyse
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Diagnostic National",
        "⚖️ Parité Fille-Garçon",
        "🌾 Fracture Urbain / Rural",
        "📉 Chocs & Résilience de Crise",
        "🗺️ Typologie & Vulnérabilité",
        "🎯 Simulateur d'Impact (What-If)",
        "📑 Livrables & Restitution Ministérielle"
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

        # 1. Graphique en barres de l'IPS par région (Plein écran / grande largeur)
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

        # 2. Graphique de Corrélation Filles vs Garçons (Aéré et lisible)
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
        # Ligne d'égalité stricte 45 degrés
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

    # ------------------ ONGLET 5 : TYPOLOGIE & VULNÉRABILITÉ ------------------
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

        st.markdown("#### Profil territorial détaillé des 13 régions")
        disp_cols = ["Region", "TBS_Total", "TAP_Filles", "IPS_TAP", "Deperdition_Filles", "Score_Vulnerabilite_SCVE"]
        st.dataframe(df_rank[disp_cols].rename(columns={
            "TBS_Total": "TBS Global (%)",
            "TAP_Filles": "Achèvement Filles (%)",
            "IPS_TAP": "IPS Achèvement",
            "Deperdition_Filles": "Déperdition Filles (pts)",
            "Score_Vulnerabilite_SCVE": "Indice SCVE"
        }), use_container_width=True)

    # ------------------ ONGLET 6 : SIMULATEUR WHAT-IF ------------------
    with tab6:
        st.subheader("🎯 Simulateur d'Impact de Politiques Publiques (What-If)")
        st.write("Projeter l'impact d'interventions ciblées sur l'achèvement scolaire des filles et l'équité territoriale.")

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
            st.markdown("##### 📋 Recommandation opérationnelle générée :")
            if cur_tap_f < 40:
                st.error(f"🔴 **Priorité Urgente :** La région **{s_region}** nécessite un plan de choc associant sécurisation physique, gratuité de la cantine et kits de dignité.")
            elif latrine > 40:
                st.success(f"🟢 L'investissement dans les blocs de latrines séparées offre le plus fort taux d'élasticité sur la rétention des filles au CM1-CM2.")

    # ------------------ ONGLET 7 : RESTITUTION & DOCUMENTS ------------------
    with tab7:
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
