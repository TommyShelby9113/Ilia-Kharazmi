from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import openai
import json
from dosage_ai import calculate_dosage, get_all_drugs, search_drugs, DRUGS_DATABASE

app = Flask(__name__)
CORS(app)
app.secret_key = 'ilya-medical-ai-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

CNN_MODEL_PATH = 'models/skin_cancer_cnn.h5'
IMG_SIZE = 128  
CANCER_CLASSES = {
    0: "ملانوم (بدخیم)",
    1: "کارسینوم سلول بازال (بدخیم)",
    2: "کارسینوم سلول سنگفرشی (بدخیم)",
    3: "خال خوش‌خیم",
    4: "کراتوز سبوره‌ای (خوش‌خیم)",
    5: "درماتوفیبروما (خوش‌خیم)",
    6: "ضایعه عروقی (خوش‌خیم)"
}

def create_simple_model():
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
    
    model = Sequential([
        Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        Conv2D(16, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Conv2D(32, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(len(CANCER_CLASSES), activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

try:
    os.makedirs('models', exist_ok=True)
    if os.path.exists(CNN_MODEL_PATH):
        skin_cancer_model = load_model(CNN_MODEL_PATH)
        print("✅ مدل CNN با موفقیت بارگذاری شد.")
    else:
        print("⚠️ مدل CNN یافت نشد. مدل جدید ساخته می‌شود...")
        skin_cancer_model = create_simple_model()
        skin_cancer_model.save(CNN_MODEL_PATH)
        print("✅ مدل جدید ایجاد و ذخیره شد.")
except Exception as e:
    print(f"⚠️ خطا در بارگذاری مدل: {e}")
    skin_cancer_model = create_simple_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'skin_image' not in request.files:
        return jsonify({'error': 'هیچ فایلی انتخاب نشده است.'}), 400
    
    file = request.files['skin_image']
    if file.filename == '':
        return jsonify({'error': 'نام فایل خالی است.'}), 400
    
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        return jsonify({'error': 'لطفاً فقط فایل تصویری آپلود کنید.'}), 400
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    result = predict_skin_cancer(filepath)
    
    return jsonify(result)

def predict_skin_cancer(image_path):
    """تابع پیش‌بینی نوع سرطان با مدل CNN"""
    try:
        img = Image.open(image_path).resize((IMG_SIZE, IMG_SIZE))
        img_array = np.array(img) / 255.0
        
        if len(img_array.shape) == 2:
            img_array = np.stack([img_array] * 3, axis=-1)
        elif img_array.shape[2] == 4:
            img_array = img_array[:, :, :3]
        
        img_array = np.expand_dims(img_array, axis=0)
        
        predictions = skin_cancer_model.predict(img_array, verbose=0)
        confidence = np.max(predictions) * 100
        class_idx = np.argmax(predictions)
        
        
        result = {
            "class_name": CANCER_CLASSES.get(class_idx, "ناشناخته"),
            "confidence": round(confidence, 2),
            "is_malignant": "بدخیم" if class_idx < 3 else "خوش‌خیم",
            "image_url": f"/{image_path.replace('static/', '')}",
            "success": True
        }
        return result
    except Exception as e:
        return {"error": f"خطا در پردازش تصویر: {str(e)}", "success": False}

openai.api_key = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key-here')

@app.route('/chat', methods=['POST'])
def medical_chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'پیام نمی‌تواند خالی باشد.'}), 400
    
    system_prompt = """شما ایلیا هستید، یک دستیار هوش مصنوعی متخصص در پزشکی با دانش عمیق در زمینه:
- تشخیص و درمان بیماری‌ها
- فارماکولوژی و داروشناسی
- علائم و نشانه‌های بیماری‌ها
- آزمایش‌های تشخیصی
- پیشگیری از بیماری‌ها
- تغذیه و سبک زندگی سالم

محدودیت‌ها و دستورالعمل‌ها:
1. تنها در حوزه سلامت، بیماری‌ها، داروها و مشاوره پزشکی عمومی پاسخ دهید
2. هرگز برای مشکلات جدی جایگزین پزشک نشوید و همیشه به مراجعه به پزشک تأکید کنید
3. در موارد اورژانسی (علائم سکته، حمله قلبی، خونریزی شدید) فوراً به 115 ارجاع دهید
4. پاسخ‌ها باید علمی، دقیق و به زبان فارسی روان باشند
5. از دادن دوز دقیق دارو بدون اطلاع از شرایط بیمار خودداری کنید
6. به سوالات نامرتبط با پزشکی پاسخ ندهید و کاربر را به موضوع پزشکی راهنمایی کنید

شما ایلیا هستید، یک دستیار پزشکی حرفه‌ای و دلسوز."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=800,
            presence_penalty=0.3,
            frequency_penalty=0.3
        )
        reply = response.choices[0].message.content
        return jsonify({'reply': reply, 'success': True})
    except Exception as e:
        return jsonify({'error': f'خطا در ارتباط با OpenAI: {str(e)}', 'success': False})

@app.route('/get_drugs', methods=['GET'])
def get_drugs():
    """بازگرداندن لیست کامل داروها"""
    try:
        drugs = get_all_drugs()
        return jsonify({'drugs': drugs, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False})

@app.route('/search_drugs', methods=['GET'])
def search_drugs_api():
    """جستجوی داروها"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'drugs': [], 'success': True})
    
    try:
        results = search_drugs(query)
        return jsonify({'drugs': results, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False})

@app.route('/calculate_dose', methods=['POST'])
def calculate_dose():
    try:
        data = request.json
        weight = float(data.get('weight', 70))
        age = int(data.get('age', 45))
        genetic_marker = data.get('genetic_marker', 'normal')
        drug_name = data.get('drug_name', '')
        
        if not drug_name:
            return jsonify({'error': 'لطفاً یک دارو انتخاب کنید.', 'success': False}), 400
        
        result = calculate_dosage(
            drug_name=drug_name,
            weight=weight,
            age=age,
            gene_variant=genetic_marker,
            renal_function="normal",
            hepatic_function="normal"
        )
        
        if result is None:
            return jsonify({'error': 'داروی مورد نظر یافت نشد.', 'success': False}), 404
        
        # اضافه کردن اطلاعات تکمیلی
        result.update({
            "genetic_marker": genetic_marker,
            "weight_kg": weight,
            "age": age,
            "success": True
        })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'خطا در محاسبه دوز: {str(e)}', 'success': False})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)