from pymongo import MongoClient # type: ignore
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from .env
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("❌ MONGO_URI not found in .env file!")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['AyurSkinAI']
collection = db['remedies']

# Drop old remedies (optional)
collection.delete_many({})

# Remedies dictionary (your massive dataset!)
remedies_db = {
    "Acne": {
        "Kumkumadi Lepam": "Made with Turmeric, Saffron, and Sandalwood, Kumkumadi Lepam is an Ayurvedic remedy for acne. Turmeric acts as an anti-inflammatory and antibacterial agent, reducing redness and preventing the growth of acne-causing bacteria. Saffron, packed with antioxidants, helps fade pigmentation, brightens the skin, and promotes healing. Sandalwood soothes irritated skin, controls excessive oil, and prevents clogging of pores. Together, these ingredients rejuvenate the skin, making it radiant and healthy.",
        "Yavvanapidaka Soap": "Formulated with Aloe Vera and Turmeric, this soap is effective in managing acne. Aloe Vera hydrates and soothes the skin, reducing irritation and redness caused by acne. Turmeric works as an antimicrobial agent, eliminating acne-causing bacteria and preventing future breakouts. Regular use of this soap leaves the skin smooth, clear, and blemish-free.",
        "Sarivakalpa": "Combining Sariva and Turmeric, Sarivakalpa works as a natural blood purifier that reduces acne from within. Sariva removes toxins from the bloodstream, which can trigger acne flare-ups, while Turmeric offers anti-inflammatory and antibacterial benefits, calming irritated skin and preventing infection. Together, they promote healthy, clear skin from the inside out.",
        "Leach Therapy (Jalaukavacharana)": "Leech therapy is an ancient detoxification method used for treating severe acne. Medicinal leeches draw out toxins from the affected area, improve blood circulation, and reduce inflammation. This method helps to heal deep-seated acne lesions and enhances skin regeneration for long-lasting relief.",
        "Panchanimba Churna": "Made primarily with Neem, Panchanimba Churna is a powerful herbal remedy for acne. Neem has antibacterial and antifungal properties which help clear up active acne and prevent new breakouts. It detoxifies the skin and soothes irritation, promoting a smooth and glowing complexion."
    },
    "Eczema": {
        "Arogyavardhini Rasa": "Formulated with Ginger, Cardamom, and Pepper, Arogyavardhini Rasa is a traditional Ayurvedic remedy for eczema. Ginger acts as an anti-inflammatory agent, reducing redness and irritation. Cardamom soothes the skin, while Pepper improves blood circulation, aiding in the absorption of nutrients to heal damaged skin. Together, these ingredients detoxify the body and help restore skin health.",
        "Panchatikta Ghritam": "Made with Neem, Vasaca, Amla, and Ghee, Panchatikta Ghritam is a ghee-based formulation for treating eczema. Neem provides antibacterial and antifungal benefits, while Vasaca and Amla help to reduce inflammation and boost skin repair. The ghee acts as a carrier, deeply hydrating and nourishing the skin, making it effective for managing dryness and irritation caused by eczema.",
        "Chakramardha Taila": "Derived from Chakramardha, this herbal oil is specifically designed to relieve eczema symptoms. Chakramardha has potent anti-inflammatory and antifungal properties that soothe irritated skin, reduce redness, and prevent infection. Regular application helps restore the skin’s natural barrier.",
        "Mahamanjistadi Kwatha": "Containing Manjista, Haridra (Turmeric), Amla, Triphala, and Saariva, Mahamanjistadi Kwatha is a detoxifying herbal decoction. Manjista purifies the blood, reducing eczema flare-ups, while Haridra and Amla provide anti-inflammatory and antioxidant benefits. Triphala and Saariva enhance the body’s natural detoxification process, leading to healthier and clearer skin."
    },
    "Melanoma": {
        "Amrita Ghanavati": "Amrita, also known as Guduchi, is the key ingredient in Amrita Ghanavati. It is renowned for its immune-boosting and detoxifying properties. This remedy helps in eliminating harmful toxins from the body, reducing oxidative stress, and promoting healthy skin regeneration. Its anti-inflammatory and antioxidant effects make it effective in managing symptoms and progression of melanoma.",
        "Kanchanara Guggulu": "A combination of Kanchanara, Ginger, Triphala, and Guggulu, this formulation helps in reducing abnormal tissue growth and boosting immunity. Kanchanara works to shrink tumor-like growths, while Ginger and Triphala enhance blood circulation and detoxification. Guggulu, a resin with anti-inflammatory properties, further supports skin healing and repair.",
        "Panchatikta Gritha": "Made with Neem, Vasaca, and ghee, this ghee-based preparation is a potent remedy for inflammatory skin conditions like melanoma. Neem and Vasaca work as anti-inflammatory and antioxidant agents to slow the progression of abnormal cell growth. Ghee nourishes the body from within, enhances absorption of herbs, and helps repair damaged skin cells.",
        "Suvarna Malini Vasanta": "This herbal formulation includes Swarnabhasma (gold ash), Nagabhasma (lead ash), and Saffron, making it a unique remedy for melanoma. Swarnabhasma and Nagabhasma have rejuvenating and immunomodulatory properties, while Saffron enhances cellular repair and reduces pigmentation. Together, they strengthen the immune response and promote healthy skin.",
        "Ashwagandha Arista": "Containing Ashwagandha, Manjista, Haridra, and Chandana, this herbal wine is an adaptogenic remedy for melanoma. Ashwagandha boosts immunity and reduces stress, which can exacerbate the condition. Manjista and Haridra purify the blood and reduce inflammation, while Chandana provides a cooling effect and soothes irritated skin."
    },
    "Basal Cell Carcinoma": {
        "Ashwagandha": "With its adaptogenic and anti-cancer properties, Ashwagandha strengthens the immune system and helps manage basal cell carcinoma. It reduces oxidative stress and inflammation, promoting healthy cell regeneration. Ashwagandha can be consumed as a supplement or applied externally in herbal preparations for localized treatment.",
        "Turmeric Paste": "Rich in curcumin, Turmeric has potent anti-inflammatory, antioxidant, and anticancer properties. When applied as a paste, it reduces inflammation and promotes the healing of basal cell carcinoma lesions. It also prevents further damage to the skin by neutralizing free radicals.",
        "Chakramardha Taila":"Derived from Chakramardha, this herbal oil is used to treat basal cell carcinoma. Chakramardha has strong anti-inflammatory and antimicrobial properties, which soothe the skin, reduce irritation, and support healing. Its regular application helps reduce lesion size and inflammation.",
        "Chanderprabha Vati": "Made with Chandraprabha, Karpura, Amrita, and Haridra, this remedy detoxifies the body and balances doshas, making it effective in managing basal cell carcinoma. Chandraprabha and Karpura purify the blood and strengthen immunity, while Amrita and Haridra offer antioxidant and anti-inflammatory benefits, reducing lesion progression.",
        "Kanchanara Guggulu": "This herbal formulation combines Kanchanara and Guggulu to address basal cell carcinoma. Kanchanara reduces swelling and abnormal cell growth, while Guggulu detoxifies the blood and enhances tissue repair. Together, they work to slow down the progression of carcinoma and support overall skin health."
    },
    "Psoriasis": {
        "Kaishora Guggulu":"Combining Amla, Haridra, Amrita, Ginger, and Pepper, Kaishora Guggulu is a powerful remedy for psoriasis. Amla and Haridra offer antioxidant and anti-inflammatory benefits, while Amrita helps detoxify the body. Ginger and Pepper improve digestion and circulation, promoting the body's natural ability to heal psoriatic lesions.",
        "Panchakarma": "An Ayurvedic detoxification therapy, Panchakarma focuses on eliminating toxins that aggravate psoriasis. It includes procedures like Vamana (therapeutic vomiting) and Virechana (purgation), which cleanse the digestive system, balance doshas, and rejuvenate the skin, making it an effective treatment for chronic skin conditions.",
        "Arogyavardhini Rasa": "Made with Triphala, Shilajitu, Guggulu, Neem, and Katuki, this formulation addresses the root cause of psoriasis by detoxifying the liver and skin. Triphala and Neem purify the blood, Shilajitu strengthens immunity, Guggulu reduces inflammation, and Katuki aids in detoxification, improving overall skin health.",
        "Panchatikta Gritha": "Containing Neem, Haritaki, and Haridra in a ghee-based formula, this remedy soothes inflamed skin and reduces scaling in psoriasis. The ghee deeply nourishes the skin, while Neem and Haridra provide antibacterial and anti-inflammatory benefits, helping to manage symptoms effectively.",
        "Vatari Guggulu": "Made with Castor Oil, Shuddha Gandhaka, Guggulu, and Triphala, Vatari Guggulu helps in reducing joint inflammation and skin lesions associated with psoriasis. Castor Oil acts as a mild laxative, aiding detoxification, while Guggulu and Triphala enhance blood purification and skin repair."
    },
    "Normal Skin/Unknown": {
        "Normal skin/Unknown": "No visible signs of skin conditions were detected..."
    }
}

# Insert new data
for disease, remedies in remedies_db.items():
    for name, description in remedies.items():
        collection.insert_one({
            "disease": disease,
            "remedy_name": name,
            "description": description
        })

print("✅ Remedies uploaded to MongoDB Atlas successfully!")
