# Détecteur de Moquerie - Cynic 🕵️‍♂️

**L'IA qui traduit enfin le *bullshit* corporate pour vous.**

[![Test du Code de Cynic](https://github.com/RubenVP2/cynic/actions/workflows/ci.yml/badge.svg)](https://github.com/RubenVP2/cynic/actions/workflows/ci.yml)
![Licence MIT](https://img.shields.io/badge/Licence-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.9+-yellow.svg)
![Maintained](https://img.shields.io/badge/Maintenu%3F-Oui%2C%20avec%20sarcasme-red.svg)

Fatigué(e) des "cordialement" qui sonnent comme des menaces ? Des "je me permets de te relancer" qui vous donnent des sueurs froides ? Vous sentez le passif-agressif, mais vous n'êtes pas sûr(e) ?

Ne doutez plus. Cet outil, propulsé par l'intelligence (artificielle et cynique) de Mistral, analyse pour vous les non-dits, les sous-entendus et les coups bas cachés dans vos e-mails et messages professionnels.

---

## 🎯 Le Problème que nous résolvons

Le monde de l'entreprise est une jungle. Et dans cette jungle, le langage est une arme. Nous vous aidons à décoder les attaques les plus sournoises :

-   `"Pour faire suite à notre échange..."` (Traduction : "Comme tu n'as rien écouté, je répète...")
-   `"Sauf erreur de ma part..."` (Traduction : "Tu as tort et je vais le prouver.")
-   `"Merci d'avance."` (Traduction : "Tu n'as pas le choix.")
-   `"OK."` (Traduction : Déclaration de guerre nucléaire.)

## ✨ Features

-   **Analyse Sémantique Avancée** : Grâce à l'API Mistral, notre IA ne se contente pas de chercher des mots-clés, elle *comprend* le contexte.
-   **Score de Moquerie Impitoyable** : Un score de 0 à 10 pour quantifier précisément à quel point on vous prend pour un jambon.
-   **Verdicts Percutants et Drôles** : Parce que si c'est pour pleurer, autant que ce soit de rire.
-   **Interface Terminal Élégante** : Une expérience utilisateur soignée grâce à la magie de la bibliothèque `rich`.

## 🚀 Installation : Prêt(e) à voir la vérité en face ?

Pour installer le Détecteur, suivez ces quelques étapes. Un peu de courage, la révélation est proche.

1.  **Clonez ce dépôt magnifique :**
    ```bash
    git clone [https://github.com/VOTRE_PSEUDO/detecteur-de-moquerie.git](https://github.com/VOTRE_PSEUDO/detecteur-de-moquerie.git)

    cd detecteur-de-moquerie
    ```

2.  **Installez les dépendances nécessaires :** (Assurez-vous d'avoir Python 3.9+ installé)
    ```bash
    pip install -e .[dev]
    ```

3.  **Configurez votre clé secrète :**
    -   Copiez le fichier d'exemple `.env.example` en un fichier `.env`.
    
        ```bash
        cp .env.example .env
        ```
    -   Ouvrez le fichier `.env` et remplacez `"votre_cle_api_ici"` par votre véritable clé API Mistral. Ce fichier est ignoré par Git, votre secret est donc en sécurité.

## 🛠️ Utilisation

Une fois l'installation terminée, lancez le programme depuis la racine du projet avec la commande suivante :

```bash
python -m detecteur_moquerie.cli
```

L'application vous guidera alors pour entrer le contexte initial et la réponse que vous souhaitez analyser.

**Aperçu de la machine en action :**
```
🕵️‍♂️ Le Détecteur de Moquerie 2.0 (Powered by Mistral) 🕵️‍♀️
─────────────────────────────────────────────────────────────
Pour commencer, décris la situation.
Quel était le message ou la question d'origine ? > Je t'ai envoyé le rapport hier, tu as pu y jeter un oeil ?

Maintenant, donne-moi la réponse que tu as reçue.
Quelle a été la réponse à analyser ? > Pour information, je suis assez occupé en ce moment. Cordialement.

[Analyse en cours... Connexion à l'intelligence suprême de Mistral...]

--- RAPPORT D'ANALYSE DE MISTRAL ---

Score de moquerie estimé : 8 / 10
┌─────────────────────────────────────────────────────────────────────────┐
│ Le "Pour information" est un carton jaune et le "Cordialement" est le   │
│ carton rouge qui l'accompagne. On vous fait comprendre que vous dérangez│
│ poliment. Très poliment.                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🤝 Contribuer

Votre talent pour déceler la mauvaise foi est légendaire ? Vous avez des idées pour rendre cet outil encore plus impitoyable ? Les contributions sont les bienvenues !

1. Forkez le projet.
2. Créez une nouvelle branche (git checkout -b feature/nouvelle-idee-geniale).
3. Faites vos modifications.
4. Ouvrez une Pull Request.

Quelques idées pour contribuer :

- Améliorer le PROMPT_SYSTEME pour rendre l'IA encore plus fine ou plus drôle.
- Ajouter des options (choix du modèle Mistral, etc.).
- Créer une interface web (pour les plus ambitieux).
- Corriger les bugs que vous pourriez trouver.

## 📜 Licence
Ce projet est distribué sous la Licence MIT. Voir le fichier LICENSE pour plus de détails. En gros, faites-en ce que vous voulez, mais ne venez pas vous plaindre si vous vous faites virer.

---

Disclaimer : Cet outil est à but humoristique et éducatif. Je ne peut être tenu responsable des claviers cassés, des démissions soudaines ou des conversations professionnelles devenues subitement très honnêtes.
