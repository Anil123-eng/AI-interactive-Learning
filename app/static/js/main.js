/* ============================================================
   Hello World with AI - Main JavaScript
   ============================================================ */

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.flash').forEach(function (flash) {
        setTimeout(function () {
            if (flash.parentElement) flash.remove();
        }, 5000);
    });
});

// Generic fetch JSON helper with CSRF token
function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

async function postJSON(url, data) {
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        let detail = '';
        try {
            const err = await res.json();
            detail = err.error || '';
        } catch (_) { /* ignore */ }
        throw new Error(detail || `Request failed (${res.status})`);
    }
    return res.json();
}

// Simple inline code editor auto-resize
function autoGrow(textarea) {
    if (!textarea) return;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

