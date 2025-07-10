from flask import Flask, render_template, request, jsonify, Blueprint

app = Flask(__name__)

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return render_template("index.html")

@routes.route("/predict")
def predict():
    return render_template("predict.html")

@routes.route("/chatbot")
def chatbot_ui():
    return render_template("chatbot.html")

@routes.route("/chatbot", methods=["POST"])
def chatbot_api():
    data = request.get_json()
    # If user sends a free-text question (symptoms)
    if "question" in data:
        question = data["question"].lower()
        # Expanded symptom-to-advice mapping
        if "fever" in question:
            diagnosis = "Fever is an elevated body temperature, often a sign of infection."
            suggestion = "Rest, drink fluids, and monitor your temperature. See a doctor if it persists or is very high."
        elif "fatigue" in question or "tired" in question or "exhausted" in question:
            diagnosis = "Fatigue means feeling tired or lacking energy."
            suggestion = "Get enough rest, eat well, and manage stress. If it continues, consult a doctor."
        elif "headache" in question:
            diagnosis = "Headache is pain in the head, which can vary in severity."
            suggestion = "Rest, stay hydrated, and avoid bright lights. See a doctor if severe or frequent."
        elif "cough" in question:
            diagnosis = "Cough helps clear your airways and can be dry or with mucus."
            suggestion = "Drink warm fluids and avoid irritants. See a doctor if it lasts more than a week."
        elif "muscle ache" in question or "muscle pain" in question or "sore muscles" in question:
            diagnosis = "Muscle aches are common with infections or after physical activity."
            suggestion = "Rest, gentle stretching, and stay hydrated. See a doctor if severe or persistent."
        elif "nausea" in question:
            diagnosis = "Nausea is feeling sick to your stomach and wanting to vomit."
            suggestion = "Eat light meals, avoid strong smells, and rest. See a doctor if it doesn't improve."
        elif "diarrhea" in question:
            diagnosis = "Diarrhea means frequent, loose, or watery stools."
            suggestion = "Drink fluids to prevent dehydration. See a doctor if it lasts more than 2 days."
        elif "night sweat" in question:
            diagnosis = "Night sweats are excessive sweating during sleep."
            suggestion = "Keep your room cool. If it happens often, consult a doctor."
        elif "chest pain" in question:
            diagnosis = "Chest pain can be serious and may signal a heart problem."
            suggestion = "If severe, radiating, or with shortness of breath, seek emergency care."
        elif "abdominal pain" in question or "stomach pain" in question:
            diagnosis = "Abdominal pain can have many causes."
            suggestion = "Rest, avoid heavy meals, and see a doctor if severe or persistent."
        elif "dizzy" in question or "dizziness" in question or "lightheaded" in question:
            diagnosis = "Dizziness is feeling lightheaded or unsteady."
            suggestion = "Sit or lie down, drink water, and see a doctor if it continues."
        elif "sore throat" in question:
            diagnosis = "Sore throat is pain or irritation in the throat."
            suggestion = "Drink warm fluids and rest your voice. See a doctor if it lasts more than a week."
        elif "rash" in question or "skin" in question or "itch" in question:
            diagnosis = "Skin rashes or itching can have many causes."
            suggestion = "Keep the area clean and avoid scratching. See a doctor if it spreads or is severe."
        elif "shortness of breath" in question or "breathless" in question:
            diagnosis = "Shortness of breath is difficulty breathing."
            suggestion = "Rest and avoid exertion. Seek immediate care if severe or with chest pain."
        elif "swelling" in question:
            diagnosis = "Swelling is abnormal enlargement of body parts."
            suggestion = "Elevate the area and avoid standing for long. See a doctor if sudden or severe."
        elif "weight loss" in question:
            diagnosis = "Unintentional weight loss can be a sign of illness."
            suggestion = "Monitor your weight and consult a doctor if you keep losing weight."
        elif "loss of appetite" in question or "not hungry" in question:
            diagnosis = "Loss of appetite means not feeling hungry."
            suggestion = "Eat small, frequent meals. See a doctor if it lasts more than a few days."
        elif "bowel" in question or "constipation" in question or "stool" in question:
            diagnosis = "Changes in bowel habits can include constipation, diarrhea, or changes in stool color."
            suggestion = "Eat fiber-rich foods and drink water. See a doctor if changes persist."
        elif "vomit" in question or "vomiting" in question:
            diagnosis = "Vomiting is forceful expulsion of stomach contents."
            suggestion = "Sip fluids to stay hydrated. See a doctor if you can't keep fluids down."
        elif "faint" in question or "fainting" in question or "passed out" in question:
            diagnosis = "Fainting is a temporary loss of consciousness."
            suggestion = "Lie down and elevate your legs. See a doctor to find the cause."
        elif "itch" in question or "itching" in question:
            diagnosis = "Itching is an uncomfortable skin sensation."
            suggestion = "Avoid scratching and use moisturizer. See a doctor if severe."
        elif "eye" in question or "eye irritation" in question or "red eye" in question:
            diagnosis = "Eye irritation can cause redness, itching, or watering."
            suggestion = "Avoid rubbing your eyes. Use clean water to rinse. See a doctor if it doesn't improve."
        elif "runny nose" in question:
            diagnosis = "Runny nose is excessive nasal discharge."
            suggestion = "Blow your nose gently and stay hydrated."
        elif "stuffy nose" in question or "nasal congestion" in question:
            diagnosis = "Stuffy nose is nasal congestion."
            suggestion = "Use saline drops and stay hydrated."
        elif "sneeze" in question or "sneezing" in question:
            diagnosis = "Sneezing is a reflex to clear your nose."
            suggestion = "Avoid allergens and keep your environment clean."
        elif "pain" in question:
            diagnosis = "Pain can occur in various parts of the body."
            suggestion = "Rest and use over-the-counter pain relief if needed. See a doctor if severe or unexplained."
        else:
            diagnosis = "Sorry, I couldn't identify your symptoms. Please provide more details or consult a doctor."
            suggestion = "For any severe or persistent symptoms, seek medical attention."
        return jsonify({"diagnosis": diagnosis, "suggestion": suggestion})

    # Otherwise, do risk analysis as before
    risk = []
    advice = []

    age = int(data.get("age", 0))
    bmi = float(data.get("bmi", 0))
    smoke = data.get("smoke", "No")
    alcohol = data.get("alcohol", "No")
    family = data.get("familyHistory", "No")
    stress = data.get("stressLevel", "No")
    exercise = data.get("exercise", "No")
    sleep = float(data.get("sleep", 0))
    activity = data.get("activity", "")
    salt = data.get("saltIntake", "No")
    bp_family = data.get("bpFamilyHistory", "No")
    frequent_urine = data.get("frequentUrine", "No")
    fatigue = data.get("fatigue", "No")
    vision = data.get("visionIssue", "No")

    if age > 45:
        risk.append("Your age increases your risk for chronic diseases.")
        advice.append("Get regular health checkups.")
    if bmi > 30:
        risk.append("Your BMI is in the obese range.")
        advice.append("Consult a nutritionist for a weight management plan.")
    elif bmi > 25:
        risk.append("Your BMI is in the overweight range.")
        advice.append("Consider a balanced diet and regular exercise.")
    if smoke == "Yes":
        risk.append("Smoking increases your risk for heart, lung, and cancer diseases.")
        advice.append("Try to quit smoking. Seek support if needed.")
    if alcohol == "Yes":
        risk.append("Alcohol consumption can affect your liver, heart, and increase cancer risk.")
        advice.append("Limit or avoid alcohol.")
    if family == "Yes":
        risk.append("Family history increases your risk for chronic diseases.")
        advice.append("Be extra vigilant with screenings and healthy habits.")
    if stress == "Yes":
        risk.append("High stress can impact your heart and immune system.")
        advice.append("Practice stress management: meditation, exercise, or hobbies.")
    if exercise == "No":
        risk.append("Lack of exercise increases your risk for obesity, diabetes, and heart disease.")
        advice.append("Aim for at least 30 minutes of activity most days.")
    if sleep < 6:
        risk.append("Short sleep duration can increase risk for obesity, diabetes, and heart disease.")
        advice.append("Aim for 7-8 hours of sleep per night.")
    if activity == "Sedentary":
        risk.append("Sedentary lifestyle increases risk for chronic diseases.")
        advice.append("Increase your daily movement and take regular breaks from sitting.")
    if salt == "Yes":
        risk.append("High salt intake can increase blood pressure.")
        advice.append("Reduce salt in your diet.")
    if bp_family == "Yes":
        risk.append("Family history of high blood pressure increases your risk.")
        advice.append("Monitor your blood pressure regularly.")
    if frequent_urine == "Yes":
        risk.append("Frequent urination or thirst can be a sign of diabetes.")
        advice.append("Consult a doctor for blood sugar testing.")
    if fatigue == "Yes":
        risk.append("Fatigue or excessive hunger can be a sign of diabetes or thyroid issues.")
        advice.append("Consult a healthcare provider for evaluation.")
    if vision == "Yes":
        risk.append("Blurred vision or slow-healing wounds can be a sign of diabetes.")
        advice.append("Consult a doctor for evaluation.")

    if not risk:
        risk.append("No major health risks detected based on your answers.")
        advice.append("Keep up your healthy lifestyle!")

    return jsonify({
        "diagnosis": " ".join(risk),
        "suggestion": " ".join(advice)
    })

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)