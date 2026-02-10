# to run the code 

"""

This seed data has duplicate reviews

1. py manage.py shell 



2. If you want to start fresh (careful - deletes existing seeded data!)
from products.models import Category, Product, ProductImage, Review, Brand, Tag
from users.models import User
Category.objects.all().delete()
Product.objects.all().delete()
ProductImage.objects.all().delete()
Review.objects.all().delete()
Brand.objects.all().delete()
Tag.objects.all().delete()
User.objects.filter(email__startswith="test").delete()   # only test users

3. exec(open('seed_data.py').read())
    
"""



import os
import django
import random
from decimal import Decimal
from django.utils.text import slugify
from django.db import IntegrityError
import cloudinary
import cloudinary.uploader

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green_harvest_backend.settings')
django.setup()

from products.models import Category, Tag, Brand, Product, ProductImage, Review
from users.models import User

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

# ────────────────────────────────────────────────
# Your product data (corrected + additional 10) - unchanged from your last version
# ────────────────────────────────────────────────

corrected_products = [
    {
        "name": "Green Apple",
        "original_price": 20.99,
        "discount_percentage": round((20.99 - 14.99) / 20.99 * 100, 2), # ~28.58
        "category": "Apples", # Will map to hierarchical
        "description": "Discover the refreshing tartness of our premium Green Apples, carefully selected from sustainable orchards to deliver unmatched freshness and quality. These crunchy delights are perfect for those seeking a healthy, on-the-go snack or as a key ingredient in classic desserts like apple pies and crisps. Grown without synthetic pesticides, they embody the essence of natural farming practices that prioritize both flavor and environmental health.\n\nWith their vibrant green hue and juicy flesh, Green Apples offer a zesty balance of sweetness and acidity that elevates any dish. Whether sliced into salads, blended into smoothies, or baked into wholesome treats, they provide versatility in the kitchen while supporting overall wellness through their nutrient-rich profile.\n\n* 100g of Green Apples provides about 52 calories\n* Excellent source of dietary fiber for digestive health\n* Packed with vitamin C to boost immunity\n* Contains antioxidants that promote skin health and reduce inflammation\n\nIncorporate these exceptional Green Apples into your daily routine for a burst of natural energy and flavor. Ideal for families, athletes, and health enthusiasts alike, they represent the pinnacle of organic produce available today.",
        "weight": "1 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 750,
        "tags": ["Apple", "Green", "Fruit"],
        "images": [
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Green_Apple_wp4nv7.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Green_Apple_wp4nv7.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Green_Apple_wp4nv7.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Green_Apple_wp4nv7.png"
        ]
    },
    {
        "name": "Surjapur Mango",
        "original_price": 20.99,
        "discount_percentage": round((20.99 - 14.99) / 20.99 * 100, 2),
        "category": "Mangoes",
        "description": "Indulge in the exotic sweetness of Surjapur Mangoes, harvested at peak ripeness from tropical groves known for their rich soil and ideal climate. These luscious fruits offer a perfect blend of tangy and sweet flavors, making them an excellent choice for fresh eating, chutneys, or decadent mango lassis. Sourced organically, they ensure a pure taste experience free from artificial additives.\n\nThe smooth, golden flesh of Surjapur Mangoes melts in your mouth, providing a tropical escape with every bite. Ideal for fruit salads, smoothies, or even grilled as a unique dessert, they bring authentic regional flavors to your table while supporting sustainable agriculture.\n\n* 100g of Surjapur Mango provides approximately 60 calories\n* Rich in vitamins A and C for eye and immune health\n* Natural source of dietary fiber aiding digestion\n* Contains enzymes that promote healthy skin and hair\n\nElevate your culinary adventures with these premium Surjapur Mangoes, a staple in many traditional cuisines. Their vibrant aroma and juicy texture make them a must-have for fruit lovers seeking quality and authenticity.",
        "weight": "1 kg",
        "color": "mango",
        "type": "Organic",
        "stock_count": 750,
        "tags": ["Surjapur", "Mango", "Green", "Fruit"],
        "images": [
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Surjapur_Mango_rdfpod.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Surjapur_Mango_rdfpod.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Surjapur_Mango_rdfpod.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Surjapur_Mango_rdfpod.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Surjapur_Mango_rdfpod.png"
        ]
    },
    {
        "name": "Red Tomatoes",
        "original_price": 12.0,
        "discount_percentage": round((12.0 - 9.0) / 12.0 * 100, 2), # 25.0
        "category": "Vegetables",
        "description": "Experience the burst of flavor from our vine-ripened Red Tomatoes, grown in sun-drenched fields to achieve optimal juiciness and vibrant color. These versatile staples are essential for creating fresh salsas, robust pasta sauces, or simple caprese salads. Organically cultivated, they deliver pure, unadulterated taste without any chemical residues.\n\nWith their firm texture and sweet-acidic balance, Red Tomatoes enhance a wide array of dishes from soups to stews. They are a cornerstone of healthy eating, providing essential nutrients that support heart health and overall vitality.\n\n* 100g of Red Tomatoes provides about 18 calories\n* High in lycopene, an antioxidant for heart protection\n* Source of vitamins C and K for immune and bone health\n* Low-calorie option for weight-conscious diets\n\nBring the essence of summer to your kitchen year-round with these exceptional Red Tomatoes. Their fresh-from-the-farm quality makes them indispensable for both novice and seasoned cooks.",
        "weight": "1 kg",
        "color": "Red",
        "type": "Organic",
        "stock_count": 1800,
        "tags": ["Tomato", "Red", "Juicy"],
        "images": [
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Red_Tomatos_e7eiic.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Red_Tomatos_e7eiic.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Red_Tomatos_e7eiic.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Red_Tomatos_e7eiic.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Red_Tomatos_e7eiic.png"
        ]
    },
    {
        "name": "Fresh Cauliflower",
        "original_price": 20.0,
        "discount_percentage": round((20.0 - 17.0) / 20.0 * 100, 2), # 15.0
        "category": "Vegetables",
        "description": "Savor the mild, nutty flavor of our farm-fresh Cauliflower, harvested at the perfect stage for maximum tenderness and nutritional value. This versatile vegetable shines in roasted dishes, cauliflower rice, or as a low-carb alternative in various recipes. Grown organically, it ensures a clean, wholesome addition to your meals.\n\nThe dense, white florets of Cauliflower are packed with fiber and vitamins, making it a favorite for health-focused diets. Whether steamed, mashed, or baked, it absorbs flavors beautifully while contributing to a balanced diet.\n\n* 100g of Fresh Cauliflower provides around 25 calories\n* Abundant in vitamin C and K for antioxidant support\n* High fiber content for digestive wellness\n* Supports weight loss with its low-calorie profile\n\nTransform your cooking with this nutrient powerhouse, ideal for vegetarian and keto lifestyles. Our Fresh Cauliflower brings quality and freshness to every bite.",
        "weight": "1 kg",
        "color": "White",
        "type": "Organic",
        "stock_count": 600,
        "tags": ["Cauliflower", "White", "Healthy", "Vegetarian"],
        "images": [
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Fresh_Cauliflower_uwr6so.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Fresh_Cauliflower_uwr6so.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Fresh_Cauliflower_uwr6so.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Fresh_Cauliflower_uwr6so.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674453/Fresh_Cauliflower_uwr6so.png"
        ]
    },
    {
        "name": "Green Lettuce",
        "original_price": 14.99,
        "discount_percentage": None, # current == original
        "category": "Vegetables",
        "description": "Enjoy the crisp freshness of our Green Lettuce, picked daily from organic fields to provide the ultimate in crunch and nutrition for your salads and sandwiches. This leafy green is a staple for healthy eating, offering lightness and versatility in countless dishes. Free from pesticides, it represents the best of natural cultivation.\n\nThe tender leaves of Green Lettuce are hydrating and low in calories, perfect for building voluminous salads or wrapping fillings for a gluten-free option. Its mild flavor complements bold dressings and toppings seamlessly.\n\n* 100g of Green Lettuce provides approximately 15 calories\n* Rich in vitamins A and K for vision and bone health\n* High water content for hydration\n* Source of folate for cellular function\n\nMake Green Lettuce a cornerstone of your nutritious meals, enhancing both flavor and health benefits. It's an essential item for anyone prioritizing fresh, clean eating.",
        "weight": "0.5 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 1200,
        "tags": ["Salad", "Fresh", "Lettuce", "Green", "Vegetarian"],
        "images": [
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Lettuce_egujdc.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Lettuce_egujdc.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Lettuce_egujdc.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Lettuce_egujdc.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Lettuce_egujdc.png"
        ]
    },
    {
        "name": "Green Capsicum",
        "original_price": 20.99,
        "discount_percentage": round((20.99 - 14.99) / 20.99 * 100, 2),
        "category": "Vegetables",
        "description": "Delight in the crisp, fresh taste of our Green Capsicum, cultivated organically for superior quality and flavor in stews, grills, and stir-fries. These bell peppers add a vibrant crunch and mild sweetness to any meal. Sourced from trusted farms, they ensure purity and sustainability.\n\nThe smooth, glossy skin and juicy interior of Green Capsicum make it ideal for stuffing, slicing, or roasting, enhancing dishes with their unique texture and taste.\n\n* 100g of Green Capsicum provides about 20 calories\n* Loaded with vitamin C for immune support\n* Good source of fiber for gut health\n* Contains antioxidants for cellular protection\n\nIncorporate Green Capsicum into your cooking for a nutritious boost that's both delicious and versatile. Perfect for vegetarian recipes and healthy lifestyles.",
        "weight": "1 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 850,
        "tags": ["Capsicum", "Bell Pepper", "Green", "Organic", "Vegetarian"],
        "images": [
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Capsicum_uu5bie.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Capsicum_uu5bie.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Capsicum_uu5bie.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Capsicum_uu5bie.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Capsicum_uu5bie.png"
        ]
    },
    {
        "name": "Green Chilli",
        "original_price": 14.99,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Add a fiery kick to your dishes with our hand-picked Green Chillies, grown organically to deliver authentic heat and freshness. These spicy peppers are essential for curries, salsas, and marinades, bringing bold flavor to any cuisine. Sourced sustainably, they offer pure, intense taste.\n\nThe slender, vibrant green pods of Green Chillies provide adjustable spiciness, allowing you to control the heat in your recipes while enjoying their fresh, grassy notes.\n\n* 100g of Green Chilli provides approximately 40 calories\n* High in capsaicin for metabolism boost\n* Source of vitamins A and C for eye and immune health\n* Natural pain reliever properties\n\nSpice up your meals with these premium Green Chillies, a must for lovers of bold flavors. Their versatility makes them indispensable in global cooking traditions.",
        "weight": "0.25 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 3000,
        "tags": ["Spicy", "Chilli", "Hot", "Vegetarian"],
        "images": [
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Chilli_b6zrtx.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Chilli_b6zrtx.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Chilli_b6zrtx.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Chilli_b6zrtx.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Chilli_b6zrtx.png" 
        ]
    },
    {
        "name": "Eggplant",
        "original_price": 14.99,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Explore the rich, meaty texture of our glossy Eggplants, organically grown for optimal flavor absorption in curries, roasts, and grills. These deep-purple gems are perfect for vegetarian mains like eggplant parmesan or baba ganoush. Harvested fresh, they ensure quality and nutrition.\n\nThe spongy flesh of Eggplant becomes tender and flavorful when cooked, making it a versatile ingredient that pairs well with bold spices and sauces.\n\n* 100g of Eggplant provides about 25 calories\n* Rich in fiber for digestive support\n* Contains antioxidants like nasunin for brain health\n* Low in carbs for keto-friendly diets\n\nDiscover new culinary possibilities with our premium Eggplants, ideal for healthy, satisfying meals. Their unique qualities make them a favorite in Mediterranean and Asian cuisines.",
        "weight": "1.5 kg",
        "color": "Purple",
        "type": "Organic",
        "stock_count": 1100,
        "tags": ["Eggplant", "Aubergine", "Purple", "Vegetarian"],
        "images": [
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Eggplant_qp6uxe.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Eggplant_qp6uxe.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Eggplant_qp6uxe.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Eggplant_qp6uxe.png",
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Eggplant_qp6uxe.png"
        ]
    },
    {
        "name": "Organic Carrots",
        "original_price": 8.99,
        "discount_percentage": None,
        "category": "Root Vegetables",
        "description": "Taste the natural sweetness of our Organic Carrots, pulled from nutrient-rich soil at peak maturity for the best crunch and flavor. These vibrant orange roots are ideal for snacking, juicing, or adding to soups and stews. Grown without chemicals, they offer pure, earthy goodness.\n\nThe crisp texture and beta-carotene richness of Carrots make them a health staple, supporting vision and immune function in delicious ways.\n\n* 100g of Organic Carrots provides around 41 calories\n* High in beta-carotene for eye health\n* Source of fiber and potassium for heart support\n* Antioxidant properties for overall wellness\n\nIncorporate these versatile Organic Carrots into your diet for a nutritious boost. Perfect for all ages, they add color and health to every meal.",
        "weight": "1 kg",
        "color": "Orange",
        "type": "Organic",
        "stock_count": 2200,
        "tags": ["Carrot", "Orange", "Root Vegetable", "Vegetarian"],
        "images": [
            "https://www.shutterstock.com/image-photo/fresh-carrots-sliced-isolated-on-600nw-2535894659.jpg",
            "https://www.shutterstock.com/image-photo/fresh-carrots-sliced-isolated-on-600nw-2535894659.jpg",
            "https://www.shutterstock.com/image-photo/fresh-carrots-sliced-isolated-on-600nw-2535894659.jpg",
            "https://www.shutterstock.com/image-photo/fresh-carrots-sliced-isolated-on-600nw-2535894659.jpg",
            "https://www.shutterstock.com/image-photo/fresh-carrots-sliced-isolated-on-600nw-2535894659.jpg"
        ]
    },
    {
        "name": "Fresh Spinach",
        "original_price": 5.5,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Revitalize your meals with our tender Fresh Spinach, harvested young for maximum iron content and delicate flavor in smoothies, salads, and sautés. This nutrient-dense green is a powerhouse for health, offering versatility in both raw and cooked forms. Organically grown for purity and freshness.\n\nThe vibrant leaves of Spinach are packed with vitamins, making it an excellent choice for boosting energy and supporting bone health.\n\n* 100g of Fresh Spinach provides about 23 calories\n* Rich in iron for blood health\n* High in vitamins A, C, and K for immunity and vision\n* Folate content supports cell growth\n\nMake Fresh Spinach a daily essential for vibrant health and delicious dishes. Its quick preparation makes it ideal for busy lifestyles.",
        "weight": "0.2 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 1500,
        "tags": ["Spinach", "Leafy", "Green", "Vegetarian"],
        "images": [
            "https://adelaidefresh.com.au/cdn/shop/files/spinach_1024x.webp?v=1713158555",
            "https://adelaidefresh.com.au/cdn/shop/files/spinach_1024x.webp?v=1713158555",
            "https://adelaidefresh.com.au/cdn/shop/files/spinach_1024x.webp?v=1713158555",
            "https://adelaidefresh.com.au/cdn/shop/files/spinach_1024x.webp?v=1713158555",
            "https://adelaidefresh.com.au/cdn/shop/files/spinach_1024x.webp?v=1713158555"
        ]
    },
    {
        "name": "Yellow Onions",
        "original_price": 4.99,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Unlock layers of flavor with our pungent Yellow Onions, essential for building depth in soups, sauces, and caramelized dishes. Grown organically, these versatile bulbs offer a perfect balance of sweetness and sharpness when cooked. Sourced for quality and longevity.\n\nThe firm, golden skins protect the juicy layers inside, making Yellow Onions a kitchen staple for savory recipes worldwide.\n\n* 100g of Yellow Onions provides approximately 40 calories\n* Source of quercetin antioxidant for heart health\n* Contains prebiotic fibers for gut support\n* Vitamin C for immune function\n\nElevate your cooking foundation with these reliable Yellow Onions, indispensable for both everyday meals and gourmet creations.",
        "weight": "2 kg",
        "color": "Yellow",
        "type": "Organic",
        "stock_count": 4000,
        "tags": ["Onion", "Yellow", "Cooking"],
        "images": [
            "https://growhoss.com/cdn/shop/products/yellow-sweet-spanish-utah-onion_460x@2x.jpg?v=1691784853",
            "https://growhoss.com/cdn/shop/products/yellow-sweet-spanish-utah-onion_460x@2x.jpg?v=1691784853",
            "https://growhoss.com/cdn/shop/products/yellow-sweet-spanish-utah-onion_460x@2x.jpg?v=1691784853",
            "https://growhoss.com/cdn/shop/products/yellow-sweet-spanish-utah-onion_460x@2x.jpg?v=1691784853",
            "https://growhoss.com/cdn/shop/products/yellow-sweet-spanish-utah-onion_460x@2x.jpg?v=1691784853"
        ]
    },
    {
        "name": "Red Bell Pepper",
        "original_price": 15.0,
        "discount_percentage": round((15.0 - 12.5) / 15.0 * 100, 2), # 16.67
        "category": "Vegetables",
        "description": "Brighten your plates with our sweet Red Bell Peppers, ripened on the vine for maximum vitamin C content and crunch in stir-fries and stuffings. These organic peppers offer a smoky sweetness that's perfect for grilling or fresh salads. Harvested at peak for flavor.\n\nThe thick walls and juicy interior of Red Bell Peppers make them ideal for adding color and nutrition to diverse cuisines.\n\n* 100g of Red Bell Pepper provides about 31 calories\n* Exceptional vitamin C source for collagen production\n* Antioxidants like beta-carotene for skin health\n* Low-calorie with high fiber for satiety\n\nIncorporate Red Bell Peppers for a nutritious, flavorful enhancement to your meals. Their versatility suits both raw and cooked applications beautifully.",
        "weight": "0.5 kg",
        "color": "Red",
        "type": "Organic",
        "stock_count": 940,
        "tags": ["Pepper", "Red", "Sweet", "Vegetarian"],
        "images": [
            "https://sc02.alicdn.com/kf/H11b3acff15514be39458c1d186316e5bH.png",
            "https://sc02.alicdn.com/kf/H11b3acff15514be39458c1d186316e5bH.png",
            "https://sc02.alicdn.com/kf/H11b3acff15514be39458c1d186316e5bH.png",
            "https://sc02.alicdn.com/kf/H11b3acff15514be39458c1d186316e5bH.png",
            "https://sc02.alicdn.com/kf/H11b3acff15514be39458c1d186316e5bH.png"
        ]
    },
    {
        "name": "Garlic Bulbs",
        "original_price": 2.99,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Infuse your dishes with the aromatic potency of our Garlic Bulbs, organically cultivated for strong flavor and health benefits in seasonings and sauces. These essential cloves are known for their immune-boosting properties and culinary versatility. Freshly harvested for maximum impact.\n\nThe plump, white cloves of Garlic release a pungent aroma when crushed, elevating everything from marinades to roasts.\n\n* 100g of Garlic Bulbs provides approximately 149 calories\n* Rich in allicin for antibacterial effects\n* Supports heart health with sulfur compounds\n* High in manganese and vitamin B6\n\nMake Garlic Bulbs a staple in your pantry for authentic flavors and wellness support. Their bold profile enhances global cuisines effortlessly.",
        "weight": "0.1 kg",
        "color": "White",
        "type": "Organic",
        "stock_count": 5000,
        "tags": ["Garlic", "Aromatic", "Seasoning"],
        "images": [
            "https://m.media-amazon.com/images/I/71OuWVJpp5L.jpg",
            "https://m.media-amazon.com/images/I/71OuWVJpp5L.jpg",
            "https://m.media-amazon.com/images/I/71OuWVJpp5L.jpg",
            "https://m.media-amazon.com/images/I/71OuWVJpp5L.jpg",
            "https://m.media-amazon.com/images/I/71OuWVJpp5L.jpg"
        ]
    },
    {
        "name": "Cucumber",
        "original_price": 7.5,
        "discount_percentage": round((7.5 - 6.5) / 7.5 * 100, 2), # 13.33
        "category": "Vegetables",
        "description": "Refresh your senses with our hydrating Cucumbers, grown organically for crisp texture and mild flavor in salads, pickles, and infused waters. These cooling vegetables are perfect for summer dishes and healthy snacking. Sourced fresh for optimal quality.\n\nThe smooth, green skin and juicy flesh of Cucumbers provide a light, refreshing base for various recipes while aiding hydration.\n\n* 100g of Cucumber provides about 16 calories\n* High water content for natural hydration\n* Source of vitamin K for blood clotting\n* Antioxidants for skin rejuvenation\n\nAdd Cucumbers to your routine for a low-calorie, nutritious option that's versatile and delicious. Ideal for detox drinks and fresh meals.",
        "weight": "0.5 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 1300,
        "tags": ["Cucumber", "Fresh", "Hydrating"],
        "images": [
            "https://i.pinimg.com/736x/78/b2/de/78b2de06151c2e1a4aefae0255a645d8.jpg",
            "https://i.pinimg.com/736x/78/b2/de/78b2de06151c2e1a4aefae0255a645d8.jpg",
            "https://i.pinimg.com/736x/78/b2/de/78b2de06151c2e1a4aefae0255a645d8.jpg",
            "https://i.pinimg.com/736x/78/b2/de/78b2de06151c2e1a4aefae0255a645d8.jpg",
            "https://i.pinimg.com/736x/78/b2/de/78b2de06151c2e1a4aefae0255a645d8.jpg"
        ]
    },
    {
        "name": "Ginger Root",
        "original_price": 13.0,
        "discount_percentage": None,
        "category": "Root Vegetables",
        "description": "Awaken your palate with our spicy Ginger Root, organically grown for potent flavor and digestive benefits in teas, stir-fries, and baked goods. This aromatic rhizome is essential for Asian-inspired dishes and natural remedies. Freshly dug for authenticity.\n\nThe knobby, tan exterior hides a fibrous, zesty interior that adds warmth and depth to recipes while supporting nausea relief.\n\n* 100g of Ginger Root provides approximately 80 calories\n* Contains gingerol for anti-inflammatory effects\n* Aids digestion and reduces nausea\n* Source of potassium and magnesium\n\nIncorporate Ginger Root for its medicinal and culinary prowess, enhancing both health and flavor in your daily life.",
        "weight": "0.25 kg",
        "color": "Brown",
        "type": "Organic",
        "stock_count": 700,
        "tags": ["Ginger", "Spice", "Root"],
        "images": [
            "https://static.vecteezy.com/system/resources/thumbnails/006/972/792/small/fresh-ginger-rhizome-with-sliced-and-green-leaves-isolated-on-white-background-with-clipping-path-free-photo.jpg",
            "https://static.vecteezy.com/system/resources/thumbnails/006/972/792/small/fresh-ginger-rhizome-with-sliced-and-green-leaves-isolated-on-white-background-with-clipping-path-free-photo.jpg",
            "https://static.vecteezy.com/system/resources/thumbnails/006/972/792/small/fresh-ginger-rhizome-with-sliced-and-green-leaves-isolated-on-white-background-with-clipping-path-free-photo.jpg",
            "https://static.vecteezy.com/system/resources/thumbnails/006/972/792/small/fresh-ginger-rhizome-with-sliced-and-green-leaves-isolated-on-white-background-with-clipping-path-free-photo.jpg",
            "https://static.vecteezy.com/system/resources/thumbnails/006/972/792/small/fresh-ginger-rhizome-with-sliced-and-green-leaves-isolated-on-white-background-with-clipping-path-free-photo.jpg"
        ]
    },
    {
        "name": "Sweet Corn",
        "original_price": 5.0,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Savor the natural sweetness of our golden Sweet Corn, harvested fresh for tender kernels perfect in salads, soups, or grilled on the cob. This organic staple brings summery flavor to your table year-round. Sourced from fertile fields for quality.\n\nThe plump, yellow ears of Sweet Corn offer a burst of juiciness and natural sugars, making it a family favorite for barbecues and side dishes.\n\n* 100g of Sweet Corn provides about 86 calories\n* Good source of fiber for digestive health\n* Contains lutein for eye protection\n* Provides energy-boosting carbohydrates\n\nEnjoy Sweet Corn for its versatile, delicious nature that complements any meal with nutrition and taste.",
        "weight": "0.5 kg",
        "color": "Yellow",
        "type": "Organic",
        "stock_count": 1600,
        "tags": ["Corn", "Sweet", "Cob"],
        "images": [
            "https://www.veggycation.com.au/siteassets/veggycationvegetable/sweet-corn.jpg",
            "https://www.veggycation.com.au/siteassets/veggycationvegetable/sweet-corn.jpg",
            "https://www.veggycation.com.au/siteassets/veggycationvegetable/sweet-corn.jpg",
            "https://www.veggycation.com.au/siteassets/veggycationvegetable/sweet-corn.jpg",
            "https://www.veggycation.com.au/siteassets/veggycationvegetable/sweet-corn.jpg"
        ]
    },
    {
        "name": "Russet Potatoes",
        "original_price": 10.99,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Discover the fluffy interior of our starchy Russet Potatoes, ideal for mashing, baking, or frying into crispy delights. Organically grown in rich soil, these versatile tubers provide comfort food classics with superior quality. Harvested for optimal storage and flavor.\n\nThe rough, brown skin encases a light, mealy flesh that's perfect for absorbing butter and seasonings in various preparations.\n\n* 100g of Russet Potatoes provides approximately 77 calories\n* High in potassium for blood pressure control\n* Source of vitamin C and B6 for energy\n* Complex carbs for sustained fuel\n\nRely on Russet Potatoes for hearty, nutritious meals that satisfy and nourish the whole family.",
        "weight": "2.5 kg",
        "color": "Brown",
        "type": "Organic",
        "stock_count": 3500,
        "tags": ["Potato", "Starchy", "Baking"],
        "images": [
            "https://www.simplyrecipes.com/thmb/KN0_1D5tEosls-G9C-OmJ02DdEY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Yukin-Vs-Gold-LEAD-01-d250aa91a1b540058f305f70d9b6d585.jpg",
            "https://www.simplyrecipes.com/thmb/KN0_1D5tEosls-G9C-OmJ02DdEY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Yukin-Vs-Gold-LEAD-01-d250aa91a1b540058f305f70d9b6d585.jpg",
            "https://www.simplyrecipes.com/thmb/KN0_1D5tEosls-G9C-OmJ02DdEY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Yukin-Vs-Gold-LEAD-01-d250aa91a1b540058f305f70d9b6d585.jpg",
            "https://www.simplyrecipes.com/thmb/KN0_1D5tEosls-G9C-OmJ02DdEY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Yukin-Vs-Gold-LEAD-01-d250aa91a1b540058f305f70d9b6d585.jpg",
            "https://www.simplyrecipes.com/thmb/KN0_1D5tEosls-G9C-OmJ02DdEY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Yukin-Vs-Gold-LEAD-01-d250aa91a1b540058f305f70d9b6d585.jpg"
        ]
    },
    {
        "name": "Zucchini",
        "original_price": 11.5,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Embrace the mild versatility of our Green Zucchini, organically cultivated for tender flesh in sautés, spirals, or baked goods. This summer squash adds subtle flavor and nutrition to low-carb meals. Freshly picked for quality.\n\nThe elongated, green form of Zucchini makes it perfect for quick cooking methods that preserve its crispness and nutrients.\n\n* 100g of Zucchini provides about 17 calories\n* High in vitamin C and potassium\n* Low-carb option for weight management\n* Hydrating with high water content\n\nUtilize Zucchini for healthy, creative cooking that supports wellness and tastes great in every season.",
        "weight": "0.5 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 900,
        "tags": ["Zucchini", "Green", "Squash"],
        "images": [
            "https://static.vecteezy.com/system/resources/thumbnails/004/289/558/small/zucchini-isolated-on-white-background-photo.jpg",
            "https://static.vecteezy.com/system/resources/thumbnails/004/289/558/small/zucchini-isolated-on-white-background-photo.jpg",
            "https://static.vecteezy.com/system/resources/thumbnails/004/289/558/small/zucchini-isolated-on-white-background-photo.jpg",
            "https://static.vecteezy.com/system/resources/thumbnails/004/289/558/small/zucchini-isolated-on-white-background-photo.jpg",
            "https://static.vecteezy.com/system/resources/thumbnails/004/289/558/small/zucchini-isolated-on-white-background-photo.jpg"
        ]
    },
    {
        "name": "Red Onion",
        "original_price": 6.5,
        "discount_percentage": round((6.5 - 5.5) / 6.5 * 100, 2), # 15.38
        "category": "Vegetables",
        "description": "Add sharp zest to your dishes with our colorful Red Onions, organically grown for crisp texture in salads, pickles, and grilled recipes. These vibrant bulbs offer a milder flavor than yellow varieties. Sourced fresh for superior taste.\n\nThe purple-red layers of Red Onions provide visual appeal and a sweet pungency that enhances raw and cooked applications alike.\n\n* 100g of Red Onion provides approximately 40 calories\n* Rich in anthocyanins for antioxidant benefits\n* Supports immune health with vitamin C\n* Prebiotic fibers for gut wellness\n\nIncorporate Red Onions for flavor depth and nutritional value in your favorite meals.",
        "weight": "1 kg",
        "color": "Red",
        "type": "Organic",
        "stock_count": 2100,
        "tags": ["Onion", "Red", "Salad"],
        "images": [
            "https://www.edenbrothers.com/cdn/shop/files/onion-ruby-red-shk-1_94c13225-d0e6-4f7d-b738-16baceab4aa0.jpg?v=1726674318",
            "https://www.edenbrothers.com/cdn/shop/files/onion-ruby-red-shk-1_94c13225-d0e6-4f7d-b738-16baceab4aa0.jpg?v=1726674318",
            "https://www.edenbrothers.com/cdn/shop/files/onion-ruby-red-shk-1_94c13225-d0e6-4f7d-b738-16baceab4aa0.jpg?v=1726674318",
            "https://www.edenbrothers.com/cdn/shop/files/onion-ruby-red-shk-1_94c13225-d0e6-4f7d-b738-16baceab4aa0.jpg?v=1726674318",
            "https://www.edenbrothers.com/cdn/shop/files/onion-ruby-red-shk-1_94c13225-d0e6-4f7d-b738-16baceab4aa0.jpg?v=1726674318"
        ]
    },
    {
        "name": "Chinese Cabbage",
        "original_price": 48.0,
        "discount_percentage": round((48.0 - 17.28) / 48.0 * 100, 2), # 64.0
        "category": "Vegetables",
        "description": "Discover the crisp, mild flavor of our Chinese Cabbage, organically grown for tender leaves in stir-fries, kimchi, and salads. This versatile green adds lightness and nutrition to Asian-inspired dishes. Harvested fresh for quality.\n\nThe elongated heads of Chinese Cabbage offer a juicy crunch that's perfect for quick cooking or raw preparations, absorbing flavors beautifully.\n\n* 100g of Chinese Cabbage provides about 13 calories\n* High in vitamin C and K for immunity and bones\n* Low-calorie with fiber for weight control\n* Contains glucosinolates for cancer prevention\n\nIncorporate Chinese Cabbage for healthy, flavorful meals that bring authenticity to your kitchen.",
        "weight": "03 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 5413,
        "tags": ["Vegetables", "Healthy", "Chinese", "Cabbage", "Green Cabbage"],
        "images": [
            "https://media.riverford.co.uk/images/photo-4480x4480-aecbdd74da1860a1dc74a00589521dd9.jpg",
            "https://media.riverford.co.uk/images/photo-4480x4480-aecbdd74da1860a1dc74a00589521dd9.jpg",
            "https://media.riverford.co.uk/images/photo-4480x4480-aecbdd74da1860a1dc74a00589521dd9.jpg",
            "https://media.riverford.co.uk/images/photo-4480x4480-aecbdd74da1860a1dc74a00589521dd9.jpg",
            "https://media.riverford.co.uk/images/photo-4480x4480-aecbdd74da1860a1dc74a00589521dd9.jpg"
        ]
    }
]

