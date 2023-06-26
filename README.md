# __Dokumentation zur Installation von ReID und des AIDeck Converters__

Diese README beschreibt die notwendigen Schritte eines clean install der deep-person-reid Software sowie des AIDeck Converters.
Letzterer ermöglicht es einen Videostream einer Crazyfliedrohne mit AIDeck empfangen zu können. Für den Empfang des Videostreams wird kein ROS benötigt.

Abschnitte welche mit **(OPTIONAL)** markiert sind werden nur benötigt falls noch nicht installiert (bspw. git).

__ToDos__  

- Testcase 2 vervollständigen

## Installation der Requirements
**(OPTIONAL)**
```console
sudo apt install git
```

### Repositories clonen
```console
git clone https://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@github.com/Aeneias0207/ReID.git
git clone https://github.com/KaiyangZhou/deep-person-reid.git
```
> jetzt Build-Ordner erstellen, s. Readme von v4l2loopback  
```console
git clone https://github.com/umlaeute/v4l2loopback
make && sudo make install
sudo depmod -a
```
> The depmod -a call will re-calculate module dependencies, in order to automatically load additional kernel modules required by v4l2loopback. The call may not be necessary on modern systems.

### (OPTIONAL) Download & Installation Miniconda
[Download von Website](https://docs.conda.io/en/latest/miniconda.html)
```console
bash Miniconda3-latest-Linux-x86_64.sh
```

### Erstellen des conda Environments
```console
conda create --name torchreid python=3.8
conda activate torchreid
```

## Installation Dependencies
> conda environment muss aktiv sein

```console
cd ~/deep-person-reid/
pip install -r requirements.txt
conda install pytorch torchvision
python setup.py develop
```

## re-id_starterpack
> Wird benötigt da Files (z.B. aideck_palletid/models/model.pth.tar) zu groß sind, um in Github hochgeladen zu werden  
>[Link zu Sciebo](https://tu-dortmund.sciebo.de/f/321038868)  
Download re-id_starterpack-Ordner gesamt als .zip

```console
mv ~/Downloads/re-id_starterpack.zip ~/Documents
cd ~/Documents
unzip re-id_starterpack && rm re-id_starterpack
cd re-id_starterpack
unzip "*.zip" && rm *.zip
```

## Testcases/ Funktionstests
**Testcase 1 - Nur Bildübertragung von Drohne zum neuaufgesetzten PC**

@Drohnen-PC (Dartagnan)
```console
cd ~/Dokumente/crazyswarm_reid_demo/crazyswarm
. jump_to_scripts.sh
cfclient
```
Im cfclient:
- (GUI) Connect -> Connect to Crazyflie
- (GUI) Console -> suche nach Wifi connected to ip: 192.168.2.XX

@eigener Rechner
```console
sudo modprobe v4l2loopback
ls -1 /sys/devices/virtual/video4linux
```
> evtl. video device-Nummer im AI Deck Connector anpassen
```console
cd ~/Dokumente/REPO_NAME
code ai_deck_connector.py
```
Ändere die Variable ID-Adresse zur IP-Adresse aus dem cfclient
```python
IP = 192.168.2.XX
```
```console
conda activate torchreid
python3 ai_deck_connector.py
```
Nun sollten sich zwei Fenster öffnen die jeweils in Schwarz/Weiß-Bild der Kamera zeigen und ein Farbbild.
Der erste Testcase ist damit erfolgreich abgeschlossen. Die Fenster schließen sich mit "Q".

**Testcase 2 - Bildübertragung und Identifikation der Klötzchen**

Schließe **Testcase 1** ab.

```console
conda activate torchreid
cd ~/Dokumente/REPO_NAME
python3 video.py
python3 find_signature.py -v ~/PATH_TO_VIDEO/video.mp4
```
