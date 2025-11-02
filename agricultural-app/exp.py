import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Configuration de la page
st.set_page_config(
    page_title="Expérimentation Agricole - Apprentissage",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Soundous5//agricultural-experiment-app/agricultural-app',
        'Report a bug': "https://github.com/Soundous5//agricultural-experiment-app/agricultural-app/issues",
        'About': "# Agricultural Experimentation Learning App\nVersion 1.0"
    }
)

# Mobile detection and optimization
def is_mobile():
    """Detect if user is on mobile device"""
    try:
        return st.session_state.get('mobile_device', False)
    except:
        return False

# Add custom CSS for mobile responsiveness
st.markdown("""
<style>
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            font-size: 16px;
            padding: 12px;
        }
        .stNumberInput input {
            font-size: 16px;
        }
        .stSelectbox select {
            font-size: 16px;
        }
        input, select, textarea {
            font-size: 16px !important;
        }
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.title("🌱 Apprentissage de l'Expérimentation Agricole")
st.subheader("Comprendre chaque étape avant le calcul de F")

# Sidebar pour navigation
st.sidebar.title("Étapes d'apprentissage")
etape = st.sidebar.selectbox(
    "Choisissez l'étape :",
    [
        "1. Choix du dispositif",
        "2. Saisie des données",
        "3. Calcul des DDL",
        "4. Calcul des sommes de carrés",
        "5. Calcul des carrés moyens",
        "6. Calcul du F",
        "7. Comparaison F théorique",
        "8. Interprétation"
    ]
)

# Initialisation des variables de session
if 'dispositif' not in st.session_state:
    st.session_state.dispositif = None
if 'donnees' not in st.session_state:
    st.session_state.donnees = None
if 'ddl_calculated' not in st.session_state:
    st.session_state.ddl_calculated = False

# Étape 1: Choix du dispositif
if etape == "1. Choix du dispositif":
    st.header("📋 Étape 1: Comprendre et choisir le dispositif expérimental")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Dispositifs disponibles :")
        dispositif_choisi = st.radio(
            "Sélectionnez votre dispositif :",
            [
                "Bloc Randomisé Complet (BRC)",
                "Carré Latin",
                "Dispositif en Split-plot"
            ]
        )
        st.session_state.dispositif = dispositif_choisi
    
    with col2:
        st.subheader("Pourquoi ce choix ?")
        if dispositif_choisi == "Bloc Randomisé Complet (BRC)":
            st.info("""
            **Bloc Randomisé Complet (BRC)**
            **Principe :** Contrôler une source de variation connue
            **Structure :**
            - Traitements répartis aléatoirement dans chaque bloc
            - Chaque traitement apparaît une fois par bloc

            **Sources de variation :**
            - Variation due aux traitements
            - Variation due aux blocs
            - Variation résiduelle (erreur)
            """)
        elif dispositif_choisi == "Carré Latin":
            st.info("""
            **Carré Latin**
            **Principe :** Contrôler deux sources de variation

            **Structure :**
            - Lignes et colonnes
            - Chaque traitement apparaît une fois par ligne et par colonne
            **Sources de variation :**
            - Variation due aux traitements
            - Variation due aux lignes
            - Variation due aux colonnes
            - Variation résiduelle
            """)
        else:
            st.info("""
            **Dispositif Split-plot**
            **Principe :** Deux facteurs avec précisions différentes
            **Structure :**
            - Parcelles principales (facteur A)
            - Sous-parcelles (facteur B)
            **Sources de variation :**
            - Variation facteur A
            - Variation facteur B
            - Interaction A×B
            - Erreurs principales et secondaires
            """)
    
    if st.button("✅ J'ai compris le principe, passer à l'étape suivante"):
        st.success("Dispositif sélectionné ! Passez à l'étape 2.")

# Étape 2: Saisie des données
elif etape == "2. Saisie des données":
    if st.session_state.dispositif is None:
        st.error("⚠️ Retournez à l'étape 1 pour choisir un dispositif !")
    else:
        st.header("📊 Étape 2: Saisie des données expérimentales")
        st.write(f"**Dispositif choisi :** {st.session_state.dispositif}")
        
        if st.session_state.dispositif == "Bloc Randomisé Complet (BRC)":
            col1, col2 = st.columns([1, 1])
            
            with col1:
                nb_traitements = st.number_input("Nombre de traitements", min_value=2, max_value=10, value=4)
                nb_blocs = st.number_input("Nombre de blocs", min_value=2, max_value=10, value=3)
            
            with col2:
                st.write("**Questions de réflexion :**")
                st.write("- Pourquoi utiliser plusieurs blocs ?")
                st.write("- Que représente chaque bloc dans votre expérience ?")
            
            st.subheader("Saisissez vos données :")
            
            donnees = []
            for b in range(nb_blocs):
                for t in range(nb_traitements):
                    donnees.append({
                        'Bloc': f'Bloc_{b+1}',
                        'Traitement': f'T{t+1}',
                        'Valeur': 0.0
                    })
            
            df_saisie = pd.DataFrame(donnees)
            
            st.write("**Tableau de saisie des données :**")
            
            donnees_saisies = {}
            for b in range(nb_blocs):
                st.write(f"**{df_saisie.iloc[b*nb_traitements]['Bloc']} :**")
                cols_bloc = st.columns(nb_traitements)
                for t in range(nb_traitements):
                    with cols_bloc[t]:
                        key = f"B{b+1}_T{t+1}"
                        donnees_saisies[key] = st.number_input(
                            f"T{t+1}", 
                            value=10.0 + np.random.normal(0, 2),
                            key=key,
                            step=0.1
                        )
            
            donnees_finales = []
            for b in range(nb_blocs):
                for t in range(nb_traitements):
                    donnees_finales.append({
                        'Bloc': b+1,
                        'Traitement': t+1,
                        'Valeur': donnees_saisies[f"B{b+1}_T{t+1}"]
                    })
            
            st.session_state.donnees = pd.DataFrame(donnees_finales)
            st.session_state.nb_traitements = nb_traitements
            st.session_state.nb_blocs = nb_blocs
            
            st.subheader("Récapitulatif des données :")
            pivot_table = st.session_state.donnees.pivot(index='Bloc', columns='Traitement', values='Valeur')
            st.dataframe(pivot_table, use_container_width=True)
            
            if st.button("✅ Données saisies, passer aux calculs DDL"):
                st.success("Données enregistrées ! Passez à l'étape 3.")

# Étape 3: Calcul des DDL
elif etape == "3. Calcul des DDL":
    if st.session_state.donnees is None:
        st.error("⚠️ Saisissez d'abord vos données à l'étape 2 !")
    else:
        st.header("🧮 Étape 3: Comprendre et calculer les Degrés de Liberté (DDL)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🤔 D'abord, réfléchissons...")
            st.write("**Questions :**")
            st.write("1. Combien avez-vous d'observations au total ?")
            st.write("2. Combien de paramètres allez-vous estimer ?")
            st.write("3. Pourquoi le DDL total = n - 1 ?")
            
            nb_obs_total = len(st.session_state.donnees)
            nb_trait = st.session_state.nb_traitements  
            nb_blocs = st.session_state.nb_blocs
            
            st.write(f"**Dans votre expérience :**")
            st.write(f"- Nombre total d'observations : {nb_obs_total}")
            st.write(f"- Nombre de traitements : {nb_trait}")
            st.write(f"- Nombre de blocs : {nb_blocs}")
        
        with col2:
            st.subheader("✏️ Calculez vous-même :")
            
            st.write("**DDL Total :**")
            ddl_total_etudiant = st.number_input("DDL Total = ", value=0, key="ddl_total")
            ddl_total_correct = nb_obs_total - 1
            
            st.write("**DDL Traitements :**")
            ddl_trait_etudiant = st.number_input("DDL Traitements = ", value=0, key="ddl_trait")
            ddl_trait_correct = nb_trait - 1
            
            st.write("**DDL Blocs :**")
            ddl_blocs_etudiant = st.number_input("DDL Blocs = ", value=0, key="ddl_blocs")
            ddl_blocs_correct = nb_blocs - 1
            
            st.write("**DDL Erreur :**")
            ddl_erreur_etudiant = st.number_input("DDL Erreur = ", value=0, key="ddl_erreur")
            ddl_erreur_correct = (nb_trait - 1) * (nb_blocs - 1)
        
        if st.button("🔍 Vérifier mes calculs"):
            resultats = []
            
            if ddl_total_etudiant == ddl_total_correct:
                st.success(f"✅ DDL Total correct : {ddl_total_correct}")
                resultats.append(True)
            else:
                st.error(f"❌ DDL Total incorrect. Réponse : {ddl_total_correct} (car n-1 = {nb_obs_total}-1)")
                resultats.append(False)
            
            if ddl_trait_etudiant == ddl_trait_correct:
                st.success(f"✅ DDL Traitements correct : {ddl_trait_correct}")
                resultats.append(True)
            else:
                st.error(f"❌ DDL Traitements incorrect. Réponse : {ddl_trait_correct} (car t-1 = {nb_trait}-1)")
                resultats.append(False)
            
            if ddl_blocs_etudiant == ddl_blocs_correct:
                st.success(f"✅ DDL Blocs correct : {ddl_blocs_correct}")
                resultats.append(True)
            else:
                st.error(f"❌ DDL Blocs incorrect. Réponse : {ddl_blocs_correct} (car b-1 = {nb_blocs}-1)")
                resultats.append(False)
            
            if ddl_erreur_etudiant == ddl_erreur_correct:
                st.success(f"✅ DDL Erreur correct : {ddl_erreur_correct}")
                resultats.append(True)
            else:
                st.error(f"❌ DDL Erreur incorrect. Réponse : {ddl_erreur_correct} (car (t-1)(b-1) = ({nb_trait}-1)×({nb_blocs}-1))")
                resultats.append(False)
            
            somme_ddl = ddl_trait_correct + ddl_blocs_correct + ddl_erreur_correct
            if somme_ddl == ddl_total_correct:
                st.info(f"✅ Vérification : {ddl_trait_correct} + {ddl_blocs_correct} + {ddl_erreur_correct} = {ddl_total_correct}")
            
            if all(resultats):
                st.session_state.ddl_calculated = True
                st.balloons()
                st.success("🎉 Parfait ! Vous maîtrisez les DDL. Passez à l'étape 4.")

# Étape 4: Calcul des sommes de carrés
elif etape == "4. Calcul des sommes de carrés":
    if not st.session_state.get('ddl_calculated', False):
        st.error("⚠️ Maîtrisez d'abord les DDL à l'étape 3 !")
    else:
        st.header("🧮 Étape 4: Calcul des Sommes de Carrés")
        
        donnees = st.session_state.donnees
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 Vos données :")
            pivot_table = donnees.pivot(index='Bloc', columns='Traitement', values='Valeur')
            st.dataframe(pivot_table)
            
            moyenne_generale = donnees['Valeur'].mean()
            st.write(f"**Moyenne générale :** {moyenne_generale:.3f}")
            
            moy_traitements = donnees.groupby('Traitement')['Valeur'].mean()
            st.write("**Moyennes par traitement :**")
            for t, moy in moy_traitements.items():
                st.write(f"- Traitement {t}: {moy:.3f}")
            
            moy_blocs = donnees.groupby('Bloc')['Valeur'].mean()
            st.write("**Moyennes par bloc :**")
            for b, moy in moy_blocs.items():
                st.write(f"- Bloc {b}: {moy:.3f}")
        
        with col2:
            st.subheader("🔢 Formules à comprendre :")
            st.latex(r'SC_{Total} = \sum_{i,j} (X_{ij} - \bar{X})^2')
            st.latex(r'SC_{Traitements} = b \sum_j (\bar{X}_j - \bar{X})^2')
            st.latex(r'SC_{Blocs} = t \sum_i (\bar{X}_i - \bar{X})^2')
            st.latex(r'SC_{Erreur} = SC_{Total} - SC_{Traitements} - SC_{Blocs}')
        
        st.subheader("📈 Calculs détaillés :")
        
        sc_total = ((donnees['Valeur'] - moyenne_generale) ** 2).sum()
        st.write(f"**SC Total :** {sc_total:.3f}")
        
        nb_blocs = st.session_state.nb_blocs
        sc_traitements = nb_blocs * ((moy_traitements - moyenne_generale) ** 2).sum()
        st.write(f"**SC Traitements :** {sc_traitements:.3f}")
        
        nb_trait = st.session_state.nb_traitements
        sc_blocs = nb_trait * ((moy_blocs - moyenne_generale) ** 2).sum()
        st.write(f"**SC Blocs :** {sc_blocs:.3f}")
        
        sc_erreur = sc_total - sc_traitements - sc_blocs
        st.write(f"**SC Erreur :** {sc_erreur:.3f}")
        
        st.session_state.sc_total = sc_total
        st.session_state.sc_traitements = sc_traitements
        st.session_state.sc_blocs = sc_blocs
        st.session_state.sc_erreur = sc_erreur
        
        if st.button("✅ J'ai compris les sommes de carrés"):
            st.success("Parfait ! Passez à l'étape 5 pour les carrés moyens.")

# Étape 5: Calcul des carrés moyens
elif etape == "5. Calcul des carrés moyens":
    if 'sc_total' not in st.session_state:
        st.error("⚠️ Calculez d'abord les sommes de carrés à l'étape 4 !")
    else:
        st.header("📊 Étape 5: Des Sommes de Carrés aux Carrés Moyens")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🧠 Principe des Carrés Moyens")
            st.info("""
            **Carré Moyen = Somme de Carrés ÷ DDL**
            
            Pourquoi diviser par les DDL ?
            - Pour obtenir une variance estimée
            - Pour comparer des sources de variation
            - Pour calculer le test F
            """)
            
            st.subheader("📋 Récapitulatif précédent :")
            
            nb_trait = st.session_state.nb_traitements
            nb_blocs = st.session_state.nb_blocs
            ddl_trait = nb_trait - 1
            ddl_blocs = nb_blocs - 1  
            ddl_erreur = (nb_trait - 1) * (nb_blocs - 1)
            
            st.write("**DDL :**")
            st.write(f"- Traitements: {ddl_trait}")
            st.write(f"- Blocs: {ddl_blocs}")
            st.write(f"- Erreur: {ddl_erreur}")
            
            st.write("**Sommes de Carrés :**")
            st.write(f"- SC Traitements: {st.session_state.sc_traitements:.3f}")
            st.write(f"- SC Blocs: {st.session_state.sc_blocs:.3f}")
            st.write(f"- SC Erreur: {st.session_state.sc_erreur:.3f}")
        
        with col2:
            st.subheader("✏️ Calculez les Carrés Moyens :")
            
            st.write("**CM Traitements :**")
            cm_trait_etudiant = st.number_input(
                f"CM Traitements = {st.session_state.sc_traitements:.3f} ÷ {ddl_trait} =",
                value=0.0,
                step=0.001,
                key="cm_trait"
            )
            
            st.write("**CM Blocs :**")
            cm_blocs_etudiant = st.number_input(
                f"CM Blocs = {st.session_state.sc_blocs:.3f} ÷ {ddl_blocs} =",
                value=0.0,
                step=0.001,
                key="cm_blocs"
            )
            
            st.write("**CM Erreur :**")
            cm_erreur_etudiant = st.number_input(
                f"CM Erreur = {st.session_state.sc_erreur:.3f} ÷ {ddl_erreur} =",
                value=0.0,
                step=0.001,
                key="cm_erreur"
            )
        
        cm_trait_correct = st.session_state.sc_traitements / ddl_trait
        cm_blocs_correct = st.session_state.sc_blocs / ddl_blocs
        cm_erreur_correct = st.session_state.sc_erreur / ddl_erreur
        
        if st.button("🔍 Vérifier mes calculs CM"):
            tolerance = 0.01
            resultats = []
            
            if abs(cm_trait_etudiant - cm_trait_correct) < tolerance:
                st.success(f"✅ CM Traitements correct : {cm_trait_correct:.3f}")
                resultats.append(True)
            else:
                st.error(f"❌ CM Traitements incorrect. Réponse : {cm_trait_correct:.3f}")
                resultats.append(False)
            
            if abs(cm_blocs_etudiant - cm_blocs_correct) < tolerance:
                st.success(f"✅ CM Blocs correct : {cm_blocs_correct:.3f}")
                resultats.append(True)
            else:
                st.error(f"❌ CM Blocs incorrect. Réponse : {cm_blocs_correct:.3f}")
                resultats.append(False)
            
            if abs(cm_erreur_etudiant - cm_erreur_correct) < tolerance:
                st.success(f"✅ CM Erreur correct : {cm_erreur_correct:.3f}")
                resultats.append(True)
            else:
                st.error(f"❌ CM Erreur incorrect. Réponse : {cm_erreur_correct:.3f}")
                resultats.append(False)
            
            if all(resultats):
                st.session_state.cm_traitements = cm_trait_correct
                st.session_state.cm_blocs = cm_blocs_correct
                st.session_state.cm_erreur = cm_erreur_correct
                st.balloons()
                st.success("🎉 Excellent ! Vous pouvez maintenant calculer F !")

# Étape 6: Calcul du F
elif etape == "6. Calcul du F":
    if 'cm_erreur' not in st.session_state:
        st.error("⚠️ Calculez d'abord les carrés moyens à l'étape 5 !")
    else:
        st.header("🎯 Étape 6: Calcul du F calculé")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🧠 Comprendre le test F")
            st.info("""
            **F = Carré Moyen de l'effet / Carré Moyen de l'erreur**
            
            **Logique :**
            - Si l'effet est significatif → F sera grand
            - Si pas d'effet → F sera proche de 1
            - L'erreur est au dénominateur (référence)
            """)
            
            st.subheader("📊 Vos Carrés Moyens :")
            st.write(f"- CM Traitements: {st.session_state.cm_traitements:.3f}")
            st.write(f"- CM Blocs: {st.session_state.cm_blocs:.3f}")  
            st.write(f"- CM Erreur: {st.session_state.cm_erreur:.3f}")
        
        with col2:
            st.subheader("✏️ Calculez le F :")
            
            st.write("**F Traitements :**")
            f_trait_etudiant = st.number_input(
                f"F = {st.session_state.cm_traitements:.3f} ÷ {st.session_state.cm_erreur:.3f} =",
                value=0.0,
                step=0.01,
                key="f_trait"
            )
            
            st.write("**F Blocs :**")
            f_blocs_etudiant = st.number_input(
                f"F = {st.session_state.cm_blocs:.3f} ÷ {st.session_state.cm_erreur:.3f} =",
                value=0.0,
                step=0.01,
                key="f_blocs"
            )
        
        f_trait_correct = st.session_state.cm_traitements / st.session_state.cm_erreur
        f_blocs_correct = st.session_state.cm_blocs / st.session_state.cm_erreur
        
        if st.button("🔍 Vérifier mes calculs F"):
            tolerance = 0.01
            resultats = []
            
            if abs(f_trait_etudiant - f_trait_correct) < tolerance:
                st.success(f"✅ F Traitements correct : {f_trait_correct:.3f}")
                resultats.append(True)
            else:
                st.error(f"❌ F Traitements incorrect. Réponse : {f_trait_correct:.3f}")
                resultats.append(False)
            
            if abs(f_blocs_etudiant - f_blocs_correct) < tolerance:
                st.success(f"✅ F Blocs correct : {f_blocs_correct:.3f}")
                resultats.append(True)
            else:
                st.error(f"❌ F Blocs incorrect. Réponse : {f_blocs_correct:.3f}")
                resultats.append(False)
            
            if all(resultats):
                st.session_state.f_traitements = f_trait_correct
                st.session_state.f_blocs = f_blocs_correct
                st.balloons()
                st.success("🎉 F calculés ! Maintenant comparons avec F théorique !")

# Étape 7: Comparaison F théorique
elif etape == "7. Comparaison F théorique":
    if 'f_traitements' not in st.session_state:
        st.error("⚠️ Calculez d'abord le F à l'étape 6 !")
    else:
        st.header("📊 Étape 7: Comparaison avec F théorique")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎯 Vos F calculés :")
            st.write(f"- **F Traitements :** {st.session_state.f_traitements:.3f}")
            st.write(f"- **F Blocs :** {st.session_state.f_blocs:.3f}")
            
            st.subheader("⚙️ Paramètres pour F théorique :")
            alpha = st.selectbox("Seuil de signification (α):", [0.05, 0.01, 0.001], index=0)
            
            nb_trait = st.session_state.nb_traitements
            nb_blocs = st.session_state.nb_blocs
            ddl1_trait = nb_trait - 1
            ddl2 = (nb_trait - 1) * (nb_blocs - 1)
            ddl1_blocs = nb_blocs - 1
            
            st.write(f"**DDL pour Traitements :** ν1 = {ddl1_trait}, ν2 = {ddl2}")
            st.write(f"**DDL pour Blocs :** ν1 = {ddl1_blocs}, ν2 = {ddl2}")
        
        with col2:
            st.subheader("📖 F théorique (table de Fisher)")
            
            f_theor_trait = stats.f.ppf(1 - alpha, ddl1_trait, ddl2)
            f_theor_blocs = stats.f.ppf(1 - alpha, ddl1_blocs, ddl2)
            
            st.write(f"**F théorique Traitements** (α={alpha}):")
            st.write(f"F({ddl1_trait},{ddl2}) = **{f_theor_trait:.3f}**")
            
            st.write(f"**F théorique Blocs** (α={alpha}):")
            st.write(f"F({ddl1_blocs},{ddl2}) = **{f_theor_blocs:.3f}**")
        
        st.subheader("🔍 Comparaison et Décision :")
        
        col3, col4 = st.columns([1, 1])
        
        with col3:
            st.write("**Pour les Traitements :**")
            if st.session_state.f_traitements > f_theor_trait:
                st.success(f"✅ F calc ({st.session_state.f_traitements:.3f}) > F théor ({f_theor_trait:.3f})")
                st.success("**Conclusion : Effet des traitements SIGNIFICATIF** 📈")
            else:
                st.error(f"❌ F calc ({st.session_state.f_traitements:.3f}) ≤ F théor ({f_theor_trait:.3f})")
                st.error("**Conclusion : Effet des traitements NON significatif**")
        
        with col4:
            st.write("**Pour les Blocs :**")
            if st.session_state.f_blocs > f_theor_blocs:
                st.success(f"✅ F calc ({st.session_state.f_blocs:.3f}) > F théor ({f_theor_blocs:.3f})")
                st.success("**Conclusion : Effet des blocs SIGNIFICATIF** 📈")
            else:
                st.info(f"ℹ️ F calc ({st.session_state.f_blocs:.3f}) ≤ F théor ({f_theor_blocs:.3f})")
                st.info("**Conclusion : Effet des blocs NON significatif**")
        
        st.subheader("📊 Visualisation des F")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        categories = ['F calculé', 'F théorique']
        values_trait = [st.session_state.f_traitements, f_theor_trait]
        colors_trait = ['red' if st.session_state.f_traitements > f_theor_trait else 'blue', 'gray']
        ax1.bar(categories, values_trait, color=colors_trait, alpha=0.7)
        ax1.set_title('Traitements')
        ax1.set_ylabel('Valeur F')
        ax1.grid(True, alpha=0.3)
        
        values_blocs = [st.session_state.f_blocs, f_theor_blocs]
        colors_blocs = ['red' if st.session_state.f_blocs > f_theor_blocs else 'blue', 'gray']
        ax2.bar(categories, values_blocs, color=colors_blocs, alpha=0.7)
        ax2.set_title('Blocs')
        ax2.set_ylabel('Valeur F')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        if st.button("✅ J'ai compris la comparaison F"):
            st.success("Parfait ! Passez à l'interprétation finale !")

# Étape 8: Interprétation
elif etape == "8. Interprétation":
    if 'f_traitements' not in st.session_state:
        st.error("⚠️ Completez d'abord toutes les étapes précédentes !")
    else:
        st.header("🎓 Étape 8: Interprétation des résultats")
        
        st.subheader("📋 Récapitulatif de votre analyse ANOVA")
        
        nb_trait = st.session_state.nb_traitements
        nb_blocs = st.session_state.nb_blocs
        ddl_trait = nb_trait - 1
        ddl_blocs = nb_blocs - 1  
        ddl_erreur = (nb_trait - 1) * (nb_blocs - 1)
        ddl_total = nb_trait * nb_blocs - 1
        
        f_theor_trait = stats.f.ppf(0.95, ddl_trait, ddl_erreur)
        f_theor_blocs = stats.f.ppf(0.95, ddl_blocs, ddl_erreur)
        
        p_value_trait = 1 - stats.f.cdf(st.session_state.f_traitements, ddl_trait, ddl_erreur)
        p_value_blocs = 1 - stats.f.cdf(st.session_state.f_blocs, ddl_blocs, ddl_erreur)
        
        anova_table = pd.DataFrame({
            'Source de variation': ['Traitements', 'Blocs', 'Erreur', 'Total'],
            'DDL': [ddl_trait, ddl_blocs, ddl_erreur, ddl_total],
            'Somme des carrés': [
                f"{st.session_state.sc_traitements:.3f}",
                f"{st.session_state.sc_blocs:.3f}",
                f"{st.session_state.sc_erreur:.3f}",
                f"{st.session_state.sc_total:.3f}"
            ],
            'Carré moyen': [
                f"{st.session_state.cm_traitements:.3f}",
                f"{st.session_state.cm_blocs:.3f}",
                f"{st.session_state.cm_erreur:.3f}",
                "-"
            ],
            'F calculé': [
                f"{st.session_state.f_traitements:.3f}",
                f"{st.session_state.f_blocs:.3f}",
                "-",
                "-"
            ],
            'F théorique (5%)': [
                f"{f_theor_trait:.3f}",
                f"{f_theor_blocs:.3f}",
                "-",
                "-"
            ],
            'p-value': [
                f"{p_value_trait:.4f}",
                f"{p_value_blocs:.4f}",
                "-",
                "-"
            ],
            'Significatif ?': [
                "OUI" if st.session_state.f_traitements > f_theor_trait else "NON",
                "OUI" if st.session_state.f_blocs > f_theor_blocs else "NON",
                "-",
                "-"
            ]
        })
        
        st.dataframe(anova_table, use_container_width=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🔍 Interprétation des Traitements")
            if st.session_state.f_traitements > f_theor_trait:
                st.success("""
                ✅ **Effet significatif des traitements**
                
                **Cela signifie :**
                - Les traitements ont un effet réel
                - Les différences observées ne sont pas dues au hasard
                - Vous pouvez rejeter H₀ : "pas de différence entre traitements"
                
                **Prochaines étapes :**
                - Test post-hoc (Tukey, Newman-Keuls...)
                - Comparaison multiple des moyennes
                """)
            else:
                st.error("""
                ❌ **Effet non significatif des traitements**
                
                **Cela signifie :**
                - Pas de preuve d'effet des traitements
                - Les différences peuvent être dues au hasard
                - Vous acceptez H₀
                
                **Possible causes :**
                - Traitements réellement sans effet
                - Variabilité trop importante
                - Nombre de répétitions insuffisant
                """)
        
        with col2:
            st.subheader("🔍 Interprétation des Blocs")
            if st.session_state.f_blocs > f_theor_blocs:
                st.success("""
                ✅ **Effet significatif des blocs**
                
                **Cela signifie :**
                - Le dispositif en blocs était justifié
                - Il y a effectivement de la variabilité entre blocs
                - Vous avez bien contrôlé cette source de variation
                """)
            else:
                st.info("""
                ℹ️ **Effet non significatif des blocs**
                
                **Cela signifie :**
                - Pas de grande différence entre blocs
                - Le dispositif en blocs n'était peut-être pas nécessaire
                - Mais cela ne nuit pas à l'analyse
                """)
        
        st.subheader("📊 Coefficient de Variation (CV%)")
        moyenne_generale = st.session_state.donnees['Valeur'].mean()
        ecart_type_erreur = np.sqrt(st.session_state.cm_erreur)
        cv_percent = (ecart_type_erreur / moyenne_generale) * 100
        
        st.write(f"**CV% = (√CM_erreur / Moyenne générale) × 100**")
        st.write(f"CV% = (√{st.session_state.cm_erreur:.3f} / {moyenne_generale:.3f}) × 100 = **{cv_percent:.1f}%**")
        
        if cv_percent < 10:
            st.success(f"✅ CV% = {cv_percent:.1f}% : Très bonne précision expérimentale")
        elif cv_percent < 20:
            st.info(f"✅ CV% = {cv_percent:.1f}% : Bonne précision expérimentale")
        elif cv_percent < 30:
            st.warning(f"⚠️ CV% = {cv_percent:.1f}% : Précision moyenne")
        else:
            st.error(f"❌ CV% = {cv_percent:.1f}% : Précision insuffisante")
        
        st.subheader("📈 Graphique des moyennes par traitement")
        moyennes_trait = st.session_state.donnees.groupby('Traitement')['Valeur'].agg(['mean', 'std'])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x_pos = np.arange(len(moyennes_trait))
        bars = ax.bar(x_pos, moyennes_trait['mean'], 
                     yerr=moyennes_trait['std'], 
                     capsize=5, alpha=0.7, 
                     color='lightblue', edgecolor='navy')
        
        ax.set_xlabel('Traitements')
        ax.set_ylabel('Valeur moyenne')
        ax.set_title('Moyennes par traitement avec écart-type')
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f'T{i}' for i in moyennes_trait.index])
        ax.grid(True, alpha=0.3)
        
        for i, (bar, mean_val) in enumerate(zip(bars, moyennes_trait['mean'])):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   f'{mean_val:.2f}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.subheader("🤔 Questions de réflexion")
        st.write("""
        **Maintenant que vous maîtrisez l'ANOVA, réfléchissez :**
        
        1. **Pourquoi chaque étape est-elle importante ?**
           - DDL → degrés de liberté disponibles
           - SC → quantification de la variabilité
           - CM → variance estimée
           - F → rapport des variances
        
        2. **Que faire maintenant ?**
           - Si significatif → tests de comparaisons multiples
           - Si non significatif → revoir l'expérimentation
        
        3. **Comment améliorer l'expérience ?**
           - Plus de répétitions pour diminuer l'erreur
           - Mieux contrôler les conditions
           - Choix d'un dispositif plus adapté
        """)
        
        if st.button("🎉 J'ai maîtrisé l'ANOVA !"):
            st.balloons()
            st.success("""
            🎓 **Félicitations !** 
            
            Vous maîtrisez maintenant :
            - La logique de l'analyse de variance
            - Le calcul étape par étape 
            - L'interprétation des résultats
            - L'importance de chaque étape
            
            Vous êtes prêt(e) pour vos expérimentations agricoles ! 🌱
            """)

# Aide contextuelle dans la sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Aide")

if etape.startswith("1."):
    st.sidebar.info("Choisissez le dispositif qui correspond à votre expérimentation")
elif etape.startswith("2."):
    st.sidebar.info("Saisissez des données réalistes pour votre apprentissage")
elif etape.startswith("3."):
    st.sidebar.info("Les DDL représentent les degrés de liberté. Réfléchissez aux paramètres estimés.")
elif etape.startswith("4."):
    st.sidebar.info("Les sommes de carrés quantifient la variabilité de chaque source")
elif etape.startswith("5."):
    st.sidebar.info("Les carrés moyens sont des variances estimées")
elif etape.startswith("6."):
    st.sidebar.info("Le F compare la variance de l'effet à celle de l'erreur")
elif etape.startswith("7."):
    st.sidebar.info("Comparez votre F calculé au F théorique pour décider")
else:
    st.sidebar.info("Interprétez vos résultats dans le contexte agricole")

st.sidebar.markdown("---")
st.sidebar.write("💡 **Conseil :** Prenez le temps de comprendre chaque étape avant de passer à la suivante !")
