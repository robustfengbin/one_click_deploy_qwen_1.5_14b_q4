from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer


app = FastAPI()
print("app started")

device = "cuda"  # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen1.5-14B-Chat-GPTQ-Int4",
    torch_dtype="auto",
    device_map="auto"
)
print("model loaded")

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-14B-Chat-GPTQ-Int4")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    prompt = request.question
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=1024
    )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    port = 7860
    print("Server started.port:",port)
    uvicorn.run(app, host="0.0.0.0", port=port)