import os, json, re
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

df = pd.read_csv("Recalculated_Aquaculture_Water_Suitability_Signals_WQI_Derived.csv")

FEATURES = ["Temperature","Turbidity (cm)","Dissolved Oxygen (mg L-1)","Biochemical Oxygen Demand (mg L-1)","Carbon Dioxide (mg L-1)","pH","Total Alkalinity (mg L-1 as CaCO3)","Total Hardness (mg L-1 as CaCO3)","Calcium (mg L-1)","Estimated Magnesium (mg L-1)","Ammonia (mg L-1)","Nitrite (mg L-1)","Phosphorus (mg L-1)","Hydrogen Sulphide (mg L-1)","Plankton Abundance (No. L-1)"]

def get_similar_cases(params, n=3):
    distances = df[FEATURES].apply(lambda row: ((row - pd.Series(params)) ** 2).sum() ** 0.5, axis=1)
    closest = df.loc[distances.nsmallest(n).index]
    return "\n".join("  - WQI: " + str(round(r["Water Quality Index (WQI)"],2)) + ", Label: " + str(r["WQI-Derived Aquaculture Suitability Classification"]) for _, r in closest.iterrows())

def predict_water_quality(params):
    prompt = ("You are a water quality expert.\n\nSimilar cases:\n" + get_similar_cases(params) +
        "\n\nClassify into ONE of: Highly Suitable, Suitable, Restricted / Stressed, Unsuitable / Critical\n\nParameters:\n" +
        "\n".join("  - " + k + ": " + str(v) for k, v in params.items()) +
        '\n\nReply ONLY with JSON: {"classification":"<class>","confidence":"<High/Medium/Low>","reason":"<one sentence>","probabilities":{"Highly Suitable":0,"Suitable":0,"Restricted / Stressed":0,"Unsuitable / Critical":0}}')
    response = client.chat.completions.create(
        model=x,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1024,
        extra_body={"chat_template_kwargs": {"enable_thinking": True}, "reasoning_budget": 1024}
    )
    raw = re.sub(r"```json|```", "", response.choices[0].message.content.strip()).strip()
    return json.loads(raw)
