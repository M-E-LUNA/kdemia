import os
import django
import json
import ssl
import urllib.request

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

api_key = getattr(settings, 'GEMINI_API_KEY', '').strip()
print(f"\n1. Probando clave que termina en: ...{api_key[-6:]}")

# Hacemos una pregunta real directa
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [
        {
            "parts": [{"text": "Di únicamente: Hola, Tuzy está funcionando correctamente."}]
        }
    ]
}

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)

print("2. Enviando pregunta de prueba a Google Gemini...\n")

try:
    with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
        result = json.loads(response.read().decode('utf-8'))
        reply = result['candidates'][0]['content']['parts'][0]['text']
        print("✅ ¡ÉXITO TOTAL!")
        print("Respuesta de Gemini:", reply)
except urllib.error.HTTPError as he:
    print(f"❌ ERROR HTTP DE GOOGLE ({he.code}):")
    print(he.read().decode('utf-8'))
except Exception as e:
    print("❌ ERROR GENERAL:", e)