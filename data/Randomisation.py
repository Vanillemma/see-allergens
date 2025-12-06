import csv
import random
import itertools
import os

Food_product = [
    "Almond Cookies", "Aloo Gobi", "Aloo Paratha", "Apple", "Apple Cider",
    "Apple Crisp", "Apple Pie", "Avocado Toast", "Bacon-Wrapped Shrimp",
    "Baked Apple", "Baked Brie", "Baked Chicken Wings", "Baked Cod",
    "Baked Garlic Parmesan Chicken", "Baked Salmon", "Baked Ziti",
    "Banana Bread", "Banana Pudding", "Banana Smoothie", "BBQ Ribs",
    "Beef and Broccoli", "Beef and Mushroom Stir-Fry", "Beef Burger",
    "Beef Burritos", "Beef Chili", "Beef Kabobs", "Beef Stir-Fry",
    "Beef Stroganoff", "Beef Tacos", "Beef Wellington", "Berry Cobbler",
    "Berry Crumble", "Berry Parfait", "Berry Smoothie", "Biryani",
    "Black Bean Soup", "Blueberry Muffins", "Blueberry Pancakes",
    "Brussels Sprouts", "Buffalo Wings", "Butter Chicken", "Butter Naan",
    "Butternut Squash Soup", "Cabbage Rolls", "Caesar Pasta Salad",
    "Caesar Salad", "Caesar Salad Wrap", "Caesar Shrimp Skewers",
    "Caesar Wrap", "Caprese Salad", "Caprese Sandwich", "Caprese Skewers",
    "Caramel Apple", "Caramel Popcorn", "Carrot Cake", "Cheddar Cheese",
    "Cheese Pizza", "Chicken Alfredo", "Chicken Alfredo Pizza",
    "Chicken and Rice Soup", "Chicken Biryani", "Chicken Caesar Salad",
    "Chicken Caesar Wrap", "Chicken Curry", "Chicken Enchiladas",
    "Chicken Fettuccine Alfredo", "Chicken Korma", "Chicken Malai Tikka",
    "Chicken Noodle Casserole", "Chicken Noodle Soup", "Chicken Parmesan",
    "Chicken Piccata", "Chicken Pot Pie", "Chicken Quesadilla",
    "Chicken Satay", "Chicken Shawarma", "Chicken Stir-Fry",
    "Chicken Teriyaki", "Chocolate Cake", "Chocolate Chip Cookies",
    "Chocolate Chip Pancakes", "Chocolate Mousse", "Chole Bhature",
    "Chole Kulche", "Cilantro Lime Chicken", "Cinnamon Rolls",
    "Coconut Curry", "Cucumber Salad", "Dahi Vada", "Dal Makhani",
    "Dosa", "Egg Fried Rice", "Egg Salad", "Egg Salad Sandwich",
    "Eggplant Parmesan", "Fish Sticks", "French Fries",
    "French Onion Soup", "Fruit Salad", "Garlic Bread", "Garlic Shrimp",
    "Gazpacho", "Gobi Manchurian", "Greek Gyro", "Greek Gyro Wrap",
    "Greek Lemon Chicken", "Greek Lemon Potatoes", "Greek Moussaka",
    "Greek Salad", "Greek Spanakopita", "Greek Yogurt",
    "Greek Yogurt Parfait", "Green Smoothie",
    "Grilled Portobello Mushroom Burger", "Gulab Jamun",
    "Hawaiian Pizza", "Honey Glazed Carrots", "Honey Mustard Chicken",
    "Honey Soy Glazed Salmon", "Hyderabadi Biryani", "Jalebi", "Kheer",
    "Key Lime Pie", "Lemon Bars", "Lemon Dill Salmon",
    "Lemon Herb Roasted Chicken", "Lemonade", "Lemon Garlic Chicken",
    "Lemon Garlic Shrimp", "Lemon Pepper Chicken",
    "Lemon Poppy Seed Muffins", "Lentil Curry", "Lentil Salad",
    "Lentil Soup", "Lobster Bisque", "Lobster Roll",
    "Malabar Fish Curry", "Malai Chicken Tikka", "Malai Kofta",
    "Mango Coconut Popsicles", "Mango Lassi", "Mango Salsa",
    "Margherita Pasta", "Margherita Pizza", "Masala Dosa",
    "Mashed Potatoes", "Matar Paneer", "Milk Chocolate",
    "Minestrone Soup", "Miso Soup", "Mixed Berry Pie",
    "Mushroom and Goat Cheese Flatbread", "Mushroom Risotto",
    "Mushroom Soup", "Mutton Biryani", "Oatmeal",
    "Oatmeal Raisin Cookies", "Omelette", "Onion Rings",
    "Orange Chicken", "Orange Juice", "Pancake Stack", "Pancakes",
    "Pancetta Pasta", "Paneer Tikka", "Pani Puri", "Paniyaram",
    "Pasta Carbonara", "Pav Bhaji", "Peanut Butter", "Pecan Pie",
    "Pesto Chicken", "Pesto Pasta", "Pesto Pasta Salad", "Pesto Pizza",
    "Pineapple Upside-Down Cake", "Plain Quiche", "Prawn Biryani",
    "Prawn Curry", "Pumpkin Pie", "Pumpkin Soup", "Quiche",
    "Quiche Lorraine", "Quinoa Salad", "Quinoa Stuffed Peppers", "Rabri",
    "Rajma Chawal", "Raita", "Ranch Dressing", "Raspberry Cheesecake",
    "Raspberry Spinach Salad", "Rasmalai", "Rasgulla", "Ratatouille",
    "Ratatouille Pasta", "Ratatouille Pizza", "Ratatouille Tart",
    "Rice Pudding", "Rogan Josh", "Roasted Brussels Sprouts", "Samosa",
    "Salsa", "Sausage and Pepper Pizza", "Sausage Pizza",
    "Shrimp Fried Rice", "Shrimp Scampi", "Shrimp Scampi Pasta",
    "S'mores", "Soy Milk", "Spaghetti Bolognese",
    "Spinach and Feta Stuffed Chicken", "Spinach Artichoke Dip",
    "Spinach Salad", "Spinach Stuffed Chicken", "Strawberry Shortcake",
    "Strawberry Smoothie", "Strawberry Spinach Salad",
    "Strawberry Yogurt", "Stuffed Bell Peppers",
    "Stuffed Cabbage Rolls", "Stuffed Mushrooms",
    "Stuffed Portobello Mushrooms", "Stuffed Tomatoes", "Sushi",
    "Sushi Bowl", "Sushi Rolls", "Sweet and Sour Chicken",
    "Sweet Potato Casserole", "Sweet Potato Fries", "Tandoori Chicken",
    "Teriyaki Beef", "Teriyaki Salmon", "Tiramisu", "Tofu Curry",
    "Tofu Scramble", "Tofu Stir-Fry", "Tomato Bruschetta",
    "Tomato Soup", "Tuna Salad", "Tuna Sandwich", "Vanilla Cupcakes",
    "Vanilla Ice Cream", "Vanilla Yogurt", "Vada Pav",
    "Vegetable Biryani", "Vegetable Curry", "Vegetable Lasagna",
    "Vegetable Soup", "Vegetable Stir-Fry", "Veggie Burger",
    "Veggie Omelette", "Wheat Bread", "Zucchini Bread",
    "Zucchini Noodles", "Zucchini Noodles with Pesto",
    "Bagel", "Baguette", "Baklava", "BBQ Chicken Pizza", "Beet Salad",
    "Beetroot Soup", "Berry Jam", "Broccoli Cheddar Soup", "Brownies",
    "Burrito Bowl", "Cauliflower Pizza", "Chai Latte", "Cheese Fondue",
    "Cheesecake", "Chicken Fried Rice", "Chicken Gyro", "Chicken Nuggets",
    "Chicken Tenders", "Chili Cheese Fries", "Chimichanga", "Chocolate Bar",
    "Couscous", "Crème Brûlée", "Crispy Tofu", "Croissant", "Cuban Sandwich",
    "Curry Laksa", "Deviled Eggs", "Dumplings", "Edamame", "Falafel",
    "Falafel Wrap", "Focaccia", "Fried Calamari", "Fried Chicken", 
    "Fried Rice", "Granola", "Greek Baklava", "Guacamole", "Hamburger",
    "Hot Chocolate", "Hot Dog", "Hummus", "Ice Cream Sandwich",
    "Katsu Curry", "Kimchi", "Lasagna", "Mac and Cheese", "Mozzarella Sticks",
    "Acai Bowl", "Adobo Chicken", "Aged Cheddar", "Agua Fresca", "Aioli",
    "Alfredo Pasta Bake", "Almond Butter", "Amaretto Cake", "Anchovy Pizza",
    "Antipasto Salad", "Apple Fritters", "Apricot Tart", "Arancini",
    "Arepas", "Artichoke Dip", "Asian Noodle Bowl", "Asparagus Soup",
    "Baba Ganoush", "Bagel Sandwich", "Baked Mac and Cheese",
    "Baked Sweet Potatoes", "Baklava Cheesecake", "Bao Buns",
    "Barbecue Chicken", "Barley Soup", "Basil Pesto", "Basmati Rice",
    "Beef Bolognese Lasagna", "Beef Brisket", "Beef Empanadas",
    "Beef Fajitas", "Beef Jerky", "Beef Pho", "Belgian Waffles",
    "Berry Tart", "Bibimbap", "Biscotti", "Black Forest Cake",
    "Black Pepper Chicken", "Black Tea", "Blackberry Pie", "BLT Sandwich",
    "Boba Milk Tea", "Bolognese Pizza", "Bolognese Stuffed Shells",
    "Borscht", "Bourbon Chicken", "Bread Pudding", "Breakfast Burrito",
    "Breakfast Sandwich", "Broccoli Soup", "Brown Rice Bowl", "Bulgogi",
    "Burrata Salad", "Butter Biscuits", "Buttermilk Pancakes",
    "Butterscotch Pudding", "Cacio e Pepe", "Cajun Chicken",
    "Cajun Fries", "Cajun Pasta", "California Roll",
    "Calzone", "Canelé", "Cannelloni", "Cannoli", "Cantaloupe Smoothie",
    "Caramel Cheesecake", "Caramel Latte", "Carne Asada",
    "Carrot Ginger Soup", "Cashew Chicken", "Cauliflower Curry",
    "Cauliflower Rice", "Caviar", "Ceviche", "Cheddar Biscuits",
    "Cheese Fondue", "Cheese Omelette", "Cheesy Garlic Mashed Potatoes",
    "Cherry Cobbler", "Cherry Cheesecake", "Cherry Pie", "Chicken Adobo",
    "Chicken Bites", "Chicken Caesar Pasta", "Chicken Chimichanga",
    "Chicken Cordon Bleu", "Chicken Doner", "Chicken Dumplings",
    "Chicken Fajitas", "Chicken Gyros Plate", "Chicken Kebab",
    "Chicken Nuggets Meal", "Chicken Pho", "Chicken Potstickers",
    "Chicken Ranch Wrap", "Chicken Samosa", "Chicken Slider",
    "Chicken Soup with Dumplings", "Chicken Tinga Tacos",
    "Chili Con Carne", "Chili Garlic Noodles", "Chimichurri Steak",
    "Chips and Salsa", "Choco Lava Cake", "Chocolate Croissant",
    "Chocolate Donut", "Chocolate Fudge", "Chocolate Pie",
    "Chow Mein", "Churros", "Cinnamon Apple Oatmeal",
    "Cinnamon Donuts", "Clam Chowder", "Club Sandwich", "Coconut Cake",
    "Coconut Cookies", "Coconut Ice Cream", "Coconut Milk", "Coconut Rice",
    "Coffee Cake", "Coleslaw", "Corn Chowder", "Corn Dogs", "Cornbread",
    "Cottage Pie", "Couscous Salad", "Crab Cakes", "Crab Rangoon",
    "Cranberry Muffins", "Cream Cheese Bagel", "Creamy Tomato Pasta",
    "Crepes", "Crispy Beef", "Crispy Chicken Sandwich",
    "Crispy Spring Rolls", "Croque Monsieur", "Cuban Rice and Beans",
    "Cucumber Raita", "Curry Chicken Salad", "Curry Puffs",
    "Custard Tart", "Daal Tadka", "Deep Dish Pizza", "Dill Pickles",
    "Dim Sum", "Double Cheeseburger", "Dragon Roll", "Dulce de Leche Cake",
    "Dumpling Soup", "Eclairs", "Egg Curry", "Egg Rolls", "Egg Tart",
    "Egyptian Koshari", "Elote", "Empanadas", "Enchilada Soup",
    "Fajita Bowl", "Falooda", "Feta Pasta", "Fish Curry", "Fish Pie",
    "Fish Tacos", "Focaccia Sandwich", "Fondant Potatoes",
    "French Toast", "Fried Dumplings", "Fried Pickles",
    "Fried Rice Noodles", "Frittata", "Frog Legs", "Fruit Tart",
    "Funnel Cake", "Galette", "Garlic Butter Steak", "Garlic Knots",
    "Ginger Chicken", "Ginger Cookies", "Gnocchi", "Goat Cheese Salad",
    "Goulash", "Granola Bar", "Greek Chicken Bowl", "Green Curry",
    "Green Tea Latte", "Grilled Cheese Sandwich", "Grilled Halloumi",
    "Grilled Lamb Chops", "Grilled Peach Salad", "Grilled Steak",
    "Gyudon", "Halloumi Fries", "Ham and Cheese Sandwich",
    "Ham Omelette", "Hamburger Steak", "Hash Browns", "Hawaiian Chicken",
    "Hazelnut Cake", "Herb Butter Pasta", "Hibachi Chicken",
    "Hoisin Chicken", "Honey Garlic Pork", "Honey Lemon Drink",
    "Hot Wings", "Ice Cream Cake", "Italian Sub", "Jambalaya",
    "Japanese Curry", "Jasmine Rice", "Kale Salad", "Kebab Plate",
    "Korean Fried Chicken", "Kung Pao Chicken", "Lamb Biryani",
    "Lamb Curry", "Lamb Kebab", "Lamb Shawarma", "Lasagna Roll-Ups",
    "Latte Macchiato", "Lava Cake", "Lemon Meringue Pie",
    "Lemon Tart", "Lentil Dal", "Lime Chicken", "Lobster Mac and Cheese",
    "Lobster Tail", "Lumpia", "Macadamia Cookies",
    "Macarons", "Mahi Mahi Tacos", "Mango Chutney", "Mango Ice Cream",
    "Mango Sticky Rice", "Maple Donuts", "Maple Syrup Pancakes",
    "Meatball Marinara", "Meatball Sub", "Mediterranean Bowl", "Mille Feuille",
    "Mint Chutney", "Miso Ramen", "Mixed Nuts", "Mojito Mocktail",
    "Molten Chocolate Cake", "Mongolian Beef", "Mozzarella Sticks",
    "Mushroom Burger", "Naan Pizza", "Nasi Goreng", "Nicoise Salad",
    "Noodle Soup", "Nutella Crepes", "Oat Cookies", "Oreo Cheesecake",
    "Apple Juice", "Orange Juice", "Grape Juice", "Pineapple Juice", "Mango Juice",
    "Guava Juice", "Passion Fruit Juice", "Pear Juice", "Peach Juice", "Apricot Juice",
    "Strawberry Juice", "Blueberry Juice", "Raspberry Juice", "Cranberry Juice", "Blackberry Juice",
    "Watermelon Juice", "Cantaloupe Juice", "Honeydew Juice", "Kiwi Juice", "Lemon Juice",
    "Lime Juice", "Dragon Fruit Juice", "Lychee Juice", "Papaya Juice", "Pomegranate Juice",
    "Tropical Juice Blend", "Mixed Berry Juice", "Coconut Water", "Sparkling Water",
    "Lemon Sparkling Water", "Lime Sparkling Water", "Peach Sparkling Water",
    "Berry Sparkling Water", "Grapefruit Sparkling Water", "Orange Sparkling Water",
    "Ginger Sparkling Water", "Cucumber Mint Water", "Strawberry Infused Water",
    "Lemon Mint Water", "Watermelon Mint Water", "Pineapple Infused Water",
    "Apple Cinnamon Infused Water", "Orange Basil Water", "Lemon Ginger Water",
    "Blueberry Mint Water", "Iced Tea Lemon", "Iced Tea Peach", "Iced Tea Mango",
    "Iced Tea Raspberry", "Iced Tea Green Tea", "Iced Tea Black Tea", "Iced Chai Tea",
    "Iced Matcha Tea", "Sweet Tea", "Unsweetened Iced Tea", "Hibiscus Iced Tea",
    "Mint Iced Tea", "Honey Lemon Tea", "Hot Chocolate", "White Hot Chocolate",
    "Dark Hot Chocolate", "Peppermint Hot Chocolate", "Vanilla Hot Chocolate",
    "Mocha", "Caramel Latte", "Vanilla Latte", "Hazelnut Latte", "Cinnamon Latte",
    "Pumpkin Spice Latte", "Flat White", "Cappuccino", "Espresso", "Double Espresso",
    "Americano", "Cortado", "Macchiato", "Caramel Macchiato", "Iced Coffee",
    "Iced Latte", "Iced Mocha", "Iced Caramel Latte", "Cold Brew", "Nitro Cold Brew",
    "Matcha Latte", "Iced Matcha Latte", "Chai Latte", "Dirty Chai Latte",
    "Milkshake Vanilla", "Milkshake Chocolate", "Milkshake Strawberry",
    "Milkshake Banana", "Milkshake Oreo", "Milkshake Peanut Butter",
    "Milkshake Caramel", "Banana Smoothie", "Strawberry Smoothie",
    "Mango Smoothie", "Pineapple Smoothie", "Berry Smoothie",
    "Peach Smoothie", "Chocolate Smoothie", "Vanilla Smoothie",
    "Green Smoothie", "Protein Smoothie", "Coffee Smoothie",
    "Tropical Smoothie", "Avocado Smoothie", "Papaya Smoothie",
    "Coconut Smoothie", "Kiwi Smoothie", "Dragon Fruit Smoothie",
    "Watermelon Smoothie", "Guava Smoothie", "Matcha Smoothie",
    "Oreo Smoothie", "Energy Drink Original", "Energy Drink Sugar-Free",
    "Energy Drink Tropical", "Energy Drink Berry", "Energy Drink Citrus",
    "Cola", "Cola Zero", "Cola Cherry", "Cola Vanilla", "Cola Lime",
    "Lemon Soda", "Lime Soda", "Orange Soda", "Grape Soda", "Pineapple Soda",
    "Cream Soda", "Root Beer", "Ginger Ale", "Ginger Beer", "Tonic Water",
    "Club Soda", "Apple Cider", "Pear Cider", "Cherry Cider",
    "Sparkling Apple Cider", "Sparkling Pear Cider", "Virgin Mojito",
    "Virgin Piña Colada", "Virgin Margarita", "Virgin Daiquiri",
    "Virgin Strawberry Daiquiri", "Virgin Mango Daiquiri",
    "Shirley Temple", "Arnold Palmer", "Lemonade", "Strawberry Lemonade",
    "Blueberry Lemonade", "Raspberry Lemonade", "Peach Lemonade",
    "Watermelon Lemonade", "Mango Lemonade", "Pink Lemonade",
    "Orange Lemonade", "Grapefruit Lemonade", "Iced Lemonade Tea",
    "Yuzu Lemonade", "Ginger Lemonade", "Mint Lemonade", "Chai Frappe",
    "Caramel Frappe", "Mocha Frappe", "Coffee Frappe", "Oreo Frappe",
    "Vanilla Frappe", "Coconut Frappe", "Matcha Frappe", "Berry Frappe",
    "Chocolate Milk", "Strawberry Milk", "Banana Milk", "Vanilla Milk",
    "Almond Milk Drink", "Coconut Milk Drink", "Matcha Milk",
    "Rose Milk", "Thandai", "Lassi Sweet", "Lassi Mango", "Lassi Rose",
    "Iced Cocoa", "Pink Drink", "Coconut Refresher", "Dragon Fruit Refresher",
    "Mango Refresher", "Blue Lagoon Mocktail", "Sunset Mocktail",
    "Citrus Cooler", "Berry Cooler", "Tropical Cooler", "Mint Cooler",
    "Pineapple Cooler", "Coconut Lime Cooler", "Kiwi Refresher",
    "Iced Hibiscus Refresher", "Berry Punch", "Tropical Punch"
]

