import socket  # UDP soketini oluşturmak için
import threading  # Eşzamanlı mesaj alımını sağlamak için

localhost = "127.0.0.1"  # Sunucu IP adresi
udp_port = 12346  # UDP bağlantı portu
buffer_size = 1024

# serverdan mesajları alan thread
def receive_mesaj(sock):
    while True:
        try:
            mesaj, addr = sock.recvfrom(buffer_size)  # Sunucudan mesaj al
            if mesaj:
                mesaj = mesaj.decode() #mesajı çöz ve yazdır
                print(mesaj)  #ekrana yazdır
                if mesaj.strip() == "Bağlantı kapatılıyor...":
                    break
        except OSError:
            break

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP soketi oluşturma

isim = input("Kullanıcı adınızı girin: ")  # Kullanıcı adını iste
udp_socket.sendto(isim.encode(), (localhost, udp_port))  # Kullanıcı adını servera gönderme

thread = threading.Thread(target=receive_mesaj, args=(udp_socket,))  # Mesaj alım thread oluşturma
thread.start()

while True:
    mesaj = input()  # Kullanıcıdan mesaj alan ve mesaj'a atayan satır
    if mesaj.strip().lower() == "görüşürüz":  # Çıkış komutunu "görüşürüz" olarak belirledik
        udp_socket.sendto(mesaj.encode(), (localhost, udp_port))  # Çıkış mesajı gönderme
        break
    udp_socket.sendto(f"{mesaj}".encode(), (localhost, udp_port))  # Mesajı sunucuya gönderme

thread.join()
udp_socket.close()  # Soketi kapat