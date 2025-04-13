from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox

from constants import CompressionMethods


def plot_comparison_graph(
    image_paths: list[str], 
    compression_rates: dict[CompressionMethods, list[float]],
) -> None:
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


def plot_comparison_bar_chart(
    image_sizes: list[int], 
    data_to_decompress_sises: list[int], 
    method: str,
) -> None:
    fig, ax = plt.subplots(figsize=(5.5, 6))
    fig.canvas.manager.set_window_title("Сравнение значений")
    plt.title("График сравнения размеров сжатого\n изображения с исходным")
    
    labels = ["Исходное изображение", f"Сжатое изображение\n({method})"]

    ax.bar(
        labels, 
        image_sizes, 
        label='Размер информации об изображении', 
    )
    ax.bar(
        labels, 
        data_to_decompress_sises, 
        bottom=image_sizes, 
        label='Размер информации для восстановления изображения',
    )

    ax.set_ylim(0, 119)
    ax.set_xticks(labels)
    ax.set_ylabel('Размер (в процентах от исходного файла)')
    ax.set_xlabel('Тип изображения (названия)')

    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.6, linestyle='--')

    plt.show()
