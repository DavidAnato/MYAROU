(function () {
    'use strict';

    function getTotalInput(form, prefix) {
        return form.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
    }

    function getInitialInput(form, prefix) {
        return form.querySelector(`input[name="${prefix}-INITIAL_FORMS"]`);
    }

    function syncBlockIdsToInputs(form) {
        if (!form) return;
        form.querySelectorAll('[data-block-form]').forEach((card) => {
            if (card.closest('[data-block-empty-template]') || card.classList.contains('hidden')) return;
            const pk = card.getAttribute('data-block-pk');
            const idInput = card.querySelector('input[name^="blocks-"][name$="-id"]');
            if (pk && idInput) idInput.value = String(pk);
        });
    }

    function syncBlockFormsetManagement(form) {
        const list = form.querySelector('[data-block-forms]');
        const totalInput = getTotalInput(form, 'blocks');
        const initialInput = getInitialInput(form, 'blocks');
        if (!list || !totalInput) return;

        const rows = [...list.querySelectorAll('[data-block-form]')].filter(
            (row) => !row.closest('[data-block-empty-template]'),
        );
        const withPk = rows.filter((row) => {
            const v = row.querySelector('input[name^="blocks-"][name$="-id"]')?.value;
            return v && String(v).trim() !== '';
        });
        totalInput.value = String(rows.length);
        if (initialInput) initialInput.value = String(withPk.length);
    }

    function syncImageFormsetManagement(form) {
        const totalInput = getTotalInput(form, 'images');
        const initialInput = getInitialInput(form, 'images');
        if (!totalInput) return;

        const rows = [...form.querySelectorAll('[data-block-image-form]')].filter(
            (row) => !row.closest('[data-block-image-empty-template]'),
        );
        const withPk = rows.filter((row) => {
            const v = row.querySelector('input[name^="images-"][name$="-id"]')?.value;
            return v && String(v).trim() !== '';
        });
        totalInput.value = String(rows.length);
        if (initialInput) initialInput.value = String(withPk.length);
    }

    function applyBlockPkToCard(card, item) {
        if (!card || !item || !item.id) return;
        card.setAttribute('data-block-pk', String(item.id));
        card.setAttribute('data-form-prefix', String(item.form_prefix));
        card.removeAttribute('data-awaiting-id');
        const idInput = card.querySelector('input[name^="blocks-"][name$="-id"]');
        if (idInput) idInput.value = String(item.id);
    }

    function getVisibleBlockCards(list) {
        if (!list) return [];
        return [...list.querySelectorAll('[data-block-form]:not(.hidden)')].filter(
            (card) => !card.closest('[data-block-empty-template]')
        );
    }

    function updateBlockCount(section) {
        const list = section?.querySelector('[data-block-forms]');
        const countEl = section?.querySelector('[data-block-count]');
        const emptyState = section?.querySelector('[data-block-empty-state]');
        const count = getVisibleBlockCards(list).length;

        if (countEl) {
            countEl.textContent = count === 0 ? '0' : count === 1 ? '1 bloc' : `${count} blocs`;
        }
        if (emptyState) {
            emptyState.classList.toggle('hidden', count > 0);
        }
    }

    function reindexBlockCards(list) {
        if (!list) return;
        getVisibleBlockCards(list).forEach((card, idx) => {
            card.setAttribute('data-block-index', String(idx));
            const orderInput = card.querySelector('input[name$="-order"]');
            if (orderInput) orderInput.value = idx * 10;
            const gallery = card.querySelector('[data-block-gallery-images]');
            if (gallery) gallery.setAttribute('data-block-card-index', String(idx));
        });
    }

    function destroyCKEditorIn(root) {
        if (!window.CKEDITOR) return;
        root.querySelectorAll('textarea[id]').forEach((ta) => {
            if (CKEDITOR.instances[ta.id]) {
                try {
                    CKEDITOR.instances[ta.id].updateElement();
                    CKEDITOR.instances[ta.id].destroy(true);
                } catch (e) { /* ignore */ }
            }
        });
    }

    function blockCardUsesContent(card) {
        if (!card) return false;
        const type = card.querySelector('[name$="-block_type"]')?.value || '';
        return type === 'richtext' || type === 'image_text';
    }

    function initCKEditorIn(root) {
        if (!window.CKEDITOR) return;
        const card = root.closest('[data-block-form]');
        if (card && !blockCardUsesContent(card)) return;
        const form = root.closest('form') || document.getElementById('pageSettingsForm');
        root.querySelectorAll('textarea[id]').forEach((ta) => {
            if (ta.closest('[data-block-empty-template]')) return;
            if (!ta.id.includes('content')) return;

            if (CKEDITOR.instances[ta.id]) {
                window.DashboardCKEditorFix?.setupEditor?.(CKEDITOR.instances[ta.id]);
                return;
            }

            try {
                const editor = CKEDITOR.replace(ta.id);
                if (editor) {
                    editor.on('instanceReady', () => {
                        window.DashboardCKEditorFix?.setupEditor?.(editor);
                    });
                }
            } catch (e) { /* ignore */ }
        });
    }

    function clearHiddenBlockFields(card, blockType) {
        if (!card || !blockType) return;
        const uses = {
            video: blockType === 'video',
            image: ['hero', 'image', 'image_text'].includes(blockType),
            content: ['richtext', 'image_text'].includes(blockType),
            cta: blockType === 'cta',
            badge: blockType === 'hero',
            subtitle: ['hero', 'video', 'cta'].includes(blockType),
        };
        if (!uses.video) {
            const el = card.querySelector('[name$="-video_url"]');
            if (el) el.value = '';
        }
        if (!uses.cta) {
            card.querySelectorAll('[name$="-button_text"], [name$="-button_text_en"], [name$="-button_url"]')
                .forEach((el) => { el.value = ''; });
        }
        if (!uses.badge) {
            card.querySelectorAll('[name$="-badge"], [name$="-badge_en"]').forEach((el) => { el.value = ''; });
        }
        if (!uses.subtitle) {
            card.querySelectorAll('[name$="-subtitle"], [name$="-subtitle_en"]').forEach((el) => { el.value = ''; });
        }
        if (!uses.content) {
            card.querySelectorAll('[name$="-content"], [name$="-content_en"]').forEach((el) => { el.value = ''; });
            destroyCKEditorIn(card);
        }
    }

    function updateLayoutSelect(card, blockType) {
        if (!card) return;
        const wrap = card.querySelector('[data-block-layout-field]');
        const select = card.querySelector('select[name^="blocks-"][name$="-layout"]');
        if (!wrap || !select) return;

        const layouts = window.BUILDER_LAYOUTS && window.BUILDER_LAYOUTS[blockType];
        if (!layouts || !layouts.length) {
            wrap.classList.add('hidden');
            select.value = '';
            return;
        }

        wrap.classList.remove('hidden');
        const current = select.value;
        const defaultVal = (window.BUILDER_LAYOUT_DEFAULTS && window.BUILDER_LAYOUT_DEFAULTS[blockType])
            || layouts[0][0];
        select.innerHTML = layouts.map(([value, label]) => (
            `<option value="${String(value).replace(/"/g, '&quot;')}">${String(label).replace(/</g, '&lt;')}</option>`
        )).join('');
        select.value = layouts.some(([v]) => v === current) ? current : defaultVal;
    }

    function getRowFormIndex(row, prefix) {
        const attr = row.getAttribute('data-form-prefix');
        if (attr !== null && attr !== '') {
            const n = parseInt(attr, 10);
            if (!Number.isNaN(n)) return n;
        }
        const el = row.querySelector(`[name^="${prefix}-"]`);
        if (el && el.name) {
            const m = el.name.match(new RegExp(`^${prefix}-(\\d+)-`));
            if (m) return parseInt(m[1], 10);
        }
        return null;
    }

    function renumberBlockFormPrefixes(form, list, options) {
        const reinitEditors = !options || options.reinitEditors !== false;
        const rows = [...list.querySelectorAll('[data-block-form]')].filter(
            (row) => !row.closest('[data-block-empty-template]'),
        );
        const visible = rows.filter((r) => !r.classList.contains('hidden'));
        const hidden = rows.filter((r) => r.classList.contains('hidden'));
        const ordered = [...visible, ...hidden];
        let changed = false;

        ordered.forEach((row, newIdx) => {
            const currentIdx = getRowFormIndex(row, 'blocks');
            if (currentIdx === newIdx) return;
            changed = true;
            destroyCKEditorIn(row);
            row.querySelectorAll('[name^="blocks-"]').forEach((el) => {
                el.name = el.name.replace(/^blocks-\d+-/, `blocks-${newIdx}-`);
                if (el.id) el.id = el.id.replace(/^id_blocks-\d+-/, `id_blocks-${newIdx}-`);
            });
            row.setAttribute('data-form-prefix', String(newIdx));
            if (reinitEditors) initCKEditorIn(row);
        });

        const totalInput = getTotalInput(form, 'blocks');
        if (totalInput) totalInput.value = ordered.length;
        reindexBlockCards(list);
        return changed;
    }

    function reinitAllEditors(form) {
        if (!form) return;
        form.querySelectorAll('[data-block-form]').forEach((card) => {
            if (card.closest('[data-block-empty-template]') || card.classList.contains('hidden')) return;
            initCKEditorIn(card);
        });
        window.DashboardCKEditorFix?.hideCkeNotifications?.();
    }

    function sanitizeImageFormIds(form) {
        if (!form) return;
        form.querySelectorAll('[data-block-image-form]').forEach((row) => {
            if (row.closest('[data-block-image-empty-template]') || row.classList.contains('hidden')) return;
            const idInput = row.querySelector('input[name^="images-"][name$="-id"]');
            const blockInput = row.querySelector('input[name^="images-"][name$="-block"]');
            if (!idInput || !blockInput || !idInput.value) return;
            if (idInput.value === blockInput.value) {
                idInput.value = '';
            }
        });
    }

    function renumberImageFormPrefixes(form) {
        const rows = [...form.querySelectorAll('[data-block-image-form]')].filter(
            (r) => !r.closest('[data-block-image-empty-template]'),
        );
        const visible = rows.filter((r) => !r.classList.contains('hidden'));
        const hidden = rows.filter((r) => r.classList.contains('hidden'));
        const ordered = [...visible, ...hidden];

        ordered.forEach((row, newIdx) => {
            const currentIdx = getRowFormIndex(row, 'images');
            if (currentIdx === newIdx) return;
            row.querySelectorAll('[name^="images-"]').forEach((el) => {
                el.name = el.name.replace(/^images-\d+-/, `images-${newIdx}-`);
                if (el.id) el.id = el.id.replace(/^id_images-\d+-/, `id_images-${newIdx}-`);
            });
            row.setAttribute('data-form-prefix', String(newIdx));
        });

        const totalInput = getTotalInput(form, 'images');
        if (totalInput) totalInput.value = ordered.length;
    }

    function updateMediaUrl(container, url) {
        if (!container || !url) return;
        if (window.DashboardForms && typeof window.DashboardForms.setMediaPreviewSrc === 'function') {
            window.DashboardForms.setMediaPreviewSrc(container, url, { fromServer: true });
        }
        const media = container.querySelector('[data-media-container]') || container;
        const fileInput = media.querySelector('input[type="file"]');
        if (fileInput) {
            try {
                fileInput.files = new DataTransfer().files;
            } catch (e) {
                fileInput.value = '';
            }
        }
    }

    function imageRowHasContent(row) {
        if (!row) return false;
        const idInput = row.querySelector('input[name^="images-"][name$="-id"]');
        if (idInput && idInput.value) return true;
        const fileInput = row.querySelector('input[type="file"][name^="images-"]');
        if (fileInput && fileInput.files && fileInput.files.length) return true;
        if (window.DashboardForms && typeof window.DashboardForms.getMediaPreviewUrl === 'function') {
            const url = window.DashboardForms.getMediaPreviewUrl(row);
            if (url) return true;
        }
        const existing = row.querySelector('[data-existing-image]');
        if (existing && existing.src && !existing.classList.contains('hidden')) return true;
        return false;
    }

    function pruneEmptyImageRows(form) {
        if (!form) return;
        let removed = false;
        form.querySelectorAll('[data-block-image-form]').forEach((row) => {
            if (row.closest('[data-block-image-empty-template]') || row.classList.contains('hidden')) return;
            if (!imageRowHasContent(row)) {
                row.remove();
                removed = true;
            }
        });
        if (removed) renumberImageFormPrefixes(form);
    }

    function getBlockGallerySection(el) {
        return el && el.closest('[data-block-gallery-section]');
    }

    function bindGalleryControls(form) {
        if (!form || form.dataset.galleryControlsBound === '1') return;
        form.dataset.galleryControlsBound = '1';

        form.addEventListener('click', (e) => {
            const multiBtn = e.target.closest('[data-block-gallery-multi-button]');
            if (multiBtn) {
                e.preventDefault();
                const section = getBlockGallerySection(multiBtn);
                const input = section && section.querySelector('[data-block-gallery-multi-input]');
                if (input) input.click();
            }
        });

        form.addEventListener('change', (e) => {
            const input = e.target;
            if (!input.matches('[data-block-gallery-multi-input]')) return;
            const section = getBlockGallerySection(input);
            if (!section) return;
            let added = false;
            Array.from(input.files || []).forEach((f) => {
                if (!f.type || !f.type.startsWith('image/')) return;
                if (addBlockImageRow(form, section, f)) added = true;
            });
            input.value = '';
            if (added) builderNotify(form, false);
        });

        form.addEventListener('dragover', (e) => {
            const dropzone = e.target.closest('[data-block-gallery-dropzone]');
            if (!dropzone) return;
            e.preventDefault();
            dropzone.classList.add('border-emerald-500', 'bg-emerald-50', 'dark:bg-emerald-900/20');
            dropzone.classList.remove('border-gray-300', 'dark:border-gray-600');
        });

        form.addEventListener('dragleave', (e) => {
            const dropzone = e.target.closest('[data-block-gallery-dropzone]');
            if (!dropzone || dropzone.contains(e.relatedTarget)) return;
            dropzone.classList.remove('border-emerald-500', 'bg-emerald-50', 'dark:bg-emerald-900/20');
            dropzone.classList.add('border-gray-300', 'dark:border-gray-600');
        });

        form.addEventListener('drop', (e) => {
            const dropzone = e.target.closest('[data-block-gallery-dropzone]');
            if (!dropzone) return;
            e.preventDefault();
            dropzone.classList.remove('border-emerald-500', 'bg-emerald-50', 'dark:bg-emerald-900/20');
            dropzone.classList.add('border-gray-300', 'dark:border-gray-600');
            const section = getBlockGallerySection(dropzone);
            if (!section) return;
            let added = false;
            Array.from(e.dataTransfer.files || []).forEach((f) => {
                if (!f.type || !f.type.startsWith('image/')) return;
                if (addBlockImageRow(form, section, f)) added = true;
            });
            if (added) builderNotify(form, false);
        });
    }

    function updateBlockGalleryIndices(section) {
        const list = section && section.querySelector('[data-gallery-images-list]');
        if (!list) return;
        const rows = [...list.querySelectorAll('[data-block-image-form]:not(.hidden)')];
        rows.forEach((row, idx) => {
            const label = row.querySelector('[data-block-gallery-index]');
            if (label) label.textContent = String(idx + 1);
            const orderInput = row.querySelector('input[name$="-order"]');
            if (orderInput) orderInput.value = String(idx * 10);
        });
        const countEl = section.querySelector('[data-block-gallery-count]');
        const max = parseInt(section.getAttribute('data-gallery-max') || '50', 10);
        if (countEl) countEl.textContent = `(${rows.length}/${max})`;
    }

    function addBlockImageRow(form, section, file) {
        const blockId = section.getAttribute('data-block-id');
        if (!blockId) return null;

        const template = form.querySelector('[data-block-image-empty-template]');
        const list = section.querySelector('[data-gallery-images-list]');
        const totalInput = getTotalInput(form, 'images');
        if (!template || !list || !totalInput) return null;

        const max = parseInt(section.getAttribute('data-gallery-max') || '50', 10);
        const visibleCount = list.querySelectorAll('[data-block-image-form]:not(.hidden)').length;
        if (visibleCount >= max) return null;

        const index = parseInt(totalInput.value, 10);
        let html = getTemplateHtml(template).replace(/images-__prefix__/g, `images-${index}`).replace(/__prefix__/g, String(index));
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html.trim();
        const row = wrapper.firstElementChild;
        enableFormFields(row);
        row.setAttribute('data-block-id', blockId);
        row.setAttribute('data-form-prefix', String(index));
        const cardIndex = section.getAttribute('data-block-card-index');
        if (cardIndex !== null && cardIndex !== '') {
            row.setAttribute('data-block-card-index', cardIndex);
        }
        const blockInput = row.querySelector('input[name$="-block"]');
        if (blockInput) blockInput.value = blockId;
        const orderInput = row.querySelector('input[name$="-order"]');
        if (orderInput) orderInput.value = String(visibleCount * 10);

        list.appendChild(row);
        totalInput.value = index + 1;

        if (window.DashboardForms && window.DashboardForms.initMediaDropzones) {
            window.DashboardForms.initMediaDropzones(row);
        }

        if (file && window.DashboardForms && typeof window.DashboardForms.setSingleFile === 'function') {
            const inp = row.querySelector('input[type="file"][name^="images-"]');
            window.DashboardForms.setSingleFile(inp, file);
        }

        updateBlockGalleryIndices(section);
        return row;
    }

    function initBlockGallerySortable(section, form) {
        const list = section.querySelector('[data-gallery-images-list]');
        if (!list || !window.Sortable || list.dataset.sortableBound === '1') return;
        list.dataset.sortableBound = '1';
        Sortable.create(list, {
            handle: '.builder-image-row-handle',
            animation: 150,
            ghostClass: 'sortable-ghost',
            onEnd: () => {
                updateBlockGalleryIndices(section);
                builderNotify(form, false);
            },
        });
    }

    function initBlockGallerySection(section, form) {
        if (!section) return;
        const blockId = section.getAttribute('data-block-id');
        if (!blockId) return;

        updateBlockGalleryIndices(section);
        initBlockGallerySortable(section, form);
    }

    function initAllBlockGallerySections(form) {
        if (!form) return;
        form.querySelectorAll('[data-block-gallery-section]').forEach((section) => {
            if (section.getAttribute('data-block-id')) {
                initBlockGallerySection(section, form);
            }
        });
    }

    function enableGalleryBlock(form, card, blockId) {
        const section = card.querySelector('[data-block-gallery-section]');
        if (!section) return;

        section.setAttribute('data-block-id', String(blockId));
        card.setAttribute('data-block-pk', String(blockId));

        const pending = section.querySelector('[data-gallery-pending]');
        if (pending) {
            const tpl = form.querySelector('[data-block-gallery-ui-template]');
            if (tpl) {
                section.innerHTML = tpl.innerHTML;
            } else {
                pending.remove();
            }
        }

        initBlockGallerySection(section, form);
    }

    function setAllBlocksCollapsed(form, collapsed) {
        form.querySelectorAll('[data-block-form]:not(.hidden)').forEach((card) => {
            if (card.closest('[data-block-empty-template]')) return;
            if (window.Alpine && typeof Alpine.$data === 'function') {
                try {
                    const data = Alpine.$data(card);
                    if (data) data.collapsed = collapsed;
                } catch (e) { /* ignore */ }
            }
        });
    }

    function highlightBlock(card) {
        if (!card) return;
        card.classList.remove('builder-card--highlight');
        void card.offsetWidth;
        card.classList.add('builder-card--highlight');
        card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        setTimeout(() => card.classList.remove('builder-card--highlight'), 2000);
    }

    function triggerLivePreview(form) {
        if (window.DashboardForms && typeof window.DashboardForms.triggerPreviewUpdate === 'function') {
            window.DashboardForms.triggerPreviewUpdate(form);
        }
    }

    function builderNotify(form, immediate) {
        triggerLivePreview(form);
        if (form && form._builderSync) {
            form._builderSync.notify({ immediate: !!immediate });
        } else if (form) {
            form.dispatchEvent(new Event('input', { bubbles: true }));
            form.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    function initSortable(list, form, section) {
        if (!list || !window.Sortable) return;
        Sortable.create(list, {
            handle: '.block-drag-handle',
            animation: 180,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            onEnd: () => {
                reindexBlockCards(list);
                updateBlockCount(section);
                builderNotify(form, false);
            },
        });
    }

    function initAlpineCard(card, blockType) {
        if (window.Alpine && typeof Alpine.initTree === 'function') {
            Alpine.initTree(card);
        }
        if (window.Alpine && typeof Alpine.$data === 'function') {
            try {
                const data = Alpine.$data(card);
                if (data) {
                    data.blockType = blockType;
                    data.collapsed = false;
                    data.locale = 'fr';
                }
            } catch (e) { /* ignore */ }
        }
        const typeSelect = card.querySelector('[name$="-block_type"]');
        if (typeSelect) typeSelect.value = blockType;
        updateLayoutSelect(card, blockType);
    }

    function enableFormFields(root) {
        if (!root) return;
        root.querySelectorAll('fieldset[disabled]').forEach((fs) => { fs.disabled = false; });
        root.querySelectorAll('input[disabled], select[disabled], textarea[disabled], button[disabled]').forEach((el) => {
            el.disabled = false;
        });
    }

    function getTemplateHtml(template) {
        if (!template) return '';
        const fieldset = template.querySelector('fieldset');
        return fieldset ? fieldset.innerHTML : template.innerHTML;
    }

    function addBlockFromTemplate(section, form, blockType) {
        const template = section.querySelector('[data-block-empty-template]');
        const list = section.querySelector('[data-block-forms]');
        const totalInput = getTotalInput(form, 'blocks');
        if (!template || !list || !totalInput) return;

        const index = parseInt(totalInput.value, 10);
        const type = blockType || 'richtext';
        let html = getTemplateHtml(template).replace(/__prefix__/g, String(index));
        html = html.replace(/blocks-__prefix__/g, `blocks-${index}`);
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html.trim();
        const card = wrapper.firstElementChild;
        card.setAttribute('data-form-prefix', String(index));
        enableFormFields(card);
        list.appendChild(card);

        totalInput.value = index + 1;
        initAlpineCard(card, type);
        bindBlockCard(card, form, section);
        reindexBlockCards(list);
        updateBlockCount(section);
        highlightBlock(card);

        if (window.Alpine && typeof Alpine.$data === 'function') {
            try {
                const sectionData = Alpine.$data(section);
                if (sectionData && 'pickerOpen' in sectionData) sectionData.pickerOpen = false;
            } catch (e) { /* ignore */ }
        }

        if (window.DashboardForms && window.DashboardForms.initMediaDropzones) {
            window.DashboardForms.initMediaDropzones(card);
        }
        initCKEditorIn(card);
        window.DashboardCKEditorFix?.hideCkeNotifications?.();
        builderNotify(form, false);
    }

    async function removeBlockRow(btn, form, section) {
        if (window.DashboardForms && window.DashboardForms.confirm) {
            const ok = await window.DashboardForms.confirm({
                title: 'Supprimer ce bloc ?',
                message: 'Le bloc sera retiré de la page après enregistrement.',
            });
            if (!ok) return;
        }
        const card = btn.closest('[data-block-form]');
        if (!card) return;
        const del = card.querySelector('input[name$="-DELETE"]');
        const idInput = card.querySelector('input[name^="blocks-"][name$="-id"]');
        const pk = (idInput && idInput.value) || card.getAttribute('data-block-pk');
        const hadPk = !!pk;
        if (del && hadPk) {
            del.checked = true;
            card.classList.add('hidden');
        } else {
            card.remove();
        }
        const list = form.querySelector('[data-block-forms]');
        if (list) renumberBlockFormPrefixes(form, list, { reinitEditors: false });
        updateBlockCount(section);
        builderNotify(form, hadPk);
    }

    function parseFaqJson(raw) {
        try {
            return raw ? JSON.parse(raw) : [];
        } catch (e) {
            return [];
        }
    }

    function renderFaqRows(editor) {
        const hidden = editor.querySelector('input[name$="-faq_json"]');
        const container = editor.querySelector('[data-faq-rows]');
        if (!hidden || !container) return;

        const items = parseFaqJson(hidden.value);
        container.innerHTML = items.map((item, idx) => (
            `<div class="builder-faq-row grid grid-cols-1 gap-2" data-faq-index="${idx}">` +
            `<input type="text" data-faq-q placeholder="Question FR" value="${escapeAttr(item.q || '')}" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2">` +
            `<input type="text" data-faq-q-en placeholder="Question EN" value="${escapeAttr(item.q_en || '')}" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2">` +
            `<textarea data-faq-a rows="2" placeholder="Réponse FR" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2">${escapeHtml(item.a || '')}</textarea>` +
            `<textarea data-faq-a-en rows="2" placeholder="Réponse EN" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2">${escapeHtml(item.a_en || '')}</textarea>` +
            `<button type="button" data-remove-faq-row class="text-xs text-red-600 font-bold self-start hover:underline">Retirer cette question</button></div>`
        )).join('');

        container.querySelectorAll('[data-remove-faq-row]').forEach((btn) => {
            btn.addEventListener('click', () => {
                const row = btn.closest('[data-faq-index]');
                const i = parseInt(row.getAttribute('data-faq-index'), 10);
                const next = parseFaqJson(hidden.value).filter((_, j) => j !== i);
                hidden.value = JSON.stringify(next);
                renderFaqRows(editor);
                formChange(editor, true);
            });
        });

        container.querySelectorAll('input, textarea').forEach((el) => {
            el.addEventListener('input', () => {
                syncFaqHidden(editor);
                formChange(editor);
            });
        });
    }

    function syncFaqHidden(editor, notifyChange) {
        const hidden = editor.querySelector('input[name$="-faq_json"]');
        const container = editor.querySelector('[data-faq-rows]');
        if (!hidden || !container) return;
        const items = [];
        container.querySelectorAll('[data-faq-index]').forEach((row) => {
            items.push({
                q: row.querySelector('[data-faq-q]')?.value || '',
                q_en: row.querySelector('[data-faq-q-en]')?.value || '',
                a: row.querySelector('[data-faq-a]')?.value || '',
                a_en: row.querySelector('[data-faq-a-en]')?.value || '',
            });
        });
        hidden.value = JSON.stringify(items);
        if (notifyChange !== false) formChange(editor);
    }

    function syncAllFaqEditors(form) {
        form.querySelectorAll('[data-faq-editor]').forEach((editor) => syncFaqHidden(editor, false));
    }

    function syncCKEditors() {
        if (!window.CKEDITOR) return;
        Object.values(window.CKEDITOR.instances).forEach((inst) => {
            try {
                inst.updateElement();
            } catch (e) { /* ignore */ }
        });
    }

    function escapeHtml(str) {
        const d = document.createElement('div');
        d.textContent = str || '';
        return d.innerHTML;
    }

    function escapeAttr(str) {
        return escapeHtml(str).replace(/"/g, '&quot;');
    }

    function formChange(el, immediate) {
        const form = el.closest('form');
        if (form) builderNotify(form, immediate);
    }

    function addBlockImage(form, blockId) {
        const section = form.querySelector(`[data-block-gallery-section][data-block-id="${blockId}"]`);
        if (!section) return;
        if (addBlockImageRow(form, section)) builderNotify(form, true);
    }

    async function handleDeleteBlockImage(btn, form) {
        if (window.DashboardForms && window.DashboardForms.confirm) {
            const ok = await window.DashboardForms.confirm({
                title: 'Supprimer cette image ?',
                message: 'Cette image sera retirée de la galerie du bloc.',
            });
            if (!ok) return;
        }
        const row = btn.closest('[data-block-image-form]');
        if (!row) return;
        const section = row.closest('[data-block-gallery-section]');
        const isNew = btn.hasAttribute('data-delete-new');

        if (isNew) {
            row.remove();
            const totalInput = getTotalInput(form, 'images');
            if (totalInput) {
                totalInput.value = Math.max(0, parseInt(totalInput.value, 10) - 1);
            }
            renumberImageFormPrefixes(form);
        } else {
            const del = row.querySelector('input[name$="-DELETE"]');
            if (del) del.checked = true;
            row.classList.add('hidden');
        }

        if (section) updateBlockGalleryIndices(section);
        builderNotify(form, false);
    }

    function bindBlockCard(card, form, section) {
        if (!card || card.dataset.blockCardBound === '1') return;
        card.dataset.blockCardBound = '1';
        const typeSelect = card.querySelector('[name$="-block_type"]');
        if (typeSelect) {
            typeSelect.addEventListener('change', () => {
                const nextType = typeSelect.value;
                if (window.Alpine && typeof Alpine.$data === 'function') {
                    try {
                        const data = Alpine.$data(card);
                        if (data) data.blockType = nextType;
                    } catch (e) { /* ignore */ }
                }
                updateLayoutSelect(card, nextType);
                clearHiddenBlockFields(card, nextType);
                formChange(card, true);
            });
            updateLayoutSelect(card, typeSelect.value);
        }

        const visibility = card.querySelector('input[name$="-is_visible"]');
        if (visibility && !visibility.dataset.builderBound) {
            visibility.dataset.builderBound = '1';
            visibility.addEventListener('change', () => builderNotify(form, true));
        }

        const deleteBtn = card.querySelector('[data-delete-block-row]');
        if (deleteBtn && !deleteBtn.dataset.builderBound) {
            deleteBtn.dataset.builderBound = '1';
            deleteBtn.addEventListener('click', (e) => {
                removeBlockRow(e.currentTarget, form, section);
            });
        }

        const faqEditor = card.querySelector('[data-faq-editor]');
        if (faqEditor) {
            renderFaqRows(faqEditor);
            const addFaqBtn = faqEditor.querySelector('[data-add-faq-row]');
            if (addFaqBtn && !addFaqBtn.dataset.builderBound) {
                addFaqBtn.dataset.builderBound = '1';
                addFaqBtn.addEventListener('click', () => {
                    const hidden = faqEditor.querySelector('input[name$="-faq_json"]');
                    const items = parseFaqJson(hidden?.value);
                    items.push({ q: '', q_en: '', a: '', a_en: '' });
                    if (hidden) hidden.value = JSON.stringify(items);
                    renderFaqRows(faqEditor);
                    formChange(faqEditor, true);
                });
            }
        }

    }

    function initBlockEditor(form) {
        if (!form || form.dataset.blockEditorReady === '1') return;
        form.dataset.blockEditorReady = '1';
        const section = form.querySelector('[data-block-section]');
        if (!section) return;

        const list = section.querySelector('[data-block-forms]');
        initSortable(list, form, section);
        reindexBlockCards(list);
        updateBlockCount(section);

        section.querySelectorAll('[data-add-block-type]').forEach((btn) => {
            if (btn.dataset.builderBound) return;
            btn.dataset.builderBound = '1';
            btn.addEventListener('click', () => {
                const blockType = btn.getAttribute('data-add-block-type');
                addBlockFromTemplate(section, form, blockType);
            });
        });

        const collapseBtn = section.querySelector('[data-collapse-all-blocks]');
        if (collapseBtn && !collapseBtn.dataset.builderBound) {
            collapseBtn.dataset.builderBound = '1';
            collapseBtn.addEventListener('click', () => {
                setAllBlocksCollapsed(form, true);
            });
        }
        const expandBtn = section.querySelector('[data-expand-all-blocks]');
        if (expandBtn && !expandBtn.dataset.builderBound) {
            expandBtn.dataset.builderBound = '1';
            expandBtn.addEventListener('click', () => {
                setAllBlocksCollapsed(form, false);
            });
        }

        form.querySelectorAll('[data-block-form]').forEach((card) => {
            if (card.closest('[data-block-empty-template]')) return;
            bindBlockCard(card, form, section);
            initCKEditorIn(card);
            const typeSelect = card.querySelector('[name$="-block_type"]');
            if (typeSelect) updateLayoutSelect(card, typeSelect.value);
        });

        form.addEventListener('click', (e) => {
            const btn = e.target.closest('[data-delete-block-image]');
            if (btn) {
                e.preventDefault();
                handleDeleteBlockImage(btn, form);
            }
        });

        bindGalleryControls(form);

        form.addEventListener('submit', () => {
            syncCKEditors();
            syncAllFaqEditors(form);
        });

        if (window.DashboardForms && window.DashboardForms.initMediaDropzones) {
            window.DashboardForms.initMediaDropzones(form);
        }
        initAllBlockGallerySections(form);
    }

    window.DashboardBlockEditor = {
        init: initBlockEditor,
        syncBeforePreview(form) {
            syncCKEditors();
            if (form) syncAllFaqEditors(form);
        },
        prepareForSave(form) {
            syncCKEditors();
            if (form) syncAllFaqEditors(form);
            syncBlockIdsToInputs(form);
            sanitizeImageFormIds(form);
            pruneEmptyImageRows(form);
            const list = form.querySelector('[data-block-forms]');
            if (list) {
                const renumbered = renumberBlockFormPrefixes(form, list, { reinitEditors: false });
                if (renumbered) {
                    getVisibleBlockCards(list).forEach((row) => initCKEditorIn(row));
                }
            }
            renumberImageFormPrefixes(form);
            syncBlockIdsToInputs(form);
            syncBlockFormsetManagement(form);
            syncImageFormsetManagement(form);
            syncCKEditors();
        },
        syncBlockIdsToInputs,
        syncBlockFormsetManagement,
        syncImageFormsetManagement,
        applyBlockPkToCard,
        reinitAllEditors,
        enableGalleryBlock,
        updateMediaUrl,
        updateLayoutSelect,
        renumberBlockFormPrefixes,
        refreshGallerySections(form) {
            if (!form) return;
            form.querySelectorAll('[data-block-gallery-section]').forEach((section) => {
                if (section.getAttribute('data-block-id')) {
                    initBlockGallerySection(section, form);
                }
                updateBlockGalleryIndices(section);
            });
        },
        notify: builderNotify,
    };
})();
