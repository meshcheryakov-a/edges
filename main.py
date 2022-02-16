# Задание:
#
# Реализовать приложение, которое будет вполнять следующую последовательность действий:
# 1. Считать изображение по указанному пользователем пути,
# 2. Выполнить необходимое по варианту преобразование над ним с указанными пользователем параметрами,
# 3. Продемонстрировать исходное, преобразованное изображение и их гистрограммы,
# 4. Сохранить преобразованное изображение по указанному пользователем пути.
#
# Входные параметры:
# 1. Путь к исходному изображению,
# 2. Путь, по которому будет сохранено результирующее изображение,
# 3. Параметры, необходимые для выполнения заданного преобразования.
#
# Вариант №4: Выделение контуров
# Дополнительные параметры: Параметр, отвечающий за выбор алгоритма
#

# Считываем параметры в качестве аргументов командной строки с помощью argparse
import argparse
parser = argparse.ArgumentParser(description='Выделение контуров')
parser.add_argument('-i', '--input_file_path', type=str, help='Путь к исходному изображению', required=True)
parser.add_argument('-o', '--output_file_path', type=str, help='Путь, по которому будет сохранено результирующее изображение', required=True)
parser.add_argument('-a', '--algorithm', type=str, choices=['prewitt', 'sobel', 'roberts', 'scharr'], help='Параметр, отвечающий за выбор алгоритма', required=True)
args = parser.parse_args()

# Считываем изображение по указанному пользователем пути с помощью scikit-image
from skimage.io import imread, imsave
input_image = imread(args.input_file_path)

# Выделение контуров с помощью методов Prewitt/Sobel/Roberts/Scharr в зависимости от выбора пользователя
from skimage.filters import prewitt, sobel, roberts, scharr
from skimage.color import rgb2gray
output_image = []
if args.algorithm == 'prewitt':
    output_image = prewitt(rgb2gray(input_image))
elif args.algorithm == 'sobel':
    output_image = sobel(rgb2gray(input_image))
elif args.algorithm == 'roberts':
    output_image = roberts(rgb2gray(input_image))
elif args.algorithm == 'scharr':
    output_image = scharr(rgb2gray(input_image))
else:
    print('Неверный параметр --algorithm')

# Демонстрация исходного, преобразованного изображения и их гистограмм распределения яркостей
from matplotlib import pyplot as plt
from skimage.io import imshow, show
from skimage.exposure import histogram
fig = plt.figure(figsize=(10, 5))
fig.add_subplot(2, 2, 1)
imshow(input_image)
fig.add_subplot(2, 2, 2)
imshow(output_image)
fig.add_subplot(2, 2, 3)
hist_red, bins_red = histogram(input_image[:, :, 2])
hist_green, bins_green = histogram(input_image[:, :, 1])
hist_blue, bins_blue = histogram(input_image[:, :, 0])
plt.ylabel('Число отсчётов')
plt.xlabel('Значения яркости')
plt.title('Гистограмма распределения яркостей')
plt.plot(bins_red, hist_red, color='red', linestyle='-', linewidth=1)
plt.plot(bins_green, hist_green, color='green', linestyle='-', linewidth=1)
plt.plot(bins_blue, hist_blue, color='blue', linestyle='-', linewidth=1)
plt.legend(['red', 'green', 'blue'])
fig.add_subplot(2, 2, 4)
hist, bins = histogram(output_image)
plt.ylabel('Число отсчётов')
plt.xlabel('Значения яркости')
plt.title('Гистограмма распределения яркостей')
plt.plot(bins, hist, color='gray', linestyle='-', linewidth=1)
plt.legend(['gray'])
show()

# Сохраняем преобразованное изображение по указанному пользователем пути
import numpy as np
imsave(args.output_file_path, (output_image*255).astype(np.uint8))
