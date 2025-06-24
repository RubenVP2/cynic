// cynic/web/static/hall-of-fame.js

document.addEventListener('DOMContentLoaded', async () => {
    const listDiv = document.getElementById('hall-of-fame-list');
    const spinner = document.getElementById('spinner');

    try {
        const response = await fetch('/api/hall-of-fame');
        if (!response.ok) throw new Error('Impossible de charger le palmarès.');

        const entries = await response.json();

        spinner.style.display = 'none';

        if (entries.length === 0) {
            listDiv.innerHTML = '<p>Le palmarès est encore vide. Soyez le premier à soumettre une perle !</p>';
            return;
        }

        let content = '';
        entries.forEach((entry, index) => {
            // Simple escaping to prevent basic HTML injection
            const escapeHTML = str => str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
            const contexte = entry.contexte ? `<p><strong>Contexte:</strong> <blockquote>${escapeHTML(entry.contexte)}</blockquote></p>` : '';
            const reponse = `<p><strong>Réponse analysée:</strong> <blockquote>${escapeHTML(entry.reponse)}</blockquote></p>`;

            content += `
                <div class="entry">
                    <div class="entry-header">
                        <h2>#${index + 1}</h2>
                        <div class="entry-score">${entry.score} / 10</div>
                    </div>
                    <div class="entry-body">
                        ${contexte}
                        ${reponse}
                    </div>
                </div>
            `;
        });
        listDiv.innerHTML = content;

    } catch (error) {
        spinner.style.display = 'none';
        listDiv.innerHTML = `<p style="color: red;"><strong>Erreur :</strong> ${error.message}</p>`;
    }
});