# Live muziekgenerator
Live muziekgenerator op basis van a priori kennis voor aanpasbare artificiële instrumentale muziek


Universiteit Gent \
Faculteit: Ingenieurswetenschappen en architectuur \
Opleiding: Master of Science in de industriële Wetenschappen Elektronica-ICT \
Academiejaar: 2019-2020

Auteur: Laurens Van Goethem (01604762)

Begeleidingscommissie: \
prof. dr. ir. Paul Devos  (promotor) \
prof. dr. ir. Dick Botteldooren  (promotor) \
dr. ir. Alejandro Osses Vecchi (begeleider)


## Inhoud code

- **main.py**: File dat gebruikt wordt als start om de verschillende functies op te kunnen roepen.
- **datamodel.py**: File dat het MLP-regressormodel creëert.
- **mir_main.py**: File dat de in- en uitkomende kenmerkdata manipuleert. Maakt het lookup model.
- **mir_features.py**: File dat de basisinformatie en MIR-features uit een audiosignaal haalt en eventueel plot. 
- **music_main.py**: File dat de algemene werking van FoxDot beheert en controleert.
- **music_parameter.py**: File dat de initiële parameters van de muziek bevat. Dit zijn de basiselementen voor de structuur en kunnen worden aangepast.
- **music_structure.py**: File dat alle muzikale structuren bevat zoals strofe, refrein en intro. Creëert de groepen waarin de instrumenten spelen.
- **music_building.py**: File dat de verschillende melodieën en motieven creëert.
- **SuperCollider_startup.scd**: File om FoxDot in SuperCollider te starten.
- **supercollider_info.csv**: CSV-bestand van de parameters van de opgenomen FoxDot nummers.
- **supercollider_info.xlsx**: Excel-bestand van de parameters van de opgenomen FoxDot nummers.
- **audiofiles**:
    - **deam**: Map die wav-files van de deam dataset bevat.
    - **supercollider**: Map die wav-files van gemaakte opnames met FoxDot bevat.
    - **snd**: Map die alle mogelijke instrumentengeluiden/noten bevatten die FoxDot gebruikt om muziek te maken. 
- **features_data**:
    - **plots**: Map met de plots van de features en de annotatie van het lookup-model
    - **data_...csv**: CSV-bestand met de gevonden muziekfeatures uit een bepaalde map van 'audiofiles'. 
    - **data_...xlsx**: Excel-bestand met de gevonden muziekfeatures uit een bepaalde map van 'audiofiles'. 
    - **anno_...csv**: CSV-bestand met gevonden annotatie voor nummers uit een bepaalde map van 'audiofiles' met behulp van het lookup-model.
    - **anno_...xlsx**: Excel-bestand met gevonden annotatie voor nummers uit een bepaalde map van 'audiofiles' met behulp van het lookup-model.
    - **info_anno_supercollider**: Bijkomende informatie over de gevonden annotatie per muzieknummer ter functie van de deam dataset bij het lookup-model.
- **model_data**:
    - **plots**: Map met de plots van de annotatie van het MLP-regressormodel samen met een heatmap van het tempo en de histogrammen van de verschillen van beide modellen.
    - **anno_pred_supercollider.csv**: CSV-bestand met gevonden annotatie voor nummers met behulp van het MLP-regressormodel.
    - **dataset_...csv**: Gecombineerd CSV-bestand van features en annotaties van een bepaalde dataset om het MLP-regressormodel te trainen of laten voorspellen.  

## Installatie

Het project gebruikt python 3.7

Supercollider dient geïnstalleerd te worden op de pc als onafhankelijk programma. Link onderaan te vinden:\
https://supercollider.github.io/download

Verder moet FoxDot ook worden geïnstalleerd.

De packages (zie versie controle) kunnen geïnstalleerd worden met pip:

    pip install -r requirements.txt
    pip install FoxDot
    
In dit project worden opgenomen instrumenten gebruikt. Hiervoor worden de originele geluiden van FoxDot overschreven.
Om dit te doen worden twee mappen op volgende locatie met elkaar vervangen:
- C:\\...\MP2020_MIR_Laurens\code\audiofiles\snd
- C:\\...\MP2020_MIR_Laurens\venv\Lib\site-packages\FoxDot\snd

Dit laatste pad werkt uiteraard enkel indien een virtual environment wordt aangemaakt. Bovendien worden de audiofiles niet op
 Github geplaatst door de ongepaste grootte. 

## Gebruik

FoxDot en SuperCollider communiceren met elkaar over localhost. Het is dus belangrijk om beide programmas samen te laten runnen.

**SuperCollider**

- Open in SuperCollider het bestand: '**SuperCollider_startup.scd**'
- Installeer FoxDot door te Shift-Enteren op: Quarks.install("FoxDot")
- Shift-Enter op: 'FoxDot.start'

**FoxDot**

- Run het hoofdbestand en volg de instructies:
    
        python main.py
        
    
## Versie controle

OS: Windows 8

IDE: JetBrains Pycharm 2019.2.2 (Professional Edition)

Python 3.7

Packages
- numpy
- matplotlib
- librosa
- scipy
- FoxDot
- pandas
- scikit-learn
- openpyxl
- pillow
- xlrd
