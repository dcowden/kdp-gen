from config import KDP_CONSTANTS

MM_PER_INCH = 25.4
CM_PER_INCH = 2.54

class Cursor:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def inc_x(self,dx):
        self.x = self.x + dx
    
    def inc_y(self,dy):
        self.y = self.y + dy

    def copy(self):
        return Cursor(self.x,self.y)

class Rect:
    def __init__(self,lower_left=(0,0),size=None,upper_right=None):
        self.lower_left = lower_left
        if upper_right is None and size is None:
            raise ValueError("Must provide size or upper corner")
        
        if upper_right is not None:
            self.upper_right = upper_right
        else:
            self.upper_right = ( self.lower_left[0]+size[0], self.lower_left[1] + size[1])
    
    @property
    def w(self):
        return self.ux - self.lx
    
    @property
    def h(self):
        return self.uy - self.ly
    @property
    def lx(self):
        return self.lower_left[0]
    
    @property
    def ly(self):
        return self.lower_left[1]

    @property
    def ux(self):
        return self.upper_right[0]
    
    @property
    def uy(self):
        return self.upper_right[1]

    def size(self):
        return ( 
            self.upper_right[0] - self.lower_left[0],
            self.upper_right[1] - self.lower_left[1]
        )
    
    def grow(self,top=0,bottom=0,left=0,right=0):
        return Rect( 
            lower_left=(self.lower_left[0] - left,self.lower_left[1] - top),
            upper_right=(self.upper_right[0] + right,self.upper_right[1] + bottom),
        )


    def relative_to(self,rect):
        return Rect(
            lower_left=(
                self.lower_left[0] + rect.lower_left[0],
                self.lower_left[1] + rect.lower_left[1]
            ),
            size=rect.size()
        )

    def at(self,x,y):
        return (self.lower_left[0] + x, self.lower_left[1]+y)  

    def __str__(self):
        return str(self.lower_left) + "<-->" + str(self.upper_right) + \
              ",ux=" + str(self.ux) +",uy=" + str(self.uy)    \
              + ",lx=" + str(self.lx) + ",ly=" + str(self.ly)

def compute_font_height_from_points(unit, val_pts):
    val_inches = val_pts/72
    if unit == 'mm':
        return val_inches*MM_PER_INCH
    elif unit == 'cm':
        return val_inches*CM_PER_INCH
    elif unit == 'in':
        return val_inches
    else:
        raise ValueError("unknown unit '" + unit + "'")

def font_point_to_in(font_points):
    return font_points/72

def font_in_to_point(font_inches):
    return 72*font_inches

def set_line_options(pdf, line_options):
    pdf.set_line_width(line_options["width"])
    if line_options["dash_pattern"] == 0.0:
        pdf.set_dash_pattern()
    else:
        pdf.set_dash_pattern(
            dash=line_options["dash_pattern"][0],
            gap=line_options["dash_pattern"][1]
        )
    pdf.set_draw_color(line_options["color"])

def calculate_layout(pdf_page, grid_options):
    whole_page = Rect(lower_left=(0,0),size=(pdf_page.epw,pdf_page.eph))

    conversion_factor = 1.0
    units = grid_options["unit"]
    if units == 'mm':
        conversion_factor = 25.4
    elif units == 'cm':
        conversion_factor = 2.54
    else:
        conversion_factor = 1.0        

    if grid_options["orientation"] == "landscape":
        printable = whole_page.grow(
            top=-KDP_CONSTANTS.GUTTER_IN*conversion_factor,
            bottom=-KDP_CONSTANTS.MARGIN_IN*conversion_factor,
            left=-KDP_CONSTANTS.MARGIN_IN*conversion_factor,
            right=-KDP_CONSTANTS.MARGIN_IN*conversion_factor
        )    
    else:
        printable = whole_page.grow(
            top=-KDP_CONSTANTS.MARGIN_IN*conversion_factor,
            bottom=-KDP_CONSTANTS.MARGIN_IN*conversion_factor,
            left=-KDP_CONSTANTS.GUTTER_IN*conversion_factor,
            right=-KDP_CONSTANTS.MARGIN_IN*conversion_factor
        )

    def get_title_block_height(grid_options):
        if len(grid_options["titleBlock"]) > 0:
            block_height =  grid_options["titleBlockHeight"] 
            return block_height
        else:
            return 0.0
    
    def get_label_space(grid_options):
        if len(grid_options["gridLabels"]) > 0:
            return ( 
                grid_options["gridLabelWidth"],font_point_to_in(grid_options["gridLabelFontPoints"])
            )
        else:
            return (0,0)
    
    grid_area = printable.grow(bottom=-get_title_block_height(grid_options))

    label_space=get_label_space(grid_options)

    grid_area = grid_area.grow(left=-label_space[0], top=-label_space[1])
    y_minor_height = grid_options["y_axis"]["minor"]["width"]
    x_minor_height = grid_options["x_axis"]["minor"]["width"]
    y_slack_height = grid_area.h % y_minor_height
    x_slack_height = grid_area.w % x_minor_height
    grid_area = grid_area.grow(bottom=(-1*y_slack_height),right=(-1*x_slack_height))


    return (grid_area,printable)