# evaluate.py (V3 - Final Version)
import pandas as pd
import time
from detector import analyze_article # Imports your V3 function from detector.py

# --- Configuration ---
INPUT_CSV = 'test_data.csv'
OUTPUT_CSV = 'evaluation_results_V3.csv' # Using a new name for the output file

def evaluate_dataset():
    """
    Reads the test dataset, runs each article through the V3 detector,
    calculates the overall accuracy, and saves the detailed forensic analysis.
    """
    try:
        # Ensure pandas is installed: pip install pandas
        df = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_CSV}' not found. Make sure it's in the same directory.")
        return

    results = []
    correct_predictions = 0
    total_predictions = 0

    print(f"--- Starting V3 Cognitive Forensic Evaluation ---")
    print(f"Analyzing {len(df)} articles from '{INPUT_CSV}'...")
    print("This may take several minutes due to the advanced, multi-step analysis.")

    # Loop through each row in the dataframe
    for index, row in df.iterrows():
        text = row['text']
        true_label = row['label']
        
        # Skip empty rows that might exist in the data
        if not isinstance(text, str) or not text.strip():
            print(f"Skipping empty article at row {index + 1}.")
            continue
            
        print(f"Analyzing article {index + 1}/{len(df)}...")

        # Get the detailed analysis from your V3 detector
        analysis = analyze_article(text)
        
        predicted_verdict = "ANALYSIS_FAILED"
        is_correct = False
        
        # Check for errors from the API call or JSON parsing
        if 'error' not in analysis and 'verdict' in analysis:
            predicted_verdict = analysis.get('verdict', 'NO_VERDICT').lower()
            true_label = true_label.lower()
            
            # Compare the prediction to the true label
            if predicted_verdict == true_label:
                correct_predictions += 1
                is_correct = True
                print(f"  -> Correct! (Predicted: {predicted_verdict}, Actual: {true_label})")
            else:
                print(f"  -> Incorrect. (Predicted: {predicted_verdict}, Actual: {true_label})")
        else:
             print(f"  -> API or Formatting Error: {analysis.get('error', 'Unknown Error')}")

        total_predictions += 1
        
        # Prepare the data for the results CSV, including the new detailed analysis
        result_data = {
            'text': text,
            'true_label': true_label,
            'predicted_verdict': predicted_verdict,
            'is_correct': is_correct,
            'confidence': analysis.get('confidence_score'),
            'reason': analysis.get('reason'),
        }
        
        # Safely add the nested analysis data if it exists
        if 'analysis_summary' in analysis and isinstance(analysis['analysis_summary'], dict):
            summary = analysis['analysis_summary']
            result_data['psychological_intent'] = summary.get('psychological_intent')
            result_data['logical_fallacies'] = summary.get('logical_fallacies')
            result_data['evidence_quality'] = summary.get('evidence_quality')

        results.append(result_data)
        
        # Respect the API rate limit. 1.1 seconds is a safe interval.
        time.sleep(1.1)

    # --- Calculate and Print Final Accuracy ---
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    
    print("\n--- V3 EVALUATION COMPLETE ---")
    print(f"Total Articles Analyzed: {total_predictions}")
    print(f"Correct Predictions:     {correct_predictions}")
    print(f"Final Accuracy:          {accuracy:.2f}%")
    
    # Save the comprehensive results to the new CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nDetailed forensic results have been saved to '{OUTPUT_CSV}'.")
    print("This file now contains the full breakdown of the AI's reasoning for each article.")


if __name__ == "__main__":
    evaluate_dataset()