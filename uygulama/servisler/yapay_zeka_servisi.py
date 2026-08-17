import logging
import requests
from flask import current_app

loglayici = logging.getLogger(__name__)

class YapayZekaServisi:
    def yanit_uret(self, kullanici_mesaji: str, sohbet_gecmisi: list = None) -> str:

        self._groq_cagir(kullanici_mesaji, sohbet_gecmisi or [])

    def _sistem_talimati_olustur(self) -> str:
        # 'BUSINESS_CONTEXT' arıyoruz
        return current_app.config.get(
            "BUSINESS_CONTEXT",
            "Sen yardımcı bir iş asistanısın."
        )

    def _groq_cagir(self, kullanici_mesaji: str, gecmis: list) -> str:
        #  'GROQ_API_KEY' arıyoruz
        api_anahtari = current_app.config.get("GROQ_API_KEY", "")

        if not api_anahtari:
            loglayici.warning("GROQ_API_KEY ayarlanmamış! Demo modu devrede.")
            return self._demo_yaniti_ver(kullanici_mesaji)

        baglanti_adresi = "https://api.groq.com/openai/v1/chat/completions"
        mesajlar_dizisi = [{"role": "system", "content": self._sistem_talimati_olustur()}]
        for mesaj in gecmis: mesajlar_dizisi.append({"role": mesaj["role"], "content": mesaj["content"]})
        mesajlar_dizisi.append({"role": "user", "content": kullanici_mesaji})

        gonderilecek_veri = {
            "model": "llama-3.1-8b-instant",
            "messages": mesajlar_dizisi,
            "max_tokens": 500,
            "temperature": 0.7,
        }

        try:
            sunucu_cevabi = requests.post(baglanti_adresi, json=gonderilecek_veri, timeout=15, headers={
                "Authorization": f"Bearer {api_anahtari}",
                "Content-Type": "application/json"
            })
            sunucu_cevabi.raise_for_status()
            gelen_veri = sunucu_cevabi.json()
            uretilen_metin = gelen_veri["choices"][0]["message"]["content"]
            loglayici.info("Groq (LLaMA 3) yanıtı başarıyla üretildi.")
            return uretilen_metin.strip()
        except Exception as hata:
            loglayici.error(f"Groq API hatası: {hata}")
            raise YapayZekaServisHatasi("Groq servisine ulaşılamadı.")

    def _demo_yaniti_ver(self, kullanici_mesaji: str) -> str:
        return "Sistem API anahtarı bulunamadığı için demo modunda çalışıyor. Lütfen .env dosyanızı kontrol ediniz."

class YapayZekaServisHatasi(Exception):
    pass

yapay_zeka_servisi = YapayZekaServisi()