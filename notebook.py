from fpdf import FPDF
from datetime import datetime
from layout import Cursor,Rect,calculate_layout,KDP_CONSTANTS,set_line_options
from page_components import *
from config import *
import os.path
import copy
import numpy as np
import math
from collections import namedtuple

# TODO:
# factor line logic
# isometric for the whole page?
# configure isometric location and size
#configure isometric border

# see https://py-pdf.github.io/fpdf2/fpdf/fpdf.html#fpdf.fpdf.FPDF

def make_notebook_page(grid_options,out_file_path):
    GRID_OPTIONS=grid_options

    pdf = FPDF(
        orientation=GRID_OPTIONS["orientation"],
        unit=GRID_OPTIONS["unit"],
        format=GRID_OPTIONS["pageSize"]
    )
    

    pdf.add_page()
    pdf.set_margin(0)
    #pdf.set_margins(0,0,0)
    GRAY=(250,250,250)
    pdf.set_page_background(GRAY)

    pdf.set_creator(GRID_OPTIONS["creator"])
    pdf.set_lang("English")
    pdf.set_creation_date(datetime.now())
    pdf.set_draw_color(0)
    
    grid_area, printable = calculate_layout(pdf,GRID_OPTIONS)

    make_graph_grid(grid_area,pdf,GRID_OPTIONS)    
    make_frame(pdf,GRID_OPTIONS["thickLine"],grid_area)
    
    make_title_block(pdf,GRID_OPTIONS,grid_area)

    ##iso grid
    if GRID_OPTIONS['isometric']['enabled'] == True:
        make_iso_grid(grid_area,pdf, GRID_OPTIONS)

    watermark(pdf)
    make_page_number(pdf, grid_area,GRID_OPTIONS,1)
    pdf.output(out_file_path)


def make_pdf_test_pages():

    def generate_pathname(grid_options):
        if grid_options['isometric']['enabled']:
            iso='iso'
        else:
            iso = 'noiso'

        filename = "_".join([
            str(grid_options["pageSize"]),
            grid_options["orientation"],
            grid_options["unit"],
            iso,
            ".pdf"
            ])
        return os.path.join('output',filename)
    

    landscape_letter = GRID_OPTIONS_LETTER_IN
    portrait_metric = GRID_OPTIONS_A4_CM
    portrait_6x9_in = GRID_OPTIONS_6x9_IN

    letter_portrait =copy.deepcopy(landscape_letter)
    letter_portrait["orientation"] = 'portrait'

    landscape_a4 =copy.deepcopy(portrait_metric)
    landscape_a4["orientation"] = 'landscape'

    landscape_6x9_in =copy.deepcopy(portrait_6x9_in)
    landscape_6x9_in["orientation"] = 'landscape'

    landscape_letter_with_iso = copy.deepcopy(landscape_letter)
    landscape_letter_with_iso["isometric"]["enabled"] = True
    
    test_cases = [
        landscape_letter,
        portrait_metric,
        portrait_6x9_in,
        letter_portrait,
        landscape_a4,
        landscape_6x9_in,
        landscape_letter_with_iso
    ]

    for t in test_cases:
        make_notebook_page(t,generate_pathname(t))
    

if __name__ == "__main__":
  
    make_pdf_test_pages()