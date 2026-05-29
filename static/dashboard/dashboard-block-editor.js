(function () {
    'use strict';

    function getTotalInput(form, prefix) {
        return form.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
    }

    function reindexOrders(list) {
        list.querySelectorAll('[data-block-form]:not(.hidden)').forEach((card, idx) => {
            const orderInput = card.querySelector('.order-input, input[name$="-order"]');
            if (orderInput) orderInput.value = idx * 10;
        });
    }

    function initSortable(list, form) {
        if (!list || !window.Sortable) return;
        Sortable.create(list, {
            handle: '.block-drag-handle',
            animation: 150,
            ghostClass: 'sortable-ghost',
            onEnd: () => reindexOrders(list),
        });
    }

    function addBlockFromTemplate(section, form) {
        const template = section.querySelector('[data-block-empty-template]');
        const list = section.querySelector('[data-block-forms]');
        const totalInput = getTotalInput(form, 'blocks');
        const typeSelect = document.getElementById('newBlockType');
        if (!template || !list || !totalInput) return;

        const index = parseInt(totalInput.value, 10);
        let html = template.innerHTML.replace(/__prefix__/g, index);
        html = html.replace(/blocks-__prefix__/g, `blocks-${index}`);
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html.trim();
        const card = wrapper.firstElementChild;
        list.appendChild(card);

        const blockTypeSelect = card.querySelector('[name$="-block_type"]');
        if (blockTypeSelect && typeSelect) blockTypeSelect.value = typeSelect.value;

        totalInput.value = index + 1;
        bindBlockCard(card, form);
        reindexOrders(list);
        form.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function removeBlockRow(btn, form) {
        const card = btn.closest('[data-block-form]');
        if (!card) return;
        const del = card.querySelector('input[name$="-DELETE"]');
        if (del) {
            del.checked = true;
            card.classList.add('hidden');
        } else {
            card.remove();
            const totalInput = getTotalInput(form, 'blocks');
            if (totalInput) totalInput.value = Math.max(0, parseInt(totalInput.value, 10) - 1);
        }
        reindexOrders(form.querySelector('[data-block-forms]'));
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
            `<div class="grid grid-cols-1 gap-2 p-3 rounded-lg bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700" data-faq-index="${idx}">` +
            `<input type="text" data-faq-q placeholder="Question FR" value="${escapeAttr(item.q || '')}" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2">` +
            `<input type="text" data-faq-q-en placeholder="Question EN" value="${escapeAttr(item.q_en || '')}" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2">` +
            `<textarea data-faq-a rows="2" placeholder="Réponse FR" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2">${escapeHtml(item.a || '')}</textarea>` +
            `<textarea data-faq-a-en rows="2" placeholder="Réponse EN" class="w-full text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2">${escapeHtml(item.a_en || '')}</textarea>` +
            `<button type="button" data-remove-faq-row class="text-xs text-red-600 font-bold self-start">Retirer</button></div>`
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

    function escapeHtml(str) {
        const d = document.createElement('div');
        d.textContent = str;
        return d.innerHTML;
    }

    function escapeAttr(str) {
        return escapeHtml(str).replace(/"/g, '&quot;');
    }

    function formChange(el) {
        const form = el.closest('form');
        if (form) form.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function distributeGalleryImages(form) {
        const pool = form.querySelector('[data-block-image-pool]');
        if (!pool) return;
        form.querySelectorAll('[data-block-gallery-images]').forEach((slot) => {
            const blockId = slot.getAttribute('data-block-id');
            const target = slot.querySelector('[data-gallery-slot]');
            if (!target || !blockId) return;
            target.innerHTML = '';
            pool.querySelectorAll(`[data-block-image-form][data-block-id="${blockId}"]`).forEach((imgForm) => {
                if (imgForm.querySelector('input[name$="-DELETE"]')?.checked) return;
                target.appendChild(imgForm.cloneNode(true));
            });
        });
    }

    function addBlockImage(form, blockId) {
        const template = form.querySelector('[data-block-image-empty-template]');
        const pool = form.querySelector('[data-block-image-pool]');
        const totalInput = getTotalInput(form, 'images');
        if (!template || !pool || !totalInput) return;

        const index = parseInt(totalInput.value, 10);
        let html = template.innerHTML.replace(/images-__prefix__/g, `images-${index}`).replace(/__prefix__/g, index);
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html.trim();
        const row = wrapper.firstElementChild;
        row.setAttribute('data-block-id', blockId);
        const blockInput = row.querySelector('input[name$="-block"]');
        if (blockInput) blockInput.value = blockId;
        pool.appendChild(row);
        totalInput.value = index + 1;
        bindBlockImageRow(row, form);
        distributeGalleryImages(form);
        form.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function bindBlockImageRow(row, form) {
        const btn = row.querySelector('[data-delete-block-image]');
        if (!btn) return;
        btn.addEventListener('click', async () => {
            const pk = btn.getAttribute('data-image-pk');
            if (pk && window.DashboardForms && !btn.hasAttribute('data-delete-new')) {
                const ok = await window.DashboardForms.confirm({
                    title: 'Supprimer cette image ?',
                    message: 'Action définitive.',
                });
                if (!ok) return;
                const url = (window.DASHBOARD_API.deleteBlockImage || '') + pk + '/';
                await fetch(url, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': window.DASHBOARD_API.csrf },
                });
            }
            const del = row.querySelector('input[name$="-DELETE"]');
            if (del) del.checked = true;
            row.classList.add('hidden');
            distributeGalleryImages(form);
            form.dispatchEvent(new Event('change', { bubbles: true }));
        });
    }

    function bindBlockCard(card, form) {
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

        const delBtn = card.querySelector('[data-delete-block-row]');
        if (delBtn) delBtn.addEventListener('click', () => removeBlockRow(delBtn, form));

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
        initSortable(list, form);

        section.querySelector('[data-add-block]')?.addEventListener('click', () => addBlockFromTemplate(section, form));

        form.querySelectorAll('[data-block-form]').forEach((card) => bindBlockCard(card, form));
        form.querySelectorAll('[data-block-image-form]').forEach((row) => bindBlockImageRow(row, form));
        distributeGalleryImages(form);

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
})();
