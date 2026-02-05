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
        "discount_percentage": round((20.99 - 14.99) / 20.99 * 100, 2),  # ~28.58
        "category": "Fruits",  # Will map to hierarchical
        "description": "Tart and crunchy green apples, ideal for a healthy snack or for use in traditional apple pies.",
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
        "category": "Fruits",
        "description": "Tart and crunchy Surjapur Mango, ideal for a healthy snack or for use in traditional Mango pies.",
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
        "discount_percentage": round((12.0 - 9.0) / 12.0 * 100, 2),  # 25.0
        "category": "Vegetables",
        "description": "Vine-ripened tomatoes with a juicy interior and vibrant red skin. Perfect for fresh salsa or pasta sauces.",
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
        "discount_percentage": round((20.0 - 17.0) / 20.0 * 100, 2),  # 15.0
        "category": "Vegetables",
        "description": "Farm-fresh white cauliflower heads, rich in fiber and vitamins, perfect for roasting or making low-carb rice.",
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
        "discount_percentage": None,  # current == original
        "category": "Vegetables",
        "description": "Fresh and crisp green lettuce, harvested daily to ensure maximum crunch and nutritional value for your salads.",
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
        "description": "Premium quality green capsicum with a smooth texture, perfect for traditional slow-cooked stews and grilling.",
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
        "description": "Hand-picked spicy green chillies that add a vibrant kick and authentic heat to any culinary creation.",
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
            "https://res.cloudinary.com/dlhx7zvg3/image/upload/v1768674452/Green_Chilli_b6zrtx.png"  # image_2, may be invalid - script will skip if fails
        ]
    },
    {
        "name": "Eggplant",
        "original_price": 14.99,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Glossy, deep-purple eggplants known for their meaty interior and ability to absorb rich flavors during cooking.",
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
        "category": "Vegetables",
        "description": "Naturally sweet, earth-grown carrots harvested at peak ripeness for the best flavor and beta-carotene content.",
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
        "description": "Tender and iron-rich baby spinach leaves. Pre-washed and ready to use in your favorite healthy smoothies.",
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
        "description": "Pungent and flavorful yellow onions, an essential base for almost any savory dish or slow-simmered soup.",
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
        "discount_percentage": round((15.0 - 12.5) / 15.0 * 100, 2),  # 16.67
        "category": "Vegetables",
        "description": "Sweet and crunchy red bell peppers, packed with Vitamin C and perfect for stuffing or slicing into stir-fries.",
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
        "description": "Aromatic and high-quality garlic bulbs, known for their strong flavor profile and health-boosting properties.",
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
        "discount_percentage": round((7.5 - 6.5) / 7.5 * 100, 2),  # 13.33
        "category": "Vegetables",
        "description": "Refreshing and hydrating green cucumbers. Ideal for salads, pickling, or adding to spa-style water.",
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
        "category": "Vegetables",
        "description": "Fresh and spicy ginger root, essential for Asian cuisine and recognized for its digestive benefits.",
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
        "description": "Golden, tender sweet corn on the cob. Naturally sweet and perfect for backyard grilling or boiling.",
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
        "description": "Starchy Russet potatoes, excellent for mashing, baking, or frying into crisp golden-brown chips.",
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
        "description": "Mild and versatile green zucchini. Great for spiralizing into 'zoodles' or sautéing with garlic and herbs.",
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
        "discount_percentage": round((6.5 - 5.5) / 6.5 * 100, 2),  # 15.38
        "category": "Vegetables",
        "description": "Sharp and colorful red onions, perfect for adding a raw bite to sandwiches or pickling for tacos.",
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
        "discount_percentage": round((48.0 - 17.28) / 48.0 * 100, 2),  # 64.0
        "category": "Vegetables",
        "description": "Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla nibh diam, blandit vel consequat nec, ultrices et ipsum, Nulla varius magna a consequat pulvinar.",
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

# Additional 10 products (invented, similar theme, no images, random discounts)
additional_products = [
    {
        "name": "Red Apples",
        "original_price": 18.99,
        "discount_percentage": 10.0,
        "category": "Fruits",
        "description": "Sweet and crisp red apples, perfect for snacking or baking.",
        "weight": "1 kg",
        "color": "Red",
        "type": "Organic",
        "stock_count": 1000,
        "tags": ["Apple", "Red", "Fruit"],
        "images": []  # Skip images
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
        "images": []
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
        "images": []
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
        "images": []
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
        "images": []
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
        "images": []
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
        "images": []
    },
    {
        "name": "Beetroot",
        "original_price": 8.5,
        "discount_percentage": 10.0,
        "category": "Vegetables",
        "description": "Earthy beetroots, great for salads or juicing.",
        "weight": "1 kg",
        "color": "Purple",
        "type": "Organic",
        "stock_count": 900,
        "tags": ["Beetroot", "Purple", "Root"],
        "images": []
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
        "images": []
    },
    {
        "name": "Radish",
        "original_price": 6.99,
        "discount_percentage": None,
        "category": "Vegetables",
        "description": "Crisp radishes with a peppery bite, ideal for salads.",
        "weight": "0.5 kg",
        "color": "Red",
        "type": "Organic",
        "stock_count": 1100,
        "tags": ["Radish", "Red", "Root"],
        "images": []
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
        "Fruits": ["Apples", "Mangoes", "Citrus"],
        "Vegetables": ["Leafy Greens", "Root Vegetables", "Peppers", "Squash", "Cabbage"]
    },
    "Cooking": [],
    "Snacks": [],
    "Beverages": [],
    "Beauty & Health": [],
    "Bread & Bakery": []
}

# Popular tags from your list + unique from products
all_tags = set([
    "Healthy", "Low fat", "Vegetarian", "Kid foods", "Vitamins", "Bread", "Meat", "Snacks",
    "Lunch", "Dinner", "Breakfast", "Fruit"
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
        print(f"  Root: {name}")

    fresh_produce = category_map["Fresh Produce"]
    second_level = [("Fruits", fresh_produce), ("Vegetables", fresh_produce)]
    for name, parent in second_level:
        slug = slugify(name)
        cat, _ = Category.objects.get_or_create(name=name, slug=slug, parent=parent)
        category_map[name] = cat
        print(f"  {name} under {parent.name}")

    third_level = [
        ("Apples", "Fruits"), ("Mangoes", "Fruits"), ("Citrus", "Fruits"),
        ("Leafy Greens", "Vegetables"), ("Root Vegetables", "Vegetables"),
        ("Peppers", "Vegetables"), ("Squash", "Vegetables"), ("Cabbage", "Vegetables"),
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
        print(f"  {name} under {parent.name}")

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

        if cat_name == "Fruits":
            if "Apple" in data["name"]: preferred = "Apples"
            elif "Mango" in data["name"]: preferred = "Mangoes"
            elif "Orange" in data["name"] or "Pineapple" in data["name"]: preferred = "Citrus"
            else: preferred = "Fruits"
            category = category_map.get(preferred, category_map["Fruits"])
        elif cat_name == "Vegetables":
            if any(w in data["name"] for w in ["Lettuce", "Spinach", "Cabbage", "Chinese Cabbage"]): preferred = "Leafy Greens"
            elif any(w in data["name"] for w in ["Carrot", "Potato", "Onion", "Beetroot", "Radish", "Ginger"]): preferred = "Root Vegetables"
            elif any(w in data["name"] for w in ["Pepper", "Capsicum", "Chilli", "Bell"]): preferred = "Peppers"
            elif any(w in data["name"] for w in ["Zucchini", "Pumpkin", "Squash"]): preferred = "Squash"
            else: preferred = "Vegetables"
            category = category_map.get(preferred, category_map["Vegetables"])
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
                        folder='greenharvest_images/products',
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
                    rating=random.choices([1,2,2,3,4,4,5,5,5], k=1)[0],
                    comment=random.choice(review_comments_pool)
                )
                created += 1
            except IntegrityError:
                skipped += 1
            except Exception as e:
                print(f"Review failed: {product.name} by {user.email} → {e}")
                skipped += 1

    print(f"Reviews → created: {created}   skipped (already existed): {skipped}")

    print("Seeding complete! Check your database.")

# ────────────────────────────────────────────────
# Run
# ────────────────────────────────────────────────
seed_data()