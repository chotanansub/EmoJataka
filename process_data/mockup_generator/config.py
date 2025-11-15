"""Configuration for mockup data generation."""

# Number of stories/chapters to generate
NUM_STORIES = 10

# Number of clusters for K-means
NUM_CLUSTERS = 3

# 8 basic emotions from NRC lexicon
EMOTIONS = [
    "trust",
    "joy",
    "anger",
    "anticipation",
    "fear",
    "disgust",
    "surprise",
    "sadness"
]

# Output directory for mockup data (relative to project root)
OUTPUT_DIR = "../../data/mockup"

# Thai sample words for generating text (simplified)
THAI_SAMPLE_WORDS = [
    "พระ", "เจ้า", "เมือง", "คน", "สัตว์", "ต้นไม้", "น้ำ", "ไฟ",
    "ทอง", "เงิน", "อาหาร", "บ้าน", "วัด", "ป่า", "ภูเขา", "แม่น้ำ",
    "ดวงอาทิตย์", "ดวงจันทร์", "ดาว", "เมฆ", "ฝน", "ลม", "ดิน", "หิน"
]

# Sample Thai story titles
STORY_TITLES = [
    "พระเวสสันดร",
    "พระมหาชนก",
    "พระเตมีย์",
    "พระสุวรรณสาม",
    "พระเนมิราช",
    "พระมโหสถ",
    "พระภูริทัต",
    "พระจันทกุมาร",
    "พระนารท",
    "พระวิธูรบัณฑิต"
]

# POS tags (common Thai POS tags)
POS_TAGS = [
    "N", "V", "ADJ", "ADV", "PRON", "PREP", "CONJ", "DET", "NUM", "PUNCT"
]

# Entity types for NER
ENTITY_TYPES = [
    "PERSON",
    "LOCATION",
    "ORGANIZATION",
    "ANIMAL",
    "OBJECT"
]