# Additional products (invented, similar theme, no images, random discounts)
additional_products = [
    # New products for Cooking

    {
        "name": "Olive Oil",
        "original_price": 12.99,
        "discount_percentage": None,
        "category": "Oils & Vinegars",
        "description": "Elevate your cooking with our extra-virgin Olive Oil, cold-pressed from premium olives for rich flavor in dressings and sautés. This heart-healthy oil is a Mediterranean staple, offering smoothness and nutritional benefits. Bottled fresh for quality.\n\nThe fruity notes of Olive Oil make it ideal for drizzling or cooking, providing essential fatty acids for overall health.\n\n* 100ml of Olive Oil provides approximately 884 calories\n* High in monounsaturated fats for heart health\n* Antioxidant-rich for skin protection\n* Versatile for high-heat cooking\n\nUse Olive Oil to add authenticity and nutrition to your daily meals.",
        "weight": "0.5 l",
        "color": "Green",
        "type": "Organic",
        "stock_count": 800,
        "tags": ["Oil", "Olive", "Healthy Fat"],
        "images": [
            "https://img.drz.lazcdn.com/g/kf/Sc6702990a2ae45a4a527ee6c48d6ded5h.jpg_120x120q80.jpg_.webp",
            "https://img.drz.lazcdn.com/g/kf/Sd9cbdf5dcc25431ba5592002d08db973T.jpg_720x720q80.jpg_.webp",
            "https://img.drz.lazcdn.com/g/kf/Sd9cbdf5dcc25431ba5592002d08db973T.jpg_720x720q80.jpg_.webp",
            "https://img.drz.lazcdn.com/g/kf/Sd9cbdf5dcc25431ba5592002d08db973T.jpg_720x720q80.jpg_.webp",
        ]
    },
    {
        "name": "Brown Rice",
        "original_price": 4.49,
        "discount_percentage": 5.0,
        "category": "Grains & Flours",
        "description": "Fuel your body with our nutritious Brown Rice, whole-grain and organically grown for nutty flavor in pilafs and bowls. This fiber-rich staple supports sustained energy and digestive health. Packaged for freshness.\n\nThe chewy texture of Brown Rice complements proteins and vegetables, offering a wholesome base for meals.\n\n* 100g of Brown Rice provides about 111 calories\n* High fiber for gut health\n* Source of magnesium and selenium\n* Low glycemic index for blood sugar control\n\nChoose Brown Rice for healthy, satisfying dishes that nourish from within.",
        "weight": "1 kg",
        "color": "Brown",
        "type": "Organic",
        "stock_count": 1200,
        "tags": ["Grain", "Rice", "Whole Grain"],
        "images": [
            "https://chaldn.com/_mpimage/aci-nutrilife-brown-rice-1-kg?src=https%3A%2F%2Feggyolk.chaldal.com%2Fapi%2FPicture%2FRaw%3FpictureId%3D137066&q=best&v=1&m=400&webp=1",
            "https://chaldn.com/_mpimage/aci-nutrilife-brown-rice-1-kg?src=https%3A%2F%2Feggyolk.chaldal.com%2Fapi%2FPicture%2FRaw%3FpictureId%3D137066&q=best&v=1&m=400&webp=1",
            "https://chaldn.com/_mpimage/aci-nutrilife-brown-rice-1-kg?src=https%3A%2F%2Feggyolk.chaldal.com%2Fapi%2FPicture%2FRaw%3FpictureId%3D137066&q=best&v=1&m=400&webp=1",
        ]
    },
    {
        "name": "Turmeric Powder",
        "original_price": 5.99,
        "discount_percentage": 10.0,
        "category": "Spices & Herbs",
        "description": "Enhance your dishes with our vibrant Turmeric Powder, organically sourced for its earthy flavor and health benefits in curries and teas. This golden spice is renowned for its anti-inflammatory properties and culinary versatility. Finely ground for easy use.\n\nThe bright yellow hue of Turmeric Powder adds color and depth to recipes, supporting wellness through its active compound curcumin.\n\n* 100g of Turmeric Powder provides about 312 calories\n* Rich in curcumin for joint health\n* Antioxidant properties for immune support\n* Aids digestion and detoxification\n\nIncorporate Turmeric Powder for flavorful, health-boosting meals that bring warmth to your kitchen.",
        "weight": "0.1 kg",
        "color": "Yellow",
        "type": "Organic",
        "stock_count": 1500,
        "tags": ["Spice", "Turmeric", "Herb"],
        "images": [
            "https://chaldn.com/_mpimage/radhuni-turmeric-holud-powder-200-gm?src=https%3A%2F%2Feggyolk.chaldal.com%2Fapi%2FPicture%2FRaw%3FpictureId%3D132553&q=best&v=1&m=400&webp=1",
            "https://chaldn.com/_mpimage/radhuni-turmeric-holud-powder-200-gm?src=https%3A%2F%2Feggyolk.chaldal.com%2Fapi%2FPicture%2FRaw%3FpictureId%3D132553&q=best&v=1&m=400&webp=1",
            "https://chaldn.com/_mpimage/radhuni-turmeric-holud-powder-200-gm?src=https%3A%2F%2Feggyolk.chaldal.com%2Fapi%2FPicture%2FRaw%3FpictureId%3D132553&q=best&v=1&m=400&webp=1",
        ]
    },
    # New for Snacks
    {
        "name": "Almonds",
        "original_price": 9.99,
        "discount_percentage": 15.0,
        "category": "Nuts & Seeds",
        "description": "Snack smart with our roasted Almonds, organically sourced for crunchy texture and nutty flavor as a healthy on-the-go option. These nuts are packed with protein and healthy fats for energy. Freshly packaged.\n\nThe versatile Almonds can be eaten alone or added to trails mixes and baked goods.\n\n* 100g of Almonds provides approximately 579 calories\n* Rich in vitamin E for skin health\n* Good source of protein and fiber\n* Supports heart health with monounsaturated fats\n\nEnjoy Almonds for a nutritious boost anytime, anywhere.",
        "weight": "0.25 kg",
        "color": "Brown",
        "type": "Organic",
        "stock_count": 1000,
        "tags": ["Nut", "Almond", "Snack"],
        "images": [
            "https://img.drz.lazcdn.com/static/bd/p/038412b5c1438222dcbba3d16161d1f8.jpg_720x720q80.jpg_.webp",
            "https://img.drz.lazcdn.com/static/bd/p/ef89958d804be4cb5cb6c58f99359460.jpg_120x120q80.jpg_.webp",
            "https://img.drz.lazcdn.com/static/bd/p/fc0468fb2d58a66b75516c8909d1f63b.jpg_120x120q80.jpg_.webp",
            "https://img.drz.lazcdn.com/static/bd/p/1b39f10d7935521f2f394767b617ef38.jpg_120x120q80.jpg_.webp",
        ]
    },
    {
        "name": "Potato Chips",
        "original_price": 3.99,
        "discount_percentage": None,
        "category": "Chips & Crackers",
        "description": "Indulge in our crispy Potato Chips, made from organic potatoes for classic flavor and crunch as a satisfying snack. Lightly salted for balance. Baked for health.\n\nThe thin slices offer irresistible texture perfect for dipping or enjoying solo.\n\n* 100g of Potato Chips provides about 536 calories\n* Source of potassium\n* Low in sugar\n* Crunchy texture for satisfaction\n\nTreat yourself to Potato Chips for fun, flavorful snacking.",
        "weight": "0.15 kg",
        "color": "Golden",
        "type": "Organic",
        "stock_count": 1500,
        "tags": ["Chip", "Potato", "Snack"],
        "images": [
            "https://quasemproducts.com/wp-content/uploads/2020/07/Tomato-Tango-80gm.png",
            "https://quasemproducts.com/wp-content/uploads/2020/07/Mix-Masala-22gm.png",
            "https://chaldn.com/_mpimage/sun-chips-salt-pepper-20-gm?src=https%3A%2F%2Feggyolk.chaldal.com%2Fapi%2FPicture%2FRaw%3FpictureId%3D168337&q=best&v=1&m=400&m=400&webp=1",
        ]
    },
    {
        "name": "Raisins",
        "original_price": 4.99,
        "discount_percentage": 10.0,
        "category": "Dried Fruits",
        "description": "Sweeten your day with our plump Raisins, organically dried for natural sweetness in baking and trails mixes. These dried grapes provide quick energy and nutrition.\n\nThe chewy texture of Raisins adds delight to cereals and desserts.\n\n* 100g of Raisins provides approximately 299 calories\n* High in iron for energy\n* Source of fiber for digestion\n* Natural antioxidants\n\nIncorporate Raisins for a healthy, sweet snack option.",
        "weight": "0.2 kg",
        "color": "Dark Brown",
        "type": "Organic",
        "stock_count": 900,
        "tags": ["Dried Fruit", "Raisin", "Snack"],
        "images": [
            "https://www.khaasfood.com/wp-content/uploads/2020/08/raisins.webp",
            "https://sinin.com.bd/wp-content/uploads/2022/03/Kismis-Raisins-600x600.jpg",
            "https://www.khaasfood.com/wp-content/uploads/2020/08/raisins.webp",
        ]
    },
    # New for Beverages
    {
        "name": "Orange Juice",
        "original_price": 5.49,
        "discount_percentage": None,
        "category": "Juices",
        "description": "Refresh with our pure Orange Juice, freshly squeezed from organic oranges for tangy flavor and vitamin boost. No added sugars for natural goodness.\n\nThe vibrant liquid offers a sunny start to your day or a revitalizing drink anytime.\n\n* 100ml of Orange Juice provides about 45 calories\n* Packed with vitamin C for immunity\n* Natural electrolytes for hydration\n* Antioxidants for overall health\n\nSip Orange Juice for a delicious, nutritious beverage.",
        "weight": "1 l",
        "color": "Orange",
        "type": "Organic",
        "stock_count": 1200,
        "tags": ["Juice", "Orange", "Beverage"],
        "images": [
            "https://cdn.smithbrothersfarms.com/media/0013924_simply-orange-pulp-free-juice-46-fl-oz.jpeg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2bIw4asa-RoIdb82YxQ8E_Xo_MCf5BPPh_Q&s",
        ]
    },
    {
        "name": "Green Tea",
        "original_price": 6.99,
        "discount_percentage": 5.0,
        "category": "Teas & Coffees",
        "description": "Revive with our aromatic Green Tea, organically grown for subtle flavor and antioxidant benefits in daily brewing. Loose leaves for authenticity.\n\nThe light infusion supports metabolism and relaxation.\n\n* 100g of Green Tea provides minimal calories\n* Rich in catechins for weight management\n* Boosts brain function with caffeine\n* Antioxidant powerhouse\n\nBrew Green Tea for a calming, health-promoting ritual.",
        "weight": "0.1 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 800,
        "tags": ["Tea", "Green", "Beverage"],
        "images": [
            "https://m.media-amazon.com/images/I/61tCIeSY81L._AC_UF350,350_QL80_.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSt0IDFbuzuVjTLr8vwwq1zEiXfAxBaoL_ECA&s",
            "https://getit.qa/cdn/shop/files/1200Wx1200H-null_48da3ef9-6f62-4816-b406-d53b4f80c8e7.jpg?v=1735829937",
        ]
    },
    {
        "name": "Cola Soda",
        "original_price": 2.99,
        "discount_percentage": 10.0,
        "category": "Soft Drinks",
        "description": "Enjoy the fizz of our organic Cola Soda, naturally flavored for classic taste without artificial additives. Refreshing and bubbly.\n\nThe caramel notes provide a satisfying thirst-quencher.\n\n* 100ml of Cola Soda provides about 42 calories\n* Caffeinated for energy lift\n* Natural flavors for purity\n* Carbonated for refreshment\n\nPop open Cola Soda for fun, effervescent enjoyment.",
        "weight": "0.33 l",
        "color": "Dark",
        "type": "Organic",
        "stock_count": 2000,
        "tags": ["Soda", "Cola", "Beverage"],
        "images": [
            "https://asmishop.com/assets/images/products/1760435466aCvHnPB0.png", 
            "https://static-01.daraz.com.bd/p/dc4fbe034a444ce42a812ab691d0214c.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWaIfYX-eXul5AvrwzMf6lMQBomPQp9GdwcQ&s", 
        ]
    },

    # Fruites and Begitables
    {
        "name": "Red Apples",
        "original_price": 18.99,
        "discount_percentage": 10.0,
        "category": "Apples",
        "description": "Sweet and crisp red apples, perfect for snacking or baking.",
        "weight": "1 kg",
        "color": "Red",
        "type": "Organic",
        "stock_count": 1000,
        "tags": ["Apple", "Red", "Fruit"],
        "images": [
            "https://be.quickybd.com/admin/public/productImage/66ebeb69d3c31.jpg",
            "https://be.quickybd.com/admin/public/productImage/66ebeb69d3c31.jpg",
            "https://be.quickybd.com/admin/public/productImage/66ebeb69d3c31.jpg",
        ]
    },
    {
        "name": "Bananas",
        "original_price": 9.99,
        "discount_percentage": None,
        "category": "Fruits",
        "description": "Ripe yellow bananas, rich in potassium and great for smoothies.",
        "weight": "1 kg",
        "color": "Yellow",
        "type": "Organic",
        "stock_count": 2000,
        "tags": ["Banana", "Yellow", "Fruit"],
        "images": [
            "https://www.kroger.com/product/images/large/front/0000000094011",
            "https://images.squarespace-cdn.com/content/v1/5a50ba2280bd5ee6577db29b/c34a9269-6967-40c3-9813-f99af5a779b0/gutfit-oct-banana-blog.jpg",
        ]
    },
    {
        "name": "Oranges",
        "original_price": 12.49,
        "discount_percentage": 15.0,
        "category": "Fruits",
        "description": "Juicy oranges packed with vitamin C, ideal for fresh juice.",
        "weight": "1 kg",
        "color": "Orange",
        "type": "Organic",
        "stock_count": 1500,
        "tags": ["Orange", "Citrus", "Fruit"],
        "images": [
            "https://media.istockphoto.com/id/2124102567/photo/orange-fruit-with-leaf.jpg?s=612x612&w=0&k=20&c=TUXQZs76_KNXdbffr6B9Jm74SQ-KbXAaikxTE78Qy6o=",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyQBYeDIr5Fl5cHzRQk31LhXyyf7e_9oKDnQ&s",
        ]
    },
    {
        "name": "Broccoli",
        "original_price": 14.5,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Nutrient-dense broccoli florets, perfect for steaming or stir-fries.",
        "weight": "0.5 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 800,
        "tags": ["Broccoli", "Green", "Healthy"],
        "images": [
            "https://freshbasket.com.pk/cdn/shop/files/broccoli.jpg?v=1721745127",
            "https://freshbasket.com.pk/cdn/shop/files/broccoli.jpg?v=1721745127",
        ]
    },
    {
        "name": "Celery",
        "original_price": 7.99,
        "discount_percentage": 5.0,
        "category": "Vegetables",
        "description": "Crunchy celery stalks, great for salads or as a low-calorie snack.",
        "weight": "0.5 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 1200,
        "tags": ["Celery", "Green", "Vegetarian"],
        "images": [
            "https://www.mygardenbd.com/wp-content/uploads/2019/08/Celery-5.jpg",
            "https://images.immediate.co.uk/production/volatile/sites/30/2014/01/celery-stalks-a463fb3-scaled.jpg?quality=90&resize=708,643",
        ]
    },
    {
        "name": "Pumpkin",
        "original_price": 22.0,
        "discount_percentage": 20.0,
        "category": "Vegetables",
        "description": "Versatile pumpkin for soups, pies, or roasting.",
        "weight": "2 kg",
        "color": "Orange",
        "type": "Organic",
        "stock_count": 500,
        "tags": ["Pumpkin", "Orange", "Squash"],
        "images": [
            "https://www.healthxchange.sg/adobe/dynamicmedia/deliver/dm-aid--7f272a4e-bae5-42d0-ad04-d96dea3764ee/pumpkin-health-benefits-nutrition-facts.jpg?preferwebp=true"
            "https://www.healthxchange.sg/adobe/dynamicmedia/deliver/dm-aid--7f272a4e-bae5-42d0-ad04-d96dea3764ee/pumpkin-health-benefits-nutrition-facts.jpg?preferwebp=true"
        ]
    },
    {
        "name": "Avocado",
        "original_price": 25.99,
        "discount_percentage": None,
        "category": "Fruits",
        "description": "Creamy avocados, perfect for guacamole or toast.",
        "weight": "0.5 kg",
        "color": "Green",
        "type": "Organic",
        "stock_count": 600,
        "tags": ["Avocado", "Green", "Healthy"],
        "images": [
            "https://media.desenio.com/site_images/685d9e239ba509224c94ca6a_455595747_19445-5.jpg?auto=compress%2Cformat&fit=max&w=3840",
            "https://bivihome.com.au/wp-content/uploads/2023/05/Avocado-%E2%80%93-Hass-Variety-Each-%E5%89%AF%E6%9C%AC.png"
        ]
    },
    {
        "name": "Beetroot",
        "original_price": 8.5,
        "discount_percentage": 10.0,
        "category": "Root Vegetables",
        "description": "Earthy beetroots, great for salads or juicing.",
        "weight": "1 kg",
        "color": "Purple",
        "type": "Organic",
        "stock_count": 900,
        "tags": ["Beetroot", "Purple", "Root"],
        "images": [
            "https://cdn.shopify.com/s/files/1/0532/0998/9283/files/Understanding_Beetroot_s_Nutrients_for_Skin_Health_480x480.jpg?v=1737371595"
            "https://5.imimg.com/data5/SELLER/Default/2023/6/316774192/AM/QQ/MA/3042133/fresh-red-beetroot.jpg",
        ]
    },
    {
        "name": "Pineapple",
        "original_price": 19.99,
        "discount_percentage": 25.0,
        "category": "Fruits",
        "description": "Sweet and tangy pineapple, fresh from the tropics.",
        "weight": "1 kg",
        "color": "Yellow",
        "type": "Organic",
        "stock_count": 700,
        "tags": ["Pineapple", "Tropical", "Fruit"],
        "images": [
            "https://themeatclub.com.sg/cdn/shop/files/Pineapple.png?v=1754643333",
            "https://5.imimg.com/data5/PW/ND/MY-46595757/fresh-pineapple-281kg-29-500x500.png",
        ]
    },
    {
        "name": "Radish",
        "original_price": 6.99,
        "discount_percentage": None,
        "category": "Root Vegetables",
        "description": "Crisp radishes with a peppery bite, ideal for salads.",
        "weight": "0.5 kg",
        "color": "Red",
        "type": "Organic",
        "stock_count": 1100,
        "tags": ["Radish", "Red", "Root"],
        "images": [
            "https://m.media-amazon.com/images/I/517LlhycGUL._AC_UF1000,1000_QL80_.jpg",
            "https://m.media-amazon.com/images/I/517LlhycGUL._AC_UF1000,1000_QL80_.jpg",
        ]
    },

    # New for Beauty & Health
    {
        "name": "Vitamin C Supplement",
        "original_price": 9.99,
        "discount_percentage": None,
        "category": "Supplements",
        "description": "Boost your immunity with our organic Vitamin C Supplement, derived from natural sources for daily health support. Easy-to-swallow tablets.\n\nEssential for collagen production and antioxidant protection.\n\n* Each serving provides 1000mg of vitamin C\n* Supports immune function\n* Promotes skin health\n* Vegan and non-GMO\n\nTake Vitamin C Supplement for proactive wellness.",
        "weight": "0.1 kg",
        "color": "White",
        "type": "Organic",
        "stock_count": 600,
        "tags": ["Supplement", "Vitamin C", "Health"],
        "images": [
            "https://behealthybd.com/wp-content/uploads/2023/04/71fmv9xs6BL._AC_SL1500_-768x768.jpg",
            "https://behealthybd.com/wp-content/uploads/2023/04/Natures-Bounty-Vitamin-C-1000-mg-100-caplets-667x800.png"
        ]
    },
    {
        "name": "Organic Soap",
        "original_price": 4.49,
        "discount_percentage": 10.0,
        "category": "Personal Care",
        "description": "Cleanse gently with our Organic Soap, made from natural ingredients for moisturizing lather and fresh scent. Suitable for all skin types.\n\nThe plant-based formula nourishes while cleaning.\n\n* 100g bar provides long-lasting use\n* Free from harsh chemicals\n* Hydrates skin naturally\n* Eco-friendly packaging\n\nUse Organic Soap for daily hygiene and care.",
        "weight": "0.1 kg",
        "color": "Beige",
        "type": "Organic",
        "stock_count": 1000,
        "tags": ["Soap", "Personal Care", "Beauty"],
        "images": [
            "https://img.drz.lazcdn.com/static/bd/p/a203179c64f629c35a3d367cdfe5969d.png_720x720q80.png_.webp",
            "https://img.drz.lazcdn.com/static/bd/p/1b50f6d416d2aa0947339215f057834f.png_120x120q80.png_.webp",
        ]
    },
    {
        "name": "Natural Shampoo",
        "original_price": 8.99,
        "discount_percentage": None,
        "category": "Organic Beauty",
        "description": "Revitalize your hair with our Natural Shampoo, formulated with organic herbs for gentle cleansing and shine. Sulfate-free for health.\n\nThe herbal blend strengthens and nourishes strands.\n\n* 200ml bottle provides multiple uses\n* Promotes scalp health\n* Adds volume and luster\n* Suitable for all hair types\n\nChoose Natural Shampoo for beautiful, healthy hair.",
        "weight": "0.2 l",
        "color": "Clear",
        "type": "Organic",
        "stock_count": 700,
        "tags": ["Shampoo", "Beauty", "Hair Care"],
        "images": [
            "https://www.ohsogo.com/cdn/shop/files/fop_1_1.jpg?v=1717927689&width=1500",
            "https://www.ohsogo.com/cdn/shop/files/fop_1_1.jpg?v=1717927689&width=1500",
        ]
    },
    # New for Bread & Bakery
    {
        "name": "Whole Grain Bread",
        "original_price": 3.99,
        "discount_percentage": 5.0,
        "category": "Breads",
        "description": "Nourish with our Whole Grain Bread, baked fresh from organic grains for hearty texture and nutrition in sandwiches and toasts. Sliced for convenience.\n\nThe dense loaf offers sustained energy and flavor.\n\n* 100g of Whole Grain Bread provides about 247 calories\n* High fiber for digestion\n* Source of whole grains for heart health\n* No artificial preservatives\n\nEnjoy Whole Grain Bread for wholesome meals.",
        "weight": "0.5 kg",
        "color": "Brown",
        "type": "Organic",
        "stock_count": 900,
        "tags": ["Bread", "Whole Grain", "Bakery"],
        "images": [
            "https://m.media-amazon.com/images/I/41rGup4dLRL._SS400_.jpg",
            "https://www.girlversusdough.com/wp-content/uploads/2025/09/whole-grain-seeded-bread-soft-crumb.jpg"
        ]
    },
    {
        "name": "Croissant",
        "original_price": 2.49,
        "discount_percentage": None,
        "category": "Pastries",
        "description": "Indulge in our flaky Croissant, handcrafted from organic butter and flour for buttery layers and light texture. Perfect for breakfast.\n\nThe golden pastry melts in your mouth with every bite.\n\n* Each Croissant provides about 231 calories\n* Rich in flavor\n* Freshly baked daily\n* Ideal with coffee\n\nTreat yourself to Croissant for a delightful start.",
        "weight": "0.08 kg",
        "color": "Golden",
        "type": "Organic",
        "stock_count": 1200,
        "tags": ["Pastry", "Croissant", "Bakery"],
        "images": [
            "https://cdn.uengage.io/uploads/7175/image-749238-1738604822.jpeg",
            "https://cdn.uengage.io/uploads/7175/image-749238-1738604822.jpeg",
        ]
    },
    {
        "name": "Chocolate Cookie",
        "original_price": 1.99,
        "discount_percentage": 10.0,
        "category": "Cakes & Cookies",
        "description": "Satisfy cravings with our chewy Chocolate Cookie, made from organic cocoa for rich taste and soft center. Perfect snack size.\n\nThe decadent treat combines sweetness and texture.\n\n* Each Cookie provides about 160 calories\n* Made with real chocolate\n* No artificial flavors\n* Great for sharing\n\nBite into Chocolate Cookie for sweet enjoyment.",
        "weight": "0.05 kg",
        "color": "Brown",
        "type": "Organic",
        "stock_count": 1500,
        "tags": ["Cookie", "Chocolate", "Bakery"],
        "images": [
            "https://slattery.co.uk/wp-content/uploads/2024/09/double-chocolate-cookies-pack-slattery.webp",
            "https://i5.walmartimages.com/asr/6c8985e9-48d1-42ab-91c1-f94a3d42d717.30396a557fcb4aae974b593cfe31cda4.jpeg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRG0dZwkMLGm_MPwbVOlz40BkmXtKpxne3LFw&s",
        ]
    }
]

