def build_prompt(user_input, matched_rows=None):
    advice_intro = (
        "You are HealthMate, a friendly health advisor. Based on the user's input and data, "
        "generate a personalized, easy-to-understand health tip in a short paragraph.\n\n"
    )
    example = f"User says: '{user_input}'\n"

    context = ""
    if matched_rows is not None and hasattr(matched_rows, "empty") and not matched_rows.empty:
        for _, row in matched_rows.iterrows():
            age = row.get('age', 'unknown')
            steps = row.get('steps', 'unknown')
            sleep = row.get('sleep_hours', 'unknown')
            glucose = row.get('glucose', 'unknown')
            context += f"User Profile → Age: {age}, Steps: {steps}, Sleep: {sleep}, Glucose: {glucose}\n"

    final_prompt = advice_intro + context + example + "Advice:"
    return final_prompt