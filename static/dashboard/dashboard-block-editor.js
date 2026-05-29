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
                form.dispatchEvent(new Event('change', { bubbles: true }));
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

    function addBlockFromTemplate(section, form, blockType) {
        const template = section.querySelector('[data-block-empty-template]');
        const list = section.querySelector('[data-block-forms]');
        const totalInput = getTotalInput(form, 'blocks');
        if (!template || !list || !totalInput) return;

        const index = parseInt(totalInput.value, 10);
        const type = blockType || 'richtext';
        let html = template.innerHTML.replace(/__prefix__/g, String(index));
        html = html.replace(/blocks-__prefix__/g, `blocks-${index}`);
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html.trim();
        const card = wrapper.firstElementChild;
        list.appendChild(card);

        totalInput.value = index + 1;
        initAlpineCard(card, type);
        bindBlockCard(card, form);
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
        form.dispatchEvent(new Event('change', { bubbles: true }));
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
        form.dispatchEvent(new Event('change', { bubbles: true }));
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
                formChange(editor);
            });
        });

        container.querySelectorAll('input, textarea').forEach((el) => {
            el.addEventListener('input', () => syncFaqHidden(editor));
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

    function formChange(el) {
        const form = el.closest('form');
        if (form) form.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function addBlockImage(form, blockId) {
        const template = form.querySelector('[data-block-image-empty-template]');
        const gallery = form.querySelector(`[data-block-gallery-images][data-block-id="${blockId}"]`);
        const list = gallery && gallery.querySelector('[data-gallery-images-list]');
        const totalInput = getTotalInput(form, 'images');
        if (!template || !list || !totalInput) return;

        const index = parseInt(totalInput.value, 10);
        let html = template.innerHTML.replace(/images-__prefix__/g, `images-${index}`).replace(/__prefix__/g, String(index));
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html.trim();
        const row = wrapper.firstElementChild;
        row.setAttribute('data-block-id', blockId);
        const cardIndex = gallery.getAttribute('data-block-card-index');
        if (cardIndex !== null && cardIndex !== '') {
            row.setAttribute('data-block-card-index', cardIndex);
        }
        const blockInput = row.querySelector('input[name$="-block"]');
        if (blockInput) blockInput.value = blockId;
        list.appendChild(row);
        totalInput.value = index + 1;
        if (window.DashboardForms && window.DashboardForms.initMediaDropzones) {
            window.DashboardForms.initMediaDropzones(row);
        }
        form.dispatchEvent(new Event('change', { bubbles: true }));
    }

    async function handleDeleteBlockImage(btn, form) {
        if (window.DashboardForms && window.DashboardForms.confirm) {
            const ok = await window.DashboardForms.confirm({
                title: 'Supprimer cette image ?',
                message: 'Cette image sera retirée de la galerie.',
            });
            if (!ok) return;
        }
        const row = btn.closest('[data-block-image-form]');
        const pk = btn.getAttribute('data-image-pk');
        if (pk && !btn.hasAttribute('data-delete-new')) {
            const url = (window.DASHBOARD_API.deleteBlockImage || '') + pk + '/';
            try {
                await fetch(url, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': window.DASHBOARD_API.csrf },
                });
            } catch (e) { /* ignore */ }
        }
        const del = row && row.querySelector('input[name$="-DELETE"]');
        if (del) del.checked = true;
        if (row) row.classList.add('hidden');
        form.dispatchEvent(new Event('change', { bubbles: true }));
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
                form.dispatchEvent(new Event('change', { bubbles: true }));
            });
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
            });
        }

        card.querySelector('[data-add-block-image]')?.addEventListener('click', (e) => {
            const blockId = e.currentTarget.getAttribute('data-target-block');
            if (blockId) addBlockImage(form, blockId);
        });
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
    }

    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('pageSettingsForm');
        if (form && form.getAttribute('data-preview-type') === 'custom-page') {
            initBlockEditor(form);
            if (window.DashboardForms) window.DashboardForms.init(form);
        }
    });

    window.DashboardBlockEditor = {
        syncBeforePreview(form) {
            syncCKEditors();
            if (form) syncAllFaqEditors(form);
        },
    };
})();
