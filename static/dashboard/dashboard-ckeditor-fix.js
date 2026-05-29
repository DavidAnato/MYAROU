(function () {
    'use strict';

    /** Masque les bannières CKEditor (version non sécurisée, etc.) */
    function hideCkeNotifications() {
        document.querySelectorAll('.cke_notifications_area, .cke_notification').forEach((el) => {
            el.style.setProperty('display', 'none', 'important');
            el.style.setProperty('visibility', 'hidden', 'important');
            el.style.setProperty('opacity', '0', 'important');
            el.style.setProperty('height', '0', 'important');
            el.style.setProperty('max-height', '0', 'important');
            el.style.setProperty('overflow', 'hidden', 'important');
            el.style.setProperty('pointer-events', 'none', 'important');
            el.setAttribute('aria-hidden', 'true');
        });
    }

    function cancelEditorNotifications(editor) {
        if (!editor || editor._builderNotificationsBlocked) return;
        editor._builderNotificationsBlocked = true;
        editor.on('notificationShow', (evt) => {
            evt.cancel();
        });
    }

    function bindEditorLiveSync(editor, form) {
        if (!editor || !form || editor._builderLiveSync) return;
        editor._builderLiveSync = true;

        let keyTimer = null;
        const notify = () => {
            hideCkeNotifications();
            form.dispatchEvent(new Event('input', { bubbles: true }));
            form.dispatchEvent(new Event('change', { bubbles: true }));
        };

        editor.on('change', notify);
        editor.on('afterPaste', notify);
        editor.on('mode', notify);
        editor.on('key', () => {
            if (keyTimer) clearTimeout(keyTimer);
            keyTimer = setTimeout(notify, 80);
        });
    }

    function setupEditor(editor) {
        const form = document.getElementById('pageSettingsForm');
        cancelEditorNotifications(editor);
        hideCkeNotifications();
        if (form) bindEditorLiveSync(editor, form);
    }

    function initExistingEditors() {
        if (!window.CKEDITOR) return;
        Object.values(CKEDITOR.instances).forEach(setupEditor);
        hideCkeNotifications();
    }

    function watchNotifications() {
        hideCkeNotifications();
        if (window._ckeNotificationObserver) return;
        window._ckeNotificationObserver = new MutationObserver(hideCkeNotifications);
        window._ckeNotificationObserver.observe(document.body, {
            childList: true,
            subtree: true,
        });
        setInterval(hideCkeNotifications, 400);
    }

    function boot() {
        watchNotifications();
        initExistingEditors();

        if (window.CKEDITOR) {
            CKEDITOR.on('instanceReady', (ev) => setupEditor(ev.editor));
            CKEDITOR.on('instanceCreated', (ev) => setupEditor(ev.editor));
        }

        [200, 600, 1200, 2500, 5000].forEach((ms) => setTimeout(initExistingEditors, ms));
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }

    window.DashboardCKEditorFix = {
        hideCkeNotifications,
        setupEditor,
        bindEditorLiveSync,
    };
})();
