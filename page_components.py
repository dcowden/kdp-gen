from fpdf import FPDF
from layout import set_line_options,font_point_to_in,Cursor,compute_font_height_from_points
from config import KDP_CONSTANTS
import math
import numpy as np

def make_page_number(pdf,grid_area,grid_options,page_number):
    pdf.set_font('helvetica', size=14,style="BI")
    cursor = Cursor( grid_area.ux,grid_area.uy)

    EXTRA_SPACE_FACTOR=1.0
    STD_PADDING = grid_options["standardPadding"]
    title_block_height = grid_options["titleBlockHeight"]
    page_block_width = grid_options["pageBlockWidth"]

    pdf.set_xy(grid_area.ux-page_block_width-STD_PADDING,grid_area.uy+STD_PADDING)

    pdf.cell(
        text=str(page_number),
        w=page_block_width*EXTRA_SPACE_FACTOR,
        h=title_block_height*EXTRA_SPACE_FACTOR,
        border=0,
        fill=False,
        align="R"
    )   

def watermark(pdf):
    pdf.set_font('helvetica',size=72,style="BI")
    with pdf.local_context(fill_opacity=0.3, stroke_opacity=0.5):
        pdf.set_fill_color((100,100,100))
        pdf.text(pdf.epw*.1,pdf.eph*.5,text="Demo Demo")

def make_frame(pdf,line_width,rect):
    #outer frame
    pdf.set_line_width(line_width)
    pdf.set_draw_color(0)
    pdf.set_dash_pattern()
    
    pdf.rect(rect.lx,rect.ly,rect.w,rect.h)

def make_title_block(pdf, grid_options, grid_area):

    cursor = Cursor( grid_area.ux,grid_area.uy)

    FONT_SIZE=grid_options["gridLabelFontPoints"]
    WIDTH=grid_options["pageBlockWidth"]
    TEXT_PAD=grid_options["standardPadding"]
    THICK_LINE=grid_options["thickLine"]
    HEIGHT = grid_options["titleBlockHeight"]
    consumed_width = 0
    if "P" in grid_options["titleBlock"]:
        consumed_width += WIDTH
        input_field(cursor,grid_options,pdf,"PAGE",width=WIDTH,height=HEIGHT,text_pad_in=TEXT_PAD,font_size_pt=FONT_SIZE)

    if "N" in grid_options["titleBlock"]:
        consumed_width += WIDTH
        input_field(cursor,grid_options,pdf,"NEXT>",width=WIDTH,height=HEIGHT,text_pad_in=TEXT_PAD,font_size_pt=FONT_SIZE)

    if "V" in grid_options["titleBlock"]:
        consumed_width += WIDTH
        input_field(cursor,grid_options,pdf,"PREV<",width=WIDTH,height=HEIGHT,text_pad_in=TEXT_PAD,font_size_pt=FONT_SIZE)

    if "D" in grid_options["titleBlock"]:
        date_field_width = grid_options["dateBlockWidth"]
        consumed_width += date_field_width
        input_field(cursor,grid_options,pdf,"DATE",width=date_field_width,height=HEIGHT,text_pad_in=TEXT_PAD,font_size_pt=FONT_SIZE)

    if "T" in grid_options["titleBlock"]:
        remaining_width = grid_area.w - consumed_width
        input_field(cursor,grid_options,pdf,"TITLE",width=remaining_width,height=HEIGHT,text_pad_in=TEXT_PAD,font_size_pt=FONT_SIZE)    


def make_iso_grid(grid_area, pdf, grid_options ):

    iso_options = grid_options["isometric"]
    iso_minor_options = iso_options["minor"]
    iso_major_options = iso_options["major"]
    w = iso_options["width"] 
    h = iso_options["height"]

    cursor = Cursor( grid_area.ux - w, grid_area.ly)
    cursor_vlines = cursor.copy()

    pdf.set_fill_color(255)
    pdf.rect(x=cursor_vlines.x,y=cursor_vlines.y,w=w,h=h,style="FD")

    end_x = cursor_vlines.x + w
    end_y = cursor_vlines.y + h

    #vertical lines
    for x in np.arange(cursor_vlines.x,end_x,iso_minor_options["width"]):
        set_line_options(pdf,iso_minor_options["line_options"])
        pdf.line(cursor_vlines.x,cursor_vlines.y,x,end_y)
        cursor_vlines.inc_x(iso_minor_options["width"])        

    #isometric lines
    ht = iso_minor_options["width"]
    icursor = cursor.copy()
    tan30 = math.tan(math.radians(30))
    H=tan30*w
    W=icursor.x+w

    #righthand lines
    start_y = icursor.y-H 
    end_y = icursor.y + h 
    for y in np.arange(start_y,end_y,ht):
        if y < icursor.y:
            #lines cut off at top
            dy=(icursor.y-y)
            pdf.line(icursor.x+(dy/tan30),icursor.y,W,y+H)
            pdf.line(W-(dy/tan30),icursor.y,icursor.x,y+H)
        elif y < (end_y - H):
            #lines in full view                
            pdf.line(icursor.x,y,W,y+H)
            pdf.line(W,y,icursor.x,y+H)
        else:
            dy=end_y - y
            #lines cut off at bottom
            pdf.line(icursor.x,y,icursor.x+(dy/tan30),end_y)
            pdf.line(W,y,W-dy/tan30,end_y)


