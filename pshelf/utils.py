from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def generate_case_study(project):
    prompt = (
        f"Write a detailed case study about the project named '{project.project_name}', "
        f"created by {project.name} on {project.project_date}. "
        f"Description: {project.project_description}. "
        f"Technologies used: {project.project_technologies}. "
        f"Outcomes: {project.project_outcomes}."
    )
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(
        inputs,
        max_length=300,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        temperature=0.7,
    )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text
