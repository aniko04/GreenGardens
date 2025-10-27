# My Likes Feature - Yoqtirgan Mahsulotlar

Bu feature foydalanuvchilarning yoqtirgan mahsulotlarini ko'rish imkonini beradi.

## Qo'shilgan yangi funksionallik:

### 1. My Likes sahifasi (/my-likes)
- Foydalanuvchi yoqtirgan barcha mahsulotlarni ko'rsatadi
- Pagination (sahifa bo'lib ko'rsatish) qo'shilgan
- Login qilmagan foydalanuvchilar uchun login taklifi
- Bo'sh wishlist uchun maxsus xabar

### 2. Navigation Menu
- "Shop" dropdowniga "My Likes" linki qo'shilgan
- Header-da yoqtirgan mahsulotlar hisobchisi (❤️ icon bilan)

### 3. Context Processor
- `home/context_processors.py`-ga `likes_context` qo'shilgan
- Barcha sahifalarda `{{ likes_count }}` mavjud

### 4. Real-time Updates
- Like/unlike qilinganda header-dagi hisobchi avtomatik yangilanadi
- JavaScript orqali AJAX so'rovlar bilan ishlaydi

## Foydalanish:

1. **Mahsulotni yoqtirish:**
   - Istalgan mahsulot sahifasida ❤️ tugmasini bosing
   - Yoqtirilgan mahsulot qizil rang oladi

2. **Yoqtirgan mahsulotlarni ko'rish:**
   - Header-dagi ❤️ icon-ga bosing yoki
   - Navigation menu-dan "Shop" → "My Likes"ni tanlang

3. **Yoqtirgan mahsulotlardan o'chirish:**
   - My Likes sahifasida ❤️ tugmasini qayta bosing

## Texnik tafsilotlar:

### Yangi fayllar:
- `templates/my-likes.html` - Asosiy template

### O'zgartirilgan fayllar:
- `home/views.py` - `my_likes` view qo'shilgan
- `home/urls.py` - `my-likes` URL qo'shilgan  
- `home/context_processors.py` - `likes_context` qo'shilgan
- `core/settings.py` - Context processor ro'yxatga qo'shilgan
- `templates/base.html` - Navigation va header yangilangan

### API Endpoints (Mavjud):
- `/api/user/{product_id}/likes/` - Mahsulot yoqtirilganligini tekshirish
- `/api/user/{product_id}/like/add` - Mahsulotni yoqtirish/rad etish  
- `/api/likes/count/` - Yoqtirgan mahsulotlar soni

## Database:
- `Like` modeli allaqachon mavjud edi
- Yangi migration kerak emas

## Xususiyatlar:
- ✅ Login qilgan foydalanuvchilar uchun ishlydi
- ✅ Real-time hisobchi yangilanishi
- ✅ Responsive dizayn
- ✅ Pagination qo'llab-quvvatlash
- ✅ Bo'sh holat uchun maxsus ko'rinish
- ✅ AJAX orqali tez ishlash

## Test qilish:
```bash
# Server ishga tushirish
python manage.py runserver

# Browser-da quyidagi sahifalarni oching:
http://localhost:8000/my-likes
http://localhost:8000/products

# Mahsulotni like qiling va my-likes sahifasini tekshiring
```