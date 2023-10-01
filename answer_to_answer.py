from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

def data_to_text(question, table):

    result_list = []
    for row in table:
        result_list.append(row[0])
    
    data = ", ".join(result_list)

    input_text = f"Rewrite the answer '{data}' to create a detailed response to the question '{question}?'"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids)
    
    return tokenizer.decode(outputs[0])