Main_ingredient = [
    "Almonds", "Apple", "Apples", "Avocado", "Bacon", "Basil", "Beef", "Bell peppers", "Black beans",
    "Bread", "Brie cheese", "Brussels sprouts", "Butter", "Buttermilk", "Butternut squash", "Cabbage",
    "Carrots", "Cauliflower", "Cheddar cheese", "Cheese", "Chicken", "Chicken breast", "Chicken broth",
    "Chickpeas", "Chocolate", "Cod", "Coconut milk", "Cottage cheese", "Cream", "Cream cheese",
    "Cucumber", "Cucumbers", "Curry paste", "Dal (lentils)", "Dough", "Eggplant", "Eggs", "Feta cheese",
    "Fermented batter", "Fish fillets", "Flour", "Garlic", "Goat cheese", "Greek yogurt", "Grilled chicken",
    "Ground beef", "Ham", "Hyderabadi biryani rice", "Kidney beans", "Lamb", "Lemon juice", "Lime juice",
    "Lobster", "Mango", "Milk", "Milk solids", "Miso paste", "Mixed berries", "Mixed vegetables",
    "Mushrooms", "Mutton", "Oats", "Olive oil", "Onions", "Oranges", "Paneer", "Pasta", "Peanuts",
    "Pesto sauce", "Pineapple", "Pork ribs", "Potatoes", "Prawns", "Quinoa", "Raw fish", "Rice",
    "Romaine lettuce", "Salmon", "Salmon fillet", "Sausage", "Semolina", "Shrimp", "Soybeans",
    "Spinach", "Sushi rice", "Sweet potatoes", "Tomato sauce", "Tomatoes", "Tofu", "Tuna",
    "Vanilla (for desserts)", "Vegetables", "Wheat flour", "Yogurt", "Yogurt (milk, cultures)", "Zucchini",
    "Blueberries", "Strawberries", "Açaí Bowl", "Adobo Chicken", "Ahi Tuna Poke Bowl",
    "Air Fryer Chicken Wings", "Antipasto Platter", "Apple Fritters", "Arancini", "Avocado Salad",
    "Baba Ganoush", "Bagel with Cream Cheese", "Bahn Mi Sandwich", "Baked Alaska", "Baked Beans",
    "Baked Oatmeal", "Baklava", "Balinese Curry", "Bangers and Mash", "Basil Pesto", "Beef Bourguignon",
    "Beef Empanadas", "Beef Lo Mein", "Beef Nachos", "Beef Pho", "Beef Sliders", "Beef Tartare",
    "Beet Salad", "Belgian Waffles", "Bibimbap", "Biscuits and Gravy", "Black Forest Cake",
    "BLT Sandwich", "Borscht", "Boston Cream Pie", "Bread Pudding", "Breakfast Burrito",
    "Breakfast Casserole", "Breakfast Quesadilla", "Brownies", "Bubble Tea", "Bulgogi",
    "Buttermilk Pancakes", "Cajun Chicken", "Cajun Shrimp", "California Roll", "Cannoli", "Carrot Soup",
    "Chana Masala", "Char Siu Bao", "Charcuterie Board", "Cheeseburger", "Cheesecake", "Chicken Adobo",
    "Chicken Cacciatore", "Chicken Cordon Bleu", "Chicken Fried Rice", "Chicken Gyro", "Chicken Marsala",
    "Chicken Nachos", "Chicken Pad Thai", "Chicken Panini", "Chicken Pho", "Chicken Salad",
    "Chicken Souvlaki", "Chicken Tenders", "Chicken Tikka Masala", "Chicken Tortilla Soup",
    "Chicken Wrap", "Chilaquiles", "Chili Cheese Fries", "Chimichanga", "Chocolate Brownies",
    "Chocolate Croissant", "Chocolate Fondue", "Chocolate Truffles", "Chow Mein", "Cioppino",
    "Clam Chowder", "Cobb Salad", "Coconut Shrimp", "Coffee Cake", "Coleslaw", "Corn Chowder",
    "Corn Fritters", "Cornbread", "Crab Cakes", "Crab Rangoon", "Cream of Mushroom Soup",
    "Creme Brulee", "Croissant", "Croque Monsieur", "Cuban Sandwich", "Currywurst", "Dakgangjeong",
    "Danish Pastry", "Deviled Eggs", "Dim Sum", "Donburi", "Donuts", "Duck Confit", "Duck à l'Orange",
    "Dumplings", "Edamame", "Egg Drop Soup", "Egg Benedict", "Egg Curry", "Egg Foo Young", "Empanadas",
    "Enchiladas Verdes", "Fajitas", "Falafel", "Filet Mignon", "Fish and Chips", "Fish Curry", "Flan",
    "Focaccia Bread", "Fortune Cookies", "French Toast", "Fried Calamari", "Fried Catfish", "Fried Chicken",
    "Fried Green Tomatoes", "Fried Ice Cream", "Fried Okra", "Fried Plantains", "Frittata",
    "Frozen Yogurt", "Fudge", "Galette", "Garlic Roasted Potatoes", "Gelato", "General Tso's Chicken",
    "Gnocchi", "Goulash", "Graham Crackers", "Greek Chicken", "Green Bean Casserole", "Green Curry",
    "Grilled Cheese Sandwich", "Grilled Corn", "Grilled Eggplant", "Grilled Fish", "Grilled Pork Chops",
    "Grilled Steak", "Grilled Vegetables", "Guacamole", "Gumbo", "Gyudon", "Hainanese Chicken Rice",
    "Halwa", "Ham and Cheese Croissant", "Ham Sandwich", "Hamburger Helper", "Harissa Chicken",
    "Hash Browns", "Hawaiian Roll", "Hot and Sour Soup", "Hot Chocolate", "Hot Dog", "Hot Pot", "Hummus",
    "Ice Cream Sundae", "Irish Stew", "Italian Sub", "Jambalaya", "Japanese Curry", "Japchae",
    "Jerk Chicken", "Kabsa", "Katsu Curry", "Kebab", "Kimchi", "Kimchi Fried Rice", "Kimchi Jjigae",
    "King Crab Legs", "Kung Pao Chicken", "Lamb Chops", "Lamb Curry", "Lamb Kebabs", "Lamb Vindaloo",
    "Lasagna", "Latkes", "Lava Cake", "Leek and Potato Soup", "Lemon Rice", "Lentil Dal",
    "Lobster Mac and Cheese", "Lobster Newburg", "Loco Moco", "Macaroni and Cheese", "Macarons",
    "Mahimahi", "Mango Sticky Rice", "Mapo Tofu", "Marinated Olives", "Massaman Curry", "Matcha Latte",
    "Meatballs", "Meatloaf", "Mediterranean Bowl", "Mediterranean Salad", "Meringue", "Mint Chutney",
    "Miso Glazed Salmon", "Mochi", "Mofongo", "Mongolian Beef", "Mozzarella Sticks", "Mushroom Gravy",
    "Mussels Marinara", "Nasi Goreng", "New England Clam Chowder", "Nicoise Salad", "Noodle Soup",
    "Okonomiyaki", "Olive Tapenade", "Omelet du Fromage", "Oysters Rockefeller", "Pad See Ew", "Paella",
    "Pajeon", "Palak Paneer", "Panang Curry", "Panna Cotta", "Pasta e Fagioli", "Pasta Primavera",
    "Pastrami Sandwich", "Patatas Bravas", "Pea Soup", "Peach Cobbler", "Peanut Butter Cookies",
    "Peanut Sauce", "Pecan Cookies", "Peking Duck", "Pepper Steak", "Philly Cheesesteak", "Pickles",
    "Pico de Gallo", "Pierogi", "Poached Eggs", "Poached Salmon", "Polenta", "Pomegranate Salad",
    "Popcorn Chicken", "Pork Belly", "Pork Chop", "Pork Dumplings", "Pork Loin", "Pork Schnitzel",
    "Pork Tenderloin", "Pot Roast", "Potato Bread", "Potato Chips", "Potato Gnocchi", "Potato Leek Soup",
    "Poutine", "Prosciutto", "Prosciutto-Wrapped Asparagus", "Pulled Pork", "Pumpkin Bread",
    "Pumpkin Ravioli", "Pumpkin Spice Latte", "Queso Dip", "Rack of Lamb", "Ramen", "Raspberry Tart",
    "Red Bean Buns", "Red Velvet Cake", "Reuben Sandwich", "Roast Beef", "Roast Duck", "Roast Turkey",
    "Roasted Asparagus", "Roasted Beets", "Roasted Cauliflower", "Roasted Chickpeas", "Roasted Garlic",
    "Roasted Pumpkin", "Roasted Red Peppers", "Roasted Root Vegetables", "Roasted Squash",
    "Rocky Road Ice Cream", "Roti", "Rum Cake", "Saffron Rice", "Salmon Patties", "Salsa Verde",
    "Saltimbocca", "Samosa Chaat", "Sashimi", "Sausage Gravy", "Sausage Rolls", "Scalloped Potatoes",
    "Scallops", "Scotch Eggs", "Seafood Paella", "Seafood Platter", "Sesame Chicken", "Sesame Noodles",
    "Shakshuka", "Shepherd's Pie", "Shish Taouk", "Short Ribs", "Shrimp Cocktail", "Shrimp Etouffee",
    "Shrimp Gumbo", "Shrimp Po' Boy", "Shrimp Tempura", "Sichuan Beef", "Sloppy Joe", "Smoked Salmon",
    "Sopaipillas", "Sorbet", "Sourdough Bread", "Spaghetti Aglio e Olio", "Spaghetti Squash",
    "Spicy Tuna Roll", "Spring Rolls", "Squash Soup", "Steak Au Poivre", "Steak Frites", "Steak Salad",
    "Steak Sandwich", "Steamed Buns", "Steamed Fish", "Sticky Rice", "Stir Fry Noodles", "Stuffed Dates",
    "Stuffed Pasta Shells", "Succotash", "Sugar Cookies", "Summer Rolls", "Sunomono", "Sushi Burrito",
    "Sweet and Sour Pork", "Sweet Corn Soup", "Swiss Cheese Fondue", "Swiss Roll", "Tabbouleh",
    "Taco Salad", "Tacos al Pastor", "Tagine", "Taiyaki", "Takoyaki", "Tandoori Fish", "Tandoori Roti",
    "Tapioca Pudding", "Tarte Tatin", "Tater Tots", "Tempura Udon", "Teriyaki Glaze",
    "Thai Basil Chicken", "Thai Green Curry", "Thai Iced Tea", "Thai Salad", "Three Bean Salad",
    "Tilapia", "Tom Kha Gai", "Tortellini", "Tres Leches Cake", "Truffle Fries", "Tuna Melt",
    "Tuna Pasta", "Tuna Steak", "Turkey Burger", "Turkey Club Sandwich", "Turkey Meatballs",
    "Turkish Delight", "Turmeric Rice", "Tzatziki", "Udon Noodles", "Upside-Down Cake",
    "Vanilla Pudding", "Vegetable Korma", "Vegetable Lo Mein", "Vegetable Pakora",
    "Vegetable Tempura", "Vegetarian Chili", "Veggie Pizza", "Venison Stew",
    "Vietnamese Spring Rolls", "Waldorf Salad", "Watermelon Salad", "White Chocolate", "White Rice",
    "Wonton Soup", "Yakitori", "Yellow Curry", "Yorkshire Pudding", "Yuca Fries", "Zucchini Fritters"
]

