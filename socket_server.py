#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import socket
import json
import threading  # Hem ROS hem de soket sunucusu için gerekli
import sys
from mavros_msgs.msg import State

# --- Global Değişkenler ---
# Bağlı olan istemci soketini tutmak için
client_conn = None
# Birden fazla thread'in 'client_conn' değişkenine aynı anda erişmesini engellemek için kilit
conn_lock = threading.Lock()
# -------------------------


def mavros_state_callback(msg):
    """
    /mavros/state topic'inden her mesaj geldiğinde bu fonksiyon çalışır.
    """
    global client_conn

    # Kilit ile güvenli bir şekilde global 'client_conn' değişkenine eriş
    with conn_lock:
        if client_conn:
            try:
                # 1. ROS mesajından istediğimiz verileri bir sözlüğe (dictionary) aktar
                data = {
                    'connected': msg.connected,
                    'armed': msg.armed,
                    'guided': msg.guided,
                    'mode': msg.mode,
                    'system_status': msg.system_status
                }

                # 2. Sözlüğü JSON formatında bir string'e dönüştür
                #    Her JSON mesajının sonuna '\n' (yeni satır) ekliyoruz.
                #    Bu, istemcinin mesajların nerede bittiğini anlamasını sağlar.
                json_data = json.dumps(data) + '\n'

                # 3. Veriyi UTF-8 formatında encode edip soket üzerinden gönder
                client_conn.sendall(json_data.encode('utf-8'))

            except socket.error as e:
                # İstemci bağlantıyı aniden kapattıysa veya bir hata oluştuysa
                print(f"Soket gönderme hatası (istemci bağlantıyı kesmiş olabilir): {e}")
                client_conn.close()
                client_conn = None # Bağlantıyı sıfırla

def socket_server_thread():
    """
    İstemcilerden gelen bağlantıları kabul etmek için ayrı bir thread'de çalışır.
    """
    global client_conn
    HOST = '127.0.0.1'  # Localhost
    PORT = 12345        # Kullanılacak port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Adresin tekrar kullanılmasına izin ver (programı hemen yeniden başlatabilmek için)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Soket sunucusu {HOST}:{PORT} üzerinde dinlemede...")

        # ROS çalıştığı sürece yeni bağlantıları kabul et
        while not rospy.is_shutdown():
            try:
                # Yeni bir bağlantı bekle (Bu satır engelleyicidir)
                conn, addr = server_socket.accept()
                print(f"{addr} adresinden yeni bir bağlantı kabul edildi.")

                with conn_lock:
                    # Eğer varsa eski bağlantıyı kapat
                    if client_conn:
                        print("Mevcut bağlantı kapatılıyor, yeni bağlantı kabul ediliyor.")
                        client_conn.close()
                    # Yeni bağlantıyı global değişken olarak ata
                    client_conn = conn

                # Bu basit sunucu aynı anda sadece 1 istemciye hizmet verir.
                # Callback fonksiyonu 'client_conn' üzerinden veri göndermeye başlar.
                # Eğer istemcinin bağlantısı koparsa, callback'teki 'except' bloğu
                # 'client_conn'i None yapar. Bu thread'in de bunu fark etmesi gerekir.

                # Bağlantı aktif olduğu sürece bekle
                while not rospy.is_shutdown():
                    with conn_lock:
                        if client_conn is None:
                            print("İstemci bağlantısı kapandı, yeni bağlantı bekleniyor.")
                            break # İç döngüden çık ve yeni 'accept'e git
                    rospy.sleep(1.0) # Bağlantıyı periyodik olarak kontrol et

            except socket.error as e:
                if not rospy.is_shutdown():
                    print(f"Soket kabul hatası: {e}")
                    break # Ana döngüden çık

    except Exception as e:
        print(f"Soket sunucusu başlatanmAdı: {e}")
    finally:
        server_socket.close()
        print("Soket sunucusu kapatıldı.")

if __name__ == '__main__':
    try:
        # 1. ROS Node'unu başlat
        rospy.init_node('mavros_socket_publisher', anonymous=True)

        # 2. MAVROS topic'ine abone ol
        rospy.Subscriber('/mavros/state', State, mavros_state_callback)
        print("ROS subscriber başlatıldı, /mavros/state dinleniyor...")

        # 3. Soket sunucusunu ayrı bir thread'de başlat
        #    Böylece 'rospy.spin()' ana thread'i tıkamaz.
        server_thread = threading.Thread(target=socket_server_thread)
        server_thread.daemon = True  # Ana program (rospy) kapanınca bu thread de kapansın
        server_thread.start()

        # 4. Ana thread'i ROS'un çalışması için 'spin'e al (programın kapanmasını engeller)
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        print("Program kapatılıyor...")
    finally:
        # Program kapanırken soketi de temizle
        with conn_lock:
            if client_conn:
                client_conn.close()
