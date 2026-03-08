document.addEventListener('DOMContentLoaded', function () {
    // Auto-hide flash messages if present.
    const flashMessages = document.querySelectorAll('.flash-message[data-autohide="true"]');
    flashMessages.forEach(function (node) {
        window.setTimeout(function () {
            node.classList.add('hidden');
        }, 5000);
    });

    // Generic password visibility toggle.
    document.querySelectorAll('[data-toggle-password]').forEach(function (button) {
        button.addEventListener('click', function () {
            const inputId = button.getAttribute('data-toggle-password');
            const input = document.getElementById(inputId);
            if (!input) {
                return;
            }
            input.type = input.type === 'password' ? 'text' : 'password';
        });
    });
});
