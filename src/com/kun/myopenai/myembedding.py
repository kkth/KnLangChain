from openai import OpenAI
import pandas as pd


if __name__ == "__main__":
    #Define the text for which you want to generate embeddings
    text = [
        "Once upon a time, there was a little girl who lived in a village.",
        "She was very happy and loved to play with her friends."
    ]

    client = OpenAI()
    df = pd.read_csv('output/embedded_1k_reviews.csv')
    df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)

    def get_embedding(text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input = [text], model=model).data[0].embedding

    df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-3-small'))
    df.to_csv('output/embedded_1k_reviews.csv', index=False)