Sweetener = [ "Sugar","Honey","None","Brown sugar","Mayonnaise","Rice vinegar","Milk","Caramel","Tamarind","Maple syrup","Corn Syrup"]

Fat_Oil = [ "Butter","None","Vegetable oil","Olive oil","Sour cream","Yogurt","Ghee","Cream","Peanut butter","Peanut oil","Soy sauce","Coconut oil","Coconut milk","Mustard","Heavy cream","Cream cheese","Bacon","Milk powder","Margarine","Soy oil","Sesame oil","Almond oil" ]

Allergens = [ "Gluten","Tree nuts","Celery","None","Milk","Egg","Fish","Mustard","Soy","Peanut" ]

Seasoning = [
    "Flour", "Salt", "Garlic", "Herbs", "Parmesan cheese", "Caesar dressing",
    "Lettuce", "Tomato sauce", "Basil", "Pepper", "Mozzarella cheese", "Cream",
    "Mushroom", "Onion", "Vanilla extract", "Cheese", "Breadcrumbs",
    "Tandoori spices", "Milk", "Marinara sauce", "Cardamom", "Feta cheese",
    "Vegetable broth", "Fresh tomatoes", "Arborio rice", "Granola",
    "Mixed berries", "Spinach", "Phyllo dough", "Eggs", "Noodles", "Yogurt",
    "Kashmiri red chili", "Tikka masala", "Spices", "Rose water", "Syrup",
    "Nuts", "Beef broth", "Bread", "Mustard", "Celery", "Soy sauce",
    "Teriyaki sauce", "Ginger", "Raw fish", "Vegetables", "Pectin", "Sugar",
    "Water", "BBQ sauce", "Tomato broth", "Balsamic vinegar", "Enchilada sauce",
    "Cilantro", "Pineapple", "Bell peppers", "Seasonings", "Taco seasoning",
    "Rice", "Paprika", "Curry powder", "Curry paste", "Nutmeg", "Vinaigrette",
    "Puff pastry", "Dill", "Lemon", "Capers", "Lemon juice", "Lime",
    "Cinnamon", "Curry spices", "Masala spices", "Mustard seeds",
    "Curry leaves", "Pav bread", "Chutney", "Biryani masala",
    "Chole masala", "Potato masala", "Manchurian sauce", "Emulsifiers",
    "Turmeric", "Nori (seaweed)", "Graham cracker crust", "Shortcake",
    "Coffee", "Cocoa", "Pumpkin spice", "Pastry", "Saffron syrup",
    "Cocoa powder", "Maple syrup", "Raisins", "Chocolate chips",
    "Whipped cream", "Oats", "Raspberries", "Blueberries", "Ham"
]


