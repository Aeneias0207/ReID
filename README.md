# __Dokumentation zur Installation von ReID und des AIDeck Converters__

Diese README beschreibt die notwendigen Schritte eines clean install der deep-person-reid Software sowie des AIDeck Converters.
Letzterer ermöglicht es einen Videostream einer Crazyfliedrohne mit AIDeck empfangen zu können. Für den Empfang des Videostreams wird kein ROS benötigt.

__ToDos__  

- Beschreibung ergänzen wie man an die IP-Adresse der Drohne gelangt
- Testszenario einfügen am Ende, dass Installation erfolgreich war ("Starte jetzt die Programme/Führe Programm xyz aus und halte die Drohne vor den Block um zu sehen ob dieser erkannt wird")

## Installation der Requirements
```console
sudo apt install git
```

### Repositories clonen
```console
git clone https://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@github.com/Aeneias0207/ReID.git
git clone https://github.com/KaiyangZhou/deep-person-reid.git
```
> jetzt Build-Ordner erstellen, in der Readme von v4l2loopback
```console
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
conda install pytorch torchvision
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
unzip "*.zip" && rm *.zip
```

## Testcase/ Funktionstest
> Hier einfügen
