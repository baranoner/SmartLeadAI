def uygulama_olustur(ayar_adi=None):
    uygulama = Flask(__name__, template_folder='sablonlar')
    # 1) Ayarları yükle (geliştirme mi, üretim mi?)
    secilen_ayar = ayar_secici.get(ayar_adi, ayar_secici['gelistirme'])
    uygulama.config.from_object(secilen_ayar)
    # 2) Dış sitelerin bağlanmasına izin ver (CORS)
    CORS(uygulama, origins=uygulama.config.get('CORS_ALLOWED_ORIGINS', '*'),
    methods=['GET', 'POST', 'OPTIONS'])
    # 3) Veritabanı tablosunu hazırla (yoksa oluştur)
    with uygulama.app_context():
        veritabani_baslat(uygulama)
    # 4) Adresleri (rotaları) sisteme tanıt
    from uygulama.rotalar import api_arayuzu, sayfa_arayuzu
    uygulama.register_blueprint(api_arayuzu, url_prefix='/api')
    uygulama.register_blueprint(sayfa_arayuzu)
    return uygulama