PREFIXES = [
    "Walmart", "Safeway", "Whole Foods Market", "Aldi (US)", "Trader Joe's", "Publix", "Giant Eagle",
    "Meijer", "H-E-B", "Target", "QFC", "Hannaford", "Ralphs", "Loblaws", "Sobeys", "Metro",
    "No Frills", "Provigo", "Maxi", "FreshCo", "Food Basics", "Save On Foods", "Co-op",
    "T&T Supermarket", "Costco", "Carrefour", "Lidl", "Edeka", "Tesco", "Auchan", "E.Leclerc",
    "SPAR", "Hemköp", "Casino", "Picard", "Sainsbury's", "Monoprix", "Franprix", "Biocoop",
    "Grand Frais", "Kroger", "Albertsons", "Ahold Delhaize", "Wegmans", "Hy-Vee", "Stop & Shop",
    "Giant Food", "Food Lion", "Harris Teeter", "King Soopers", "Fred Meyer", "Smith's",
    "WinCo Foods", "Market Basket", "Weis Markets", "Price Chopper", "ShopRite", "Acme Markets",
    "Jewel-Osco", "Shaw's", "Star Market", "Vons", "Pavilions", "Randalls", "Tom Thumb",
    "United Supermarkets", "Stater Bros", "Bashas'", "Food 4 Less", "Cub Foods", "Fareway",
    "Fresh Thyme", "Lucky's Market", "Natural Grocers", "Sprouts Farmers Market",
    "The Fresh Market", "Earth Fare", "MOM's Organic Market", "New Seasons Market",
    "Bristol Farms", "Gelson's Markets", "Mollie Stone's", "PCC Community Markets",
    "Central Market", "United Grocers", "Associated Food Stores", "Supervalu", "Nash Finch",
    "SpartanNash", "Wakefern Food Corp", "C&S Wholesale Grocers", "Superstore", "Thrifty Foods",
    "Longo's", "Farm Boy", "Pete's Frootique", "Choices Markets", "Nesters Market", "IGA",
    "Overwaitea Food Group", "Federated Co-operatives", "Kal Tire", "M&M Food Market",
    "Bulk Barn", "Nature's Emporium", "Starsky Fine Foods", "Highland Farms", "Adonis",
    "Marché Tau", "Kim Phat", "H Mart", "99 Ranch Market", "JFC International",
    "Mitsuwa Marketplace", "Marukai", "Seiwa Market", "Nijiya Market", "Assi Plaza",
    "Grand Asia Market", "Patel Brothers", "India Bazaar", "Albertsons Market",
    "Cardenas Markets", "El Super", "Fiesta Mart", "Northgate González Markets",
    "Super A Foods", "Superior Grocers", "Vallarta Supermarkets", "C-Town Supermarkets",
    "Fine Fare", "Key Food", "Associated Supermarket", "Bravo Supermarkets",
    "Compare Foods", "Food Bazaar", "Western Beef", "Pioneer Supermarkets", "Met Foods",
    "City Acres Market", "Fairway Market", "Zabar's", "Eataly", "Dean & DeLuca",
    "Balducci's", "Browne Trading Company", "Citarella", "Eli's Market",
    "Grace's Marketplace", "Murray's Cheese", "Agata & Valentina", "D'Artagnan",
    "Despaña", "Kalustyan's", "Sahadi's", "Economy Candy", "The Spice House",
    "Penzey's Spices", "World Spice Merchants",
    "Billa", "Rewe", "Migros", "Coop (CH)", "Denner", "Aldi Süd", "Aldi Nord",
    "Penny Market", "Netto Marken-Discount", "Norma", "Kaufland",
    "Waitrose", "Booths", "Iceland", "Morrisons", "Asda",
    "Colruyt", "Delhaize", "Intermarché", "GrandOpt",
    "Jumbo", "Albert Heijn", "Dirk", "Coop Nederland",
    "Conad", "Esselunga", "EuroSpin", "MD Discount", "Pam",
    "Dia", "Mercadona", "Consum", "Eroski",
    "Biedronka", "Zabka", "Carrefour Polska",
    "Sobeys Urban Fresh", "Your Independent Grocer", "Fortinos",
    "Fresh St. Market", "Urban Fare",
    "Chedraui", "Soriana", "La Comer", "Superama", "OXXO",
    "Makro Peru", "Tottus", "Plaza Vea", "Santa Isabel",
    "Jumbo Chile", "Lider", "Montecarlo Market",
    "Carrefour UAE", "Lulu Hypermarket", "Choithrams", "Spinneys",
    "Danube", "Panda", "Manuel Market", "Al Meera", "Megamart Qatar",
    "Aeon", "Don Quijote", "FamilyMart", "Lawson", "7-Eleven Japan",
    "FairPrice", "Sheng Siong", "Cold Storage", "ParknShop", "Wellcome",
    "SM Markets", "Robinsons", "Hypermart", "Lotte Mart", "GS25", "Emart",
    "Shoprite Africa", "Pick n Pay", "Checkers", "Spar South Africa",
    "Game Stores", "Nakumatt (legacy)", "Naivas", "Uchumi",
    "Woolworths", "Coles", "ALDI Australia", "Foodland", "IGA Australia",
    "Countdown", "New World", "Pak'nSave",
    "Fresh Market Co.", "Organic Valley Store", "Good Harvest Market", "Urban Green Grocers",
    "GreenLeaf Market", "PureFoods Store", "Harvest Lane Market", "EcoMart", "Green Choice Market",
    "PrimeFresh Superstore", "DailyValue Market", "Village Grocer", "City Fresh Market",
    "Neighborhood Foods", "Local Harvest Co.", "Sunrise Market", "Nature’s Basket",
    "Evergreen Foods", "Farmgate Market", "Fresh Roots Store", "Green Basket Market",
    "Harvest Hub", "Prime Grocers", "Better Foods Market", "Fresh Planet Market",
    "Happy Market", "Everyday Grocers", "Jungle Fresh Market", "Global Market Hub",
    "Wholemart", "MaxiMart", "SuperMart Express", "QuickBuy Market", "Everyday Essentials",
    "Select Foods Market", "EcoGrocer", "Family Grocers", "Urban Basket", "MegaMart Local",
    "Grocery Point", "Daily Stop Market", "Nature’s Way Market", "Daily Mart Hub",
    "MetroFood Shop", "CornerFarm Market", "Grocery Depot", "Essentials Co.",
    "SmartChoice Grocers", "UltraFresh Market", "Vista Foods", "GoodChoice Store",
    "MarketWorld", "Farm & Fresh", "FreshSpot Market", "Grocer’s Lane",
    "Farmway Market", "CityGroce", "PureHarvest Market", "FreshValue Store",
    "BudgetMart", "SmartBuy Foods", "EcoChoice Superstore", "Community Market Co.",
    "PrimeBargain Foods", "Food Essentials Market", "Fresh Isles Market",
    "Earthy Foods", "Purely Market", "Natural Earth Market", "BoldFoods Store",
    "Urban Fresh Hub", "JustGroceries", "Farmhouse Superstore", "SunMart",
    "GreenSquare Market", "StorePlus", "ValueHouse Foods", "GreenTree Grocers",
    "EcoHarvest Foods", "BetterMart", "PureSource Foods", "Fresh & More",
    "FoodGiant Mini", "Village Essentials", "GoodFoods Hub", "MegaGroceries",
    "UltraGrocer", "TrueValue Market", "GreenBox Foods", "FreshStop Mini",
    "MetroFresh Hub", "Perfect Pick Market", "FarmBasket Co.", "Food Universe",
    "FreshDrop Market", "Market Circle", "Community Grocer Hub", "FarmCity Market",
    "SunCoast Market", "Golden Harvest Store", "FreshRack Grocers", "GoGrocer",
    "Market Depot", "Local Market Express", "DailyMart Select", "EpicFoods Store",
    "ProGrocer", "National Grocers Hub", "Green Horizon Market", "VitalFresh Market",
    "Urban Roots Store", "House & Harvest", "MarketOne", "FreshFields Co.",
    "HappyGrocer", "PureFoods Center", "FoodVillage", "Harvest Pro Market",
    "FreshDay Grocers", "HealthyChoice Market", "PureNature Grocers", "ValueOne Market",
    "FreshNexus Market", "Grocery Sphere", "Premium Foods Market", "SunHarvest Store",
    "UltraChoice Market", "Megafood Market", "SmartShop Mart", "FreshNation Co.",
    "GoodLife Market", "Golden Leaf Market", "FreshNest Grocers", "Bright Foods",
    "Better Fresh Market", "Urban Delights Store", "Grocery Garden", "UrbanCart Market",
    "EarthMarket", "Global Fresh Market", "FarmFresh Corner", "Supercity Grocers",
    "Daily Essentials Hub", "ValueFresh Store", "Neighborhood Market Co.",
    "FamilyNeeds Market", "Planet Grocer", "NatureTown Market", "Fresh Foods Plaza",
    "Capital Foods Market", "EcoWorld Grocer", "FreshBay Market", "MegaValue Market",
    "Budget Basket Store", "Urban Food Outlet", "GreenRoots Co.", "Village Basket Market",
    "Super General Store", "FarmDirect Market", "EcoPrime Market", "UltraMart Express",
    "UrbanFood District", "FreshLux Market", "DailyStreet Market", "EcoLine Foods",
    "Harvest Street Market", "FoodTown Mini", "OneStop Grocer", "FoodMaxx Local",
    "FreshBridge Market", "BrightMart", "FoodWorks Co.", "MetroGrocer Center",
    "Local Choice Market", "Freshway Market", "ValuLand Market", "FarmPeak Foods",
    "UrbanNatural Market", "Morning Fresh Store", "GreenFarm Mini", "FoodHub Express",
    "FreshPicks Market", "SunFoods Store", "GreenRoots Market", "LuxeGrocers",
    "EarthTone Market", "Fresh Orchard Market", "TrueNature Grocers", "GreenDay Foods"
]

