# ReadMe

> Bu proje retina görüntüsünü alır ve sırsı ile

* Resmi gray yap
* Binary ye çevir
* Thinning yap
* Graph çıkar
* Graph localdeki ile benzetime sokar



- **`Dosya Yapısı`**
    - **ImageToGraph**
      - [imageToBinary](#imageToGraph)  
      - [gou_hall_Thinning](#thinnig)
      - [ToGraph](#toGraph)
      - [gabolFilter](#gabolFilter)
      - [Utility](#utility)
    - **Similarty**
      - [CosSimilarty](#CosSimilarty)
      - _FactorySimilarty_
      - [Eigenvector](#Eigenvector)
    


## imageToGraph
gri resmi alıp onu binaryi ye çevirir, kodun orjinal kaynağı aşağıdaki linktedir. 
![image](https://github.com/cantek41/RetinaRecognition/blob/master/image/A01_1.jpg){:height="100px" width="100px"}
![image](https://github.com/cantek41/RetinaRecognition/blob/master/image/A01_1_bloodvessel.png) 
[kaynak](https://github.com/getsanjeev/retina-features/blob/master/bloodvessels.py)

## thinnig
binary image ın iskeletini çıkartır
![image](https://github.com/cantek41/RetinaRecognition/blob/master/image/graphh.png)

[kaynak](https://github.com/tastyminerals/thinning_py3)

## toGraph
![image](https://github.com/cantek41/RetinaRecognition/blob/master/image/wwwsde.png)

ToGraph : burada iskeleti çıkartılmış resim üzerindeki vertexler bulunur
minutiae_at algoritması kullanılır
[kaynak](https://github.com/rtshadow/biometrics/blob/master/crossing_number.py)

## gabolFilter
![image](https://github.com/cantek41/RetinaRecognition/blob/master/image/wwwsd.png)

Vertexleri bulunmuş olan Graph ın edge lerini belirler
[kaynak](http://scikit-image.org/docs/dev/auto_examples/edges/plot_skeleton.html#sphx-glr-auto-examples-edges-plot-skeleton-py)

## utility
Graphı image gibi konumlandılmış şeklinde export etmeyi sağlar.
[kaynak](https://github.com/05dirnbe/nefi.git)

## CosSimilarty
İki grafın kosinus benzerliğini bulur

## Eigenvector
İki grafın Eigenvector benzerliğini bulur 


# Gereksinimler
* pip install networkx==1.9
* pip install thinning_py3
* pip install -U scikit-image
* pip install opencv-python
* pip install numpy
* pip install matplotlib

Cantekin Çelihası
