from openai import AzureOpenAI

class AOAI:
    def __init__(self, endpoint, api_key, api_version, chat_deployment, embedding_deployment):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.chat_deployment = chat_deployment
        self.embedding_deployment = embedding_deployment

    def embed(self, texts):
        # texts can be list[str]
        res = self.client.embeddings.create(
            model=self.embedding_deployment,
            input=texts
        )
        return [d.embedding for d in res.data]

    def chat(self, system_prompt: str, user_prompt: str):
        res = self.client.chat.completions.create(
            model=self.chat_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2
        )
        return res.choices[0].message.content
