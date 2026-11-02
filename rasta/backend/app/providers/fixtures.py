"""Predefined sample assessments used ONLY by MockAnalysisProvider for the four synthetic examples.
Source quotes are exact substrings of the example texts."""

_ACT = {
    "en": "Do not send money yet.",
    "ur": "Abhi paise na bhejein.",
}

FIXTURES: dict[str, dict[str, dict]] = {
    "family_emergency": {
        "en": {
            "risk_band": "high_concern", "scam_category": "family_impersonation",
            "observed_facts": {"claimed_identity": "A family member writing from a new number", "requested_action": "Send money urgently", "amount": "Rs 50000", "urgency_present": True, "secrecy_present": True, "verification_code_requested": False},
            "warning_signals": [
                {"label": "New number, unverified identity", "source_quote": "Main naye number se baat kar raha hoon", "explanation": "A claim to be a relative on a new number cannot be confirmed from the message alone."},
                {"label": "Urgent money request", "source_quote": "Emergency hai, Rs 50000 bhej dein", "explanation": "Urgency plus a money request is a common pressure pattern, though real emergencies also happen."},
                {"label": "Secrecy requested", "source_quote": "Kisi ko mat batana", "explanation": "Being asked to tell no one stops you from checking with other family members."},
            ],
            "uncertainty": "Rasta cannot tell whether this is really your relative; a genuine emergency is possible. This is not proof of fraud.",
            "recommended_actions": ["Do not send money yet.", "Call your relative on the number you had before this message.", "Check with another trusted relative."],
            "safe_reply": "I will call you on your old number first. I can't send money until I have spoken to you directly.",
            "family_verification_suggested": True,
        },
        "ur": {
            "risk_band": "high_concern", "scam_category": "family_impersonation",
            "observed_facts": {"claimed_identity": "Naye number se likhne wala khud ko rishtedar bata raha hai", "requested_action": "Jaldi paise bhejna", "amount": "Rs 50000", "urgency_present": True, "secrecy_present": True, "verification_code_requested": False},
            "warning_signals": [
                {"label": "Naya number, pehchan tasdeeq nahi", "source_quote": "Main naye number se baat kar raha hoon", "explanation": "Naye number se rishtedar hone ka dawa sirf message se confirm nahi ho sakta."},
                {"label": "Jaldi paise ki mang", "source_quote": "Emergency hai, Rs 50000 bhej dein", "explanation": "Jaldi aur paise ki mang aksar dabao ka tareeqa hota hai, lekin sachi emergency bhi ho sakti hai."},
                {"label": "Raaz rakhne ko kaha", "source_quote": "Kisi ko mat batana", "explanation": "Kisi ko na batane se aap doosre ghar walon se confirm nahi kar paate."},
            ],
            "uncertainty": "Rasta nahi bata sakta ke yeh waqai aapka rishtedar hai ya nahi; sachi emergency bhi ho sakti hai. Yeh fraud ka saboot nahi hai.",
            "recommended_actions": ["Abhi paise na bhejein.", "Rishtedar ko us purane number par call karein jo is message se pehle aapke paas tha.", "Kisi aur qabil-e-aitbaar rishtedar se poochh lein."],
            "safe_reply": "Main pehle aapke purane number par call karunga/karungi. Seedhi baat kiye baghair paise nahi bhej sakta/sakti.",
            "family_verification_suggested": True,
        },
    },
    "code_request": {
        "en": {
            "risk_band": "high_concern", "scam_category": "otp_theft",
            "observed_facts": {"claimed_identity": "Demo Bank support", "requested_action": "Read out a login verification code", "amount": None, "urgency_present": True, "secrecy_present": False, "verification_code_requested": True},
            "warning_signals": [
                {"label": "Login code requested", "source_quote": "Jo login verification code aapko mila hai woh abhi mujhe bata dein", "explanation": "Genuine support does not need you to read out a login code; sharing it can let someone into your account."},
                {"label": "Account-closure pressure", "source_quote": "Aapka account band ho raha hai", "explanation": "Threatening to close an account is a common way to create pressure."},
                {"label": "Unverified bank identity", "source_quote": "Main Demo Bank support se hoon", "explanation": "A message alone cannot prove the sender works for a bank."},
            ],
            "uncertainty": "Rasta cannot verify who sent this. Even so, a request for a login code is a serious warning sign.",
            "recommended_actions": ["Do not share the code with anyone.", "Contact the bank using the number on your card or official app.", "Do not use contact details from this message."],
            "safe_reply": "I do not share login codes. I will contact the bank through its official number.",
            "family_verification_suggested": False,
        },
        "ur": {
            "risk_band": "high_concern", "scam_category": "otp_theft",
            "observed_facts": {"claimed_identity": "Demo Bank support", "requested_action": "Login verification code batana", "amount": None, "urgency_present": True, "secrecy_present": False, "verification_code_requested": True},
            "warning_signals": [
                {"label": "Login code maanga ja raha hai", "source_quote": "Jo login verification code aapko mila hai woh abhi mujhe bata dein", "explanation": "Asli support ko aapse login code poochne ki zaroorat nahi hoti; code dene se koi aapke account mein aa sakta hai."},
                {"label": "Account band hone ka dabao", "source_quote": "Aapka account band ho raha hai", "explanation": "Account band hone ki dhamki dabao banane ka aam tareeqa hai."},
                {"label": "Bank ki pehchan tasdeeq nahi", "source_quote": "Main Demo Bank support se hoon", "explanation": "Sirf message se yeh sabit nahi hota ke bhejne wala bank ka hai."},
            ],
            "uncertainty": "Rasta bhejne wale ki tasdeeq nahi kar sakta. Phir bhi login code ki darkhwast ek sanjeeda warning nishani hai.",
            "recommended_actions": ["Code kisi ko na dein.", "Bank ko card ya official app par diye gaye number par call karein.", "Is message mein diye gaye rabta ke zaraye istemal na karein."],
            "safe_reply": "Main login code share nahi karta/karti. Main bank ke official number par khud rabta karunga/karungi.",
            "family_verification_suggested": False,
        },
    },
    "legit_looking": {
        "en": {
            "risk_band": "insufficient_evidence", "scam_category": "unclear",
            "observed_facts": {"claimed_identity": None, "requested_action": "Call back to confirm payment details", "amount": None, "urgency_present": False, "secrecy_present": False, "verification_code_requested": False},
            "warning_signals": [
                {"label": "Payment details mentioned", "source_quote": "phir payment details confirm kar lete hain", "explanation": "The message mentions payment details but asks for no money, code or secrecy."},
            ],
            "uncertainty": "No clear warning signs were found in this short text. That does not mean it is safe; confirm who is asking before sharing payment details.",
            "recommended_actions": ["Call the person on a number you already know.", "Share payment details only once you are sure who is asking."],
            "safe_reply": "Thanks. I will call you on your usual number and we can confirm the details then.",
            "family_verification_suggested": False,
        },
        "ur": {
            "risk_band": "insufficient_evidence", "scam_category": "unclear",
            "observed_facts": {"claimed_identity": None, "requested_action": "Call kar ke payment details confirm karna", "amount": None, "urgency_present": False, "secrecy_present": False, "verification_code_requested": False},
            "warning_signals": [
                {"label": "Payment details ka zikr", "source_quote": "phir payment details confirm kar lete hain", "explanation": "Message mein payment details ka zikr hai lekin paise, code ya raaz rakhne ki mang nahi hai."},
            ],
            "uncertainty": "Is mukhtasar text mein koi wazeh warning nishani nahi mili. Is ka matlab yeh nahi ke yeh mehfooz hai; payment details dene se pehle yaqeen kar lein ke kaun poochh raha hai.",
            "recommended_actions": ["Us shakhs ko aise number par call karein jo aap pehle se jaante hain.", "Payment details tabhi dein jab aapko yaqeen ho ke kaun poochh raha hai."],
            "safe_reply": "Shukriya. Main aapke aam number par call karunga/karungi, tab details confirm kar lenge.",
            "family_verification_suggested": False,
        },
    },
    "ambiguous_urgency": {
        "en": {
            "risk_band": "insufficient_evidence", "scam_category": "unclear",
            "observed_facts": {"claimed_identity": None, "requested_action": "Call the sender", "amount": None, "urgency_present": True, "secrecy_present": False, "verification_code_requested": False},
            "warning_signals": [
                {"label": "Urgency", "source_quote": "Mujhe abhi help chahiye", "explanation": "Urgency alone does not show fraud; a real person may need help."},
            ],
            "uncertainty": "There is too little information to judge. A genuine emergency is possible.",
            "recommended_actions": ["Call the person on a number you already know.", "If you fear they are in danger, contact family or local emergency services."],
            "safe_reply": "I want to help. I am calling you on your usual number now; please pick up.",
            "family_verification_suggested": True,
        },
        "ur": {
            "risk_band": "insufficient_evidence", "scam_category": "unclear",
            "observed_facts": {"claimed_identity": None, "requested_action": "Bhejne wale ko call karna", "amount": None, "urgency_present": True, "secrecy_present": False, "verification_code_requested": False},
            "warning_signals": [
                {"label": "Jaldi", "source_quote": "Mujhe abhi help chahiye", "explanation": "Sirf jaldi fraud ka saboot nahi; asli insaan ko bhi madad chahiye ho sakti hai."},
            ],
            "uncertainty": "Faisla karne ke liye maloomat bohat kam hain. Sachi emergency bhi ho sakti hai.",
            "recommended_actions": ["Us shakhs ko aise number par call karein jo aap pehle se jaante hain.", "Agar khatre ka andesha ho to ghar walon ya local emergency services se rabta karein."],
            "safe_reply": "Main madad karna chahta/chahti hoon. Abhi aapke aam number par call kar raha/rahi hoon, please uthayein.",
            "family_verification_suggested": True,
        },
    },
}
