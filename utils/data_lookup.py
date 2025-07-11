import pandas as pd

# Load dataset
df = pd.read_csv("data/diabetes_with_wearables.csv")

def search_relevant_facts(user_query: str, top_k: int = 3) -> str:
    """
    Very simple keyword-based search from the wearable dataset.
    Matches user's query with column names or values.
    """
    relevant_rows = []

    # Go row by row and check if any cell contains a keyword from the query
    for _, row in df.iterrows():
        for col in df.columns:
            if str(row[col]).lower() in user_query.lower():
                relevant_rows.append(row)
                break
        if len(relevant_rows) >= top_k:
            break

    if not relevant_rows:
        return "No direct match found in dataset."
    
    summary = ""
    for i, row in enumerate(relevant_rows, 1):
        summary += f"\n{i}. Age: {row.get('age', 'N/A')}, Steps: {row.get('steps', 'N/A')}, Sleep: {row.get('sleep_hours', 'N/A')}, Glucose: {row.get('glucose', 'N/A')}"
    
    return summary.strip()
