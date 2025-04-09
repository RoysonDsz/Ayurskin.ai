import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from tensorflow.keras.models import load_model  # type: ignore
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # To securely load your API key from .env (optional but recommended)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # OR directly paste the key




app = Flask(__name__)



# Load the trained CNN model
model = load_model("resnet_model_93.06.keras")
# model = load_model("Transformer.pth")


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
        "Normal skin/Unknown": "No visible signs of skin conditions were detected, offering reassurance that your skin appears healthy. For Normal Skin, maintaining good skincare practices like cleansing, moisturizing, and sun protection is recommended. For Unknown Images (such as objects like bikes, environmental photos, or images unrelated to skin disease prediction), the system may not have sufficient confidence in making a clear classification. In such cases, further review or input may be required. If concerns persist, consulting an expert is always recommended for more accurate insights."
    }
}


# Define class names
class_names = ['Acne', 'Basal Cell Carcinoma', 'Eczema', 'Melanoma', 'Normal Skin/Unknown', 'Psoriasis']
IMAGE_SIZE = 224

# Create an upload directory
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Utility Functions
def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_image(image_path, image_size, model, class_names):
    """Preprocess the image and make a prediction using the model."""
    try:
        # Read and preprocess the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Invalid image file.")
        image_resized = cv2.resize(image, (image_size, image_size))
        image = np.expand_dims(image_resized, axis=0)

        # Predict
        prediction = model.predict(image, verbose=0)
        predicted_class = class_names[np.argmax(prediction)]
        confidence = np.max(prediction)
        return predicted_class, confidence
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None, None


        
# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prediction')
def prediction_page():
    return render_template('prediction.html')

@app.route('/healthfoods')
def healthfoods():
    return render_template('healthfoods.html')

@app.route('/skincare')
def skincare():
    return render_template('skincare.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/remedies', methods=['POST'])
def remedies():
    data = request.get_json()
    predicted_class = data.get("predicted_class")

    if not predicted_class:
        return jsonify({"error": "No disease provided"}), 400

    try:
        # Prompt Gemini to generate remedies
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        prompt = (
            f"You're an expert Ayurvedic assistant. Give 4-5 Ayurvedic remedies for the skin condition '{predicted_class}'. "
            "For each remedy, give a name and a short explanation of how it works. Make it easy to understand for someone new to Ayurveda."
        )
        response = model.generate_content(prompt)
        lines = response.text.split("\n")
        remedies_dict = {str(i+1): line for i, line in enumerate(lines) if line.strip()}
        
        
        return jsonify({"remedies": remedies_dict})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/chatbot_api', methods=['POST'])
def chatbot_api():
    data = request.get_json()
    user_message = data.get("message", "")
    predicted_disease = data.get("predicted_class", "Normal Skin/Unknown")

    try:
        # Start building the smart, friendly prompt
        base_intro = (
            "You are AyurSkin Bot — a chill, knowledgeable, Gen Z-friendly AI assistant "
            "that helps users with skin health issues. You give helpful, honest, and "
            "relatable advice about skin conditions, treatments (Ayurvedic + modern), and skincare tips.\n\n"
        )

        # If we have a known disease and remedies, add that context
        if predicted_disease in remedies_db:
            remedies = ""
            for name, details in remedies_db[predicted_disease].items():
                remedies += f"- {name}: {details}\n"
            context = (
                f"The user is asking a follow-up question related to: {predicted_disease}.\n"
                f"Here are some known Ayurvedic remedies:\n{remedies}\n\n"
            )
        else:
            context = (
                f"The user may not have a specific skin condition diagnosed, or it's unknown "
                f"(Predicted: {predicted_disease}). Just provide helpful general skin health advice based on their question.\n\n"
            )

        # Final full prompt
        prompt = (
            base_intro +
            context +
            f"User said: \"{user_message}\"\n\n"
            "Your reply should be short, chill, and straight to the point — like a helpful text from a friend. No long essays. If the user wants more info, they’ll ask again."
        )


        # Generate response from Gemini
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        reply = response.text.strip()

        return jsonify({"response": reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/predict', methods=['POST'])
def predict():
    """Handle file upload and make predictions."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PNG, JPG, and JPEG are allowed."}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({"error": f"File save failed: {e}"}), 500

    # Predict
    predicted_class, confidence = predict_image(file_path, IMAGE_SIZE, model, class_names)
    if predicted_class:
        result = {
            "predicted_class": predicted_class,
            "confidence": f"{confidence * 100:.2f}%",
            "image_url": f"/uploads/{file.filename}"
        }
        return jsonify(result)
    else:
        return jsonify({"error": "Prediction failed"}), 500
    
    
port = int(os.environ.get("PORT", 5000))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