all_products_data = corrected_products + additional_products

# ────────────────────────────────────────────────
# Categories, tags, brands – unchanged
# ────────────────────────────────────────────────

# Provided categories + hierarchical structure
# Root: Fresh Produce, Cooking, Snacks, Beverages, Beauty & Health, Bread & Bakery
# Sub under Fresh Produce: Fruits (with Apples, Mangoes), Vegetables (with Leafy Greens, Root Vegetables, Peppers, etc.)
category_structure = {
    "Fresh Produce": {
        "Fruits": ["Apples", "Mangoes", "Citrus", "Tropical"],
        "Vegetables": ["Leafy Greens", "Root Vegetables", "Peppers", "Squash", "Cruciferous", "Allium", "Other Vegetables"]
    },
    "Cooking": {
        "Spices & Herbs": [],
        "Oils & Vinegars": [],
        "Grains & Flours": []
    },
    "Snacks": {
        "Nuts & Seeds": [],
        "Chips & Crackers": [],
        "Dried Fruits": []
    },
    "Beverages": {
        "Juices": [],
        "Teas & Coffees": [],
        "Soft Drinks": []
    },
    "Beauty & Health": {
        "Supplements": [],
        "Personal Care": [],
        "Organic Beauty": []
    },
    "Bread & Bakery": {
        "Breads": [],
        "Pastries": [],
        "Cakes & Cookies": []
    }
}