def make_graph_grid(grid_area,pdf, grid_options):

    (end_x, end_y) = (grid_area.ux,grid_area.uy)

    #x axis first
    x_options = grid_options["x_axis"]
    y_options = grid_options["y_axis"]
    x_minor_options = x_options["minor"]
    x_major_options = x_options["major"]
    y_minor_options = y_options["minor"]
    y_major_options = y_options["major"]
    initial_x, initial_y = (grid_area.lx,grid_area.ly)

    cursor = Cursor(initial_x,initial_y)
    BLEED_MAJORS=0

    #x lines
    for x in np.arange(cursor.x,end_x,x_minor_options["width"]):
        set_line_options(pdf,x_minor_options["line_options"])
        pdf.line(cursor.x,cursor.y,x,end_y)
        cursor.inc_x(x_minor_options["width"])

    cursor.x = initial_x
    line_count = 0
    major_width = x_minor_options["width"]*x_major_options["multiple"]
    LABEL_PADDING = grid_options["standardPadding"] 
    LABEL_WIDTH=grid_options["gridLabelWidth"]  
    LABEL_FONT_HEIGHT_PTS=grid_options["gridLabelFontPoints"]
    LABEL_HEIGHT=compute_font_height_from_points(grid_options['unit'],LABEL_FONT_HEIGHT_PTS)

    y_label_offset = LABEL_HEIGHT/2.0
    
    
    for x in np.arange(cursor.x,end_x,major_width):
        set_line_options(pdf,x_major_options["line_options"])

        pdf.line(cursor.x,cursor.y-BLEED_MAJORS,x,end_y+BLEED_MAJORS)

        if "H" in grid_options["gridLabels"] :
            pdf.set_font('helvetica', size=LABEL_FONT_HEIGHT_PTS,style="B")
            pdf.set_xy(cursor.x-LABEL_WIDTH,cursor.y-LABEL_HEIGHT-LABEL_PADDING)                
            if line_count > 0:
                label_format = x_major_options["labelFormat"]
                if x_major_options["labelValue"] == "MAJOR":
                    labeltext = label_format.format(int(line_count / x_major_options["multiple"]))
                else:
                    labeltext = label_format.format(line_count)
                pdf.cell(text=labeltext,border=False,align='R',fill=False,w=LABEL_WIDTH,h=LABEL_HEIGHT)

        cursor.inc_x(major_width)

        line_count += int(x_major_options["multiple"])

    cursor.x = initial_x

    #y lines
    for y in np.arange(cursor.y,end_y,y_minor_options["width"]):
        set_line_options(pdf,y_minor_options["line_options"])
        pdf.line(cursor.x,cursor.y,end_x,y)

        cursor.inc_y(y_minor_options["width"])

    cursor.y = initial_y
    line_count = 0
    major_width = y_minor_options["width"]*y_major_options["multiple"]


    y_label_offset = y_minor_options["width"]/2.0
    x_label_offset = 0.125
    for y in np.arange(cursor.y,end_y,major_width):
        set_line_options(pdf,y_major_options["line_options"])

        pdf.line(cursor.x-BLEED_MAJORS,cursor.y,end_x+BLEED_MAJORS,y)

        if "V" in grid_options["gridLabels"] :
            pdf.set_font('helvetica', size=6,style="B")
            pdf.set_xy(cursor.x-LABEL_WIDTH,cursor.y-LABEL_HEIGHT-LABEL_PADDING)
            if line_count > 0:
                label_format = y_major_options["labelFormat"]
                if y_major_options["labelValue"] == "MAJOR":
                    labeltext = label_format.format(int(line_count / y_major_options["multiple"]))
                else:
                    labeltext = label_format.format(line_count)                
                pdf.cell(text=labeltext,border=False,align='R',fill=False,w=LABEL_WIDTH,h=LABEL_HEIGHT)
        cursor.inc_y(major_width)

        line_count += int(y_major_options["multiple"])



def input_field(cursor,grid_options,pdf, text,width=0.5,height=0.375,text_pad_in=0.04,font_size_pt=10):
    THICK_LINE_INCHES=grid_options["thickLine"]
    cursor.inc_x(-width)
    pdf.set_line_width(THICK_LINE_INCHES)
    font_height = compute_font_height_from_points(grid_options["unit"],font_size_pt)
    y_loc = cursor.y + text_pad_in + font_height
    pdf.set_fill_color(255)
    pdf.set_dash_pattern()
    pdf.rect(w=width,h=height,x=cursor.x, y=cursor.y,style="FD")

    pdf.set_line_width(THICK_LINE_INCHES)
    pdf.set_font('helvetica', size=font_size_pt,style="B")
    pdf.set_text_shaping(True)
    pdf.text(text=text,x=cursor.x+ text_pad_in,y=y_loc)

