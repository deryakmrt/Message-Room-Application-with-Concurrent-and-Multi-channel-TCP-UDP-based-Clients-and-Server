# Message Room Application with Concurrent and Multi-channel TCP & UDP Clients and Server

## Overview
This project is a Message Room Application that supports concurrent and multi-channel communication using both TCP and UDP protocols. It involves creating a server that listens for and handles incoming messages from multiple clients simultaneously, and clients that can connect to the server using either TCP or UDP.

## Features
- **Concurrent Server**: The server is designed to handle multiple clients concurrently, creating a new thread for each client request.
- **Multi-channel Communication**: Supports both TCP and UDP communication, processing incoming TCP connections and UDP messages.
- **User Authentication**: Validates user names for both TCP and UDP clients to ensure uniqueness within the chat room.
- **Real-time Messaging**: Broadcasts messages from any client to all other connected clients, displaying the sender's username and protocol.
- **User Notifications**: Informs all clients when a new user joins or leaves the chat room.

## How to Run

### Server
1. Start the server by running the server script.
   ```bash
   python server.py
2. The server will listen for both TCP and UDP messages, process them, and relay them to all connected clients.

### Clients
1. Start a TCP or UDP client by running the respective client script.
   ```bash
    # For TCP client
    python tcp_client.py

    # For UDP client
    python udp_client.py
2. When a client connects, it will prompt for a username. The username must be unique within the chat room.
3. If the username is already taken, the client will be asked to enter a different username.
### Messaging
Clients can send messages to the server, which will broadcast the message to all connected clients.  
Messages will be displayed with the sender's username and the protocol used (TCP/UDP).
### Notifications
When a new client joins, the server will notify all clients with the new user's username and protocol.
- Server: User1 [UDP] has connected. Welcome!  
- Client: Welcome User1, you are connected via UDP.

When a client leaves, the server will notify all clients that the user has left the chat room.  
- Example: User1 [TCP] has left the chat.

### Example Messages  
User1[TCP] : Hello  
User2[UDP] : Hi everyone  
User2[UDP] : Goodbye  
### Exiting
- TCP clients can disconnect by closing the connection.
- UDP clients should send a "goodbye" message to notify the server before disconnecting.


=============================================================================

# Eşzamanlı ve Çok kanallı TCP&UDP tabanlı İstemciler ve Sunucu içerikli Mesaj Odası Uygulaması 
Message Room Application with Concurrent and Multi-channel TCP UDP based Clients and Server

1. Programda önce sunucu (server) kısmı çalıştırılacak, sunucu kısmı tüm soketlerden gelebilecek TCP ve UDP mesajlarını dinleyecek ve bağlı tüm istemcilere iletecektir. Sunucunun eşzamanlı (concurrent) bir nitelikte olması beklenmektedir bu noktada her bir client talebi için yeni bir iş parçacığının oluşturulması gerekir. Server hem TCP hem de UDP iletişimi kullanan multithreaded bir yapıda olmalıdır.  Yani sunucu Gelen TCP bağlantılarını ve mesajlarını işler, TCP kullanıcı adı doğrulaması yapar, Gelen UDP mesajlarını işler ve kullanıcı adı doğrulamasını yapar. Kullanıcı bağlantıları ve ayrıca tüm TCP ve UDP istemcilere ait mesajları sunucu konsolunda görüntüler. TCP bağlantılarını ve UDP isteklerini dikkate alır ve yeni iş parçacıklarının atamasını yapar. 
2. Her bir İstemci (client) kodu çalıştırıldığında sunucuya yeni bir bağlantı gerçekleştirecektir. İstemciler TCP istemciler ve UDP istemciler olmak üzere iki çeşit olacaktır.  
3. Server’a birden fazla kullanıcı bağlanabilir ve sohbet edebilir. Aynı anda en az bir TCP ve en az bir UDP istemcisi mesaj odası uygulamasını kullanmak isteyebilir.  
4. Yeni bir client ilk kez bağlandığında/mesaj göndermek istediğinde yalnızca kullanıcı adı sorulması yeterlidir. Aynı kullanıcı adına sahip kullanıcılar sohbet odasında bulunmamalıdır. Bunun için bir uyarı mesajı gönderilmelidir örneğin “Bu kullanıcı adı zaten alınmış, lütfen başka bir kullanıcı adı girin”. Yeni bir kullanıcı bağlandığında server tarafından bağlanan kullanıcıya ait kullanıcı adı ve protokol (TCP veya UDP) bilgisi sohbet odasına bildirilmelidir yani server ekranında örneğin “User1 [UDP] ile bağlanmıştır hoşgeldiniz”. Ayrıca client ekranında “Hoşgeldiniz User1 UDP ile bağlısınız” mesajı görünmelidir. 
5. Her bir client sohbet odasına gönderilen mesajları server ekranında, mesajı gönderen kullanıcı ve kullanılan protokol bilgisi ile birlikte görebilmelidir. Örneğin;  
User1[TCP] : Merhaba  
User2[UDP] : Selam Gençler  
User2[UDP] : Görüşürüz   
7. Bir kullanıcı sohbet odasından ayrıldığında server tarafından bu bilgi sohbet odasında paylaşılmalıdır. TCP bağlantısında bu protokol gereği bağlantının close edilmesi ile belirlenebilir. UDP tarafında ise bir kullanıcı ayrılması gerektiğinde “görüşürüz” mesajını göndererek ayrılmalıdır. Bu sayede server ilgili UDP istemcinin kullanıcı adını listeden silebilecektir. Eğer UDP kullancısı mesaj göndermeden ayrılırsa ve tekrar bağlanmaya çalışırsa aynı kullanıcı ismi ile buna izin verilmemelidir. 
