// JavaScript for the responsive navigation menu
document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('nav');
    const navLinks = document.querySelectorAll('.nav-links li');

    burger.addEventListener('click', () => {
        nav.classList.toggle('active');

        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s;
            }
        });

        // Burger animation
        burger.classList.toggle('toggle'));
});