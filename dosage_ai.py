import json
import os

DRUGS_DATABASE = [
    {"name": "Warfarin", "persian_name": "وارفارین", "category": "ضد انعقاد", "base_dose": 5.0, "unit": "mg", "half_life": "40 ساعت", "dose_range": "2-10"},
    {"name": "Clopidogrel", "persian_name": "کلوپیدوگرل", "category": "ضد پلاکت", "base_dose": 75.0, "unit": "mg", "half_life": "8 ساعت", "dose_range": "75-300"},
    {"name": "Aspirin", "persian_name": "آسپیرین", "category": "ضد پلاکت", "base_dose": 81.0, "unit": "mg", "half_life": "6 ساعت", "dose_range": "81-325"},
    {"name": "Metoprolol", "persian_name": "متوپرولول", "category": "بتا بلاکر", "base_dose": 50.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "25-200"},
    {"name": "Atenolol", "persian_name": "آتنولول", "category": "بتا بلاکر", "base_dose": 50.0, "unit": "mg", "half_life": "7 ساعت", "dose_range": "25-100"},
    {"name": "Carvedilol", "persian_name": "کارودیلول", "category": "بتا بلاکر", "base_dose": 12.5, "unit": "mg", "half_life": "8 ساعت", "dose_range": "6.25-50"},
    {"name": "Lisinopril", "persian_name": "لیزینوپریل", "category": "ACE inhibitor", "base_dose": 10.0, "unit": "mg", "half_life": "12 ساعت", "dose_range": "5-40"},
    {"name": "Enalapril", "persian_name": "انالاپریل", "category": "ACE inhibitor", "base_dose": 10.0, "unit": "mg", "half_life": "11 ساعت", "dose_range": "5-40"},
    {"name": "Losartan", "persian_name": "لوزارتان", "category": "ARB", "base_dose": 50.0, "unit": "mg", "half_life": "9 ساعت", "dose_range": "25-100"},
    {"name": "Valsartan", "persian_name": "والزارتان", "category": "ARB", "base_dose": 80.0, "unit": "mg", "half_life": "6 ساعت", "dose_range": "80-320"},
    {"name": "Amlodipine", "persian_name": "آملودیپین", "category": "مسدودکننده کلسیم", "base_dose": 5.0, "unit": "mg", "half_life": "30 ساعت", "dose_range": "2.5-10"},
    {"name": "Nifedipine", "persian_name": "نیفدیپین", "category": "مسدودکننده کلسیم", "base_dose": 30.0, "unit": "mg", "half_life": "2 ساعت", "dose_range": "30-90"},
    {"name": "Digoxin", "persian_name": "دیگوکسین", "category": "گلیکوزید قلبی", "base_dose": 0.25, "unit": "mg", "half_life": "40 ساعت", "dose_range": "0.125-0.5"},
    {"name": "Amiodarone", "persian_name": "آمیودارون", "category": "ضد آریتمی", "base_dose": 200.0, "unit": "mg", "half_life": "58 روز", "dose_range": "100-400"},
    {"name": "Furosemide", "persian_name": "فوروزماید", "category": "ادرارآور", "base_dose": 40.0, "unit": "mg", "half_life": "2 ساعت", "dose_range": "20-80"},
    {"name": "Hydrochlorothiazide", "persian_name": "هیدروکلروتیازید", "category": "ادرارآور", "base_dose": 25.0, "unit": "mg", "half_life": "8 ساعت", "dose_range": "12.5-50"},
    {"name": "Spironolactone", "persian_name": "اسپیرونولاکتون", "category": "ادرارآور", "base_dose": 25.0, "unit": "mg", "half_life": "20 ساعت", "dose_range": "25-100"},
    
    {"name": "Metformin", "persian_name": "متفورمین", "category": "دیابت", "base_dose": 500.0, "unit": "mg", "half_life": "6 ساعت", "dose_range": "500-2000"},
    {"name": "Glibenclamide", "persian_name": "گلی بنکلامید", "category": "دیابت", "base_dose": 5.0, "unit": "mg", "half_life": "10 ساعت", "dose_range": "2.5-20"},
    {"name": "Glipizide", "persian_name": "گلیپیزید", "category": "دیابت", "base_dose": 5.0, "unit": "mg", "half_life": "3 ساعت", "dose_range": "2.5-20"},
    {"name": "Gliclazide", "persian_name": "گلی کلازید", "category": "دیابت", "base_dose": 80.0, "unit": "mg", "half_life": "12 ساعت", "dose_range": "40-320"},
    {"name": "Pioglitazone", "persian_name": "پیوگلیتازون", "category": "دیابت", "base_dose": 30.0, "unit": "mg", "half_life": "7 ساعت", "dose_range": "15-45"},
    {"name": "Sitagliptin", "persian_name": "سیتاگلیپتین", "category": "دیابت", "base_dose": 100.0, "unit": "mg", "half_life": "12 ساعت", "dose_range": "25-100"},
    {"name": "Empagliflozin", "persian_name": "امپاگلیفلوزین", "category": "دیابت", "base_dose": 10.0, "unit": "mg", "half_life": "13 ساعت", "dose_range": "10-25"},
    {"name": "Liraglutide", "persian_name": "لیراگلوتاید", "category": "دیابت", "base_dose": 1.2, "unit": "mg", "half_life": "13 ساعت", "dose_range": "0.6-1.8"},
    
    {"name": "Sertraline", "persian_name": "سرترالین", "category": "ضد افسردگی", "base_dose": 50.0, "unit": "mg", "half_life": "26 ساعت", "dose_range": "25-200"},
    {"name": "Fluoxetine", "persian_name": "فلوکستین", "category": "ضد افسردگی", "base_dose": 20.0, "unit": "mg", "half_life": "96 ساعت", "dose_range": "10-80"},
    {"name": "Citalopram", "persian_name": "سیتالوپرام", "category": "ضد افسردگی", "base_dose": 20.0, "unit": "mg", "half_life": "35 ساعت", "dose_range": "10-40"},
    {"name": "Escitalopram", "persian_name": "اس سیتالوپرام", "category": "ضد افسردگی", "base_dose": 10.0, "unit": "mg", "half_life": "30 ساعت", "dose_range": "5-20"},
    {"name": "Paroxetine", "persian_name": "پاروکستین", "category": "ضد افسردگی", "base_dose": 20.0, "unit": "mg", "half_life": "24 ساعت", "dose_range": "10-60"},
    {"name": "Venlafaxine", "persian_name": "ونلافاکسین", "category": "ضد افسردگی", "base_dose": 75.0, "unit": "mg", "half_life": "5 ساعت", "dose_range": "37.5-225"},
    {"name": "Duloxetine", "persian_name": "دولوکستین", "category": "ضد افسردگی", "base_dose": 60.0, "unit": "mg", "half_life": "12 ساعت", "dose_range": "30-120"},
    {"name": "Bupropion", "persian_name": "بوپروپیون", "category": "ضد افسردگی", "base_dose": 150.0, "unit": "mg", "half_life": "21 ساعت", "dose_range": "150-300"},
    {"name": "Mirtazapine", "persian_name": "میرتازاپین", "category": "ضد افسردگی", "base_dose": 30.0, "unit": "mg", "half_life": "20 ساعت", "dose_range": "15-45"},
    {"name": "Trazodone", "persian_name": "ترازودون", "category": "ضد افسردگی", "base_dose": 150.0, "unit": "mg", "half_life": "7 ساعت", "dose_range": "50-400"},
    
    {"name": "Risperidone", "persian_name": "ریسپریدون", "category": "ضد روانپریشی", "base_dose": 2.0, "unit": "mg", "half_life": "20 ساعت", "dose_range": "1-6"},
    {"name": "Olanzapine", "persian_name": "اولانزاپین", "category": "ضد روانپریشی", "base_dose": 10.0, "unit": "mg", "half_life": "30 ساعت", "dose_range": "5-20"},
    {"name": "Quetiapine", "persian_name": "کوئتیاپین", "category": "ضد روانپریشی", "base_dose": 300.0, "unit": "mg", "half_life": "7 ساعت", "dose_range": "150-800"},
    {"name": "Aripiprazole", "persian_name": "آریپیپرازول", "category": "ضد روانپریشی", "base_dose": 15.0, "unit": "mg", "half_life": "75 ساعت", "dose_range": "10-30"},
    {"name": "Haloperidol", "persian_name": "هالوپریدول", "category": "ضد روانپریشی", "base_dose": 5.0, "unit": "mg", "half_life": "21 ساعت", "dose_range": "2-20"},
    
    {"name": "Valproate", "persian_name": "والپروات", "category": "ضد صرع", "base_dose": 500.0, "unit": "mg", "half_life": "15 ساعت", "dose_range": "500-2000"},
    {"name": "Lamotrigine", "persian_name": "لاموتریژین", "category": "ضد صرع", "base_dose": 100.0, "unit": "mg", "half_life": "25 ساعت", "dose_range": "25-400"},
    {"name": "Carbamazepine", "persian_name": "کاربامازپین", "category": "ضد صرع", "base_dose": 400.0, "unit": "mg", "half_life": "25 ساعت", "dose_range": "200-1200"},
    {"name": "Phenytoin", "persian_name": "فنی توئین", "category": "ضد صرع", "base_dose": 300.0, "unit": "mg", "half_life": "22 ساعت", "dose_range": "200-400"},
    {"name": "Levetiracetam", "persian_name": "لووتیراستام", "category": "ضد صرع", "base_dose": 1000.0, "unit": "mg", "half_life": "7 ساعت", "dose_range": "1000-3000"},
    {"name": "Topiramate", "persian_name": "توپیرامات", "category": "ضد صرع", "base_dose": 100.0, "unit": "mg", "half_life": "21 ساعت", "dose_range": "50-400"},
    
    {"name": "Morphine", "persian_name": "مورفین", "category": "ضد درد", "base_dose": 10.0, "unit": "mg", "half_life": "3 ساعت", "dose_range": "5-30"},
    {"name": "Codeine", "persian_name": "کدئین", "category": "ضد درد", "base_dose": 30.0, "unit": "mg", "half_life": "3 ساعت", "dose_range": "15-60"},
    {"name": "Tramadol", "persian_name": "ترامادول", "category": "ضد درد", "base_dose": 50.0, "unit": "mg", "half_life": "6 ساعت", "dose_range": "50-400"},
    {"name": "Oxycodone", "persian_name": "اکسی کدون", "category": "ضد درد", "base_dose": 10.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "5-30"},
    {"name": "Ibuprofen", "persian_name": "ایبوپروفن", "category": "ضد التهاب", "base_dose": 400.0, "unit": "mg", "half_life": "2 ساعت", "dose_range": "200-800"},
    {"name": "Naproxen", "persian_name": "ناپروکسن", "category": "ضد التهاب", "base_dose": 500.0, "unit": "mg", "half_life": "14 ساعت", "dose_range": "250-1000"},
    {"name": "Diclofenac", "persian_name": "دیکلوفناک", "category": "ضد التهاب", "base_dose": 50.0, "unit": "mg", "half_life": "2 ساعت", "dose_range": "50-150"},
    {"name": "Celecoxib", "persian_name": "سلکوکسیب", "category": "ضد التهاب", "base_dose": 200.0, "unit": "mg", "half_life": "11 ساعت", "dose_range": "100-400"},
    
    {"name": "Amoxicillin", "persian_name": "آموکسی سیلین", "category": "آنتی‌بیوتیک", "base_dose": 500.0, "unit": "mg", "half_life": "1.5 ساعت", "dose_range": "250-1000"},
    {"name": "Cephalexin", "persian_name": "سفالکسین", "category": "آنتی‌بیوتیک", "base_dose": 500.0, "unit": "mg", "half_life": "1 ساعت", "dose_range": "250-1000"},
    {"name": "Ciprofloxacin", "persian_name": "سیپروفلوکساسین", "category": "آنتی‌بیوتیک", "base_dose": 500.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "250-750"},
    {"name": "Azithromycin", "persian_name": "آزیترومایسین", "category": "آنتی‌بیوتیک", "base_dose": 500.0, "unit": "mg", "half_life": "68 ساعت", "dose_range": "250-500"},
    {"name": "Doxycycline", "persian_name": "داکسی سایکلین", "category": "آنتی‌بیوتیک", "base_dose": 100.0, "unit": "mg", "half_life": "18 ساعت", "dose_range": "100-200"},
    {"name": "Metronidazole", "persian_name": "مترونیدازول", "category": "آنتی‌بیوتیک", "base_dose": 500.0, "unit": "mg", "half_life": "8 ساعت", "dose_range": "250-750"},
    {"name": "Clarithromycin", "persian_name": "کلاریترومایسین", "category": "آنتی‌بیوتیک", "base_dose": 500.0, "unit": "mg", "half_life": "5 ساعت", "dose_range": "250-500"},
    
    {"name": "Acyclovir", "persian_name": "اسیکلوویر", "category": "ضد ویروس", "base_dose": 400.0, "unit": "mg", "half_life": "3 ساعت", "dose_range": "200-800"},
    {"name": "Valacyclovir", "persian_name": "والاسیکلوویر", "category": "ضد ویروس", "base_dose": 1000.0, "unit": "mg", "half_life": "3 ساعت", "dose_range": "500-1000"},
    {"name": "Oseltamivir", "persian_name": "اسلتامیویر", "category": "ضد ویروس", "base_dose": 75.0, "unit": "mg", "half_life": "6 ساعت", "dose_range": "30-75"},
    
    {"name": "Fluconazole", "persian_name": "فلوکونازول", "category": "ضد قارچ", "base_dose": 150.0, "unit": "mg", "half_life": "30 ساعت", "dose_range": "50-400"},
    {"name": "Itraconazole", "persian_name": "ایتراکونازول", "category": "ضد قارچ", "base_dose": 200.0, "unit": "mg", "half_life": "24 ساعت", "dose_range": "100-400"},
    
    {"name": "Omeprazole", "persian_name": "امپرازول", "category": "PPI", "base_dose": 20.0, "unit": "mg", "half_life": "1 ساعت", "dose_range": "10-40"},
    {"name": "Pantoprazole", "persian_name": "پنتوپرازول", "category": "PPI", "base_dose": 40.0, "unit": "mg", "half_life": "1.5 ساعت", "dose_range": "20-80"},
    {"name": "Ranitidine", "persian_name": "رانیتیدین", "category": "H2 blocker", "base_dose": 150.0, "unit": "mg", "half_life": "3 ساعت", "dose_range": "75-300"},
    {"name": "Famotidine", "persian_name": "فاموتیدین", "category": "H2 blocker", "base_dose": 20.0, "unit": "mg", "half_life": "3 ساعت", "dose_range": "10-40"},
    {"name": "Ondansetron", "persian_name": "اندانسترون", "category": "ضد تهوع", "base_dose": 8.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "4-16"},
    {"name": "Metoclopramide", "persian_name": "متوکلوپرامید", "category": "ضد تهوع", "base_dose": 10.0, "unit": "mg", "half_life": "5 ساعت", "dose_range": "5-20"},
    
    {"name": "Salbutamol", "persian_name": "سالبوتامول", "category": "برونکودیلاتور", "base_dose": 0.1, "unit": "mg", "half_life": "4 ساعت", "dose_range": "0.1-0.2"},
    {"name": "Montelukast", "persian_name": "مونته لوکاست", "category": "ضد آسم", "base_dose": 10.0, "unit": "mg", "half_life": "5 ساعت", "dose_range": "4-10"},
    {"name": "Theophylline", "persian_name": "تئوفیلین", "category": "برونکودیلاتور", "base_dose": 300.0, "unit": "mg", "half_life": "8 ساعت", "dose_range": "100-600"},
    
    {"name": "Levothyroxine", "persian_name": "لووتیروکسین", "category": "هورمون تیروئید", "base_dose": 100.0, "unit": "mcg", "half_life": "7 روز", "dose_range": "25-200"},
    {"name": "Methimazole", "persian_name": "متی مازول", "category": "ضد تیروئید", "base_dose": 30.0, "unit": "mg", "half_life": "6 ساعت", "dose_range": "5-60"},
    
    {"name": "Prednisolone", "persian_name": "پردنیزولون", "category": "کورتیکواستروئید", "base_dose": 10.0, "unit": "mg", "half_life": "3 ساعت", "dose_range": "5-60"},
    {"name": "Dexamethasone", "persian_name": "دگزامتازون", "category": "کورتیکواستروئید", "base_dose": 4.0, "unit": "mg", "half_life": "5 ساعت", "dose_range": "2-16"},
    
    {"name": "Hydralazine", "persian_name": "هیدرالازین", "category": "وازودیلاتور", "base_dose": 50.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "25-100"},
    {"name": "Minoxidil", "persian_name": "مینوکسیدیل", "category": "وازودیلاتور", "base_dose": 5.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "2.5-40"},
    {"name": "Diltiazem", "persian_name": "دیلتیازم", "category": "مسدودکننده کلسیم", "base_dose": 180.0, "unit": "mg", "half_life": "5 ساعت", "dose_range": "120-360"},
    {"name": "Verapamil", "persian_name": "وراپامیل", "category": "مسدودکننده کلسیم", "base_dose": 240.0, "unit": "mg", "half_life": "6 ساعت", "dose_range": "120-480"},
    
    {"name": "Lidocaine", "persian_name": "لیدوکائین", "category": "ضد آریتمی", "base_dose": 1.0, "unit": "mg/kg", "half_life": "2 ساعت", "dose_range": "1-1.5"},
    {"name": "Procainamide", "persian_name": "پروکائین آمید", "category": "ضد آریتمی", "base_dose": 500.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "250-1000"},
    
    {"name": "Loratadine", "persian_name": "لوراتادین", "category": "آنتی‌هیستامین", "base_dose": 10.0, "unit": "mg", "half_life": "8 ساعت", "dose_range": "5-10"},
    {"name": "Cetirizine", "persian_name": "ستیریزین", "category": "آنتی‌هیستامین", "base_dose": 10.0, "unit": "mg", "half_life": "9 ساعت", "dose_range": "5-10"},
    {"name": "Fexofenadine", "persian_name": "فکسوفنادین", "category": "آنتی‌هیستامین", "base_dose": 180.0, "unit": "mg", "half_life": "14 ساعت", "dose_range": "120-180"},
    
    {"name": "Levodopa", "persian_name": "لوودوپا", "category": "پارکینسون", "base_dose": 100.0, "unit": "mg", "half_life": "1.5 ساعت", "dose_range": "100-250"},
    {"name": "Pramipexole", "persian_name": "پرامیپکسول", "category": "پارکینسون", "base_dose": 0.5, "unit": "mg", "half_life": "8 ساعت", "dose_range": "0.125-4.5"},
    
    {"name": "Donepezil", "persian_name": "دونپزیل", "category": "آلزایمر", "base_dose": 5.0, "unit": "mg", "half_life": "70 ساعت", "dose_range": "5-10"},
    {"name": "Rivastigmine", "persian_name": "ریواستیگمین", "category": "آلزایمر", "base_dose": 3.0, "unit": "mg", "half_life": "1.5 ساعت", "dose_range": "1.5-6"},
    
    {"name": "Sumatriptan", "persian_name": "سوماتریپتان", "category": "میگرن", "base_dose": 50.0, "unit": "mg", "half_life": "2 ساعت", "dose_range": "25-100"},
    {"name": "Propranolol", "persian_name": "پروپرانولول", "category": "بتا بلاکر", "base_dose": 40.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "20-160"},
    
    {"name": "Zolpidem", "persian_name": "زولپیدم", "category": "خواب‌آور", "base_dose": 10.0, "unit": "mg", "half_life": "2 ساعت", "dose_range": "5-10"},
    {"name": "Melatonin", "persian_name": "ملاتونین", "category": "خواب‌آور", "base_dose": 3.0, "unit": "mg", "half_life": "1 ساعت", "dose_range": "1-10"},
    
    {"name": "Allopurinol", "persian_name": "آلوپورینول", "category": "نقرس", "base_dose": 300.0, "unit": "mg", "half_life": "2 ساعت", "dose_range": "100-800"},
    {"name": "Colchicine", "persian_name": "کلشی سین", "category": "نقرس", "base_dose": 0.6, "unit": "mg", "half_life": "9 ساعت", "dose_range": "0.6-1.2"},
    {"name": "Bisoprolol", "persian_name": "بیزوپرولول", "category": "بتا بلاکر", "base_dose": 5.0, "unit": "mg", "half_life": "11 ساعت", "dose_range": "2.5-20"},
    {"name": "Ramipril", "persian_name": "رامیپریل", "category": "ACE inhibitor", "base_dose": 5.0, "unit": "mg", "half_life": "13 ساعت", "dose_range": "1.25-10"},
    {"name": "Candesartan", "persian_name": "کاندسارتان", "category": "ARB", "base_dose": 8.0, "unit": "mg", "half_life": "9 ساعت", "dose_range": "4-32"},
    {"name": "Tamsulosin", "persian_name": "تامسولوسین", "category": "پروستات", "base_dose": 0.4, "unit": "mg", "half_life": "10 ساعت", "dose_range": "0.4-0.8"},
    {"name": "Finasteride", "persian_name": "فیناستراید", "category": "پروستات", "base_dose": 5.0, "unit": "mg", "half_life": "8 ساعت", "dose_range": "1-5"},
    {"name": "Sildenafil", "persian_name": "سیلدنافیل", "category": "اختلال نعوظ", "base_dose": 50.0, "unit": "mg", "half_life": "4 ساعت", "dose_range": "25-100"},
    {"name": "Tadalafil", "persian_name": "تادالافیل", "category": "اختلال نعوظ", "base_dose": 10.0, "unit": "mg", "half_life": "18 ساعت", "dose_range": "5-20"},
]

