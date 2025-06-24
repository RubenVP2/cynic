// cynic/web/static/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Logique du Dark Mode ---
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme) {
        document.body.classList.add(currentTheme);
        if (currentTheme === 'dark-mode') {
            toggleSwitch.checked = true;
        }
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-mode');
        toggleSwitch.checked = true;
    }

    toggleSwitch.addEventListener('change', (e) => {
        if (e.target.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light-mode');
        }
    });

    // --- Logique de l'appel API ---
    const form = document.getElementById('cynic-form');
    const resultDiv = document.getElementById('result');
    const spinner = document.getElementById('spinner');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const contexte = document.getElementById('contexte').value;
        const reponseAAnalyser = document.getElementById('reponse').value;
        const proposer = document.getElementById('proposer-au-palmares').checked;

        spinner.style.display = 'block';
        resultDiv.style.display = 'none';
        resultDiv.innerHTML = '';

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contexte: contexte,
                    reponse: reponseAAnalyser,
                    proposer_au_palmares: proposer
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Erreur inconnue.');
            }

            function escapeRegExp(string) {
                return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            }

            let texteSurligne = reponseAAnalyser;

            if (data.expressions_cyniques && data.expressions_cyniques.length > 0) {
                data.expressions_cyniques.forEach(phrase => {
                    const escapedPhrase = escapeRegExp(phrase);
                    const regex = new RegExp(escapedPhrase, 'gi');
                    texteSurligne = texteSurligne.replace(regex, `<mark>$&</mark>`);
                });
            }

            resultDiv.innerHTML = `
                <h3>Résultat de l'analyse</h3>
                <p><strong>Score de Moquerie :</strong> ${data.score} / 10</p>
                <p><strong>Verdict du Détecteur :</strong> ${data.verdict}</p>
                <h4>Texte analysé :</h4>
                <div id="highlighted-text">${texteSurligne}</div>
            `;
        } catch (error) {
            resultDiv.innerHTML = `<p style="color: var(--title-color);"><strong>Erreur :</strong> ${error.message}</p>`;
        } finally {
            spinner.style.display = 'none';
            resultDiv.style.display = 'block';
        }
    });
});