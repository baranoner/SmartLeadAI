import os
from flask import Flask
from flask_cors import CORS
from ayarlar import ayar_secici
from uygulama.database import veritabani_baslat

def uygulama_olustur(ayar_adi: str = None) -> Flask:
    # Flask uygulamasını ve HTML şablonlarının aranacağı klasörü tanımlıyoruz
    uygulama = Flask(__name__, template_folder="sablonlar")

    # Ortam değişkenine göre doğru konfigürasyonu seçip uygulamaya yüklüyoruz
    if ayar_adi is None:
        ayar_adi = os.environ.get("FLASK_ORTAMI", "gelistirme")
    secilen_ayar = ayar_secici.get(ayar_adi, ayar_secici["gelistirme"])
    uygulama.config.from_object(secilen_ayar)

    
    CORS(
        uygulama,
        origins=uygulama.config.get("CORS_ALLOWED_ORIGINS", "*"),
        methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # Uygulama bağlamında veritabanı tablolarının varlığını kontrol edip yoksa oluşturuyoruz
    with uygulama.app_context():
        veritabani_baslat(uygulama)

    # Uygulamanın alt modüllerini (Rotaları) ana sisteme monte ediyoruz
    from uygulama.rotalar import api_arayuzu, sayfa_arayuzu
    uygulama.register_blueprint(api_arayuzu, url_prefix="/api")
    uygulama.register_blueprint(sayfa_arayuzu)

    @uygulama.route("/saglik-durumu")
    def saglik_kontrolu():
        """Sunucunun Ayakta Olup Olmadığını Bildiren Uç Nokta (Health Check)."""
        from flask import jsonify
        return jsonify({"durum": "aktif", "servis": "Akıllı Satış AI"}), 200

    return uygulama