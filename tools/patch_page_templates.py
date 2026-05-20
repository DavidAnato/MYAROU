import re
from pathlib import Path

ABOUT_MAP = {
    "site.about.hero.badge": "hero_badge",
    "site.about.hero.title_prefix": "hero_title_prefix",
    "site.about.hero.title_suffix": "hero_title_suffix",
    "site.about.hero.description": "hero_description",
    "site.about.profile.years_experience": "profile_years_label",
    "site.about.profile.title_prefix": "profile_title_prefix",
    "site.about.profile.title_suffix": "profile_title_suffix",
    "site.about.profile.p1": "profile_p1",
    "site.about.profile.p2": "profile_p2",
    "site.about.profile.p3": "profile_p3",
    "site.about.profile.stats.youth": "profile_stat_youth",
    "site.about.profile.stats.continents": "profile_stat_continents",
    "site.about.journey.title": "journey_title",
    "site.about.journey.description": "journey_description",
    "site.about.journey.item1.badge": "journey_item1_badge",
    "site.about.journey.item1.title": "journey_item1_title",
    "site.about.journey.item1.desc": "journey_item1_desc",
    "site.about.journey.item2.badge": "journey_item2_badge",
    "site.about.journey.item2.title": "journey_item2_title",
    "site.about.journey.item2.desc": "journey_item2_desc",
    "site.about.journey.item3.badge": "journey_item3_badge",
    "site.about.journey.item3.title": "journey_item3_title",
    "site.about.journey.item3.desc": "journey_item3_desc",
    "site.about.journey.item4.badge": "journey_item4_badge",
    "site.about.journey.item4.title": "journey_item4_title",
    "site.about.journey.item4.desc": "journey_item4_desc",
    "site.about.video.title": "video_title",
    "site.about.video.description": "video_description",
    "site.about.values.title": "values_title",
    "site.about.values.description": "values_description",
    "site.about.values.excellence.title": "values_excellence_title",
    "site.about.values.excellence.desc": "values_excellence_desc",
    "site.about.values.solidarity.title": "values_solidarity_title",
    "site.about.values.solidarity.desc": "values_solidarity_desc",
    "site.about.values.authenticity.title": "values_authenticity_title",
    "site.about.values.authenticity.desc": "values_authenticity_desc",
    "site.about.values.impact.title": "values_impact_title",
    "site.about.values.impact.desc": "values_impact_desc",
    "site.about.vision.quote": "vision_quote",
    "site.about.vision.role": "vision_role",
    "site.about.cta.title": "cta_title",
    "site.about.cta.description": "cta_description",
    "site.about.cta.blog_btn": "cta_blog_btn",
    "site.about.cta.contact_btn": "cta_contact_btn",
}

CONTACT_MAP = {
    "site.contact.hero.title_prefix": "hero_title_prefix",
    "site.contact.hero.description": "hero_description",
    "site.contact.hero.response_time": "hero_response_time",
    "site.contact.form.title": "form_title",
    "site.contact.form.description": "form_description",
    "site.contact.info.title": "info_title",
    "site.contact.actions.title": "actions_title",
    "site.contact.actions.discover": "actions_discover",
    "site.contact.actions.support": "actions_support",
    "site.contact.social.title": "social_title",
    "site.contact.faq.title": "faq_title",
    "site.contact.faq.description": "faq_description",
    "site.contact.faq.q1": "faq_q1",
    "site.contact.faq.q1.answer": "faq_a1",
    "site.contact.faq.q2": "faq_q2",
    "site.contact.faq.q2.answer": "faq_a2",
    "site.contact.faq.q3": "faq_q3",
    "site.contact.faq.q3.answer": "faq_a3",
    "site.contact.faq.q4": "faq_q4",
    "site.contact.faq.q4.answer": "faq_a4",
}


def replace_file(path, var, mapping):
    text = path.read_text(encoding="utf-8")
    if "page_i18n" not in text:
        text = text.replace("{% load static json_i18n %}", "{% load static json_i18n page_i18n %}", 1)
    pattern = re.compile(r'\{%\s*t\s+"([^"]+)"\s*%\}')

    def repl(m):
        key = m.group(1)
        field = mapping.get(key)
        if field:
            return f'{{% page_text {var} "{field}" "{key}" %}}'
        return m.group(0)

    path.write_text(pattern.sub(repl, text), encoding="utf-8")


root = Path(__file__).resolve().parent.parent
replace_file(root / "templates/blog/about.html", "about", ABOUT_MAP)
replace_file(root / "templates/blog/contact.html", "contact_page", CONTACT_MAP)
print("patched")
