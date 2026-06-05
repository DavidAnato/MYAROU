(function () {
    'use strict';

    const HIDE_SELECTORS = [
        '.cke_notifications_area',
        '.cke_notification',
        '.cke_notification_warning',
        '.cke_notification_info',
        '.cke_notification_success',
        '.cke_notification_error',
        '[id^="cke_notifications_area_"]',
    ].join(', ');

    /** Masque les bannières CKEditor (version non sécurisée, etc.) */
    function hideCkeNotifications() {
        let hidden = 0;
        document.querySelectorAll(HIDE_SELECTORS).forEach((el) => {
            el.style.setProperty('display', 'none', 'important');
            el.style.setProperty('visibility', 'hidden', 'important');
            el.style.setProperty('opacity', '0', 'important');
            el.style.setProperty('height', '0', 'important');
            el.style.setProperty('max-height', '0', 'important');
            el.style.setProperty('width', '0', 'important');
            el.style.setProperty('overflow', 'hidden', 'important');
            el.style.setProperty('pointer-events', 'none', 'important');
            el.style.setProperty('position', 'absolute', 'important');
            el.style.setProperty('left', '-9999px', 'important');
            el.setAttribute('aria-hidden', 'true');
            hidden += 1;
        });
        return hidden;
    }

    function disableVersionCheck() {
        if (!window.CKEDITOR) return false;
        CKEDITOR.config.versionCheck = false;
        if (CKEDITOR.editorConfig) {
            const original = CKEDITOR.editorConfig;
            CKEDITOR.editorConfig = function (config) {
                original.call(this, config);
                config.versionCheck = false;
            };
        }
        return true;
    }

    function findEditorForm(editor) {
        const el = editor?.element?.$;
        if (el) {
            const form = el.closest('form');
            if (form) return form;
        }
        return document.getElementById('articleForm')
            || document.getElementById('pageSettingsForm')
            || document.getElementById('customPageBuilderForm')
            || document.querySelector('form[data-preview-type]')
            || document.querySelector('form');
    }

    function cancelEditorNotifications(editor) {
        if (!editor || editor._builderNotificationsBlocked) return;
        editor._builderNotificationsBlocked = true;
        editor.on('notificationShow', (evt) => {
            evt.cancel();
            hideCkeNotifications();
        });
    }

    function bindEditorLiveSync(editor, form) {
        if (!editor || !form || editor._builderLiveSync) return;
        editor._builderLiveSync = true;

        let keyTimer = null;
        const notify = () => {
            hideCkeNotifications();
            if (editor._builderReadyAt && Date.now() - editor._builderReadyAt < 500) return;
            if (window.DashboardForms && typeof window.DashboardForms.triggerPreviewUpdate === 'function') {
                window.DashboardForms.triggerPreviewUpdate(form);
            }
            if (form._builderSync && typeof form._builderSync.notify === 'function') {
                form._builderSync.notify({ immediate: false });
            }
        };

        editor.on('instanceReady', () => {
            editor._builderReadyAt = Date.now();
            hideCkeNotifications();
        });
        editor.on('change', notify);
        editor.on('afterPaste', notify);
        editor.on('key', () => {
            if (keyTimer) clearTimeout(keyTimer);
            keyTimer = setTimeout(notify, 400);
        });
    }

    function setupEditor(editor) {
        if (!editor) return;
        disableVersionCheck();
        cancelEditorNotifications(editor);
        hideCkeNotifications();
        const form = findEditorForm(editor);
        if (form) bindEditorLiveSync(editor, form);
    }

    function initExistingEditors() {
        if (!window.CKEDITOR) return;
        disableVersionCheck();
        Object.values(CKEDITOR.instances).forEach(setupEditor);
        hideCkeNotifications();
    }

    function watchNotifications() {
        hideCkeNotifications();
        if (window._ckeNotificationObserver) return;
        window._ckeNotificationObserver = new MutationObserver(() => {
            hideCkeNotifications();
        });
        window._ckeNotificationObserver.observe(document.documentElement, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class', 'style', 'id'],
        });
        if (!window._ckeNotificationInterval) {
            window._ckeNotificationInterval = setInterval(hideCkeNotifications, 300);
        }
    }

    function hookCkeditorGlobal() {
        if (!window.CKEDITOR || window._ckeGlobalHooked) return;
        window._ckeGlobalHooked = true;
        disableVersionCheck();
        CKEDITOR.on('instanceReady', (ev) => setupEditor(ev.editor));
        CKEDITOR.on('instanceCreated', (ev) => setupEditor(ev.editor));
        CKEDITOR.on('instanceLoaded', (ev) => setupEditor(ev.editor));
    }

    function waitForCkeditor() {
        if (window.CKEDITOR) {
            hookCkeditorGlobal();
            initExistingEditors();
            return;
        }
        if (window._ckeWaitObserver) return;
        window._ckeWaitObserver = new MutationObserver(() => {
            if (window.CKEDITOR) {
                hookCkeditorGlobal();
                initExistingEditors();
                window._ckeWaitObserver.disconnect();
                window._ckeWaitObserver = null;
            }
        });
        window._ckeWaitObserver.observe(document.documentElement, {
            childList: true,
            subtree: true,
        });
    }

    function boot() {
        watchNotifications();
        waitForCkeditor();
        hookCkeditorGlobal();
        initExistingEditors();
        [50, 200, 600, 1200, 2500, 5000, 8000].forEach((ms) => {
            setTimeout(() => {
                disableVersionCheck();
                initExistingEditors();
                hideCkeNotifications();
            }, ms);
        });
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
        disableVersionCheck,
    };
})();
