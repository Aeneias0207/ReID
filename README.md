# __Dokumentation zur Installation von ReID und des AIDeck Converters__

Diese README beschreibt die notwendigen Schritte eines clean install der deep-person-reid Software sowie des AIDeck Converters.
Letzterer ermöglicht es einen Videostream einer Crazyfliedrohne mit AIDeck empfangen zu können. Für den Empfang des Videostreams wird kein ROS benötigt.

__ToDos__  
- Installation von pandas und faiss-cpu via requirements.txt --> eigene requirements.txt erstellen und in Sciebo/github hochladen anstatt die requirements des torchreid repos zu nutzen.
- Muss Pfad geändert werden wenn eigene requirements.txt erstellt und heruntergeladen wird? Wie wählt Linux die richtige requirements.txt aus?
- Beschreibung unter 2.5 ergänzen wie man an die IP-Adresse der Drohne gelangt
- *tbd Beschreibung ergänzen wie man diese die Drohne startet*
## Installation der benötigten Komponenten (sinnvoll= zwischendurch müsste ja auch noch das Env gestartet werden? durch die Zusammenfassung würde alles kompakter werden da weniger Überschriften)
```console
sudo apt install git
(sudo) bash Miniconda3-latest-Linux-x86_64.sh

## 1. Installation ReID sowie Voraussetzungen
#### 1.1 Installation Miniconda
```console
(sudo) bash Miniconda3-latest-Linux-x86_64.sh
```
#### 1.2 Erstelle Conda Environment mit Python 3.8 (Kompatibilitätsgründe)
```console
conda create --name torchreid python=3.8
```
#### 1.3 Aktiviere Conda Environment
```console
conda activate torchreid
```
#### 1.4 (Optional) Installiere git
```console
sudo apt install git
```
#### 1.5 Download torchreid/deep-person-reid aus Git-Repository
```console
git clone https://github.com/KaiyangZhou/deep-person-reid.git
```

#### 1.6a HIER DOWNLOAD DER EIGENEN REQUIREMENTS.TXT EINFÜGEN *Anschließend 1.6b entfernen und 1.6a umbenennen*
```console
wget https://github.com/Aeneias0207/ReID/blob/4032a250b2460480f6c84442180aedf904faee21/requirements.txt
pip install -r requirements.txt
```

#### 1.6b Installieren der requirements für deep-person-reid
```console
pip install -r requirements.txt
```
(da pybase64, cv2 und pyvirtualcam ebenfalls noch installiert werden müssen wäre es sinnvoll diese in die requirements aufzunehmen aber die requirements.txt kommt aus dem git repo....)
#### 1.7 Installation von pytorch torchvision
```console
conda install pytorch torchvision -c
python setup.py develoop
```
#### 1.8 (Optional) Installation Sciebo:
```console
wget -nv https://www.sciebo.de/install/linux/Ubuntu_22.04/Release.key -O - | sudo apt-key add -
echo 'deb https://www.sciebo.de/install/linux/Ubuntu_22.04/ /' | sudo tee -a /etc/apt/sources.list.d/owncloud.list
sudo apt update
sudo apt install sciebo-client
```

#### 1.9 Download re-id_starterpack von Sciebo
>[Link zu Sciebo](https://tu-dortmund.sciebo.de/f/321038868)

#### 1.10 (Optional) Verschieben der Dokumente nach Documents
```console
cp -r re-id_starterpack/ ../Documents
```

#### 1.11 Entpacken der Dateien und entfernen der ZIPs:
(Optional)
```console
cd ../Documents
```
(Non-Optional)
```console
unzip aideck_re-id.zip && rm aideck_re-id.zip
unzip re-id_playground.zip && rm re-id_playground.zip
unzip re-id_replica_UDE.zip && rm re-id_replica_UDE.zip
```

#### 1.12 Installieren von faiss-cpu und pandas (evtl. ebenfalls in die requirements aufnehmen)
```console
pip install faiss-cpu
pip install pandas
```

## 2. Installation AIDeck Connector
AIDeck Connector ersetzt den Stream Publisher und die Konvertierung der Bilder via ROS, sodass für die Bildübertragung und -empfang keine ROS1-Installation benötigt wird. D.h. auch PCs mit Ubuntu > 18.04 können Bilder der Drohne empfangen
#### 2.1 Download aideck_connector.py (von Sciebo oder Git)
#### (Optional)
```console
conda activate torchreid
```

#### 2.2 Installation Video4Linux (v4l2loopback)
```console
git clone https://github.com/umlaeute/v4l2loopback
make && sudo make install
sudo depmod -a
```

#### 2.3 v4l2loopback ausführen:
```console
sudo modprobe v4l2loopback
```

#### 2.4 Verfügbare Devices anzeigen:
```console
ls -1 /sys/devices/virtual/video4linux
```


#### 2.5 Konfigurieren und ausführen des AI Deck Connector
```python
# IP-Adresse der Drohne ändern sowie Device-Nr.
IP = 'XXX.XXX.XXX.XXX'
DEVICE_NUMBER = X
```

Ausführen des gespeicherten Skripts:
```console
python3 ai_deck_connector.py
```
