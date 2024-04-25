from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List

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

class Message(BaseModel):
  role: str
  content: str
class QuestionRequest(BaseModel):
  model: str
  messages: List[Message]
  stream: bool = False
@app.post("/api/chat")
async def ask_question(request: QuestionRequest):
    messages = request.messages

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    start_time = datetime.now()

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=2048
    )



    end_time = datetime.now()
    duration = end_time - start_time
    total_duration = duration.total_seconds() * 1000000000  # 转换为纳秒

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response_content = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return {
        "model": request.model,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "message": {
            "role": "assistant",
            "content": response_content
        },
        "done": True,
        "total_duration": int(total_duration),
        "load_duration": 0,
        "prompt_eval_count": 0, 
        "prompt_eval_duration": 0,
        "eval_count": 0,
        "eval_duration": 0
    }

if __name__ == "__main__":
    import uvicorn
    port = 7860
    print("Server started.port:",port)
    uvicorn.run(app, host="0.0.0.0", port=port)
