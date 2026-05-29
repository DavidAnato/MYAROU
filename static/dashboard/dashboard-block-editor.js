(function () {
    'use strict';

    function getTotalInput(form, prefix) {
        return form.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
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

    function initCKEditorIn(root) {
        if (!window.CKEDITOR) return;
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

    function renumberBlockFormPrefixes(form, list) {
        const rows = [...list.querySelectorAll('[data-block-form]')].filter(
            (row) => !row.closest('[data-block-empty-template]'),
        );
        const visible = rows.filter((r) => !r.classList.contains('hidden'));
        const hidden = rows.filter((r) => r.classList.contains('hidden'));
        const ordered = [...visible, ...hidden];

        ordered.forEach((row, newIdx) => {
            destroyCKEditorIn(row);
            row.querySelectorAll('[name^="blocks-"]').forEach((el) => {
                el.name = el.name.replace(/^blocks-\d+-/, `blocks-${newIdx}-`);
                if (el.id) el.id = el.id.replace(/^id_blocks-\d+-/, `id_blocks-${newIdx}-`);
            });
            row.setAttribute('data-form-prefix', String(newIdx));
            initCKEditorIn(row);
        });

        const totalInput = getTotalInput(form, 'blocks');
        if (totalInput) totalInput.value = ordered.length;
        reindexBlockCards(list);
    }

    function renumberImageFormPrefixes(form) {
        const container = form;
        const rows = [...form.querySelectorAll('[data-block-image-form]')].filter(
            (r) => !r.closest('[data-block-image-empty-template]'),
        );
        const visible = rows.filter((r) => !r.classList.contains('hidden'));
        const hidden = rows.filter((r) => r.classList.contains('hidden'));
        const ordered = [...visible, ...hidden];

        ordered.forEach((row, newIdx) => {
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
            window.DashboardForms.setMediaPreviewSrc(container, url);
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
            window.DashboardForms.initMediaDropzones(form);
        }

        if (file && window.DashboardForms && typeof window.DashboardForms.setSingleFile === 'function') {
            const inp = row.querySelector('input[type="file"][name$="-image"]');
            window.DashboardForms.setSingleFile(inp, file);
        }

        updateBlockGalleryIndices(section);
        return row;
    }

    function initBlockGallerySection(section, form) {
        if (!section || section.dataset.blockGalleryBound === '1') return;
        const blockId = section.getAttribute('data-block-id');
        if (!blockId) return;
        section.dataset.blockGalleryBound = '1';

        updateBlockGalleryIndices(section);

        const multiInput = section.querySelector('[data-block-gallery-multi-input]');
        const multiBtn = section.querySelector('[data-block-gallery-multi-button]');
        const addBtn = section.querySelector('[data-block-gallery-add-one]');
        const dropzone = section.querySelector('[data-block-gallery-dropzone]');

        const addFiles = (files) => {
            let added = false;
            Array.from(files || []).forEach((f) => {
                if (!f.type || !f.type.startsWith('image/')) return;
                const row = addBlockImageRow(form, section, f);
                if (row) added = true;
            });
            if (added) builderNotify(form, true);
        };

        if (multiBtn && multiInput) {
            multiBtn.addEventListener('click', () => multiInput.click());
            multiInput.addEventListener('change', () => {
                addFiles(multiInput.files);
                multiInput.value = '';
            });
        }
        if (addBtn) {
            addBtn.addEventListener('click', () => {
                if (addBlockImageRow(form, section)) builderNotify(form, true);
            });
        }
        if (dropzone) {
            const setGalleryDropzoneActive = (active) => {
                dropzone.classList.toggle('border-emerald-500', active);
                dropzone.classList.toggle('bg-emerald-50', active);
                dropzone.classList.toggle('dark:bg-emerald-900/20', active);
                dropzone.classList.toggle('border-gray-300', !active);
                dropzone.classList.toggle('dark:border-gray-600', !active);
            };
            dropzone.addEventListener('dragover', (e) => {
                e.preventDefault();
                setGalleryDropzoneActive(true);
            });
            dropzone.addEventListener('dragleave', () => setGalleryDropzoneActive(false));
            dropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                setGalleryDropzoneActive(false);
                addFiles(e.dataTransfer.files);
            });
        }

        const list = section.querySelector('[data-gallery-images-list]');
        if (list && window.Sortable && !list.dataset.sortableBound) {
            list.dataset.sortableBound = '1';
            Sortable.create(list, {
                handle: '.builder-image-row-handle',
                animation: 150,
                ghostClass: 'sortable-ghost',
                onEnd: () => {
                    updateBlockGalleryIndices(section);
                    builderNotify(form, true);
                },
            });
        }
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
            delete section.dataset.blockGalleryBound;
        }

        initBlockGallerySection(section, form);
        const blockSection = form.querySelector('[data-block-section]');
        bindBlockCard(card, form, blockSection);
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
                builderNotify(form, true);
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
        builderNotify(form, true);
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
        if (del && card.querySelector('input[name$="-id"]')?.value) {
            del.checked = true;
            card.classList.add('hidden');
        } else {
            card.remove();
            const totalInput = getTotalInput(form, 'blocks');
            if (totalInput) totalInput.value = Math.max(0, parseInt(totalInput.value, 10) - 1);
        }
        const list = form.querySelector('[data-block-forms]');
        reindexBlockCards(list);
        updateBlockCount(section);
        builderNotify(form, true);
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

    function syncFaqHidden(editor) {
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
        formChange(editor);
    }

    function syncAllFaqEditors(form) {
        form.querySelectorAll('[data-faq-editor]').forEach(syncFaqHidden);
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
        builderNotify(form, true);
    }

    function bindBlockCard(card, form, section) {
        const typeSelect = card.querySelector('[name$="-block_type"]');
        if (typeSelect) {
            typeSelect.addEventListener('change', () => {
                if (window.Alpine && typeof Alpine.$data === 'function') {
                    try {
                        const data = Alpine.$data(card);
                        if (data) data.blockType = typeSelect.value;
                    } catch (e) { /* ignore */ }
                }
                formChange(card, true);
            });
        }

        const visibility = card.querySelector('input[name$="-is_visible"]');
        if (visibility && !visibility.dataset.builderBound) {
            visibility.dataset.builderBound = '1';
            visibility.addEventListener('change', () => builderNotify(form, true));
        }

        card.querySelector('[data-delete-block-row]')?.addEventListener('click', (e) => {
            removeBlockRow(e.currentTarget, form, section);
        });

        const faqEditor = card.querySelector('[data-faq-editor]');
        if (faqEditor) {
            renderFaqRows(faqEditor);
            faqEditor.querySelector('[data-add-faq-row]')?.addEventListener('click', () => {
                const hidden = faqEditor.querySelector('input[name$="-faq_json"]');
                const items = parseFaqJson(hidden?.value);
                items.push({ q: '', q_en: '', a: '', a_en: '' });
                if (hidden) hidden.value = JSON.stringify(items);
                renderFaqRows(faqEditor);
                formChange(faqEditor, true);
            });
        }

    }

    function initBlockEditor(form) {
        const section = form.querySelector('[data-block-section]');
        if (!section) return;

        const list = section.querySelector('[data-block-forms]');
        initSortable(list, form, section);
        reindexBlockCards(list);
        updateBlockCount(section);

        section.querySelectorAll('[data-add-block-type]').forEach((btn) => {
            btn.addEventListener('click', () => {
                const blockType = btn.getAttribute('data-add-block-type');
                addBlockFromTemplate(section, form, blockType);
            });
        });

        section.querySelector('[data-collapse-all-blocks]')?.addEventListener('click', () => {
            setAllBlocksCollapsed(form, true);
        });
        section.querySelector('[data-expand-all-blocks]')?.addEventListener('click', () => {
            setAllBlocksCollapsed(form, false);
        });

        form.querySelectorAll('[data-block-form]').forEach((card) => {
            if (card.closest('[data-block-empty-template]')) return;
            bindBlockCard(card, form, section);
            initCKEditorIn(card);
        });

        form.addEventListener('click', (e) => {
            const btn = e.target.closest('[data-delete-block-image]');
            if (btn) {
                e.preventDefault();
                handleDeleteBlockImage(btn, form);
            }
        });

        form.addEventListener('submit', () => {
            syncCKEditors();
            syncAllFaqEditors(form);
        });

        if (window.DashboardForms && window.DashboardForms.initMediaDropzones) {
            window.DashboardForms.initMediaDropzones(form);
        }
        initAllBlockGallerySections(form);
    }

    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('pageSettingsForm');
        if (form && form.getAttribute('data-preview-type') === 'custom-page') {
            try {
                initBlockEditor(form);
            } catch (err) {
                console.error('[builder] initBlockEditor', err);
            }
            if (window.DashboardForms) {
                try {
                    window.DashboardForms.init(form);
                } catch (err) {
                    console.error('[builder] DashboardForms.init', err);
                }
            }
        }
    });

    window.DashboardBlockEditor = {
        syncBeforePreview(form) {
            syncCKEditors();
            if (form) syncAllFaqEditors(form);
        },
        prepareForSave(form) {
            syncCKEditors();
            if (form) syncAllFaqEditors(form);
            const list = form.querySelector('[data-block-forms]');
            if (list) renumberBlockFormPrefixes(form, list);
            renumberImageFormPrefixes(form);
            syncCKEditors();
        },
        enableGalleryBlock,
        updateMediaUrl,
        renumberBlockFormPrefixes,
        refreshGallerySections(form) {
            initAllBlockGallerySections(form);
            if (!form) return;
            form.querySelectorAll('[data-block-gallery-section]').forEach(updateBlockGalleryIndices);
        },
        notify: builderNotify,
    };
})();
