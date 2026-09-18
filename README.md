# mavros_socket_telemetry

<p>
  <img src="https://img.shields.io/badge/ROS%20Noetic-22314E?style=for-the-badge&logo=ros&logoColor=white" alt="ROS Noetic" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/MAVROS-1F2A44?style=for-the-badge" alt="MAVROS" />
  <img src="https://img.shields.io/badge/TCP%20Socket-20232A?style=for-the-badge" alt="TCP Socket" />
</p>

## Overview

A small bridge that reads the vehicle state from `/mavros/state` and streams it as JSON over a TCP socket, so
applications without ROS (a CLI, a GUI or a web page) can follow the MAVROS state.

**Quick start:** `python3 socket_server.py` then `python3 socket_client.py`

## Proje hakkında

`/mavros/state` konusundaki araç durumunu okuyup TCP soketi üzerinden JSON olarak yayınlayan küçük bir köprü. Böylece
ROS kurulu olmayan bir uygulama (komut satırı, arayüz ya da web sayfası) MAVROS durumunu bu soketten takip edebilir.

```text
MAVROS --/mavros/state--> socket_server.py --TCP 127.0.0.1:12345, JSON--> socket_client.py
```

- `socket_server.py`: `/mavros/state` konusuna abone olan ROS düğümü; gelen her mesajı tek satırlık JSON olarak
  bağlı istemciye gönderir.
- `socket_client.py`: sunucuya bağlanıp gelen durumu ekrana yazan örnek istemci.

Her mesaj tek satır JSON'dur:

```json
{"connected": true, "armed": false, "guided": true, "mode": "AUTO.LOITER", "system_status": 4}
```

## Çalıştırma

MAVROS'un çalışıyor ve bir simülatöre ya da araca bağlı olması gerekir. MAVROS yoksa sunucu açılır ama veri
gelmez.

```bash
# Terminal 1
roscore

# Terminal 2: kendi MAVROS başlatma dosyanız
roslaunch mavros px4.launch

# Terminal 3: ROS ortamı yüklüyken
source /opt/ros/noetic/setup.bash
python3 socket_server.py

# Terminal 4
python3 socket_client.py
```

Adres ve port iki dosyanın başındaki `HOST` ve `PORT` değişkenlerinden değiştirilebilir.
