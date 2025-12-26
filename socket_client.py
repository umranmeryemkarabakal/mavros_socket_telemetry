#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import json
import sys

HOST = '127.0.0.1'  # Bağlanılacak sunucu (localhost)
PORT = 12345        # Bağlanılacak port

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"{HOST}:{PORT} adresine bağlanılıyor...")
    client_socket.connect((HOST, PORT))
    print("Bağlandı. Sunucudan İHA durumu bekleniyor...")

    # Soketi bir dosya nesnesine çeviriyoruz.
    # Bu, 'readline()' kullanarak veriyi satır satır okumamızı sağlar.
    # Sunucu her JSON mesajını '\n' ile bitirdiği için bu yöntem mükemmel çalışır.
    socket_file = client_socket.makefile('r')

    while True:
        # Sunucudan yeni bir satır (bir JSON mesajı) bekle
        line = socket_file.readline()

        if not line:
            # Satır boşsa, sunucu bağlantıyı kapatmış demektir.
            print("Sunucu bağlantısı kesildi.")
            break

        try:
            # Gelen satırı (JSON string) bir Python sözlüğüne (dict) parse et
            data = json.loads(line)

            # Gelen veriyi terminale yazdır
            print("-------------------------")
            print(f"  Mod:           {data.get('mode')}")
            print(f"  Arm Durumu:    {'ARMED' if data.get('armed') else 'DISARMED'}")
            print(f"  Bağlantı:      {'BAĞLI' if data.get('connected') else 'BAĞLANTI YOK'}")
            print(f"  Guided Modu:   {data.get('guided')}")
            print(f"  Sistem Statü:  {data.get('system_status')}")
            print("-------------------------")

        except json.JSONDecodeError:
            print(f"Hatalı JSON verisi alındı (parse edilemedi): {line.strip()}")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

except socket.error as e:
    print(f"Soket bağlantı hatası: {e}")
except KeyboardInterrupt:
    print("\nİstemci kapatılıyor...")
finally:
    # Program kapanırken soketleri ve dosyayı kapat
    if 'socket_file' in locals():
        socket_file.close()
    client_socket.close()
