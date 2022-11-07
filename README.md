# CO2-Guardian polkadot_hackathon
En este repositorio está todo el código para la participación en la hackaton Polkadot, la información del hardware que se diseño las tecnologías y el front

![](/home/oscar/GitHub/polkadot_hackathon/img/logo_hack.png)

## How does it work?
The solution is to create an IoT device that measures the concentration of CO2 (carbon monoxide) this device is connected to the blockchain network, once the target value of less than 820 ppm (parts per million) is exceeded, it will be deducted from the grand account to stake account, the idea is that those involved have an incentive to improve their carbon footprint and the information that may have value for those interested in measuring their environmental impact. This device in the future may be on bicycles and cars to include geolocation and create carbon monoxide concentration maps.

![](/home/oscar/GitHub/polkadot_hackathon/img/cover.jpg)

## ¿Cómo funciona?
La solución consiste en crear un dispositivo IoT que mide concentración de CO2 (monoxido de carbono) y este dispositivo se conecta a la red la blockchain, vez que se supere el valor objetivo de menos de 820 ppm (partes por millón) se descontará de la cuenta de grand a la cuenta de stake, la idea es que los implicados tengan un incentivo para mejorar su huella de carbono y la información pueda tener valor para los interesados en medir su impacto ambiental. Este dispositivo en un futuro puede estar en bicicletas y automóviles para incluir la geolocalización y crear mapas de concentración de monóxido de carbono.



## Hardware
El microcontrolador que se utilizó es una ESP32 por su bajo consumo de energía y que tiene incorporado conexión wifi, para medir el nivel de CO2 se utilizó un sensor MQ135 conectado a una de las entradas analógicas.

![](/home/oscar/GitHub/polkadot_hackathon/img/sensor.jpg)

* ESP32: <https://github.com/FablabTorino/AUG-Torino/wiki/Wemos-Lolin-board-(ESP32-with-128x64-SSD1306-I2C-OLED-display)>
* MQ135: <https://components101.com/sensors/mq135-gas-sensor-for-air-quality>

## Software
Todo el backend de la aplicación esta construido en python utilizando la libreria <https://github.com/polkascan/py-substrate-interface> para la conexion a la blockchain, fastAPI para crear los endpoint, el front esta construido con Boodstrap y la red de prueba que se utiliza es Westend

## Infraestructura
La aplicación utiliza una instancia de EC2 de la capa gratuita de AWS y una base de datos SQL RDS de AWS también en la capa gratuita.

## Video demo
El demo se puede ver en: <https://www.youtube.com/watch?v=cNkNyK1RYA0>

### Musica de fondo:
<https://www.youtube.com/watch?v=2lMLPkcBBd0&list=PLtoBum7gx6vG5qc1hTuMMODKEUWlHdDyo&index=24>
