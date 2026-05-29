/**
 * Dashboard — dropzones, galerie, aperçu live, suppression (modal + AJAX).
 */
(function (global) {
    const getCsrf = () => {
        const el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : (global.DASHBOARD_API && global.DASHBOARD_API.csrf) || '';
    };

    const confirmModal = () => document.getElementById('dashConfirmModal');

    function dashboardConfirm({ title, message }) {
        return new Promise((resolve) => {
            const modal = confirmModal();
            if (!modal) {
                resolve(global.confirm(message || title));
                return;
            }
            modal.querySelector('[data-confirm-title]').textContent = title || 'Confirmer';
            modal.querySelector('[data-confirm-message]').textContent = message || 'Êtes-vous sûr ?';
            modal.classList.remove('hidden');
            const onOk = () => { cleanup(); resolve(true); };
            const onCancel = () => { cleanup(); resolve(false); };
            const okBtn = modal.querySelector('[data-confirm-ok]');
            const cancelBtn = modal.querySelector('[data-confirm-cancel]');
            const backdrop = modal.querySelector('[data-confirm-backdrop]');
            const cleanup = () => {
                modal.classList.add('hidden');
                okBtn.removeEventListener('click', onOk);
                cancelBtn.removeEventListener('click', onCancel);
                backdrop.removeEventListener('click', onCancel);
            };
            okBtn.addEventListener('click', onOk);
            cancelBtn.addEventListener('click', onCancel);
            backdrop.addEventListener('click', onCancel);
        });
    }

    async function deleteGalleryImage(pk, model) {
        const base = global.DASHBOARD_API && global.DASHBOARD_API.deleteGalleryImage;
        if (!base || !pk) return false;
        const url = base + pk + '/delete/';
        const body = new FormData();
        body.append('model', model || 'gallery');
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrf() },
            body,
            credentials: 'same-origin',
        });
        return res.ok;
    }

    async function deleteSiteLink(pk) {
        const tpl = global.DASHBOARD_API && global.DASHBOARD_API.deleteSiteLink;
        if (!tpl || !pk) return false;
        const url = tpl.replace(/\/0\//, `/${pk}/`);
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrf() },
            credentials: 'same-origin',
        });
        return res.ok;
    }

    function setDropzoneActive(zone, active) {
        if (!zone) return;
        zone.classList.toggle('border-emerald-500', active);
        zone.classList.toggle('bg-emerald-50', active);
        zone.classList.toggle('dark:bg-emerald-900/20', active);
        zone.classList.toggle('border-gray-300', !active);
        zone.classList.toggle('dark:border-gray-600', !active);
    }

    function toAbsoluteMediaUrl(url) {
        if (!url) return '';
        if (url.startsWith('data:') || url.startsWith('blob:') || url.startsWith('http://') || url.startsWith('https://')) {
            return url;
        }
        try {
            return new URL(url, window.location.origin).href;
        } catch (e) {
            return url;
        }
    }

    function readFileAsDataUrl(file) {
        return new Promise((resolve) => {
            if (!file) {
                resolve('');
                return;
            }
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result || '');
            reader.onerror = () => resolve('');
            reader.readAsDataURL(file);
        });
    }

    function getMediaContainer(root) {
        if (!root) return null;
        if (root.matches && root.matches('[data-media-container]')) return root;
        return root.querySelector('[data-media-container]') || root;
    }

    function setMediaPreviewSrc(root, url) {
        const container = getMediaContainer(root);
        if (!container || !url) return;
        const absolute = toAbsoluteMediaUrl(url);
        container.dataset.previewSrc = absolute;
        const preview = container.querySelector('[data-preview-image]');
        const existing = container.querySelector('[data-existing-image]');
        if (preview) {
            preview.src = absolute;
            preview.classList.remove('hidden');
        }
        if (existing) {
            existing.src = absolute;
            existing.classList.remove('hidden');
        }
    }

    function clearMediaPreviewSrc(root) {
        const container = getMediaContainer(root);
        if (!container) return;
        delete container.dataset.previewSrc;
        container.querySelectorAll('[data-preview-image], [data-existing-image]').forEach((img) => {
            img.removeAttribute('src');
            img.classList.add('hidden');
        });
    }

    function getMediaPreviewUrl(root) {
        const container = getMediaContainer(root);
        if (!container) return '';
        if (container.dataset.previewSrc) {
            return container.dataset.previewSrc;
        }
        const preview = container.querySelector('[data-preview-image]');
        if (preview && preview.src && !preview.classList.contains('hidden')) {
            return toAbsoluteMediaUrl(preview.src);
        }
        const existing = container.querySelector('[data-existing-image]');
        if (existing && existing.src && !existing.classList.contains('hidden')) {
            return toAbsoluteMediaUrl(existing.src);
        }
        return '';
    }

    async function applyFileToMediaPreview(container, file) {
        if (!container || !file) return;
        const dataUrl = await readFileAsDataUrl(file);
        if (dataUrl) {
            setMediaPreviewSrc(container, dataUrl);
        }
    }

    function setSingleFile(input, file) {
        if (!input || !file) return;
        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function clearFileInput(input) {
        if (!input) return;
        try {
            input.files = new DataTransfer().files;
        } catch (e) {
            input.value = '';
        }
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function triggerPreviewUpdate(form) {
        if (form && typeof form._previewSchedule === 'function') {
            form._previewSchedule();
        } else if (form) {
            form.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    function getGalleryUrlsFromForm(form) {
        const urls = [];
        if (!form) return urls;
        form.querySelectorAll('[data-gallery-form]').forEach((row) => {
            if (row.classList.contains('hidden')) return;
            const del = row.querySelector('input[name$="-DELETE"]');
            if (del && del.checked) return;
            const url = getMediaPreviewUrl(row);
            if (url) urls.push(url);
        });
        return urls;
    }

    function notifyFormMediaChange(form) {
        triggerPreviewUpdate(form);
        if (form && form._builderSync) {
            form._builderSync.notify({ immediate: true });
        }
    }

    async function handleMediaInputChange(container, input, formRoot) {
        const zone = container.querySelector('.media-dropzone');
        const clearBtn = container.querySelector('[data-clear-file]');
        const preview = container.querySelector('[data-preview-image]');
        const existing = container.querySelector('[data-existing-image]');

        if (input && input.files && input.files[0]) {
            await applyFileToMediaPreview(container, input.files[0]);
            if (existing) existing.classList.add('hidden');
        }

        if (zone && input) {
            const fn = zone.querySelector('[data-filename]');
            if (fn) fn.textContent = input.files && input.files[0] ? input.files[0].name : '';
            const has = !!getMediaPreviewUrl(container);
            if (clearBtn) {
                clearBtn.disabled = !has;
                clearBtn.classList.toggle('opacity-50', !has);
                clearBtn.classList.toggle('cursor-not-allowed', !has);
            }
        }

        if (formRoot.getAttribute('data-preview-type') === 'custom-page') {
            notifyFormMediaChange(formRoot);
        } else {
            triggerPreviewUpdate(formRoot);
        }
    }

    function initMediaDropzones(scope) {
        if (!scope) return;
        const formRoot = scope.closest('form') || scope;
        const searchRoot = scope.matches('form') ? scope : scope;
        searchRoot.querySelectorAll('[data-media-container]').forEach((container) => {
            const input = container.querySelector('input[type="file"]');
            const zone = container.querySelector('.media-dropzone');
            const clearBtn = container.querySelector('[data-clear-file]');
            const flagName = container.getAttribute('data-clear-flag-name');
            const flagInput = flagName ? form.querySelector(`input[name="${flagName}"]`) : null;

            if (container.dataset.mediaDropzoneBound === '1') return;
            container.dataset.mediaDropzoneBound = '1';

            if (zone && input) {
                zone.addEventListener('click', (e) => {
                    if (e.target.closest('[data-clear-file]')) return;
                    input.click();
                });
                zone.addEventListener('dragover', (e) => { e.preventDefault(); setDropzoneActive(zone, true); });
                zone.addEventListener('dragleave', () => setDropzoneActive(zone, false));
                zone.addEventListener('drop', (e) => {
                    e.preventDefault();
                    setDropzoneActive(zone, false);
                    const f = e.dataTransfer.files && e.dataTransfer.files[0];
                    if (f) setSingleFile(input, f);
                });
                input.addEventListener('change', (e) => {
                    e.stopPropagation();
                    handleMediaInputChange(container, input, formRoot);
                });
            }
            if (clearBtn) {
                clearBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    try {
                        input.files = new DataTransfer().files;
                    } catch (err) {
                        input.value = '';
                    }
                    if (flagInput) flagInput.value = '1';
                    clearMediaPreviewSrc(container);
                    if (zone) {
                        const fn = zone.querySelector('[data-filename]');
                        if (fn) fn.textContent = '';
                    }
                    clearBtn.disabled = true;
                    clearBtn.classList.add('opacity-50', 'cursor-not-allowed');
                    if (formRoot.getAttribute('data-preview-type') === 'custom-page') {
                        notifyFormMediaChange(formRoot);
                    } else {
                        triggerPreviewUpdate(formRoot);
                    }
                });
            }
            if (container.dataset.previewSrc || container.querySelector('[data-existing-image]')?.src) {
                const existing = container.querySelector('[data-existing-image]');
                if (existing && existing.src && !container.dataset.previewSrc) {
                    setMediaPreviewSrc(container, existing.src);
                }
            }
        });
    }

    function initGallerySection(form) {
        const section = form.querySelector('[data-gallery-section]');
        if (!section) return () => {};
        const max = parseInt(section.getAttribute('data-gallery-max') || '50', 10);
        const model = section.getAttribute('data-formset-type') || 'gallery';
        const totalInput = section.querySelector('input[name$="-TOTAL_FORMS"]');
        const formsContainer = section.querySelector('[data-gallery-forms]');
        const template = section.querySelector('[data-gallery-empty-template]');
        const prefix = totalInput ? totalInput.name.replace('-TOTAL_FORMS', '') : '';

        const updateIndices = () => {
            formsContainer.querySelectorAll('[data-gallery-form]').forEach((el, idx) => {
                const t = el.querySelector('[data-gallery-index]');
                if (t) t.textContent = String(idx + 1);
            });
            const countEl = section.querySelector('[data-gallery-count]');
            const n = formsContainer.querySelectorAll('[data-gallery-form]').length;
            if (countEl) countEl.textContent = `(${Math.min(n, max)}/${max})`;
        };

        const addForm = () => {
            if (!template || !totalInput) return null;
            const index = parseInt(totalInput.value, 10);
            if (index >= max) return null;
            const html = template.innerHTML.replace(/__prefix__/g, index);
            const wrap = document.createElement('div');
            wrap.innerHTML = html;
            const node = wrap.firstElementChild;
            formsContainer.appendChild(node);
            totalInput.value = index + 1;
            initMediaDropzones(form);
            bindDeleteButtons(form, model);
            updateIndices();
            return node;
        };

        const multiInput = section.querySelector('[data-gallery-multi-input]');
        const multiBtn = section.querySelector('[data-gallery-multi-button]');
        const addBtn = section.querySelector('[data-gallery-add-one]');
        const dropzone = section.querySelector('[data-gallery-dropzone]');

        if (multiBtn && multiInput) {
            multiBtn.addEventListener('click', () => multiInput.click());
            multiInput.addEventListener('change', () => {
                Array.from(multiInput.files || []).forEach((file) => {
                    const node = addForm();
                    if (!node) return;
                    const inp = node.querySelector('input[type="file"][name$="-image"]');
                    setSingleFile(inp, file);
                });
                multiInput.value = '';
            });
        }
        if (addBtn) addBtn.addEventListener('click', () => {
            addForm();
            triggerPreviewUpdate(form);
        });
        if (dropzone) {
            dropzone.addEventListener('dragover', (e) => { e.preventDefault(); setDropzoneActive(dropzone, true); });
            dropzone.addEventListener('dragleave', () => setDropzoneActive(dropzone, false));
            dropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                setDropzoneActive(dropzone, false);
                Array.from(e.dataTransfer.files || []).forEach((file) => {
                    if (!file.type.startsWith('image/')) return;
                    const node = addForm();
                    if (!node) return;
                    setSingleFile(node.querySelector('input[type="file"][name$="-image"]'), file);
                });
            });
        }

        updateIndices();
        return { updateIndices, model };
    }

    function removeGalleryRow(row, form) {
        const del = row.querySelector('input[name$="-DELETE"]');
        if (del) del.checked = true;
        row.classList.add('hidden');
        const section = form.querySelector('[data-gallery-section]');
        if (section) {
            const totalInput = section.querySelector('input[name$="-TOTAL_FORMS"]');
            /* keep TOTAL_FORMS — django formset handles deleted */
        }
    }

    function bindDeleteButtons(form, defaultModel) {
        form.querySelectorAll('[data-delete-gallery-row]').forEach((btn) => {
            if (btn.dataset.bound) return;
            btn.dataset.bound = '1';
            btn.addEventListener('click', async () => {
                const row = btn.closest('[data-gallery-form]');
                const pk = row && row.getAttribute('data-image-pk');
                const section = form.querySelector('[data-gallery-section]');
                const model = (section && section.getAttribute('data-formset-type')) || defaultModel || 'gallery';
                const ok = await dashboardConfirm({
                    title: 'Supprimer cette image ?',
                    message: 'Cette action est définitive après enregistrement ou immédiate si déjà en ligne.',
                });
                if (!ok) return;
                if (pk && !btn.hasAttribute('data-delete-new')) {
                    const done = await deleteGalleryImage(pk, model);
                    if (!done) return;
                }
                if (btn.hasAttribute('data-delete-new')) {
                    row.remove();
                    const section = form.querySelector('[data-gallery-section]');
                    const totalInput = section && section.querySelector('input[name$="-TOTAL_FORMS"]');
                    if (totalInput) totalInput.value = Math.max(0, parseInt(totalInput.value, 10) - 1);
                } else {
                    removeGalleryRow(row, form);
                }
                form.dispatchEvent(new Event('change', { bubbles: true }));
            });
        });
    }

    function initPagePreview(form, iframe, deviceFrame, previewType) {
        if (!form || !iframe || !deviceFrame) return;
        const previewArea = deviceFrame.parentElement;
        let currentDevice = 'desktop';
        const msgType = previewType === 'home' ? 'home-preview' : (previewType === 'custom-page' ? 'custom-page-preview' : 'page-preview');

        const applyIframeZoom = (scale) => {
            const s = Math.max(0.2, Math.min(scale, 1));
            if (s === 1) {
                iframe.style.transform = iframe.style.width = iframe.style.height = '';
                return;
            }
            iframe.style.transformOrigin = '0 0';
            iframe.style.transform = `scale(${s})`;
            iframe.style.width = `calc(100% / ${s})`;
            iframe.style.height = `calc((100% - 2.5rem) / ${s})`;
        };

        const applyDeviceLayout = () => {
            if (currentDevice === 'mobile') {
                const w = 390, h = 844;
                deviceFrame.style.width = w + 'px';
                deviceFrame.style.height = h + 'px';
                const scale = Math.min(previewArea.clientWidth / w, previewArea.clientHeight / h, 1);
                deviceFrame.style.transform = `scale(${scale || 1})`;
                applyIframeZoom(1);
                return;
            }
            deviceFrame.style.width = deviceFrame.style.height = deviceFrame.style.transform = '';
            applyIframeZoom(currentDevice === 'tablet' ? 0.85 : 0.5);
        };

        document.querySelectorAll('.device-btn').forEach((btn) => {
            btn.addEventListener('click', () => {
                currentDevice = btn.getAttribute('data-device') || 'desktop';
                document.querySelectorAll('.device-btn').forEach((b) => {
                    const active = b === btn;
                    b.classList.toggle('bg-emerald-600', active);
                    b.classList.toggle('text-white', active);
                    b.classList.toggle('bg-gray-100', !active);
                    b.classList.toggle('dark:bg-gray-700', !active);
                    b.classList.toggle('text-gray-800', !active);
                    b.classList.toggle('dark:text-white', !active);
                });
                applyDeviceLayout();
            });
        });
        window.addEventListener('resize', applyDeviceLayout);
        applyDeviceLayout();

        const getSiteLinksFromForm = () => {
            const links = [];
            form.querySelectorAll('[data-link-card]').forEach((card) => {
                if (card.classList.contains('hidden')) return;
                const del = card.querySelector('input[name$="-DELETE"]');
                if (del && del.checked) return;
                const url = (card.querySelector('input[name$="-url"]')?.value || '').trim();
                const routeName = card.querySelector('select[name$="-route_name"]')?.value || '';
                if (!url && !routeName) return;
                const active = card.querySelector('input[name$="-is_active"]');
                if (active && !active.checked) return;
                const newTab = card.querySelector('input[name$="-open_in_new_tab"]');
                const routes = global.SITE_ROUTE_URLS || {};
                let href = url;
                if (routeName && routes[routeName]) {
                    href = routes[routeName];
                } else if (routeName && !href) {
                    href = '#';
                }
                links.push({
                    url: href,
                    route_name: routeName,
                    platform: card.querySelector('select[name$="-platform"]')?.value || 'other',
                    label: card.querySelector('input[name$="-label"]')?.value || '',
                    category: card.querySelector('select[name$="-category"]')?.value || 'social',
                    open_in_new_tab: !newTab || newTab.checked,
                    order: parseInt(card.querySelector('input[name$="-order"]')?.value || '0', 10) || 0,
                });
            });
            links.sort((a, b) => a.order - b.order);
            return links;
        };

        const buildPayload = () => {
            if (window.DashboardBlockEditor && typeof window.DashboardBlockEditor.syncBeforePreview === 'function') {
                window.DashboardBlockEditor.syncBeforePreview(form);
            }

            const payload = {};
            form.querySelectorAll('input, textarea, select').forEach((el) => {
                if (!el.name || el.type === 'file') return;
                if (el.name.includes('-DELETE')) return;
                if (el.type === 'checkbox') return;
                payload[el.name] = el.value;
            });
            if (previewType === 'custom-page') {
                payload.page_title = form.querySelector('[name="title"]')?.value || '';
                payload.page_title_en = form.querySelector('[name="title_en"]')?.value || '';
                payload.blocks = [];

                const getFieldVal = (card, suffix) => {
                    const el = card.querySelector(`[name$="-${suffix}"]`);
                    if (!el) return '';
                    if (window.CKEDITOR && el.id && window.CKEDITOR.instances[el.id]) {
                        return window.CKEDITOR.instances[el.id].getData();
                    }
                    return el.value || '';
                };

                const getImageUrl = (root) => getMediaPreviewUrl(root);

                let blockIdx = 0;
                form.querySelectorAll('[data-block-form]').forEach((card) => {
                    if (card.classList.contains('hidden')) return;
                    if (card.closest('[data-block-empty-template]')) return;
                    const del = card.querySelector('input[name$="-DELETE"]');
                    if (del && del.checked) return;

                    const block = {
                        id: card.getAttribute('data-block-pk') || '',
                        index: blockIdx,
                        block_type: getFieldVal(card, 'block_type'),
                        title: getFieldVal(card, 'title'),
                        title_en: getFieldVal(card, 'title_en'),
                        subtitle: getFieldVal(card, 'subtitle'),
                        subtitle_en: getFieldVal(card, 'subtitle_en'),
                        badge: getFieldVal(card, 'badge'),
                        badge_en: getFieldVal(card, 'badge_en'),
                        content: getFieldVal(card, 'content'),
                        content_en: getFieldVal(card, 'content_en'),
                        video_url: getFieldVal(card, 'video_url'),
                        button_text: getFieldVal(card, 'button_text'),
                        button_text_en: getFieldVal(card, 'button_text_en'),
                        button_url: getFieldVal(card, 'button_url'),
                        layout: getFieldVal(card, 'layout'),
                        faq_json: getFieldVal(card, 'faq_json'),
                        gallery_urls: [],
                    };
                    blockIdx += 1;

                    const mediaContainer = card.querySelector('[data-media-container]');
                    block.image_url = getImageUrl(mediaContainer);

                    const blockId = card.getAttribute('data-block-pk');
                    const cardIndex = card.getAttribute('data-block-index');
                    const imageSelector = blockId
                        ? `[data-block-image-form][data-block-id="${blockId}"]`
                        : `[data-block-image-form][data-block-card-index="${cardIndex}"]`;
                    form.querySelectorAll(`${imageSelector}:not(.hidden)`).forEach((row) => {
                        if (row.closest('[data-block-image-empty-template]')) return;
                        if (row.querySelector('input[name$="-DELETE"]')?.checked) return;
                        const url = getImageUrl(row);
                        if (url) block.gallery_urls.push(url);
                    });

                    payload.blocks.push(block);
                });
            } else {
                payload.site_links = getSiteLinksFromForm();
                const profile = form.querySelector('input[type="file"][name="profile_image"]');
                if (profile && profile.files && profile.files[0]) {
                    payload.profile_image_url = URL.createObjectURL(profile.files[0]);
                } else {
                    const ex = form.querySelector('[data-existing-file="profile_image"]');
                    if (ex) payload.profile_image_url = ex.src;
                }
                payload.gallery_image_urls = getGalleryUrlsFromForm(form);
            }
            return payload;
        };

        let raf = null;
        const send = () => {
            if (!iframe.contentWindow) return;
            iframe.contentWindow.postMessage({ type: msgType, payload: buildPayload() }, '*');
        };
        const schedulePreview = () => {
            if (raf) cancelAnimationFrame(raf);
            raf = requestAnimationFrame(send);
        };
        form._previewSchedule = schedulePreview;
        const schedulePreviewFromEvent = (e) => {
            if (e && e.target && e.target.type === 'file') return;
            schedulePreview();
        };
        form.addEventListener('input', schedulePreviewFromEvent);
        form.addEventListener('change', schedulePreviewFromEvent);
        iframe.addEventListener('load', schedulePreview);
        window.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'page-preview-ready') schedulePreview();
        });
        schedulePreview();
    }

    function initSiteLinksForm(form) {
        if (!form) return;
        form.querySelectorAll('[data-link-card]').forEach((card) => {
            const catSelect = card.querySelector('select[name$="-category"]');
            if (!catSelect) return;
            const sync = () => {
                card.dataset.linkCategory = catSelect.value;
            };
            sync();
            if (!catSelect.dataset.boundCategory) {
                catSelect.dataset.boundCategory = '1';
                catSelect.addEventListener('change', sync);
            }
        });
        form.querySelectorAll('[data-delete-link]').forEach((btn) => {
            btn.addEventListener('click', async () => {
                const pk = btn.getAttribute('data-link-pk');
                const card = btn.closest('[data-link-card]');
                const ok = await dashboardConfirm({
                    title: 'Supprimer ce lien ?',
                    message: 'Le lien sera retiré du site immédiatement.',
                });
                if (!ok) return;
                if (btn.hasAttribute('data-delete-new-link')) {
                    if (card) card.remove();
                    return;
                }
                if (pk) {
                    const done = await deleteSiteLink(pk);
                    if (!done) return;
                }
                if (card) card.remove();
            });
        });
    }

    function initForm(form) {
        if (!form) return;
        const previewType = form.getAttribute('data-preview-type') || 'page';
        const iframe = document.getElementById('pagePreviewIframe') || document.getElementById('homePreviewIframe');
        const deviceFrame = document.getElementById('pageDeviceFrame') || document.getElementById('deviceFrame');
        initMediaDropzones(form);
        const gallery = initGallerySection(form);
        bindDeleteButtons(form, gallery && gallery.model);
        if (form.querySelector('[data-link-card]')) initSiteLinksForm(form);
        initPagePreview(form, iframe, deviceFrame, previewType);
    }

    global.DashboardForms = {
        confirm: dashboardConfirm,
        init: initForm,
        initSiteLinks: initSiteLinksForm,
        initMediaDropzones,
        bindDeleteButtons,
        triggerPreviewUpdate,
        setMediaPreviewSrc,
        getMediaPreviewUrl,
        toAbsoluteMediaUrl,
    };

    document.addEventListener('DOMContentLoaded', () => {
        const pageForm = document.getElementById('pageSettingsForm');
        const homeForm = document.getElementById('homeSettingsForm');
        if (pageForm && pageForm.getAttribute('data-preview-type') !== 'custom-page') initForm(pageForm);
        if (homeForm) bindDeleteButtons(homeForm, 'home');
    });
})(window);
