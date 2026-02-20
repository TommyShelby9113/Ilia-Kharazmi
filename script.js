document.addEventListener('DOMContentLoaded', function() {
    const skinImageInput = document.getElementById('skinImageInput');
    const fileInfo = document.getElementById('fileInfo');
    const uploadArea = document.getElementById('uploadArea');
    const previewImage = document.getElementById('previewImage');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');

    skinImageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            fileInfo.textContent = `فایل انتخاب شده: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                imagePreviewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
            
            uploadArea.style.borderColor = '#00a86b';
            uploadArea.style.backgroundColor = '#e0f7f0';
        }
    });

    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#ffd700';
        uploadArea.style.backgroundColor = '#fff9e6';
    });

    uploadArea.addEventListener('dragleave', function() {
        uploadArea.style.borderColor = '#00a86b';
        uploadArea.style.backgroundColor = '#e0f7f0';
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            skinImageInput.files = e.dataTransfer.files;
            fileInfo.textContent = `فایل انتخاب شده: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                imagePreviewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
            
            uploadArea.style.borderColor = '#00a86b';
            uploadArea.style.backgroundColor = '#e0f7f0';
        } else {
            showAlert('لطفاً فقط فایل تصویری انتخاب کنید.', 'error');
        }
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
});

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${type}`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
        ${message}
    `;
    
    document.querySelector('main').prepend(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

async function processImage() {
    const fileInput = document.getElementById('skinImageInput');
    if (!fileInput.files[0]) {
        showAlert('لطفاً ابتدا یک تصویر انتخاب کنید.', 'error');
        return;
    }
    
    const processBtn = document.getElementById('processBtn');
    const loading = document.getElementById('loading');
    const resultCard = document.getElementById('resultCard');
    const resultImage = document.getElementById('resultImage');
    
    processBtn.style.display = 'none';
    loading.style.display = 'block';
    
    const formData = new FormData();
    formData.append('skin_image', fileInput.files[0]);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        loading.style.display = 'none';
        processBtn.style.display = 'inline-flex';
        
        if (!result.success || result.error) {
            showAlert(`خطا: ${result.error || 'خطای ناشناخته'}`, 'error');
            return;
        }
        
        document.getElementById('resultClass').textContent = result.class_name;
        document.getElementById('resultMalignancy').textContent = result.is_malignant;
        document.getElementById('resultConfidence').textContent = `${result.confidence}%`;
        
        resultImage.src = result.image_url || document.getElementById('previewImage').src;
        
        const confidenceBar = document.getElementById('confidenceBar');
        confidenceBar.style.width = `${result.confidence}%`;
        
        if (result.confidence >= 80) {
            confidenceBar.style.background = 'linear-gradient(90deg, #00a86b 0%, #00cc88 100%)';
        } else if (result.confidence >= 60) {
            confidenceBar.style.background = 'linear-gradient(90deg, #ffd700 0%, #ffed4e 100%)';
        } else {
            confidenceBar.style.background = 'linear-gradient(90deg, #ff6b6b 0%, #ff8e8e 100%)';
        }
        
        resultCard.style.display = 'block';
        
        resultCard.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error:', error);
        loading.style.display = 'none';
        processBtn.style.display = 'inline-flex';
        showAlert('خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.', 'error');
    }
}

