document.getElementById("addUserForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const username = document.getElementById("username").value;

    fetch('/add_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = data.message || data.error;
        document.getElementById("addUserForm").reset();  // Reset form
    })
    .catch(error => console.error('Error:', error));
});

// Add this function to your existing scripts.js file

document.getElementById("addSongForm")?.addEventListener("submit", function(event) {
    event.preventDefault();
    
    const title = document.getElementById("title").value;
    const artist = document.getElementById("artist").value;

    fetch('/add_song', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, artist })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = data.message || data.error;
        document.getElementById("addSongForm").reset();  // Reset form
    })
    .catch(error => console.error('Error:', error));
});

// Add this function to your existing scripts.js file

document.getElementById("voteForm")?.addEventListener("submit", function(event) {
    event.preventDefault();
    
    const winner_id = document.getElementById("winner_id").value;
    const loser_id = document.getElementById("loser_id").value;
    
    fetch('/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ winner_id, loser_id })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = data.message || data.error;
        document.getElementById("voteForm").reset();  // Reset form
    })
    .catch(error => console.error('Error:', error));
});
