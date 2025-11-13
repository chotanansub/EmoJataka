"""Generate NER (Named Entity Recognition) related CSV files."""

import pandas as pd
import random
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import NUM_STORIES, ENTITY_TYPES, OUTPUT_DIR

# Sample Thai entity names
SAMPLE_ENTITIES = {
    "PERSON": ["พระพุทธเจ้า", "พระอานนท์", "พระสารีบุตร", "พระโมคคัลลานะ", "พระมหากัสสปะ"],
    "LOCATION": ["เมืองราชคฤห์", "เมืองสาวัตถี", "เมืองกบิลพัสดุ์", "เมืองเวสาลี", "เมืองปาตลีบุตร"],
    "ORGANIZATION": ["วัด", "อาราม", "สำนัก", "คณะ"],
    "ANIMAL": ["ช้าง", "ม้า", "นก", "เสือ", "กวาง"],
    "OBJECT": ["บาตร", "จีวร", "ไม้เท้า", "ร่ม", "ตะเกียง"]
}

def generate_ner_entities():
    """Generate ner_entities.csv with named entities found in text."""
    print("Generating ner_entities.csv...")
    
    data = []
    for chapter in range(1, NUM_STORIES + 1):
        # Randomly assign some entities to each chapter
        for entity_type in ENTITY_TYPES:
            num_entities = random.randint(0, 3)
            entities = random.sample(
                SAMPLE_ENTITIES.get(entity_type, ["entity"]),
                min(num_entities, len(SAMPLE_ENTITIES.get(entity_type, ["entity"])))
            )
            
            for entity in entities:
                data.append({
                    'chapter': chapter,
                    'entity': entity,
                    'entity_type': entity_type,
                    'count': random.randint(1, 5)
                })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "ner_entities.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_ner_by_chapter():
    """Generate ner_by_chapter.csv with NER counts per chapter."""
    print(f"Generating ner_by_chapter.csv for {NUM_STORIES} chapters...")
    
    data = []
    for chapter in range(1, NUM_STORIES + 1):
        for entity_type in ENTITY_TYPES:
            data.append({
                'chapter': chapter,
                'entity_type': entity_type,
                'count': random.randint(0, 10)
            })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "ner_by_chapter.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_ner_counts():
    """Generate ner_counts.csv with overall NER entity type counts."""
    print("Generating ner_counts.csv...")
    
    data = []
    for entity_type in ENTITY_TYPES:
        data.append({
            'entity_type': entity_type,
            'count': random.randint(50, 200),
            'percentage': round(random.uniform(10.0, 30.0), 2)
        })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "ner_counts.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

if __name__ == "__main__":
    generate_ner_entities()
    generate_ner_by_chapter()
    generate_ner_counts()

