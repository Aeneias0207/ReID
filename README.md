# __Dokumentation zur Installation von ReID und des AIDeck Converters__

Diese README beschreibt die notwendigen Schritte eines clean install der deep-person-reid Software sowie des AIDeck Converters.
Letzterer ermöglicht es einen Videostream einer Crazyfliedrohne mit AIDeck empfangen zu können. Für den Empfang des Videostreams wird kein ROS benötigt.

__ToDos__  

- Beschreibung unter 2.5 ergänzen wie man an die IP-Adresse der Drohne gelangt
- *tbd Beschreibung ergänzen wie man diese die Drohne startet*
> Erklärung von Crazyswarm mit FileStructure für den Überblick und Erklärung welche Scripte für was zuständig sind
> Erklärung Kommunikationsstruktur und Aufbau unseres Systems (Drone -> PC, PC -> Drone, Was sendet welche Befehle)

## Installation der Requirements
```console
sudo apt install git
```

### Repositories clonen
```console
git clone https://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@github.com/Aeneias0207/ReID.git
git clone https://github.com/KaiyangZhou/deep-person-reid.git

> vorher noch einen Build-Ordner erstellen in der Readme von v4l2loopback
git clone https://github.com/umlaeute/v4l2loopback
make && sudo make install
sudo depmod -a
```

### Installation Miniconda und erstellen des conda Environments
```console
(sudo) bash Miniconda3-latest-Linux-x86_64.sh
conda create --name torchreid python=3.8
conda activate torchreid
```
## Installation Dependencies
> conda environment muss aktiv sein

```console
cd ~/Documents/REID_REPO
pip install -r requirements.txt
conda install pytorch torchvision -c
python setup.py develop
```

## re-id_starterpack
>[Link zu Sciebo](https://tu-dortmund.sciebo.de/f/321038868)

Download re-id_starterpack-Ordner gesamt als .zip

```console
mv ~/Downloads/re-id_starterpack.zip ~/Documents
cd ~/Documents
unzip re-id_starterpack && rm re-id_starterpack
cd re-id_starterpack
unzip aideck_re-id.zip && rm aideck_re-id.zip
unzip re-id_playground.zip && rm re-id_playground.zip
unzip re-id_replica_UDE.zip && rm re-id_replica_UDE.zip
unzip *.zip && rm *.zip
```
> Warum funktioniert der Stern nicht als Platzhalter?

## 2.2 Installation Video4Linux (v4l2loopback)
>Hier fehlt ein cd und die Erstellung von einem Build Ordner (steht auch in der ReadMe von v4l2loopback)
```console
git clone https://github.com/umlaeute/v4l2loopback
make && sudo make install
sudo depmod -a
```

### v4l2loopback ausführen:
```console
sudo modprobe v4l2loopback
```

### Verfügbare Devices anzeigen:
```console
ls -1 /sys/devices/virtual/video4linux
```

### Konfigurieren und ausführen des AIDeck-Connectors
>Wo muss das geändert werden?
```python
# IP-Adresse der Drohne ändern sowie Devicenr.
IP = 'XXX.XXX.XXX.XXX'
DEVICE_NUMBER = X
```

Ausführen des gespeicherten Skripts:
```console
python3 ai_deck_connector.py
```
