import socket  # TCP soketini oluşturmak için
import threading

localhost = "127.0.0.1"  # Sunucu IP adresi
tcpPort = 12345  # TCP bağlantı portu
buffer_size = 1024

# Sunucudan mesajları alan thread
def receive_mesaj(sock):
    while True:
        try:
            mesaj = sock.recv(buffer_size)  # serverdan mesaj al
            if mesaj:
                mesaj = mesaj.decode()
                print(mesaj)  # Mesajı ekrana yazdır
                if mesaj.strip() == "Bağlantı kapatılıyor...":
                    break
            else:
                break
        except ConnectionAbortedError:
            break
        except ConnectionResetError:
            break

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP soketi oluşturma
tcp_socket.connect((localhost, tcpPort))  # servera bağlanma

ilkmesaj = tcp_socket.recv(buffer_size).decode()
print(ilkmesaj, end="")  # İlk mesajı ekrana yazdır (Kullanıcı adınızı girin: )

isim = input()  # Kullanıcı adını isteme
tcp_socket.send(isim.encode())  # Kullanıcı adını servera gönderme

thread = threading.Thread(target=receive_mesaj, args=(tcp_socket,))  # Mesaj alım thread oluşturma
thread.start()

while True:
    mesaj = input()  # Kullanıcıdan mesaj alır ve mesaj'a atar
    if mesaj.strip().lower() == "görüşürüz":  # mesajda çıkış komutu olan "görüşürüz" yazılırsa bağlantı kapatılır
        tcp_socket.send(mesaj.encode())  # Çıkış mesajı
        break
    tcp_socket.send(mesaj.encode())  # Mesajı servera gönderme

tcp_socket.close()  # Bağlantıyı kapatır