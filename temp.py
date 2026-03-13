import google.generativeai as genai
genai.configure(api_key="AIzaSyAa_TABH1kvGEcYpBVQZS-6OGZ6RS1UriM")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)