SUFFIXES = [
    "Bio", "Budget", "Classic", "Deluxe", "Diet", "Extra", "Family Size",
    "Gluten-Free", "Lactose-Free", "Limited Edition", "Lite", "Mild", "Mini",
    "No added Sugar", "Organic", "Original", "Premium", "Spicy", "XL", "Zero",
    "Low-Fat", "High-Protein", "Sugar-Free", "Keto", "Vegan", "Vegetarian",
    "Low-Carb", "No Salt", "Low Sodium", "High Fiber", "Natural", "Artisanal",
    "Handmade", "Signature", "Special", "Value Pack", "Mega Pack", "Twin Pack",
    "Party Size", "Snack Size", "Kids", "Baby", "Extra Spicy", "Super Spicy",
    "Ultra", "Max", "Plus", "Gold", "Silver", "Platinum", "Limited",
    "Seasonal", "Holiday Edition", "Fresh", "Raw", "Frozen", "Ready-to-Eat",
    "Ready-to-Cook", "Baked", "Grilled", "Roasted", "Smoked", "Aged",
    "Crunchy", "Creamy", "Soft", "Hard", "Bold", "Strong", "Mild", "Light",
    "Dark", "Sweet", "Unsweetened", "Cold Brew", "Iced", "Sparkling",
    "Classic Style", "New Style", "Updated", "2025 Edition", "Gourmet",
    "Chef's Selection", "Local", "Imported", "Premium Quality", "Eco",
    "Recyclable", "Compostable", "Refill Pack", "Bulk", "Express", "Instant",
    "Quick", "Microwaveable", "Heat & Serve", "No Preservatives",
    "No Artificial Flavors", "Fair Trade", "Non-GMO",
    "Ultra Fresh", "Hyper Fresh", "Super Fresh", "Farm Fresh", "Daily Fresh",
    "Stone-Baked", "Wood-Fired", "Charbroiled", "Slow Cooked", "Triple Cooked",
    "Double Roasted", "Sun-Dried", "Oven-Dried", "Naturally Sweetened",
    "Low Sugar", "Reduced Sugar", "Lightly Salted", "No Gluten Added",
    "Grain-Free", "Paleo", "Wholegrain", "Whole Wheat", "Ancient Grains",
    "Sprouted", "All-Natural", "Pure", "Zero Additives", "Zero Preservatives",
    "No GMO Ingredients", "Unfiltered", "Unprocessed", "Craft", "Artisan Style",
    "Fire-Grilled", "Stone-Milled", "Cold-Pressed", "Hand-Crafted",
    "Farmhouse Style", "Country Style", "Homestyle", "Village Style",
    "Traditional", "Authentic", "Rustic", "Heritage", "Vintage",
    "Barista Edition", "Barbecue Style", "Buffalo Style", "Smoky",
    "Buttery", "Velvety", "Cream-Infused", "Triple Cream", "Double Cream",
    "Rich", "Decadent", "Hearty", "Comfort Style", "Crunchy Style",
    "Smooth Blend", "Thick Cut", "Thin Cut", "Extra Thin", "Stone-Ground",
    "Ultra-Thin", "Extra Crunch", "Crispy", "Roast Style", "Fusion Style",
    "Gourmet Blend", "Chef Crafted", "Restaurant Style", "Street Style",
    "Festival Edition", "BBQ Edition", "Party Edition", "Summer Edition",
    "Winter Edition", "Autumn Edition", "Spring Edition", "Event Edition",
    "Chef’s Edition", "Premium Roast", "Master Roast", "Fine Blend",
    "Gold Roast", "Dark Roast", "Medium Roast", "Light Roast",
    "Triple Strength", "Extra Strength", "Mild Strength", "Bold Roast",
    "Crystal Clear", "Ultra Clear", "Filtered", "Microfiltered",
    "Probiotic", "Enriched", "Fortified", "Reinforced", "Boosted",
    "Energy Boost", "Protein Boost", "Super Boost", "Mega Boost",
    "Sports Edition", "Fitness Edition", "Active", "Endurance",
    "Hydration Edition", "Thermo Edition", "Cooling", "Warming",
    "Sweetened", "Lightly Sweetened", "Unsweetened Blend",
    "Salted", "Lightly Salted", "Seasoned", "Extra Seasoned",
    "No Seasoning", "Low Seasoning", "Balanced Flavor",
    "Flavored", "Unflavored", "Original Recipe", "New Recipe",
    "Improved Formula", "Max Formula", "Ultra Formula", "Complete",
    "Super Clean", "Eco-Friendly", "Plant-Based", "Earth Edition",
    "Regen Edition", "Green Pack", "Eco Pack", "Sustainable Edition",
    "Ocean Friendly", "Forest Edition", "Recycled Pack", "Nature Pack",
    "XL Crunch", "XXL", "Jumbo Size", "Mega Size", "Ultra Size"
]
# ===============================
# FONCTION ALLERGÈNES 0–3
# ===============================
def generate_allergens():
    real = [a for a in Allergens if a != "None"]

    k = random.choices(
        population=[0, 1, 2, 3],
        weights=[0.5, 0.30, 0.15, 0.05],
        k=1
    )[0]

    if k == 0:
        return "None"

    chosen = random.sample(real, k)
    return ", ".join(chosen)

