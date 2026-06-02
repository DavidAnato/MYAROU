(function () {
    'use strict';

    const SECTION_BG_MAIN = 'main';
    const SECTION_BG_ALT = 'alt';

    const SECTION_BG_CLASSES = {
        main: 'bg-white dark:bg-[#121212]',
        alt: 'bg-gray-50 dark:bg-[#1a1a1a]',
    };

    function sectionBgClass(tone) {
        if (!tone) return '';
        return SECTION_BG_CLASSES[tone] || SECTION_BG_CLASSES.main;
    }

    function computeSectionBackgrounds(blocks) {
        const result = new Map();
        let toneIndex = 0;
        let lastEffective = SECTION_BG_MAIN;

        (blocks || []).forEach((block, idx) => {
            const key = block.id || block.pk || `idx-${idx}`;
            const type = block.block_type || 'richtext';

            if (type === 'hero') {
                result.set(key, null);
                toneIndex = 0;
                lastEffective = SECTION_BG_MAIN;
                return;
            }

            if (type === 'spacer') {
                const bg = block.section_background || block.background || 'inherit';
                let tone;
                if (bg === SECTION_BG_MAIN) tone = SECTION_BG_MAIN;
                else if (bg === SECTION_BG_ALT) tone = SECTION_BG_ALT;
                else tone = lastEffective;
                result.set(key, tone);
                lastEffective = tone;
                block.section_bg = tone;
                block.section_bg_class = sectionBgClass(tone);
                return;
            }

            const tone = toneIndex % 2 === 0 ? SECTION_BG_MAIN : SECTION_BG_ALT;
            toneIndex += 1;
            result.set(key, tone);
            lastEffective = tone;
            block.section_bg = tone;
            block.section_bg_class = sectionBgClass(tone);
        });

        return result;
    }

    window.PageBlockBackgrounds = {
        SECTION_BG_MAIN,
        SECTION_BG_ALT,
        SECTION_BG_CLASSES,
        sectionBgClass,
        computeSectionBackgrounds,
    };
})();
