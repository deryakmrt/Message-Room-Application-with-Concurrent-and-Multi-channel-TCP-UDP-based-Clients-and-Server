import socket  # TCP ve UDP soketleri oluşturmak için
import threading  # Eşzamanlılık ve iş parçacıkları oluşturmak için

localhost = "127.0.0.1"  # serverin çalışacağı IP adresi
tcpPort = 12345  # TCP  portu
udpPort = 12346  # UDP  portu
buffer_size = 1024 #Soketten okunacak veri miktarı

# TCP soketi oluşturma
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP soketi oluştur
tcp_socket.bind((localhost, tcpPort))  # TCP soketini IP ve porta bağla
tcp_socket.listen(5)

# UDP soketi oluşturma
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP soketi oluştur
udp_socket.bind((localhost, udpPort))  # UDP soketini IP ve porta bağla

istemciler = {}  # bağlı olan istemcileri burada saklar
kullanici_adlari = {}  # Kullanıcı adlarını burada saklar
#--------------------------------------------------------------------------------------------
# TCP fonksiyonu
def islem_tcp_client(conn, addr):  # conn --> connection , addr --> adres bilgisi
    conn.send("Kullanıcı adınızı girin: ".encode())  # Kullanıcı adını iste
    isim = conn.recv(buffer_size).decode().strip()  # Kullanıcı adını al ve boşlukları temizle

    if isim in istemciler:  # Kullanıcı adı daha önceden istemcilere eklenmiş mi yani benzersiz mi
        conn.send("Bu kullanıcı adı zaten alınmış, lütfen başka bir kullanıcı adı girin!".encode())
        conn.close()  # Benzersiz değilse bağlantıyı kapat
        return

    istemciler[isim] = conn  # bağlanan ismi sözlüğüne ekle
    kullanici_adlari[conn] = isim  # ismi kullanıcı adları sözlüğüne ekle

    yayinla(f"{isim}[TCP] ile bağlanmıştır.", isim)  # bu mesajı herkes görür ve hangi protokolle bağlandığı bilgisini de içerir
    conn.send(f"Hoşgeldiniz {isim} TCP ile bağlısınız".encode())

    while True:  # Sürekli mesaj alan döngü
        try:
            mesaj = conn.recv(buffer_size)  # clientten mesaj al
            if not mesaj:  # Mesaj yoksa döngüden çık
                break
            mesaj = mesaj.decode().strip()  # Mesajı çöz(decpde et) ve boşlukları temizle
            if mesaj.lower() == "görüşürüz":  # Kullanıcı çıkış yapmak istiyorsa
                conn.send("Bağlantı kapatılıyor...".encode())  # bu mesajı gönder
                break
            yayinla(f"{isim}[TCP]: {mesaj}", isim)  # Mesajı yayınla
        except ConnectionResetError:  # Bağlantı sıfırlanmışsa döngüden çık
            break

    conn.close()  # Bağlantıyı kapat
    del istemciler[isim]  # Kullanıcıyı istemciler sözlüğünden sil
    del kullanici_adlari[conn]  # ismi de kullanıcı adlarından sil
    yayinla(f"{isim}[TCP] ayrıldı.", isim)  # Ayrılma mesajını herkese yayınla
#--------------------------------------------------------------------------------------------
# UDP mesajlarını işleyen iş parçacığı fonksiyonu
def islem_udp_client():
    while True:  # Sürekli mesaj alan döngü
        mesaj, addr = udp_socket.recvfrom(buffer_size)  # UDP soketinden mesaj al
        if addr not in istemciler.values():  # Adres daha önce kaydedilmemişse
            isim = mesaj.decode().strip()  # Kullanıcı adını al ve boşlukları temizle
            if isim in istemciler:  # Kullanıcı adı daha önceden istemcilere eklenmiş mi yani benzersiz mi
                udp_socket.sendto("Bu kullanıcı adı zaten alınmış, lütfen başka bir kullanıcı adı girin.".encode(), addr)
            else:
                istemciler[isim] = addr  # Kullanıcıyı istemcilere ekle
                kullanici_adlari[addr] = isim  # ismi kullanıcı adları sözlüğüne ekle
                yayinla(f"{isim}[UDP] ile bağlanmıştır.", isim)  # Bağlantı mesajını yayınla
                udp_socket.sendto(f"Hoşgeldiniz {isim} UDP ile bağlısınız".encode(), addr)
        else:
            isim = kullanici_adlari[addr]  # ismi iste
            text = mesaj.decode().strip()  # Mesajı al ve boşlukları temizle
            if text.lower() == "görüşürüz":  # Kullanıcı çıkış yapmak istiyor mu kontrol et (kontrol ögesi "görüşürüz")
                udp_socket.sendto("Bağlantı kapatılıyor...".encode(), addr)  #kapatma mesajı gönder
                del istemciler[isim]  # Kullanıcıyı istemcilerden sil
                del kullanici_adlari[addr]  # ismi de kullanıcı adlarından sil
                yayinla(f"{isim}[UDP] ayrıldı.", isim)  # Ayrılma mesajını yayınla
            else:
                yayinla(f"{isim}[UDP]: {text}", isim)  # Mesajı yayınla
#--------------------------------------------------------------------------------------------
# Mesajı tüm istemcilere yayınlayan fonksiyon
def yayinla(mesaj, sender):
    print(mesaj)  # Mesajı server.py run ekranında gösterir
    for isim, conn in istemciler.items():  # Tüm clientlar için döngü
        if isim != sender:  # Gönderen kullanıcı hariç
            if isinstance(conn, socket.socket):  # Kullanıcı TCP bağlantısı mı?
                conn.send(mesaj.encode())  # TCP bağlantısına mesaj gönder
            else: #yoksaa
                udp_socket.sendto(mesaj.encode(), conn)  # UDP bağlantısına mesaj gönder
#--------------------------------------------------------------------------------------------
# TCP client kabul eden thread
tcp_thread = threading.Thread(target=lambda: [threading.Thread(target=islem_tcp_client, args=(conn, addr)).start() for conn, addr in iter(tcp_socket.accept, None)])
tcp_thread.start()

# UDP mesajlarını işleyen thread
udp_thread = threading.Thread(target=islem_udp_client)
udp_thread.start()

# thread bekletme
tcp_thread.join()
udp_thread.join()
