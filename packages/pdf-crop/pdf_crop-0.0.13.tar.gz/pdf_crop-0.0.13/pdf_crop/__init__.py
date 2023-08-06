from rich.console import Console
from rich.table import Table
from pdf_crop.crop_pymupdf import PymuPDFCrop
from pdf_crop.helper import rect_str


def crop(input_file, page_option: list):
    table = Table(title="PDF Crop Summary", leading=0)
    table.add_column("Page No.", justify="right", style="cyan", no_wrap=True)
    table.add_column("MediaBox", justify="right", style="magenta")
    table.add_column("CropBox", justify="right", style="magenta")
    table.add_column("Output", justify="right", style="green")

    space, threshold = (5, 0.008)
    for option in page_option:
        page_no, output_file = option[:2]
        if len(option) > 2:
            space = option[2]
        if len(option) > 3:
            space = option[3]
        pdf_crop = PymuPDFCrop(input_file=input_file, space=space, threshold=threshold)
        output_file, media_box, crop_box = pdf_crop.crop(page_no, output_file=output_file, crop_box=None)
        table.add_row(str(option[0]), rect_str(media_box), rect_str(crop_box), output_file)
    # Show summary
    console = Console()
    console.print(table)