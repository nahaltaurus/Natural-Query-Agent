import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


with open('lectures0.json', 'r') as f:
    lecture_notes = json.load(f)


with open('mp.json', 'r') as f:
    model_architectures = json.load(f)


lecture_contents = {item['Title']: item['Content'] for item in lecture_notes}


augmented_data = {
    "Milestone Model Architectures": "Some of the milestone model architectures and papers in the last few years include the Transformer model (Vaswani et al., 2017), BERT (Devlin et al., 2018), GPT-3 (Brown et al., 2020), and PaLM (Chowdhery et al., 2022). The Transformer introduced the self-attention mechanism and became the foundation for many modern language models. BERT revolutionized pre-training for natural language tasks, while GPT-3 demonstrated the capabilities of large language models. PaLM is a recent milestone, being one of the largest and most capable language models to date.",
    **lecture_contents
}


model_architectures_df = pd.DataFrame(model_architectures)
model_architectures_dict = model_architectures_df.to_dict(orient='list')
model_architectures_json = json.dumps(model_architectures_dict)


all_data = {**augmented_data, "model_architectures": model_architectures_json}

def generate_embeddings(text, model):
    return model.encode(text, convert_to_tensor=True).tolist()

def create_vector_store(data, embedding_model):
    client = chromadb.Client(Settings(persist_directory="./chroma_db"))
    collection = client.create_collection("lecture_notes")
    
    for key, value in data.items():
        if key == "model_architectures":
            # Handle the JSON data differently
            embeddings = generate_embeddings(value, embedding_model)
            collection.add(
                documents=[value],
                metadatas=[{"source": key}],
                ids=[key],
                embeddings=[embeddings]
            )
        else:
      
            chunks = [value[i:i+1000] for i in range(0, len(value), 1000)]
            for i, chunk in enumerate(chunks):
                embeddings = generate_embeddings(chunk, embedding_model)
                collection.add(
                    documents=[chunk],
                    metadatas=[{"source": key}],
                    ids=[f"{key}_{i}"],
                    embeddings=[embeddings]
                )
    
    return collection


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


vector_store = create_vector_store(all_data, embedding_model)

def process_query(query, collection, embedding_model, top_k=20):
    query_embedding = generate_embeddings(query, embedding_model)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    return results


tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")


conversation_history = []

def generate_answer(query, context, conversation_history):

    input_text = f"Answer the following question about large language models, based on the given context. If the context doesn't contain enough relevant information, say that the context is insufficient. Cite the relevant sections from the context used to construct the answer.\n\nConversation History: {' '.join(conversation_history)}\n\nQuestion: {query}\n\nContext: {context}\n\nAnswer:"
    

    input_ids = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).input_ids
    outputs = model.generate(
        input_ids,
        max_length=1000,  # Increase max_length for longer outputs
        num_return_sequences=1,
        do_sample=True,  # Enable sampling
        temperature=0.7,  # Adjust temperature for output diversity
        top_k=100,  # Consider top 100 tokens
        top_p=0.95,  # Nucleus sampling
        no_repeat_ngram_size=3  # Avoid repeating 3-grams
    )
    
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer

def generate_summary(conversation_history):

    conversation_text = ' '.join(conversation_history)
    

    input_text = f"Generate a summary of the following conversation:\n\n{conversation_text}\n\nSummary:"
    

    input_ids = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).input_ids
    outputs = model.generate(
        input_ids,
        max_length=500,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        no_repeat_ngram_size=2
    )
    
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return summary

def main():
    print("Welcome to the LLM Query Agent!")
    print("Ask questions about LLMs, lecture notes, or model architectures.")
    print("Type 'exit' to quit.")
    print("Type 'summary' to generate a summary of the conversation.")
    
    while True:
        query = input("\nEnter your question: ")
        
        if query.lower() == 'exit':
            print("Thank you for using the LLM Query Agent. Goodbye!")
            break
        elif query.lower() == 'summary':
            summary = generate_summary(conversation_history)
            print("\nConversation Summary:\n", summary)
            continue
        

        results = process_query(query, vector_store, embedding_model)
        

        context = "\n".join([doc for doc in results['documents'][0]])
        

        answer = generate_answer(query, context, conversation_history)
        print("\nAnswer:", answer)

        conversation_history.append(query)
        conversation_history.append(answer)

if __name__ == "__main__":
    main()
