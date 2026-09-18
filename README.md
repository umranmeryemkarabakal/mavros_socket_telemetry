# ROS MAVROS Soket Telemetri Köprüsü (Socket Telemetry Bridge)

<p>
  <img src="https://img.shields.io/badge/ROS%20Noetic-22314E?style=for-the-badge&logo=ros&logoColor=white" alt="ROS Noetic" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/MAVROS-1F2A44?style=for-the-badge" alt="MAVROS" />
  <img src="https://img.shields.io/badge/TCP%20Socket-20232A?style=for-the-badge" alt="TCP Socket" />
</p>

## 🇬🇧 Overview

A lightweight bridge that subscribes to `/mavros/state` and streams the vehicle state as JSON over a TCP socket, so non-ROS applications (CLI, GUI, web) can monitor MAVROS without ROS dependencies.

**Quick start:** `rosrun <your_package> socket_server.py`

## 🇹🇷 Proje hakkında

Bu depo (repository), MAVROS durum bilgilerini (`/mavros/state`) harici uygulamalara aktarmak için basit ve güvenilir bir TCP soket köprüsü sağlar.

Proje, çalışan bir ROS–MAVROS ortamındaki drone telemetri verilerini, hafif (lightweight) ve JSON tabanlı bir TCP protokolü kullanarak ROS tabanlı olmayan sistemlere iletmek üzere tasarlanmıştır.

## Genel Bakış

* `/mavros/state` topic'ine abone olur.
* Temel araç durum bilgilerini ayıklar.
* Telemetri verilerini bir TCP soketi üzerinden JSON mesajları olarak yayınlar.
* Harici uygulamaların (CLI, GUI, Web vb.) ROS bağımlılığı olmadan MAVROS durumunu izlemesine olanak tanır.

## Mimari

```text
[MAVROS]
   |
   |  /mavros/state (ROS Topic)
   v
[ROS Node - socket_server.py]
   |
   |  TCP üzerinden JSON
   v
[Harici İstemci - socket_client.py]
```

## Ön Gereksinimler

Bu proje çalışan bir MAVROS örneği gerektirir.

###### Soket sunucusunu (server) çalıştırmadan önce şunlardan emin olun:

1. ROS çalışıyor olmalı.
2. MAVROS başlatılmış ve bir simülatöre veya gerçek bir araca bağlı olmalı.
3. /mavros/state topic'i aktif olarak veri yayınlıyor olmalı.

Not: Eğer MAVROS çalışmıyorsa sunucu başlar ancak hiçbir telemetri verisi iletilmez.

## Dosyalar

* **socket_server.py:** /mavros/state topic'ine abone olan ve telemetriyi TCP üzerinden yayınlayan ROS node'u.
* **socket_client.py:** MAVROS durum verilerini alan ve ekrana yazdıran basit bir TCP istemcisi.

### Çalıştırma Sırası

1. ROS çekirdeğini (core) başlatın.
2. MAVROS'u başlatın.
3. Soket sunucusunu (socket_server.py) çalıştırın.
4. Soket istemcisini (socket_client.py) çalıştırın.

Örnek Kullanım

```bash
# Terminal 1
roscore

# Terminal 2
roslaunch mavros px4.launch   # or any MAVROS launch setup

# Terminal 3
rosrun <your_package_name> socket_server.py

# Terminal 4
python socket_client.py
```

#### Veri Formatı

Her telemetri mesajı, tek satırlık bir JSON nesnesi olarak gönderilir:

```json
{
  "connected": true,
  "armed": false,
  "guided": true,
  "mode": "AUTO.LOITER",
  "system_status": 4
}
```
