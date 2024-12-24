// Declare a variable to store the currently playing sound
let currentSound = null;

// Function to preload sound files
function preloadSound(file) {
    const audio = new Audio(file);
    audio.preload = 'auto';
    return audio;
}

// Preload the sound file once, to avoid loading it multiple times
const preloadAudio = preloadSound('sound_effects/xpclick.mp3');

// Function to handle nav link clicks and play sound
function handleNavClick(event) {
    event.preventDefault(); // Prevent default link behavior for testing

    const soundPath = event.target.dataset.sound;

    if (currentSound) {
        currentSound.pause();
        currentSound.currentTime = 0; // Reset to the beginning
    }

    // Create a new audio object for the clicked sound file
    const sound = new Audio(soundPath);
    currentSound = sound; // Set current sound to this one

    sound.play()
      .then(() => console.log("Sound played successfully"))
      .catch(err => console.error("Error playing sound:", err));

    // Allow the default link action after sound is played
    setTimeout(() => {
        window.location.href = event.target.href; // Proceed with link navigation after sound
    }, 300); // Delay to ensure sound is played first
}

// Initialize event listeners after header is loaded
document.addEventListener("DOMContentLoaded", function () {
    // Dynamically load the header
    fetch("header.html")
      .then(response => response.text())
      .then(data => {
        document.getElementById("header-container").innerHTML = data;

        // Attach event listeners to nav links
        document.querySelectorAll('.nav-link').forEach(link => {
          link.addEventListener('click', handleNavClick);
        });
      })
      .catch(error => console.error("Error loading header:", error));
});
