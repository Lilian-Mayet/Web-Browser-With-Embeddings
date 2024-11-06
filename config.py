DATABASE_URL = "mysql+pymysql://root:@localhost/webbrowser"
EMBEDDINGS_MODEL = 'all-mpnet-base-v2'

# Define domain categories with their representative keywords and descriptions
DOMAIN_CATEGORIES = {
    # Technology & Computing
    "technology": {
        "keywords": [
            "programming", "software", "hardware", "AI", "artificial intelligence",
            "computer science", "coding", "tech news", "cybersecurity", "digital",
            "machine learning", "data science", "cloud computing", "blockchain","python"
            "java","C","C#"
        ],
        "description": "Technology, computing, and digital innovation"
    },
    "gaming": {
        "keywords": [
            "video games", "gaming", "esports", "game development", "console gaming",
            "PC gaming", "mobile games", "game reviews", "gaming community",
            "game streaming", "gaming hardware", "game design"
        ],
        "description": "Video games and gaming culture"
    },
    
    # Science & Academia
    "science": {
        "keywords": [
            "physics", "chemistry", "biology", "astronomy", "research",
            "scientific discovery", "laboratory", "experiment", "theory",
            "mathematics", "environmental science", "genetics"
        ],
        "description": "Scientific research and discoveries"
    },
    "academic": {
        "keywords": [
            "research papers", "academic journals", "scholarly articles", "thesis",
            "dissertation", "academic research", "peer review", "university research",
            "academic writing", "scientific methodology", "academic publishing"
        ],
        "description": "Academic and scholarly content"
    },
    
    # Food & Culinary
    "cooking": {
        "keywords": [
            "recipes", "cooking", "baking", "food", "cuisine", "ingredients",
            "kitchen", "culinary", "meal prep", "nutrition", "dishes",
            "cooking techniques", "gastronomy", "food culture"
        ],
        "description": "Food preparation and culinary arts"
    },
    "restaurants": {
        "keywords": [
            "restaurant reviews", "dining", "food service", "restaurants",
            "fine dining", "cafes", "food critics", "restaurant industry",
            "food service", "menu", "dining experience", "restaurant business"
        ],
        "description": "Restaurant and dining industry"
    },
    
    # Health & Wellness
    "health": {
        "keywords": [
            "medicine", "fitness", "wellness", "mental health", "nutrition",
            "exercise", "healthcare", "medical research", "diet",
            "healthy living", "psychology", "medical conditions"
        ],
        "description": "Health, medicine, and wellness"
    },
    "fitness": {
        "keywords": [
            "workout", "exercise", "fitness training", "gym", "strength training",
            "cardio", "personal training", "fitness goals", "sports training",
            "bodybuilding", "fitness equipment", "workout routines"
        ],
        "description": "Fitness and physical training"
    },
    "mental_health": {
        "keywords": [
            "psychology", "therapy", "mental wellness", "counseling", "self-care",
            "mental illness", "psychological health", "emotional wellbeing",
            "mental health support", "psychiatric care", "mental health resources"
        ],
        "description": "Mental health and psychological wellness"
    },
    
    # Politics & Society
    "politics": {
        "keywords": [
            "government", "politics", "policy", "elections", "democracy",
            "political news", "legislation", "international relations",
            "political analysis", "public policy", "political debate"
        ],
        "description": "Political news and analysis"
    },
    "social_issues": {
        "keywords": [
            "social justice", "activism", "human rights", "social movements",
            "equality", "social change", "community issues", "social awareness",
            "advocacy", "social reform", "civil rights", "social policy"
        ],
        "description": "Social issues and advocacy"
    },
    
    # Business & Finance
    "business": {
        "keywords": [
            "finance", "economics", "business news", "entrepreneurship",
            "marketing", "management", "investment", "startup",
            "business strategy", "corporate", "market analysis"
        ],
        "description": "Business and finance"
    },
    "cryptocurrency": {
        "keywords": [
            "bitcoin", "blockchain", "crypto", "cryptocurrency trading",
            "digital currency", "crypto markets", "crypto news", "defi",
            "cryptocurrency investment", "crypto technology", "mining"
        ],
        "description": "Cryptocurrency and blockchain technology"
    },
    "real_estate": {
        "keywords": [
            "property", "real estate market", "housing", "real estate investment",
            "property management", "real estate development", "real estate news",
            "property listings", "real estate industry", "property market"
        ],
        "description": "Real estate and property"
    },
    
    # Entertainment & Media
    "entertainment": {
        "keywords": [
            "movies", "music", "television", "celebrities", "entertainment news",
            "pop culture", "arts", "media", "shows", "streaming",
            "entertainment industry", "entertainment reviews"
        ],
        "description": "Entertainment and media"
    },
    "movies": {
        "keywords": [
            "film reviews", "cinema", "movie industry", "film production",
            "movie news", "film criticism", "movie releases", "film analysis",
            "movie recommendations", "film directors", "movie genres"
        ],
        "description": "Movies and film industry"
    },
    "music": {
        "keywords": [
            "music industry", "musicians", "music reviews", "concerts",
            "music production", "music news", "music genres", "music releases",
            "music analysis", "music artists", "music culture"
        ],
        "description": "Music and music industry"
    },
    
    # Sports & Recreation
    "sports": {
        "keywords": [
            "sports news", "athletics", "competitions", "games",
            "football", "basketball", "soccer", "baseball",
            "sports analysis", "championships", "athletes"
        ],
        "description": "Sports and athletics"
    },
    "outdoor_recreation": {
        "keywords": [
            "hiking", "camping", "outdoor activities", "adventure sports",
            "nature activities", "outdoor gear", "wilderness", "outdoor recreation",
            "outdoor adventures", "outdoor lifestyle", "outdoor sports"
        ],
        "description": "Outdoor activities and recreation"
    },
    
    # Education & Learning
    "education": {
        "keywords": [
            "learning", "teaching", "academic", "education", "school",
            "university", "training", "courses", "educational resources",
            "study materials", "pedagogy", "educational theory"
        ],
        "description": "Education and learning"
    },
    "online_learning": {
        "keywords": [
            "e-learning", "online courses", "distance learning", "online education",
            "virtual classroom", "online teaching", "digital learning",
            "educational technology", "online training", "remote learning"
        ],
        "description": "Online education and e-learning"
    },
    
    # Lifestyle & Personal
    "lifestyle": {
        "keywords": [
            "fashion", "beauty", "home", "travel", "relationships",
            "personal development", "lifestyle tips", "self-improvement",
            "hobbies", "life advice", "social life"
        ],
        "description": "Lifestyle and personal development"
    },
    "fashion": {
        "keywords": [
            "fashion trends", "style", "fashion industry", "clothing",
            "fashion design", "fashion news", "fashion brands", "accessories",
            "fashion advice", "fashion culture", "fashion retail"
        ],
        "description": "Fashion and style"
    },
    "travel": {
        "keywords": [
            "travel destinations", "tourism", "travel tips", "travel guides",
            "vacation", "travel industry", "travel news", "travel experiences",
            "travel planning", "travel advice", "international travel"
        ],
        "description": "Travel and tourism"
    },
    
    # Home & Living
    "home_improvement": {
        "keywords": [
            "DIY", "home renovation", "home repair", "home projects",
            "home maintenance", "construction", "home improvement tips",
            "renovation advice", "home upgrades", "house repairs"
        ],
        "description": "Home improvement and DIY"
    },
    "gardening": {
        "keywords": [
            "gardening tips", "plants", "landscaping", "garden maintenance",
            "horticulture", "garden design", "plant care", "gardening advice",
            "outdoor gardens", "indoor plants", "garden planning"
        ],
        "description": "Gardening and plant care"
    },
    
    # Science & Technology Specialties
    "artificial_intelligence": {
        "keywords": [
            "AI research", "machine learning", "deep learning", "neural networks",
            "AI applications", "AI technology", "AI development", "AI news",
            "artificial intelligence advances", "AI industry", "AI ethics"
        ],
        "description": "Artificial intelligence and machine learning"
    },
    "space": {
        "keywords": [
            "space exploration", "astronomy", "space science", "space technology",
            "space news", "space industry", "space research", "space missions",
            "space discoveries", "space agencies", "space travel"
        ],
        "description": "Space exploration and astronomy"
    },
    
    # Professional & Career
    "career": {
        "keywords": [
            "job search", "career development", "professional growth",
            "career advice", "job market", "employment", "career planning",
            "professional skills", "job hunting", "career change"
        ],
        "description": "Career development and professional growth"
    },
    "entrepreneurship": {
        "keywords": [
            "startup", "business creation", "entrepreneurial skills",
            "business founding", "startup culture", "business development",
            "entrepreneur resources", "startup advice", "business growth"
        ],
        "description": "Entrepreneurship and startups"
    },
        # Automotive & Mechanics
    "automotive": {
        "keywords": [
            "cars", "automobiles", "car reviews", "vehicle maintenance", 
            "car news", "driving tips", "auto repair", "car buying guides", 
            "vehicle technology", "car models"
        ],
        "description": "All about vehicles, car maintenance, and automotive news"
    },
    "mechanics": {
        "keywords": [
            "engineering mechanics", "mechanical systems", "machine repair", 
            "mechanical engineering", "tools", "DIY repair", "mechanical equipment", 
            "mechanical principles", "fixing machines"
        ],
        "description": "Mechanics, repairs, and the principles of mechanical systems"
    },

    # Shopping & E-commerce
    "ecommerce": {
        "keywords": [
            "online shopping", "ecommerce stores", "product listings", 
            "digital marketplace", "online retail", "customer reviews", 
            "discounts", "shipping", "product reviews", "shopping tips"
        ],
        "description": "Online shopping platforms and marketplaces"
    },
    "marketplace": {
        "keywords": [
            "buying and selling", "marketplace listings", "classifieds", 
            "auctions", "used items", "secondhand", "buying guides", 
            "local deals", "marketplaces", "community sales"
        ],
        "description": "Platforms for buying, selling, and trading goods"
    },

    # Arts & Crafts
    "crafts": {
        "keywords": [
            "handmade crafts", "DIY crafts", "craft projects", "knitting", 
            "crochet", "scrapbooking", "craft supplies", "craft ideas", 
            "craft tutorials", "craft shows"
        ],
        "description": "Handicrafts, DIY projects, and artistic hobbies"
    },
    "fine_art": {
        "keywords": [
            "painting", "sculpture", "art galleries", "art exhibitions", 
            "contemporary art", "art techniques", "art history", 
            "artistic expression", "art collections", "art studios"
        ],
        "description": "Fine arts, galleries, and artistic disciplines"
    },

    # Pets & Animal Care
    "pet_care": {
        "keywords": [
            "pet health", "dog training", "cat care", "animal grooming", 
            "pet food", "veterinary care", "animal behavior", "pet adoption", 
            "animal shelters", "pet supplies"
        ],
        "description": "Caring for pets and animals"
    },
    "wildlife": {
        "keywords": [
            "wild animals", "conservation", "animal habitats", 
            "endangered species", "wildlife photography", "animal tracking", 
            "wildlife preservation", "nature reserves", "species protection"
        ],
        "description": "Wildlife, conservation, and animal protection"
    },

    # Personal Finance
    "personal_finance": {
        "keywords": [
            "budgeting", "savings", "investing", "credit score", 
            "financial planning", "debt management", "retirement planning", 
            "personal loans", "financial independence", "money management"
        ],
        "description": "Managing personal finances and financial independence"
    },
    "insurance": {
        "keywords": [
            "insurance policies", "life insurance", "health insurance", 
            "auto insurance", "home insurance", "insurance claims", 
            "insurance premiums", "insurance advice", "risk management"
        ],
        "description": "Insurance services and financial protection"
    },

    # Hobbies & Interests
    "collectibles": {
        "keywords": [
            "collecting", "antiques", "memorabilia", "trading cards", 
            "coin collecting", "stamp collecting", "rare items", 
            "vintage collectibles", "collector community"
        ],
        "description": "Collectibles, antiques, and rare items"
    },
    "board_games": {
        "keywords": [
            "board game reviews", "strategy games", "tabletop games", 
            "game rules", "game night", "card games", "game strategies", 
            "board game recommendations", "puzzles"
        ],
        "description": "Board games, tabletop games, and game strategies"
    },

    # Science & Environment
    "climate_change": {
        "keywords": [
            "global warming", "carbon emissions", "environmental policy", 
            "sustainability", "renewable energy", "climate science", 
            "carbon footprint", "climate action", "green technology"
        ],
        "description": "Climate change science, policies, and solutions"
    },
    "renewable_energy": {
        "keywords": [
            "solar power", "wind energy", "geothermal", "hydropower", 
            "energy efficiency", "renewable energy news", "clean energy", 
            "sustainable energy", "bioenergy", "green technology"
        ],
        "description": "Renewable energy sources and technology"
    },

    # Lifestyle & Home Management
    "interior_design": {
        "keywords": [
            "home decor", "furniture", "interior decorating", "design trends", 
            "home aesthetics", "space planning", "color schemes", 
            "interior styling", "furniture placement", "home improvement"
        ],
        "description": "Interior design and home decoration"
    },
    "organizing": {
        "keywords": [
            "home organization", "decluttering", "time management", 
            "productivity tips", "organizing tips", "minimalism", 
            "space-saving ideas", "efficient storage", "lifestyle hacks"
        ],
        "description": "Organizing, decluttering, and time management"
    },

    # Digital & Cybersecurity
    "cybersecurity": {
        "keywords": [
            "network security", "data privacy", "online safety", 
            "cyber threats", "hacking prevention", "data protection", 
            "encryption", "cyber attacks", "security protocols", 
            "digital security"
        ],
        "description": "Online safety, data privacy, and cybersecurity"
    },
    "software_development": {
        "keywords": [
            "coding languages", "software engineering", "development tools", 
            "API development", "coding tutorials", "software frameworks", 
            "programming tips", "software updates", "developer community"
        ],
        "description": "Software development and engineering"
    },

    # Culture & Heritage
    "history": {
        "keywords": [
            "historical events", "historical figures", "ancient history", 
            "world history", "historical analysis", "archaeology", 
            "heritage sites", "historical documentaries", "cultural heritage", 
            "artifacts"
        ],
        "description": "History and cultural heritage"
    },
    "philosophy": {
        "keywords": [
            "philosophical ideas", "moral philosophy", "ethics", 
            "existentialism", "philosophers", "critical thinking", 
            "logic", "human nature", "philosophical discussions", "philosophy books"
        ],
        "description": "Philosophy, ethics, and human thought"
    },

    # Events
    "event": {
        "keywords": [
            "event planning", "event organization", "event venues", 
            "corporate events", "celebrations", "festivals", 
            "public events", "social gatherings", "event coordination", 
            "event logistics"
        ],
        "description": "Event planning, organization, and coordination"
    },

    # Parenting & Family
    "parenting": {
        "keywords": [
            "parenting tips", "childcare", "parenting advice", "new parents", 
            "child development", "family activities", "parenting support", 
            "parenting resources", "family dynamics", "parenting styles"
        ],
        "description": "Parenting advice and family support"
    }
}

DOMAIN_TRESHOLD= 0.26

SEED_URLS = [

]