def build_prompt(user_input, matched_rows=None):
    """
    Constructs a highly structured prompt for TinyLLaMA.
    Uses explicit delimiters to separate System Instructions, Contextual Data, and the User's Query.
    """

    # 1. Define the System Instruction (Persona and Goal)
    system_instruction = (
        "You are HealthMate, a friendly, concise, and professional health advisor. "
        "Your task is to provide personalized, actionable health advice.\n"
        "STRICTLY follow these rules:\n"
        "1. Base your advice PRIMARILY on the CONTEXTUAL DATA provided below and the user's input.\n"
        "2. Do not use conversational fillers like 'Absolutely!', 'Sure, I can help with that!', or 'I appreciate it.'\n"
        "3. **OUTPUT ONLY THE ASSISTANT'S REPLY.** Do not generate text for 'USER:', 'ASSISTANT:', or any follow-up dialogue.\n"
        "4. Answer DIRECTLY in 2-4 sentences only.\n"
    )

    # 2. Format the Contextual Data block clearly
    context_data = ""
    if matched_rows is not None and hasattr(matched_rows, "empty") and not matched_rows.empty:
        context_data += "\n--- CONTEXTUAL DATA FROM HEALTH RECORDS ---\n"
        
        # Aggregate the data into a readable format for the LLM
        for _, row in matched_rows.iterrows():
            age = row.get('age', 'N/A')
            steps = row.get('steps', 'N/A')
            sleep = row.get('sleep_hours', 'N/A')
            glucose = row.get('glucose', 'N/A')
            
            # Use specific facts from the matched row to enrich the context
            context_data += f"| Match Profile -> Age: {age}, Daily Steps: {steps}, Sleep Hrs: {sleep}, Glucose: {glucose} |\n"
        
        context_data += "-------------------------------------------\n"
    else:
        context_data += "\n[No specific EHR or wearable data matches found for context.]\n"

    # 3. Combine the components using TinyLlama's preferred chat format (or a similar rigid structure)
    # The structure below is highly effective for enforcing instructions in small models.

    final_prompt = (
        f"{system_instruction}"
        f"{context_data}\n"
        f"USER: {user_input}\n"
        f"ASSISTANT: " # The assistant prefix tells the model where to begin generating
    )

    return final_prompt
