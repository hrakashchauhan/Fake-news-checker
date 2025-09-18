# prepare_data.py
import pandas as pd

print("Starting the process to create 'test_data.csv'...")

# --- File Paths ---
# This script assumes the data files are in the same directory.
KAGGLE_REAL_PATH = 'True.csv'
KAGGLE_FAKE_PATH = 'Fake.csv'
LIAR_TEST_PATH = 'test1.csv' # Using the test set as planned
NUM_SAMPLES = 25
OUTPUT_FILENAME = 'test_data.csv'

try:
    # --- Part 1: Process the KAGGLE Dataset ---
    print(f"Reading and sampling from '{KAGGLE_REAL_PATH}' and '{KAGGLE_FAKE_PATH}'...")
    
    df_real = pd.read_csv(KAGGLE_REAL_PATH)
    df_fake = pd.read_csv(KAGGLE_FAKE_PATH)

    real_samples = df_real.sample(n=NUM_SAMPLES, random_state=42)
    fake_samples = df_fake.sample(n=NUM_SAMPLES, random_state=42)

    real_samples['label'] = 'real'
    fake_samples['label'] = 'fake'
    
    df_kaggle_combined = pd.concat([real_samples, fake_samples])
    df_kaggle_combined['source'] = 'kaggle'
    
    df_kaggle_final = df_kaggle_combined[['text', 'label', 'source']]
    print(f"Successfully sampled {len(df_kaggle_final)} articles from KAGGLE.")

    # --- Part 2: Process the LIAR Dataset ---
    print(f"Reading and sampling from '{LIAR_TEST_PATH}'...")

    df_liar = pd.read_csv(LIAR_TEST_PATH)
    
    # Map the detailed LIAR labels to our simple 'real'/'fake' system
    label_map = {
        'true': 'real',
        'mostly-true': 'real',
        'half-true': None,  # Ignore ambiguous labels
        'barely-true': None,
        'false': 'fake',
        'pants-fire': 'fake'
    }

    # Check if labels are text or numbers (e.g., 1 for true, 0 for false)
    if df_liar['label'].dtype in ['int64', 'float64']:
        # This mapping might need adjustment if the integer labels are different
        print("Integer labels detected in LIAR dataset. Assuming 1=real, 0=fake.")
        label_map_int = {1: 'real', 0: 'fake'} 
        df_liar['label_mapped'] = df_liar['label'].map(label_map_int)
    else:
        df_liar['label_mapped'] = df_liar['label'].map(label_map)

    df_liar.dropna(subset=['label_mapped'], inplace=True)
    df_liar['label'] = df_liar['label_mapped']

    # Sample the data
    liar_real_samples = df_liar[df_liar['label'] == 'real'].sample(n=NUM_SAMPLES, random_state=42)
    liar_fake_samples = df_liar[df_liar['label'] == 'fake'].sample(n=NUM_SAMPLES, random_state=42)
    
    df_liar_combined = pd.concat([liar_real_samples, liar_fake_samples])
    df_liar_combined['source'] = 'liar'
    
    df_liar_combined.rename(columns={'statement': 'text'}, inplace=True)
    
    df_liar_final = df_liar_combined[['text', 'label', 'source']]
    print(f"Successfully sampled {len(df_liar_final)} statements from LIAR.")

    # --- Part 3: Combine and Save the Final Dataset ---
    print("Combining all samples...")
    
    final_df = pd.concat([df_kaggle_final, df_liar_final], ignore_index=True)
    
    # Shuffle the dataset randomly
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    final_df.to_csv(OUTPUT_FILENAME, index=False)
    
    print("\n--- PROCESS COMPLETE ---")
    print(f"Successfully created the balanced test file: '{OUTPUT_FILENAME}'")
    print(f"Total samples: {len(final_df)}")
    print("Final distribution of labels:")
    print(final_df['label'].value_counts())

except FileNotFoundError as e:
    print(f"\n--- ERROR ---")
    print(f"A required file was not found: '{e.filename}'.")
    print("Please make sure your data files are in the same directory as this script.")
except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"An unexpected error occurred: {e}")
    print("There might be an issue with a file's format or column names.")