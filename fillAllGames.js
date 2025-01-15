document.addEventListener('DOMContentLoaded', () => {
    const gamesContainer = document.getElementById('games');

    // Use the shared loadAllGames function to fetch all games
    loadAllGames()
        .then((data) => {
            populateGames(data); // Populate the games dynamically
        })
        .catch((error) => console.error('Error loading games:', error));

    // Function to populate games dynamically
    function populateGames(data) {
        gamesContainer.innerHTML = ''; // Clear existing content

        data.forEach((game) => {
            const card = document.createElement('a'); // Create an anchor element
            card.href = `game.html?id=${game.id}`; // Create a link to the game page

            // Set the card's inner HTML to include an image and title
            card.innerHTML = `
              <div class="card" data-players="${game.data_players}">
                <img src="${game.imgpath}" alt="${game.title}">
                <h3>${game.title}</h3>
              </div>
            `;

            gamesContainer.appendChild(card); // Add the card to the container
        });
    }
});
