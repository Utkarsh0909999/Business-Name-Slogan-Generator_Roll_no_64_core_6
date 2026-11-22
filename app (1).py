import os
import json
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
# Tries these in order if one is unavailable
MODELS = ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]

PROMPT = """You are a creative branding expert for startups.
Business idea: {idea}
Target audience: {audience}
Brand style: {style}

Return ONLY valid JSON (no markdown, no extra text) in this exact format:
{{
  "names": [{{"name": "...", "slogan": "..."}}],
  "pitch": ["line 1", "line 2", "line 3"]
}}
Rules:
- Exactly 10 unique, short, easy-to-pronounce business names, each with a catchy slogan under 8 words.
- The names and slogans must match the brand style: {style}.
- The pitch must be exactly 3 short lines for the business idea."""


def generate(idea, audience, style):
    client = Groq(api_key=API_KEY, timeout=30)
    prompt = PROMPT.format(idea=idea, audience=audience, style=style)
    last_error = None
    for model in MODELS:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=1.0,
            )
            text = resp.choices[0].message.content.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            last_error = e
    raise last_error


st.set_page_config(page_title="Business Name & Slogan Generator", page_icon="💡")
st.title("💡 Business Name & Slogan Generator")
st.caption("Enter your startup idea and get names, slogans and a 3-line pitch.")

if not API_KEY:
    st.error("GROQ_API_KEY not found. Add it to a .env file (see README).")
    st.stop()

with st.form("inputs"):
    idea = st.text_area("Business idea", placeholder="e.g. Eco-friendly cloth bags made by rural women")
    audience = st.text_input("Target audience", placeholder="e.g. college students and young professionals")
    style = st.selectbox("Style", ["Modern", "Playful", "Premium", "Traditional", "Techy", "Minimal"])
    submitted = st.form_submit_button("Generate")

if submitted:
    if not idea.strip() or not audience.strip():
        st.warning("Please fill in both the idea and the audience.")
    else:
        with st.spinner("Brainstorming..."):
            try:
                st.session_state["result"] = generate(idea, audience, style)
                for k in [k for k in st.session_state if k.startswith("fav_")]:
                    del st.session_state[k]
            except Exception as e:
                st.error(f"Could not generate (try again): {e}")

result = st.session_state.get("result")
if result:
    st.subheader("Names & Slogans")
    for i, item in enumerate(result["names"]):
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"**{item['name']}** — _{item['slogan']}_")
        c2.checkbox("⭐ Fav", key=f"fav_{i}")

    st.subheader("3-line Pitch")
    for line in result["pitch"]:
        st.write("• " + line)

    favs = [r for i, r in enumerate(result["names"]) if st.session_state.get(f"fav_{i}")]
    st.sidebar.header("⭐ My Favourites")
    if favs:
        txt = "\n".join(f"{f['name']} - {f['slogan']}" for f in favs)
        for f in favs:
            st.sidebar.markdown(f"**{f['name']}**  \n_{f['slogan']}_")
        st.sidebar.download_button("Download favourites", txt, "favourites.txt")
    else:
        st.sidebar.info("Tick ⭐ Fav on any option to save it here.")