async function sendMessage() {
    const userInput = document.getElementById('userMessage');
    const message = userInput.value.trim();
    
    if (!message) {
        showAlert('لطفاً پیام خود را بنویسید.', 'error');
        return;
    }
    
    const chatMessages = document.getElementById('chatMessages');
    
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user-message';
    userMessageDiv.innerHTML = `
        <div class="message-sender"><i class="fas fa-user"></i> شما</div>
        <div class="message-content">${message}</div>
    `;
    chatMessages.appendChild(userMessageDiv);
    
    userInput.value = '';
    
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot-message';
    typingIndicator.innerHTML = `
        <div class="message-sender"><i class="fas fa-robot"></i> ایلیا - دستیار پزشکی</div>
        <div class="message-content" id="typingIndicator">
            <i class="fas fa-ellipsis-h"></i> در حال پاسخ‌گویی...
        </div>
    `;
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        typingIndicator.remove();
        
        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'message bot-message';
        
        if (data.error || !data.success) {
            botMessageDiv.innerHTML = `
                <div class="message-sender"><i class="fas fa-robot"></i> ایلیا - دستیار پزشکی</div>
                <div class="message-content">
                    <i class="fas fa-exclamation-triangle"></i>
                    خطا در دریافت پاسخ: ${data.error || 'خطای ناشناخته'}
                </div>
            `;
        } else {
            botMessageDiv.innerHTML = `
                <div class="message-sender"><i class="fas fa-robot"></i> ایلیا - دستیار پزشکی</div>
                <div class="message-content">${data.reply}</div>
            `;
        }
        
        chatMessages.appendChild(botMessageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
    } catch (error) {
        console.error('Error:', error);
        typingIndicator.remove();
        
        const errorMessage = document.createElement('div');
        errorMessage.className = 'message bot-message';
        errorMessage.innerHTML = `
            <div class="message-sender"><i class="fas fa-robot"></i> ایلیا - دستیار پزشکی</div>
            <div class="message-content">
                <i class="fas fa-exclamation-triangle"></i>
                خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.
            </div>
        `;
        chatMessages.appendChild(errorMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

document.getElementById('userMessage').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});


let allDrugs = [];


async function loadDrugs() {
    try {
        const response = await fetch('/get_drugs');
        const data = await response.json();
        allDrugs = data.drugs;
        populateDrugSelect(allDrugs);
    } catch (error) {
        console.error('Error loading drugs:', error);
    }
}


function populateDrugSelect(drugs) {
    const select = document.getElementById('drugName');
    select.innerHTML = '<option value="">انتخاب دارو...</option>';
    drugs.forEach(drug => {
        const option = document.createElement('option');
        option.value = drug.name;
        option.textContent = drug.persian_name;
        select.appendChild(option);
    });
}

function searchDrugs() {
    const searchTerm = document.getElementById('drugSearch').value.toLowerCase();
    const filtered = allDrugs.filter(drug => 
        drug.name.toLowerCase().includes(searchTerm) || 
        drug.persian_name.includes(searchTerm)
    );
    populateDrugSelect(filtered);
}

async function calculateDose() {
    const weight = document.getElementById('weight').value;
    const age = document.getElementById('age').value;
    const geneticMarker = document.getElementById('geneticMarker').value;
    const drugName = document.getElementById('drugName').value;
    
    if (!weight || !age || !geneticMarker || !drugName) {
        showAlert('لطفاً تمام فیلدها را پر کنید.', 'error');
        return;
    }
    
    const doseResult = document.getElementById('doseResult');
    const calculateBtn = document.querySelector('.calculate-btn');
    const originalText = calculateBtn.innerHTML;
    calculateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> در حال محاسبه...';
    calculateBtn.disabled = true;
    
    try {
        const response = await fetch('/calculate_dose', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                weight: parseFloat(weight),
                age: parseInt(age),
                genetic_marker: geneticMarker,
                drug_name: drugName
            })
        });
        
        const data = await response.json();
        calculateBtn.innerHTML = originalText;
        calculateBtn.disabled = false;
        
        if (data.error || !data.success) {
            showAlert(`خطا: ${data.error || 'خطای ناشناخته'}`, 'error');
            return;
        }
        
        document.getElementById('resultDrug').textContent = data.drug_persian;
        document.getElementById('resultDose').textContent = data.recommended_dose_mg;
        
        let metabolismText = '';
        switch(data.genetic_marker) {
            case 'slow_metabolizer':
            case 'poor':
                metabolismText = 'متابولیسم آهسته';
                break;
            case 'fast_metabolizer':
            case 'ultra':
                metabolismText = 'متابولیسم سریع';
                break;
            default:
                metabolismText = 'متابولیسم نرمال';
        }
        
        document.getElementById('resultMetabolism').textContent = metabolismText;
        document.getElementById('resultWeight').textContent = data.weight_kg;
        document.getElementById('resultRange').textContent = data.dose_range;
        document.getElementById('doseNotes').textContent = data.notes;
        
        doseResult.style.display = 'block';
        doseResult.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error:', error);
        calculateBtn.innerHTML = originalText;
        calculateBtn.disabled = false;
        showAlert('خطا در محاسبه دوز. لطفاً دوباره تلاش کنید.', 'error');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadDrugs();
});