# Popular tags from your list + unique from products
all_tags = set([
    "Healthy", "Low fat", "Vegetarian", "Kid foods", "Vitamins", "Bread", "Meat", "Snacks",
    "Lunch", "Dinner", "Breakfast", "Fruit", "Best Seller"
])
for p in all_products_data:
    all_tags.update(p["tags"])

brands_list = [
    "Organic Farms", "Local Harvest", "Green Valley", "Fresh Fields", "Nature's Best",
    "Eco Produce", "Pure Organics", "Farm Fresh", "Healthy Roots", "Veggie Delight"
]

# ────────────────────────────────────────────────
# INCREASED NUMBER OF USERS – 30 test users
# ────────────────────────────────────────────────
users_data = [
    {"email": f"test{i}@example.com", "password": "58$ecure@47"}
    for i in range(1, 31)   # test1 to test30
]

review_comments_pool = [
    "Super fresh, will buy again!",
    "Excellent quality and taste.",
    "Very happy with this organic product.",
    "Perfect for cooking and salads.",
    "Great value for the price.",
    "One of the best I've had!",
    "Arrived in perfect condition.",
    "Highly recommend to everyone.",
    "Tasty and really crisp.",
    "Love how fresh these are!",
    "Good size and very flavorful.",
    "Definitely ordering more soon.",
]

