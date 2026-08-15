from uygulama import uygulama_olustur
# uygulama nesnemizi yaratıyoruz
uygulama = uygulama_olustur()
if __name__ == '__main__':
# Nesnemiz üzerinden run metodunu çalıştırarak uygulamayı başlatıyoruz
    uygulama.run(host='0.0.0.0', port=5000, debug=True)