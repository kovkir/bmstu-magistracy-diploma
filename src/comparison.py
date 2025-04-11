from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox

from constants import CompressionMethods


def plot_graph(image_paths, compression_rates):
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.canvas.manager.set_window_title("Выпускная квалификационная работа (Ковалец Кирилл ИУ7-42М)")
    plt.subplots_adjust(bottom=0.3)
    plt.title("Сравнение методов сжатия изображений")

    x_positions = range(len(image_paths))

    ax.plot(
        x_positions, 
        compression_rates[CompressionMethods.HYBRID], 
        '-o',
        label='Гибридный метод'
    )
    ax.plot(
        x_positions, 
        compression_rates[CompressionMethods.HUFFMAN], 
        '--o',
        label='Метод Хаффмана'
    )
    ax.plot(
        x_positions, 
        compression_rates[CompressionMethods.LZW], 
        '-.o',
        label='Метод LZW'
    )

    ax.grid(True)
    ax.legend()
    ax.set_ylabel('Степень сжатия (%)')
    ax.set_xlabel('Изображения (названия)')

    ax.set_xticks(x_positions)
    ax.set_xticklabels([img.split('/')[-1] for img in image_paths])

    ax.set_ylim(0, 100)
    ax.set_xlim(-1, len(image_paths))

    for i, image_path in enumerate(image_paths):
        img = Image.open(image_path)
        img.thumbnail((300, 300))
        imagebox = offsetbox.AnnotationBbox(
            offsetbox=offsetbox.OffsetImage(img, zoom=0.3),
            xy=(i, 0),
            xybox=(i, -30),
            frameon=False,
        )
        ax.add_artist(imagebox)

    plt.show()
