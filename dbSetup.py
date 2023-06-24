
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred_obj = {
  "type": "service_account",
  "project_id": "zombichase-e04ac",
  "private_key_id": "cdf9642f67677621dbdd5f1910f682c2e45ab6e5",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC/fNT1T3QCeF1Q\nSfBwZiwkkCF7+y546TP5HI636KGEyEzkM24bNEV8VDDq+fjawxlNgQIrvSPRO1gF\n286lgPfhtji6hA/LXaR+W4rpDXlVXPSdjgJLwzvJVPR3WS5PRKHpJkBM2t+S2kVv\nYvpI1dFcYCRWkzJpJoDz1Q8r8O3HLjZI5aXbz2DE7HYAgTWmKEKr2vy9yrgzovsG\nORPB8AE+904nozuzKBO2YWTgAiSm/4RWuokvZYPifg054lI300Sg7q8wl+BV2Sxe\nsgFVUpQs9maOIpdjBulncFzIY5llsN9EO0NhHZ0u3Ny99QhjmUg74nT9HccW8AwW\no4Wzm+evAgMBAAECggEACTpeIuviZqOsgr8fDLOhaSoSMW2tIChdsYgffDWd4kHE\neHNE2TlfWq4BMeaJCE91pTQHfQ2Fr9wg+LgbXdBFlRJZUOrzV4G0RZI3MzyYfjVX\nS055xgy33ix8OYVjnQm5ycjm0vok4xu/7XqPuDnbRI0UXNQfWxmyOWePoYNgJur5\n6Nh/j4+enRtilN54DWZyHbfnMhLKnPFfEjo9KdCdPsMwm+jm65FSE1y/PBBGvIRh\nK9eV81MC8I2FPu4EOavOYqUmHtDUxW8faHrKIrZRtxXEPwoUVnP9gCrxTNbJeciA\ntMnE2YMcGC2VCUVuN13IRWoHlsfzbwWI6JLvBMbgGQKBgQDt/ndNa3hhJIvMYUTs\n/zNVFAsCutTTn+YSppoQzkz2sjsFcPtHVBvbL70OTw9yBwLrOAjFDzNA5W1XgZum\nHD8hwLx8nLnYfay1x/j/gUcuCS6ik3dWAO8LRqvZxUijCcE5oR6i3/Ed46WoWYlB\nP+VZEWLetsUZFSrc0IzaW5gt2QKBgQDN+Z4HxE6/wpVbsr/vA7nN6TlIpWoe3KQk\n1V7puP6W4mSVXlHva9O2hWycukcaBVaSTzXGYuzIfbiT1ZCTLxYa+grKco6e8bkd\n44Hpdm+yHx7+6inwqiqL+xr6IkfVeh14D1koHxENEf/62JoFgSDhAXnKjiJ7+zDn\n73n893PkxwKBgGiH+PyPNItuUtzM6Eoz+Oboa8GiL/JXa+VLOaYiBpngRJ4qNqPo\npGeMOzx6qy0JOVX5AZkUCQ369yCVM7ks9OmtTtxothQJdv9Muuf2bz4gGFSd8q9a\nr6PDQZ3f0fySP0VBqEQfmjbnkw4zbV60YtbRFRz/J+jRbEcabpNF4bxZAoGAXmy8\ngZsA7u/pQKxlSNFQcJEmbaNHTvafWTNn24WvUMRgkAk5TqUD3Xy1GfRbfBZOZaxi\nXpwjKJZZ84vIR3EilSNjpwN1VnBCCO2vNLPS6LlToFEBAQ9BigKHj3v/qmHc+Jkw\nqi/zxSYnT3vUwAk+ZWgjyTP3oxa4iNtD9TALtSkCgYAdfAtT2ov3XxEwySnC18UG\n4ldQNnWbJ7O64b6s0y+PhtGdTSLvVE3+h8ffmTYKVYrt3L68/GAVf+3p1P5SZgGS\n11CeSuInoXLfgOU59HrF8am5s/bl0Qt1mX0HI2t9kedT+Bqs7f0Nv2w5OJMO7kyu\nwkGU0Fh8ww+1kEr0Mrjcvg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-2zokf@zombichase-e04ac.iam.gserviceaccount.com",
  "client_id": "115625101394502656687",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2zokf%40zombichase-e04ac.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Initialize Firebase Admin SDK
cred = credentials.Certificate(cred_obj)
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': "https://zombichase-e04ac-default-rtdb.europe-west1.firebasedatabase.app/",
})

# Get a database reference
ref = db.reference('/')