def calculate_dosage(drug_name, weight, age, gene_variant, renal_function="normal", hepatic_function="normal"):
    """
    محاسبه دوز دارو بر اساس:
    - drug_name: نام دارو
    - weight: وزن بیمار (kg)
    - age: سن بیمار
    - gene_variant: نوع ژن (normal, slow_metabolizer, fast_metabolizer, poor, ultra)
    - renal_function: عملکرد کلیه (normal, moderate, severe)
    - hepatic_function: عملکرد کبد (normal, impaired)
    """
    
    drug = next((d for d in DRUGS_DATABASE if d["name"] == drug_name), None)
    if not drug:
        return None
    
    base_dose = drug["base_dose"]
    
    genetic_factor = 1.0
    if gene_variant in ["slow_metabolizer", "poor"]:
        genetic_factor = 0.5  # کاهش دوز برای متابولیسم آهسته
    elif gene_variant in ["fast_metabolizer", "ultra"]:
        genetic_factor = 1.5  # افزایش دوز برای متابولیسم سریع
    
    dose = base_dose * genetic_factor
    
    dose = dose * (weight / 70)
    
    if age > 65:
        dose = dose * 0.8  # کاهش دوز برای سالمندان
    elif age < 18:
        dose = dose * 0.7  # کاهش دوز برای کودکان و نوجوانان
    elif age < 12:
        dose = dose * 0.5  # کاهش بیشتر برای کودکان
    
    if renal_function == "moderate":
        dose = dose * 0.75
    elif renal_function == "severe":
        dose = dose * 0.5
    
    if hepatic_function == "impaired":
        dose = dose * 0.6
    
    dose_range_parts = drug["dose_range"].split("-")
    min_dose = float(dose_range_parts[0]) * (weight / 70) * genetic_factor
    max_dose = float(dose_range_parts[1]) * (weight / 70) * genetic_factor
    
    final_dose = max(min_dose, min(dose, max_dose))
    
    return {
        "drug_name": drug["name"],
        "drug_persian": drug["persian_name"],
        "base_dose": base_dose,
        "calculated_dose": round(final_dose, 2),
        "dose_range": f"{round(min_dose, 1)} - {round(max_dose, 1)} {drug['unit']}",
        "unit": drug["unit"],
        "half_life": drug["half_life"],
        "category": drug["category"],
        "genetic_factor": genetic_factor,
        "notes": f"⚠️ این محاسبه بر اساس وزن، سن، ژنتیک و عملکرد کلیه/کبد است. برای دوز دقیق حتماً با پزشک مشورت کنید."
    }

def get_all_drugs():
    """بازگرداندن لیست کامل داروها"""
    return [{"name": d["name"], "persian_name": d["persian_name"], "category": d["category"]} for d in DRUGS_DATABASE]

def search_drugs(query):
    """جستجوی داروها بر اساس نام انگلیسی یا فارسی"""
    query = query.lower()
    results = []
    for drug in DRUGS_DATABASE:
        if query in drug["name"].lower() or query in drug["persian_name"]:
            results.append({
                "name": drug["name"],
                "persian_name": drug["persian_name"],
                "category": drug["category"]
            })
    return results