import streamlit as st
import pandas as pd
from openai import OpenAI

# 1. Configuration de la page
st.set_page_config(page_title="Audit RegTech IA", layout="centered", page_icon="🛡️")
st.title("🛡️ Pré-Audit Réglementaire IA")
st.markdown("Assistant d'analyse pour compléments alimentaires.")

# 2. Zone pour entrer la clé API de l'utilisateur
api_key = st.text_input("Entrez votre clé API OpenAI :", type="password")

# 3. Chargement du fichier CSV (Le Classeur)
try:
    df = pd.read_csv("donnees_reglementaires.csv", sep=";")
    base_de_donnees = df.to_string(index=False)
except Exception as e:
    st.error("⚠️ Fichier CSV introuvable. Vérifiez que le fichier 'donnees_reglementaires.csv' est bien sur GitHub.")
    base_de_donnees = ""

# 4. Interface utilisateur
formule = st.text_area("📝 Collez la liste des ingrédients de votre formule ici :", height=150)

# 5. Moteur d'Intelligence Artificielle
if st.button("Lancer l'Audit Réglementaire"):
    if not api_key:
        st.warning("Veuillez entrer votre clé API OpenAI en haut de la page.")
    elif not formule:
        st.warning("Veuillez entrer une formule à analyser.")
    else:
        with st.spinner("Analyse en cours via l'IA..."):
            client = OpenAI(api_key=api_key)
            
            # Le "System Prompt" qui bride l'IA
            prompt_systeme = f"""Tu es un auditeur strict spécialisé en affaires réglementaires agroalimentaires.
Voici la SEULE base de données réglementaire que tu as le droit d'utiliser :

{base_de_donnees}

Analyse la formule fournie par l'utilisateur. 
Règles absolues :
1. Si un ingrédient n'est pas dans la base de données ci-dessus, tu DOIS écrire : "⚠️ [Nom de l'ingrédient] : Ingrédient non répertorié - Analyse manuelle requise". Ne l'invente pas.
2. Pour les ingrédients présents dans la base, indique leur statut et leurs limites.
3. Structure ta réponse avec des émojis pour les codes couleurs (🟢 Conforme, 🟠 Restriction/Vigilance, 🔴 Interdit/Novel Food)."""
            
            try:
                reponse = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": prompt_systeme},
                        {"role": "user", "content": formule}
                    ]
                )
                st.success("Audit terminé :")
                st.markdown(reponse.choices[0].message.content)
            except Exception as e:
                st.error("Erreur avec l'API OpenAI. Vérifiez votre clé ou votre solde.")
