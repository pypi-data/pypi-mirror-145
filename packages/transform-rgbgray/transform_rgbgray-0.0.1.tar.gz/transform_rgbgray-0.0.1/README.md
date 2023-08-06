# Pacote: image_transform_rgbgray

Pacote desenvolvido a partir de um desafio de projeto na [DIO](https://digitalinnovation.one/). 
O pacote lê uma imagem, as transforma tingindo-as na cor especificada e salva. As imagens podem ser tingidas nas seguintes cores:
- Cinza;
- Vermelho;
- Azul;
- Amarelo;
- Verde.

## 🛠 Tecnologia
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />

## Instalação

```bash
pip install image_transform_rgbgray
```

## Uso

```python
from image_transform_rgbgray.processing import transformation
from image_transform_rgbgray.utils import io

image = io.read_image(path_image)
transformation.gray(image)
transformation.red(image)
transformation.blue(image)
transformation.yellow(image)
transformation.green(image)
```

## Author
Jorge Magno

### Contato:
[<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/jorge-magno-l-moraes-381a19174/) 
[<img src = "https://img.shields.io/badge/instagram-%23E4405F.svg?&style=for-the-badge&logo=instagram&logoColor=white">](https://www.instagram.com/jorgepierrot/?hl=pt-br) 
[<img src = "https://img.shields.io/badge/facebook-%231877F2.svg?&style=for-the-badge&logo=facebook&logoColor=white">](https://www.facebook.com/jorge.magno.7)
