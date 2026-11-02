"""Four synthetic examples. Not real incidents; no real numbers or accounts."""
from .textproc import normalize

EXAMPLES = [
    {
        "id": "family_emergency",
        "title_en": "Family emergency",
        "title_ur": "Khandani emergency",
        "text": "Ammi, mera phone kharab ho gaya hai. Main naye number se baat kar raha hoon. Emergency hai, Rs 50000 bhej dein. Kisi ko mat batana.",
    },
    {
        "id": "code_request",
        "title_en": "Verification-code request",
        "title_ur": "Verification code ki darkhwast",
        "text": "Main Demo Bank support se hoon. Aapka account band ho raha hai. Jo login verification code aapko mila hai woh abhi mujhe bata dein.",
    },
    {
        "id": "legit_looking",
        "title_en": "Legitimate-looking request",
        "title_ur": "Aam si darkhwast",
        "text": "Kal hum ne fees ke bare mein baat ki thi. Jab time mile mujhe call kar lena, phir payment details confirm kar lete hain.",
    },
    {
        "id": "ambiguous_urgency",
        "title_en": "Ambiguous urgency",
        "title_ur": "Mubham jaldi",
        "text": "Mujhe abhi help chahiye. Please call me.",
    },
]


def match_example(normalized_text: str) -> dict | None:
    for ex in EXAMPLES:
        if normalize(ex["text"]) == normalized_text:
            return ex
    return None