def seed_data():
    print("Starting database seeding...")

    # ────────────────────────────────────────────────
    # Categories (your existing hierarchical code)
    # ────────────────────────────────────────────────
    print("Creating categories...")
    category_map = {}

    root_names = ["Fresh Produce", "Cooking", "Snacks", "Beverages", "Beauty & Health", "Bread & Bakery"]
    for name in root_names:
        slug = slugify(name)
        cat, _ = Category.objects.get_or_create(name=name, slug=slug, defaults={'parent': None})
        category_map[name] = cat
        print(f" Root: {name}")
    fresh_produce = category_map["Fresh Produce"]
    cooking = category_map["Cooking"]
    snacks = category_map["Snacks"]
    beverages = category_map["Beverages"]
    beauty_health = category_map["Beauty & Health"]
    bread_bakery = category_map["Bread & Bakery"]
    second_level = [
        ("Fruits", fresh_produce), ("Vegetables", fresh_produce),
        ("Spices & Herbs", cooking), ("Oils & Vinegars", cooking), ("Grains & Flours", cooking),
        ("Nuts & Seeds", snacks), ("Chips & Crackers", snacks), ("Dried Fruits", snacks),
        ("Juices", beverages), ("Teas & Coffees", beverages), ("Soft Drinks", beverages),
        ("Supplements", beauty_health), ("Personal Care", beauty_health), ("Organic Beauty", beauty_health),
        ("Breads", bread_bakery), ("Pastries", bread_bakery), ("Cakes & Cookies", bread_bakery)
    ]
    for name, parent in second_level:
        slug = slugify(name)
        cat, _ = Category.objects.get_or_create(name=name, slug=slug, parent=parent)
        category_map[name] = cat
        print(f" {name} under {parent.name}")
    third_level = [
        ("Apples", "Fruits"), ("Mangoes", "Fruits"), ("Citrus", "Fruits"), ("Tropical", "Fruits"),
        ("Leafy Greens", "Vegetables"), ("Root Vegetables", "Vegetables"),
        ("Peppers", "Vegetables"), ("Squash", "Vegetables"), ("Cabbage", "Vegetables"),
        ("Cruciferous", "Vegetables"), ("Allium", "Vegetables"), ("Other Vegetables", "Vegetables"),
    ]
    for name, parent_key in third_level:
        parent = category_map.get(parent_key)
        if not parent:
            continue
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        cat, _ = Category.objects.get_or_create(name=name, slug=slug, parent=parent)
        category_map[name] = cat
        print(f" {name} under {parent.name}")

    # ────────────────────────────────────────────────
    # Tags
    # ────────────────────────────────────────────────
    print("Creating tags...")
    tags_map = {}
    for tag_name in all_tags:
        tag_slug = slugify(tag_name)
        tag, _ = Tag.objects.get_or_create(name=tag_name, slug=tag_slug)
        tags_map[tag_name] = tag

    # ────────────────────────────────────────────────
    # Brands
    # ────────────────────────────────────────────────
    print("Creating brands...")
    brands = []
    for name in brands_list:
        brand, _ = Brand.objects.get_or_create(name=name)
        brands.append(brand)

    # ────────────────────────────────────────────────
    # Users – 30 test users
    # ────────────────────────────────────────────────
    print("Creating users...")
    users = []
    for u in users_data:
        user, created = User.objects.get_or_create(email=u["email"])
        if created:
            user.set_password(u["password"])
            user.save()
        users.append(user)
    print(f"→ Created/loaded {len(users)} users")

    # ────────────────────────────────────────────────
    # Products
    # ────────────────────────────────────────────────
    print("Creating products...")
    products = []
    for data in all_products_data:
        cat_name = data["category"]
        if cat_name in ["Fruits", "Apples", "Mangoes", "Citrus", "Tropical"]:
            if "Apple" in data["name"]: preferred = "Apples"
            elif "Mango" in data["name"]: preferred = "Mangoes"
            elif "Orange" in data["name"]: preferred = "Citrus"
            elif any(w in data["name"] for w in ["Banana", "Pineapple", "Avocado"]): preferred = "Tropical"
            else: preferred = "Fruits"
            category = category_map.get(preferred, category_map["Fruits"])
        elif cat_name in ["Vegetables", "Leafy Greens", "Root Vegetables", "Peppers", "Squash", "Cruciferous", "Allium", "Other Vegetables"]:
            if any(w in data["name"] for w in ["Lettuce", "Spinach", "Cabbage", "Chinese Cabbage"]): preferred = "Leafy Greens"
            elif any(w in data["name"] for w in ["Carrot", "Potato", "Beetroot", "Radish", "Ginger"]): preferred = "Root Vegetables"
            elif any(w in data["name"] for w in ["Onion", "Garlic"]): preferred = "Allium"
            elif any(w in data["name"] for w in ["Pepper", "Capsicum", "Chilli"]): preferred = "Peppers"
            elif any(w in data["name"] for w in ["Zucchini", "Pumpkin", "Eggplant"]): preferred = "Squash"
            elif any(w in data["name"] for w in ["Cauliflower", "Broccoli"]): preferred = "Cruciferous"
            elif any(w in data["name"] for w in ["Tomato", "Cucumber", "Corn", "Celery"]): preferred = "Other Vegetables"
            else: preferred = "Vegetables"
            category = category_map.get(preferred, category_map["Vegetables"])
        elif cat_name in ["Spices & Herbs", "Oils & Vinegars", "Grains & Flours"]:
            category = category_map.get(cat_name, category_map["Cooking"])
        elif cat_name in ["Nuts & Seeds", "Chips & Crackers", "Dried Fruits"]:
            category = category_map.get(cat_name, category_map["Snacks"])
        elif cat_name in ["Juices", "Teas & Coffees", "Soft Drinks"]:
            category = category_map.get(cat_name, category_map["Beverages"])
        elif cat_name in ["Supplements", "Personal Care", "Organic Beauty"]:
            category = category_map.get(cat_name, category_map["Beauty & Health"])
        elif cat_name in ["Breads", "Pastries", "Cakes & Cookies"]:
            category = category_map.get(cat_name, category_map["Bread & Bakery"])
        else:
            category = category_map.get(cat_name, category_map["Fresh Produce"])

        base_slug = slugify(data["name"])
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        brand = random.choice(brands)

        product = Product(
            name=data["name"],
            slug=slug,
            original_price=Decimal(data["original_price"]),
            discount_percentage=Decimal(data["discount_percentage"]) if data.get("discount_percentage") else None,
            brand=brand,
            category=category,
            description=data["description"],
            weight=data["weight"],
            color=data["color"],
            type=data["type"],
            stock_count=data["stock_count"]
        )
        product.save()

        for tag_name in data["tags"]:
            product.tags.add(tags_map[tag_name])

        if "images" in data and data["images"]:
            for idx, url in enumerate(data["images"]):
                try:
                    result = cloudinary.uploader.upload(
                        url,
                        folder='Green_Harvest/products/',
                        resource_type='image'
                    )
                    ProductImage.objects.create(
                        product=product,
                        image=result['public_id'],
                        alt_text=f"{data['name']} image {idx+1}",
                        is_primary=(idx == 0)
                    )
                except Exception as e:
                    print(f"Image upload failed for {data['name']}: {url} → {e}")

        products.append(product)

    print(f"→ Created {len(products)} products")

    # ────────────────────────────────────────────────
    # Reviews – STRICTLY ONE per user per product
    # ────────────────────────────────────────────────
    print("Creating reviews...")
    created = 0
    skipped = 0

    for product in products:
        # Pick 4–10 different users for each product (depending on how many we have)
        num_reviews_target = random.randint(4, min(10, len(users)))
        selected_users = random.sample(users, k=num_reviews_target)

        for user in selected_users:
            if Review.objects.filter(product=product, user=user).exists():
                skipped += 1
                continue

            try:
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=random.choices([1,2,2,3,3,4,4,4,5,5,5], k=1)[0],
                    comment=random.choice(review_comments_pool)
                )
                created += 1
            except IntegrityError:
                skipped += 1
            except Exception as e:
                print(f"Review failed: {product.name} by {user.email} → {e}")
                skipped += 1

    print(f"Reviews → created: {created} skipped (already existed): {skipped}")

    print("Seeding complete! Check your database.")

# ────────────────────────────────────────────────
# Run
# ────────────────────────────────────────────────
seed_data()