document.addEventListener('DOMContentLoaded', function () {
    const revealNodes = document.querySelectorAll('[data-reveal]');
    if (!revealNodes.length || !('IntersectionObserver' in window)) {
        return;
    }

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });

    revealNodes.forEach(function (node) {
        observer.observe(node);
    });
});
