document.addEventListener('DOMContentLoaded', async () => {
    const gamesContainer = document.getElementById('games');
    const urlParams = new URLSearchParams(window.location.search);
    const categoryName = urlParams.get("category");
    console.log(categoryName);

    // Update the subcategory header
    document.getElementById("subcategory").innerText = categoryName;

    let gamesData = [];

    try {
        // Load all games using the loadAllGames function
        gamesData = await loadAllGames();
        populateGames(gamesData); // Populate the games dynamically
    } catch (error) {
        console.error('Error loading games data:', error);
    }

    // Function to populate games dynamically
    function populateGames(data) {
        gamesContainer.innerHTML = ''; // Clear existing content

        data.forEach((game) => {
            if (game.subcategory.toLowerCase() === categoryName.toLowerCase()) {
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
                console.log("added " + game.title);
            }
        });
    }
});
