(function () {
    'use strict';

    const SECTION_BG_MAIN = 'main';
    const SECTION_BG_ALT = 'alt';
    const SECTION_BG_AUTO = 'auto';

    const SECTION_BG_CLASSES = {
        main: 'bg-white dark:bg-[#121212]',
        alt: 'bg-gray-50 dark:bg-[#1a1a1a]',
    };

    function normalizeSectionBackground(value) {
        if (!value || value === 'inherit') return SECTION_BG_AUTO;
        if (value === SECTION_BG_MAIN || value === SECTION_BG_ALT || value === SECTION_BG_AUTO) return value;
        return SECTION_BG_AUTO;
    }

    function sectionBgClass(tone) {
        if (!tone) return '';
        return SECTION_BG_CLASSES[tone] || SECTION_BG_CLASSES.main;
    }

    function computeSectionBackgrounds(blocks) {
        const result = new Map();
        let toneIndex = 0;

        (blocks || []).forEach((block, idx) => {
            const key = block.id || block.pk || `idx-${idx}`;
            const type = block.block_type || 'richtext';

            if (type === 'hero') {
                result.set(key, null);
                toneIndex = 0;
                block.section_bg = null;
                block.section_bg_class = '';
                return;
            }

            const override = normalizeSectionBackground(
                block.section_background || block.background,
            );
            let tone;
            if (override === SECTION_BG_MAIN || override === SECTION_BG_ALT) {
                tone = override;
            } else {
                tone = toneIndex % 2 === 0 ? SECTION_BG_MAIN : SECTION_BG_ALT;
            }
            toneIndex += 1;
            result.set(key, tone);
            block.section_bg = tone;
            block.section_bg_class = sectionBgClass(tone);
        });

        return result;
    }

    window.PageBlockBackgrounds = {
        SECTION_BG_MAIN,
        SECTION_BG_ALT,
        SECTION_BG_AUTO,
        SECTION_BG_CLASSES,
        normalizeSectionBackground,
        sectionBgClass,
        computeSectionBackgrounds,
    };
})();
