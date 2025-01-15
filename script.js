(() => {
    const input = document.querySelector('#search-bar');
    const suggestions = document.querySelector('#suggestions');

    let gamesData = [];

    // Load all games using the updated loadAllGames function
    loadAllGames().then((data) => {
        gamesData = data;
    });

    input.addEventListener('input', () => {
        const searchTerm = input.value.toLowerCase();
        suggestions.innerHTML = ''; // Clear previous suggestions

        if (searchTerm.trim() !== '') {
            const filteredGames = gamesData.filter((game) =>
                game.title.toLowerCase().includes(searchTerm)
            );

            filteredGames.forEach((game) => {
                const card = document.createElement('a');
                card.classList.add('suggestion-card');
                card.href = `game.html?id=${game.id}`;
                card.innerHTML = `
                    <img src="${game.imgpath}" alt="${game.title}">
                    <p>${game.title}</p>
                `;
                suggestions.appendChild(card);
            });
        }
    });
})();
