/**
 * Poignée de redimensionnement entre formulaire et aperçu (pages dashboard).
 */
(function (global) {
    const STORAGE_KEY = 'dashboard-preview-form-width';
    const MIN_FORM = 300;
    const MIN_PREVIEW = 320;
    const DEFAULT_FORM = 420;

    function initPreviewSplit() {
        const root = document.getElementById('dashboardPreviewSplit');
        if (!root) return;

        const formPane = root.querySelector('[data-split-form]');
        const handle = root.querySelector('[data-split-handle]');
        const previewPane = root.querySelector('[data-split-preview]');
        if (!formPane || !handle || !previewPane) return;

        const applyWidth = (px) => {
            const clamped = Math.round(px);
            root.style.setProperty('--split-form-width', clamped + 'px');
            try {
                localStorage.setItem(STORAGE_KEY, String(clamped));
            } catch (e) { /* quota */ }
            global.dispatchEvent(new Event('resize'));
        };

        const clampWidth = (clientX) => {
            const rect = root.getBoundingClientRect();
            const maxW = rect.width - MIN_PREVIEW - (handle.offsetWidth || 10);
            return Math.max(MIN_FORM, Math.min(clientX - rect.left, maxW));
        };

        const saved = parseInt(localStorage.getItem(STORAGE_KEY), 10);
        applyWidth(Number.isFinite(saved) && saved >= MIN_FORM ? saved : DEFAULT_FORM);

        const onMove = (e) => {
            applyWidth(clampWidth(e.clientX));
        };

        const stop = () => {
            document.removeEventListener('mousemove', onMove);
            document.removeEventListener('mouseup', stop);
            document.body.classList.remove('select-none', 'cursor-col-resize');
        };

        handle.addEventListener('mousedown', (e) => {
            e.preventDefault();
            document.body.classList.add('select-none', 'cursor-col-resize');
            document.addEventListener('mousemove', onMove);
            document.addEventListener('mouseup', stop);
        });

        handle.addEventListener('dblclick', () => {
            applyWidth(DEFAULT_FORM);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPreviewSplit);
    } else {
        initPreviewSplit();
    }
})(window);
