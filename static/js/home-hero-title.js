/**
 * Met à jour --hero-chars sur le titre hero accueil (longueur préfixe + suffixe).
 */
(function () {
    function countChars(h1) {
        if (!h1) return 0;
        const prefix = h1.querySelector('[data-preview="hero_title_prefix"]');
        const suffix = h1.querySelector('[data-preview="hero_title_suffix"]');
        const a = (prefix && prefix.textContent ? prefix.textContent : '').trim();
        const b = (suffix && suffix.textContent ? suffix.textContent : '').trim();
        return a.length + b.length;
    }

    function adjust() {
        const h1 = document.getElementById('home-hero-title');
        if (!h1) return;
        h1.style.setProperty('--hero-chars', String(countChars(h1)));
    }

    window.HomeHeroTitle = { adjust: adjust };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', adjust);
    } else {
        adjust();
    }
})();
