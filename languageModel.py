from transformers import AutoTokenizer, AutoModelForCausalLM
from databaseFunctions import *
model = AutoModelForCausalLM.from_pretrained("./models")
tokenizer = AutoTokenizer.from_pretrained("./models")

input_text = ""

def generate_response(text):
    global input_text
    input_text += f"User: {text}{tokenizer.eos_token}Bot:"
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    
    outputs = model.generate(
        inputs,
        max_length=1024,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        temperature=0.7
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("Bot:")[-1]

def message(user_input, id):
    global input_text
    if getContext(id) == None:
        input_text = f"Your name is Epithet.{tokenizer.eos_token}"
        pushContext(input_text, id)
    else:
        input_text = getContext(id)['inputText']

    try:
        response = generate_response(user_input)
        input_text = input_text + f'{response}{tokenizer.eos_token}'
        split_parts = [part.strip() for part in input_text.split("<|endoftext|>") if part.strip()]
        result = []
        if split_parts:
            result.append(f"{split_parts[0]}<|endoftext|>")
            for i in range(1, len(split_parts), 2):
                if i + 1 >= len(split_parts):
                    break
                user_message = split_parts[i]
                bot_response = split_parts[i+1]
                combined = f"{user_message}<|endoftext|>{bot_response}<|endoftext|>"
                result.append(combined)
        if(len(result) > 4):
            p1 = result[0]
            p2 = result[-4:]
            result = [p1] + p2
        input_text = "".join(result)
        updateContext(input_text, id)
        return response
    except Exception as e:
        print(f"Error: {e}")