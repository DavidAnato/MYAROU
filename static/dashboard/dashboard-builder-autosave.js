(function () {
    'use strict';

    const DEBOUNCE_MS = 250;

    function getCsrf() {
        return window.DASHBOARD_API?.csrf || '';
    }

    function triggerLivePreview(form) {
        if (window.DashboardForms && typeof window.DashboardForms.triggerPreviewUpdate === 'function') {
            window.DashboardForms.triggerPreviewUpdate(form);
        }
    }

    function setStatus(el, state, message) {
        if (!el) return;
        el.dataset.state = state;
        el.textContent = message;
        el.classList.remove(
            'text-gray-500', 'text-emerald-600', 'text-amber-600', 'text-red-600',
            'dark:text-gray-400', 'dark:text-emerald-400', 'dark:text-amber-400', 'dark:text-red-400',
        );
        const map = {
            idle: ['text-gray-500', 'dark:text-gray-400'],
            saving: ['text-amber-600', 'dark:text-amber-400'],
            saved: ['text-emerald-600', 'dark:text-emerald-400'],
            error: ['text-red-600', 'dark:text-red-400'],
        };
        (map[state] || map.idle).forEach((c) => el.classList.add(c));
    }

    function updatePublishedBadge(isPublished) {
        const badge = document.querySelector('[data-builder-publish-badge]');
        if (!badge) return;
        badge.className = 'builder-status-badge ' + (
            isPublished ? 'builder-status-badge--published' : 'builder-status-badge--draft'
        );
        badge.innerHTML = (
            `<span class="w-1.5 h-1.5 rounded-full ${isPublished ? 'bg-emerald-500' : 'bg-amber-500'}"></span>`
            + (isPublished ? 'Publiée' : 'Brouillon')
        );
        const viewLink = document.querySelector('[data-builder-view-live]');
        if (viewLink) {
            viewLink.classList.toggle('hidden', !isPublished);
        }
    }

    function reloadPreviewIframe(previewUrl) {
        const iframe = document.getElementById('pagePreviewIframe');
        if (!iframe || !previewUrl) return;
        const sep = previewUrl.includes('?') ? '&' : '?';
        iframe.src = previewUrl + sep + '_=' + Date.now();
    }

    function applyBlockMapping(form, blocks) {
        if (!blocks || !blocks.length) return;
        blocks.forEach((item) => {
            const card = form.querySelector(`[data-block-form][data-form-prefix="${item.form_prefix}"]`);
            if (!card) return;

            card.setAttribute('data-block-pk', String(item.id));
            const idInput = card.querySelector('input[name$="-id"]');
            if (idInput) idInput.value = item.id;

            if (item.image_url) {
                const blockType = card.querySelector('[name$="-block_type"]')?.value || '';
                const mediaSection = card.querySelector(`[data-block-media-for="${blockType}"]`);
                window.DashboardBlockEditor?.updateMediaUrl?.(mediaSection || card, item.image_url);
            }

            window.DashboardBlockEditor?.enableGalleryBlock?.(form, card, item.id);
        });
    }

    function applyImageMapping(form, images) {
        if (!images || !images.length) return;
        images.forEach((item) => {
            const row = form.querySelector(`[data-block-image-form][data-form-prefix="${item.form_prefix}"]`);
            if (!row) return;
            row.setAttribute('data-image-pk', String(item.id));
            row.setAttribute('data-block-id', String(item.block_id));
            const idInput = row.querySelector('input[name$="-id"]');
            if (idInput) idInput.value = item.id;
            const blockInput = row.querySelector('input[name$="-block"]');
            if (blockInput) blockInput.value = item.block_id;
            const delBtn = row.querySelector('[data-delete-block-image]');
            if (delBtn) {
                delBtn.setAttribute('data-image-pk', String(item.id));
                delBtn.removeAttribute('data-delete-new');
            }
            if (item.image_url) {
                window.DashboardBlockEditor?.updateMediaUrl?.(row, item.image_url);
            }
        });
    }

    function initAutosave(form, config) {
        if (!form || !config.saveUrl) return null;
        if (form._builderSync) return form._builderSync;

        const statusEl = document.querySelector('[data-builder-save-status]');
        const publishBtn = document.querySelector('[data-builder-publish]');
        const publishedInput = document.getElementById('builderIsPublished');
        let timer = null;
        let inflight = null;
        let dirty = false;
        let pendingImmediate = false;

        const markDirty = () => {
            dirty = true;
            triggerLivePreview(form);
            if (!inflight) {
                setStatus(statusEl, 'idle', 'Synchronisation…');
            }
        };

        const scheduleSave = (immediate) => {
            markDirty();
            if (immediate) {
                pendingImmediate = true;
                if (timer) {
                    clearTimeout(timer);
                    timer = null;
                }
                return syncNow(false);
            }
            if (timer) clearTimeout(timer);
            timer = setTimeout(() => {
                timer = null;
                syncNow(false);
            }, DEBOUNCE_MS);
            return Promise.resolve();
        };

        const syncNow = async (publish) => {
            if (inflight) {
                if (publish) await inflight;
                else return inflight;
            }

            if (publish && publishedInput) {
                publishedInput.value = 'on';
            }

            try {
                window.DashboardBlockEditor?.prepareForSave?.(form);
            } catch (err) {
                console.error('[builder] prepareForSave', err);
            }

            const fd = new FormData(form);
            fd.set('builder_action', publish ? 'publish' : 'autosave');

            setStatus(statusEl, 'saving', publish ? 'Publication…' : 'Enregistrement…');

            inflight = fetch(config.saveUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrf() },
                body: fd,
                credentials: 'same-origin',
            }).then(async (res) => {
                const data = await res.json().catch(() => ({}));
                if (!res.ok || !data.ok) {
                    let errMsg = 'Échec de l’enregistrement';
                    if (data.errors) {
                        if (data.errors.meta) errMsg = 'Paramètres invalides';
                        else if (data.errors.blocks) errMsg = 'Erreur dans un bloc';
                        else if (data.errors.images) errMsg = 'Erreur dans une image';
                    }
                    setStatus(statusEl, 'error', errMsg);
                    dirty = true;
                    throw new Error(errMsg);
                }

                dirty = false;
                pendingImmediate = false;
                const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                setStatus(
                    statusEl,
                    'saved',
                    data.is_published
                        ? `Publiée · ${time}`
                        : `Synchronisé · ${time}`,
                );

                if (publishedInput) {
                    publishedInput.value = data.is_published ? 'on' : '';
                }
                updatePublishedBadge(data.is_published);
                applyBlockMapping(form, data.blocks);
                applyImageMapping(form, data.images);

                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        triggerLivePreview(form);
                    });
                });

                if (publish) {
                    reloadPreviewIframe(data.preview_url);
                }

                form.dispatchEvent(new CustomEvent('builder:saved', { detail: data }));

                if (publish && data.page_href) {
                    const viewLink = document.querySelector('[data-builder-view-live]');
                    if (viewLink) viewLink.href = data.page_href;
                }

                return data;
            }).catch(() => {
                if (statusEl?.dataset.state !== 'error') {
                    setStatus(statusEl, 'error', 'Erreur réseau');
                }
            }).finally(() => {
                inflight = null;
                if (dirty && pendingImmediate && !timer) {
                    syncNow(false);
                } else if (dirty && !timer) {
                    scheduleSave(false);
                }
            });

            return inflight;
        };

        const notify = (options) => {
            const immediate = !!(options && options.immediate);
            return scheduleSave(immediate);
        };

        const scheduleSaveFromEvent = (e) => {
            if (e && e.target && e.target.type === 'file') return;
            scheduleSave(false);
        };
        form.addEventListener('input', scheduleSaveFromEvent);
        form.addEventListener('change', scheduleSaveFromEvent);

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (timer) clearTimeout(timer);
            timer = null;
            syncNow(true);
        });

        if (publishBtn) {
            publishBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (timer) clearTimeout(timer);
                timer = null;
                syncNow(true);
            });
        }

        form._builderSync = { notify, syncNow };

        setStatus(statusEl, 'saved', 'Prêt');
        triggerLivePreview(form);
        setTimeout(() => syncNow(false), 200);

        return { notify, syncNow };
    }

    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('pageSettingsForm');
        if (!form || form.getAttribute('data-preview-type') !== 'custom-page') return;
        if (!form.getAttribute('data-autosave-url')) return;
        initAutosave(form, { saveUrl: form.getAttribute('data-autosave-url') });
    });

    window.DashboardBuilderAutosave = { initAutosave };
})();
