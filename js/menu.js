// JavaScript for hamburger menu functionality
// Note: Most of this logic is now in shared/header.html for encapsulation with its HTML.
// This file can be used for any menu-related JS that needs to be global or separated.

document.addEventListener('DOMContentLoaded', () => {
    console.log("menu.js loaded - Main logic is in shared/header.html's script tag for now.");

    // Example: If header is loaded dynamically, initialization might need to be called after load.
    // function initializeMenu() { ... }
    // if (document.getElementById('hamburgerToggleButton')) {
    //    initializeMenu();
    // } else {
    //    document.addEventListener('headerLoaded', initializeMenu); // Custom event
    // }
});