import math

# ===============================
# PARAMÈTRES "BIG DATA"
# ===============================
TARGET_SIZE_GB = 1
TARGET_SIZE_BYTES = TARGET_SIZE_GB * 1024 * 1024 * 1024
OUTPUT_FILE = "allergens1g.csv"

# ===============================
# GÉNÉRATION ALÉATOIRE AVEC UNICITÉ
# ===============================
def generate_big_csv():
    print(f"Génération d'un CSV de ~{TARGET_SIZE_GB} Go…")
    print(f"Fichier : {OUTPUT_FILE}")

    # Supprime l'ancien fichier s'il existe
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    n_food = len(Food_product)
    n_pref = len(PREFIXES)
    n_suf  = len(SUFFIXES)
    total_combos = n_food * n_pref * n_suf

    print(f"Combinaisons possibles (Food × Prefix × Suffix) : {total_combos:,}")

    # Choix d'un coefficient 'a' coprime avec total_combos pour avoir une permutation
    a = random.randrange(1, total_combos)
    while math.gcd(a, total_combos) != 1:
        a = random.randrange(1, total_combos)

    # Décalage 'b' aléatoire
    b = random.randrange(0, total_combos)

    print(f"Paramètres de permutation : a={a}, b={b}")

    bytes_written = 0
    row_count = 0

    with open(OUTPUT_FILE, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow([
            "Food_product", "Main_ingredient", "Sweetener",
            "Fat/Oil", "Seasoning", "Allergens", "Prefix", "Suffix"
        ])
        bytes_written = f.tell()

        # On parcourt les combinaisons dans un ordre pseudo-aléatoire
        for step in range(total_combos):
            if bytes_written >= TARGET_SIZE_BYTES:
                print("Taille cible atteinte, arrêt de la génération.")
                break

            # Index aléatoire unique dans [0, total_combos)
            idx = (a * step + b) % total_combos

            # Décodage de idx en (i_food, i_pref, i_suf)
            per_food = n_pref * n_suf
            i_food = idx // per_food
            rem    = idx %  per_food
            i_pref = rem // n_suf
            i_suf  = rem %  n_suf

            food   = Food_product[i_food]
            prefix = PREFIXES[i_pref]
            suffix = SUFFIXES[i_suf]

            # Les autres champs restent tirés au hasard
            row = [
                food,
                random.choice(Main_ingredient),
                random.choice(Sweetener),
                random.choice(Fat_Oil),
                random.choice(Seasoning),
                generate_allergens(),
                prefix,
                suffix
            ]

            writer.writerow(row)
            row_count += 1
            bytes_written = f.tell()

            if row_count % 1_000_000 == 0:
                print(
                    f"{row_count:,} lignes écrites — "
                    f"{bytes_written / (1024*1024*1024):.2f} Go"
                )

        else:
            # On est arrivé à la fin de toutes les combinaisons uniques
            print("Toutes les combinaisons uniques ont été utilisées.")

    print("\nFichier généré avec succès !")
    print(f"Lignes écrites : {row_count:,}")
    print(f"Taille finale : {bytes_written/(1024*1024*1024):.2f} Go")

if __name__ == "__main__":
    generate_big_csv()
