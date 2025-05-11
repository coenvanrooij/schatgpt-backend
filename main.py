from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from pydantic import BaseModel

app = FastAPI()

# CORS instellingen zodat frontend mag communiceren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Laad je OpenAI API-sleutel uit omgevingsvariabelen
openai.api_key = os.getenv("OPENAI_API_KEY")

class TekstVerzoek(BaseModel):
    tekst: str
    toon: str

@app.post("/verfijn")
async def verfijn_tekst(verzoek: TekstVerzoek):
    prompt = f"Herschrijf de volgende tekst op een {verzoek.toon} toon, zonder de betekenis te veranderen:\n\n{verzoek.tekst}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Je bent een empathische tekstredacteur die menselijke gevoelens helpt verwoorden."},
                {"role": "user", "content": prompt}
            ]
        )
        resultaat = response.choices[0].message.content.strip()
        return {"origineel": verzoek.tekst, "verfijnd": resultaat}
    except Exception as e:
        return {"fout": str(e)}