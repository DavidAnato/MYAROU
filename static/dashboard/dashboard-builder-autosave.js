(function () {
    'use strict';

    /** Délai après la dernière modification utilisateur avant envoi au serveur */
    const DEBOUNCE_MS = 1500;
    /** Ignore les événements DOM déclenchés par la réponse serveur (CKEditor, mapping…) */
    const POST_SAVE_QUIET_MS = 1200;

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
        const draftBtn = document.querySelector('[data-builder-draft]');
        if (draftBtn) {
            draftBtn.classList.toggle('hidden', !isPublished);
        }
        const publishBtn = document.querySelector('[data-builder-publish]');
        if (publishBtn) {
            const label = publishBtn.querySelector('[data-builder-publish-label]');
            if (label) label.textContent = isPublished ? 'Mettre à jour' : 'Publier';
        }
    }

    const BUILDER_FIELD_LABELS = {
        image: 'Image',
        image_alt: 'Texte alternatif',
        video_url: 'URL vidéo',
        content: 'Contenu',
        content_en: 'Contenu (EN)',
        title: 'Titre',
        title_en: 'Titre (EN)',
        subtitle: 'Sous-titre',
        subtitle_en: 'Sous-titre (EN)',
        badge: 'Badge',
        badge_en: 'Badge (EN)',
        button_text: 'Libellé bouton',
        button_text_en: 'Libellé bouton (EN)',
        button_url: 'Lien du bouton',
        layout: 'Disposition',
        block_type: 'Type de bloc',
        faq_json: 'FAQ',
    };

    function flattenErrorMessages(value) {
        if (!value) return [];
        if (typeof value === 'string') return [value];
        if (Array.isArray(value)) {
            return value.flatMap((item) => flattenErrorMessages(item));
        }
        if (typeof value === 'object') {
            if (value.message) return [String(value.message)];
            return Object.values(value).flatMap((item) => flattenErrorMessages(item));
        }
        return [String(value)];
    }

    function formatFormsetErrors(errors, labelPrefix) {
        if (!errors || typeof errors !== 'object') return '';
        const parts = [];
        flattenErrorMessages(errors.__all__).forEach((msg) => {
            parts.push(`${labelPrefix} : ${msg}`);
        });
        Object.keys(errors).forEach((key) => {
            if (key === '__all__') return;
            const idx = parseInt(key, 10);
            const rowLabel = Number.isNaN(idx) ? key : `${labelPrefix} ${idx + 1}`;
            const fieldErrors = errors[key];
            if (!fieldErrors || typeof fieldErrors !== 'object') return;
            Object.keys(fieldErrors).forEach((field) => {
                const label = BUILDER_FIELD_LABELS[field] || field;
                flattenErrorMessages(fieldErrors[field]).forEach((msg) => {
                    parts.push(`${rowLabel} · ${label} : ${msg}`);
                });
            });
        });
        return parts.slice(0, 2).join(' — ');
    }

    function applyFormsetErrorsToCards(form, errors) {
        if (!form || !errors) return;
        form.querySelectorAll('[data-block-form]').forEach((card) => {
            card.classList.remove('builder-card--error');
            const errBox = card.querySelector('[data-block-error-summary]');
            if (errBox) {
                errBox.textContent = '';
                errBox.classList.add('hidden');
            }
        });
        Object.keys(errors).forEach((key) => {
            if (key === '__all__') return;
            const card = form.querySelector(`[data-block-form][data-form-prefix="${key}"]`);
            if (!card) return;
            card.classList.add('builder-card--error');
            const summary = formatFormsetErrors({ [key]: errors[key] }, 'Bloc');
            let errBox = card.querySelector('[data-block-error-summary]');
            if (!errBox) {
                errBox = document.createElement('div');
                errBox.setAttribute('data-block-error-summary', '');
                errBox.className = 'text-red-600 dark:text-red-400 text-xs rounded-lg bg-red-50 dark:bg-red-900/20 p-3 mb-3';
                const body = card.querySelector('.p-4, .p-5');
                if (body) body.prepend(errBox);
            }
            errBox.textContent = summary;
            errBox.classList.remove('hidden');
        });
    }

    function deleteOrphanBlock(blockId) {
        const base = window.DASHBOARD_API?.deleteBlock;
        if (!base || !blockId) return Promise.resolve();
        const url = `${base}${blockId}/delete/`;
        return fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrf() },
            credentials: 'same-origin',
        }).catch((err) => {
            console.warn('[builder] suppression bloc orphelin', blockId, err);
        });
    }

    function reloadPreviewIframe(previewUrl) {
        const iframe = document.getElementById('pagePreviewIframe');
        if (!iframe || !previewUrl) return;
        const sep = previewUrl.includes('?') ? '&' : '?';
        iframe.src = previewUrl + sep + '_=' + Date.now();
    }

    function findBlockCardForMapping(form, item) {
        let card = form.querySelector(`[data-block-form][data-form-prefix="${item.form_prefix}"]`);
        if (!card && item.id) {
            card = form.querySelector(`[data-block-form][data-block-pk="${item.id}"]`);
        }
        if (!card) {
            const list = form.querySelector('[data-block-forms]');
            const rows = list
                ? [...list.querySelectorAll('[data-block-form]:not(.hidden)')].filter(
                    (r) => !r.closest('[data-block-empty-template]'),
                )
                : [];
            const idx = parseInt(item.form_prefix, 10);
            if (!Number.isNaN(idx) && rows[idx]) card = rows[idx];
        }
        return card;
    }

    function applyBlockMapping(form, blocks) {
        const pending = [...form.querySelectorAll('[data-block-form][data-awaiting-id="1"]')];
        if (!blocks || !blocks.length) {
            window.DashboardBlockEditor?.syncBlockFormsetManagement?.(form);
            return;
        }
        blocks.forEach((item) => {
            let card = findBlockCardForMapping(form, item);
            if (!card && pending.length) {
                card = pending.shift();
            }
            if (!card) {
                if (item.id && !form.querySelector(`[data-block-form][data-block-pk="${item.id}"]`)) {
                    deleteOrphanBlock(item.id);
                }
                return;
            }

            window.DashboardBlockEditor?.applyBlockPkToCard?.(card, item);

            if (item.image_url) {
                const imageField = card.querySelector('[data-block-image-field]');
                const target = imageField
                    ? (imageField.querySelector('[data-media-container]') || imageField)
                    : card;
                window.DashboardBlockEditor?.updateMediaUrl?.(target, item.image_url);
            }

            if (card.querySelector('[data-block-gallery-section]')) {
                window.DashboardBlockEditor?.enableGalleryBlock?.(form, card, item.id);
            }
        });
        window.DashboardBlockEditor?.syncBlockIdsToInputs?.(form);
        window.DashboardBlockEditor?.syncBlockFormsetManagement?.(form);
    }

    function applyImageMapping(form, images) {
        if (!images || !images.length) {
            window.DashboardBlockEditor?.syncImageFormsetManagement?.(form);
            return;
        }
        images.forEach((item) => {
            let row = form.querySelector(`[data-block-image-form][data-form-prefix="${item.form_prefix}"]`);
            if (!row && item.id) {
                row = form.querySelector(`[data-block-image-form][data-image-pk="${item.id}"]`);
            }
            if (!row) return;
            row.setAttribute('data-image-pk', String(item.id));
            row.setAttribute('data-block-id', String(item.block_id));
            row.setAttribute('data-form-prefix', String(item.form_prefix));
            const idInput = row.querySelector('input[name^="images-"][name$="-id"]');
            if (idInput) idInput.value = String(item.id);
            const blockInput = row.querySelector('input[name^="images-"][name$="-block"]');
            if (blockInput) blockInput.value = String(item.block_id);
            const delBtn = row.querySelector('[data-delete-block-image]');
            if (delBtn) {
                delBtn.setAttribute('data-image-pk', String(item.id));
                delBtn.removeAttribute('data-delete-new');
            }
            if (item.image_url) {
                window.DashboardBlockEditor?.updateMediaUrl?.(row, item.image_url);
            }
        });
        window.DashboardBlockEditor?.syncImageFormsetManagement?.(form);
    }

    function initAutosave(form, config) {
        if (!form || !config.saveUrl) return null;
        if (form._builderSync) return form._builderSync;

        const statusEl = document.querySelector('[data-builder-save-status]');
        const publishBtn = document.querySelector('[data-builder-publish]');
        const draftBtn = document.querySelector('[data-builder-draft]');
        const publishedInput = document.getElementById('builderIsPublished');
        let timer = null;
        let inflight = null;
        let dirty = false;
        let pendingImmediate = false;
        let pendingResave = false;
        let suppressUntil = 0;

        const isAutosavePaused = () => Date.now() < suppressUntil;

        const pauseAutosave = (ms) => {
            suppressUntil = Math.max(suppressUntil, Date.now() + ms);
        };

        const markDirty = () => {
            dirty = true;
            if (inflight) pendingResave = true;
            if (!inflight) {
                setStatus(statusEl, 'idle', 'Synchronisation…');
            }
        };

        const scheduleSave = (immediate, options) => {
            if (isAutosavePaused() && !(options && options.force)) return Promise.resolve();

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
                if (isAutosavePaused()) {
                    scheduleSave(false);
                    return;
                }
                syncNow(false);
            }, DEBOUNCE_MS);
            return Promise.resolve();
        };

        const syncNow = async (action) => {
            const publish = action === 'publish';
            const draft = action === 'draft';

            if (inflight) {
                pendingResave = true;
                if (publish || draft) await inflight;
                else return inflight;
            }

            if (publish && publishedInput) {
                publishedInput.value = 'on';
            } else if (draft && publishedInput) {
                publishedInput.value = '';
            }

            try {
                window.DashboardBlockEditor?.prepareForSave?.(form);
            } catch (err) {
                console.error('[builder] prepareForSave', err);
            }

            const fd = new FormData(form);
            if (publish) {
                fd.set('builder_action', 'publish');
            } else if (draft) {
                fd.set('builder_action', 'draft');
            } else {
                fd.set('builder_action', 'autosave');
            }

            setStatus(statusEl, 'saving', publish ? 'Publication…' : (draft ? 'Brouillon…' : 'Enregistrement…'));

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
                        if (data.errors.meta) {
                            errMsg = formatFormsetErrors(data.errors.meta, 'Paramètres') || 'Paramètres invalides';
                        } else if (data.errors.blocks) {
                            applyFormsetErrorsToCards(form, data.errors.blocks);
                            errMsg = formatFormsetErrors(data.errors.blocks, 'Bloc') || 'Erreur dans un bloc';
                        } else if (data.errors.images) {
                            errMsg = formatFormsetErrors(data.errors.images, 'Image') || 'Erreur dans une image';
                        }
                    }
                    setStatus(statusEl, 'error', errMsg);
                    dirty = false;
                    pendingImmediate = false;
                    throw new Error(errMsg);
                }

                dirty = false;
                pendingImmediate = false;
                form.querySelectorAll('[data-block-form].builder-card--error').forEach((card) => {
                    card.classList.remove('builder-card--error');
                    const errBox = card.querySelector('[data-block-error-summary]');
                    if (errBox) {
                        errBox.textContent = '';
                        errBox.classList.add('hidden');
                    }
                });
                const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                setStatus(
                    statusEl,
                    'saved',
                    data.is_published
                        ? (publish ? `Publiée · ${time}` : `Publiée · ${time}`)
                        : (draft ? `Brouillon · ${time}` : `Synchronisé · ${time}`),
                );

                if (publishedInput) {
                    publishedInput.value = data.is_published ? 'on' : '';
                }
                updatePublishedBadge(data.is_published);
                pauseAutosave(POST_SAVE_QUIET_MS);
                applyBlockMapping(form, data.blocks);
                applyImageMapping(form, data.images);
                window.DashboardBlockEditor?.refreshGallerySections?.(form);
                if (window.DashboardForms && window.DashboardForms.initMediaDropzones) {
                    window.DashboardForms.initMediaDropzones(form);
                }

                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        triggerLivePreview(form);
                    });
                });

                if (publish) {
                    reloadPreviewIframe(data.preview_url);
                }

                if (draft) {
                    const viewLink = document.querySelector('[data-builder-view-live]');
                    if (viewLink) viewLink.classList.add('hidden');
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
                dirty = false;
                pendingImmediate = false;
            }).finally(() => {
                inflight = null;
                if (pendingResave) {
                    pendingResave = false;
                    queueMicrotask(() => {
                        if (!isAutosavePaused()) syncNow(false);
                        else scheduleSave(false);
                    });
                }
            });

            return inflight;
        };

        const notify = (options) => {
            const immediate = !!(options && options.immediate);
            return scheduleSave(immediate, options);
        };

        const scheduleSaveFromEvent = (e) => {
            if (isAutosavePaused()) return;
            if (!e || !e.isTrusted) return;
            if (e.target && e.target.type === 'file') return;
            scheduleSave(false);
        };
        form.addEventListener('input', scheduleSaveFromEvent);
        form.addEventListener('change', scheduleSaveFromEvent);

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (timer) clearTimeout(timer);
            timer = null;
            syncNow('publish');
        });

        if (publishBtn) {
            publishBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (timer) clearTimeout(timer);
                timer = null;
                syncNow('publish');
            });
        }

        if (draftBtn) {
            draftBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (timer) clearTimeout(timer);
                timer = null;
                syncNow('draft');
            });
        }

        form._builderSync = { notify, syncNow };

        setStatus(statusEl, 'saved', 'Prêt');
        triggerLivePreview(form);

        return { notify, syncNow };
    }

    window.DashboardBuilderAutosave = { initAutosave };
})();
