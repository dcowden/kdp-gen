class KDP_CONSTANTS:
    BLEED_IN=0.125
    MARGIN_IN=0.25
    GUTTER_IN=0.625

GRID_OPTIONS_A4_CM={
    "unit": "mm",
    "creator": "GridMaster",
    "pageSize": "A4",
    "standardPadding": 1.5,
    "orientation": "portrait", #landscape, portrait
    "gridLabels":"VH", #Vertical=V, horizontale=H
    "gridLabelWidth": 4.0,
    "gridLabelFontPoints": 6,
    "titleBlockHeight": 10,
    "dateBlockWidth": 20,
    "thickLine":0.8,
    "pageBlockWidth": 15,
    "titleBlock":"TDPNV", # Title=T, Date=D, Pagenum=P, NextPage=N, Prevpage=V
    "x_axis":{
        "minor":{
            "width":10,
            "line_options":{
                "color":(200,200,200),
                #"dash_pattern": (0.04, 0.04),
                "dash_pattern": 0,
                "width": 0.05
            }
        },
        "major":{
            "multiple": 5.0,
            "labelValue": "MINOR",  # MAJOR or MINOR
            "labelFormat": "{:3d}",            
            "line_options":{
                "color":(0,0,0),
                "dash_pattern": 0,
                "width": 0.005
            }                       
        }
    },
    "y_axis":{
        "minor":{
            "width":10,
            "line_options":{
                "color":(200,200,200),
                #"dash_pattern": (0.04, 0.04),
                "dash_pattern": 0,
                "width": 0.05
            }
        },
        "major":{
            "multiple": 5.0,
            "labelValue": "MINOR",  # MAJOR or MINOR 
            "labelFormat": "{:3d}",                       
            "line_options":{
                "color":(0,0,0),
                "dash_pattern": 0,
                "width": 0.05
            }                       
        }
    },
    "isometric":{
        "enabled": False,
        "width": 120.0,
        "height": 120.0,
        "minor":{
            "width":10,
            "line_options":{
                "color":(200,200,200),
                "dash_pattern": 0,
                "width": 0.05
            }
        },
        "major":{
            "multiple": 4.0,
            "line_options":{
                "color":(0,0,0),
                "dash_pattern": 0,
                "width": 0.05
            }                       
        }
    }    
}

GRID_OPTIONS_LETTER_IN={
    "unit": "in",
    "creator": "GridMaster",
    "pageSize": "letter",
    "standardPadding": 0.05,
    "orientation": "landscape", #landscape, portrait
    "gridLabels":"VH", #Vertical=V, horizontale=H
    "gridLabelWidth": 0.15,
    "thickLine": 0.03,
    "gridLabelFontPoints": 6,
    "titleBlockHeight": 0.375,
    "dateBlockWidth": 0.75,
    "pageBlockWidth": 0.5,
    "titleBlock":"TDPNV", # Title=T, Date=D, Pagenum=P, NextPage=N, Prevpage=V
    "x_axis":{
        "minor":{
            "width":0.25,
            "line_options":{
                "color":(200,200,200),
                "dash_pattern": (0.04, 0.04),
                #"dash_pattern": 0,
                "width": 0.005
            }
        },
        "major":{
            "multiple": 4.0,
            "labelValue": "MAJOR",  # MAJOR or MINOR
            "labelFormat": "{:3d}",
            "line_options":{
                "color":(0,0,0),
                #"dash_pattern": (0.04, 0.04),
                "dash_pattern": 0,
                "width": 0.005
            }                       
        }
    },
    "y_axis":{
        "minor":{
            "width":0.25,
            "line_options":{
                "color":(200,200,200),
                "dash_pattern": (0.04, 0.04),
                #"dash_pattern": 0,
                "width": 0.005
            }
        },
        "major":{
            "multiple": 4.0,
            "labelValue": "MAJOR",  # MAJOR or MINOR
            "labelFormat": "{:3d}",            
            "line_options":{
                "color":(0,0,0),
                "dash_pattern": 0,
                "width": 0.005
            }                       
        }
    },
    "isometric":{
        "enabled": False,
        "width": 4.0,
        "height": 3.0,
        "minor":{
            "width":0.25,
            "line_options":{
                "color":(200,200,200),
                #"dash_pattern": (0.1, 0),
                "dash_pattern": 0,
                "width": 0.005
            }
        },
        "major":{
            "multiple": 4.0,
            "line_options":{
                "color":(0,0,0),
                "dash_pattern": 0,
                "width": 0.005
            }                       
        }
    }    
}

GRID_OPTIONS_6x9_IN={
    "unit": "in",
    "creator": "GridMaster",
    "pageSize": (6,9),
    "standardPadding": 0.05,
    "orientation": "portrait", #landscape, portrait
    "gridLabels":"VH", #Vertical=V, horizontale=H
    "gridLabelWidth": 0.1,
    "thickLine": 0.03,
    "gridLabelFontPoints": 6,
    "titleBlockHeight": 0.375,
    "dateBlockWidth": 0.75,
    "pageBlockWidth": 0.5,
    "titleBlock":"TDPNV", # Title=T, Date=D, Pagenum=P, NextPage=N, Prevpage=V
    "x_axis":{
        "minor":{
            "width":0.25,
            "line_options":{
                "color":(200,200,200),
                "dash_pattern": (0.04, 0.04),
                #"dash_pattern": 0,
                "width": 0.005
            }
        },
        "major":{
            "multiple": 4.0,
            "labelValue": "MAJOR",  # MAJOR or MINOR
            "labelFormat": "{:3d}",
            "line_options":{
                "color":(0,0,0),
                #"dash_pattern": (0.04, 0.04),
                "dash_pattern": 0,
                "width": 0.005
            }                       
        }
    },
    "y_axis":{
        "minor":{
            "width":0.25,
            "line_options":{
                "color":(200,200,200),
                "dash_pattern": (0.04, 0.04),
                #"dash_pattern": 0,
                "width": 0.005
            }
        },
        "major":{
            "multiple": 4.0,
            "labelValue": "MAJOR",  # MAJOR or MINOR
            "labelFormat": "{:3d}",            
            "line_options":{
                "color":(0,0,0),
                "dash_pattern": 0,
                "width": 0.005
            }                       
        }
    },
    "isometric":{
        "enabled": False,
        "width": 4.0,
        "height": 4.0,
        "minor":{
            "width":0.25,
            "line_options":{
                "color":(200,200,200),
                #"dash_pattern": (0.1, 0),
                "dash_pattern": 0,
                "width": 0.005
            }
        },
        "major":{
            "multiple": 4.0,
            "line_options":{
                "color":(0,0,0),
                "dash_pattern": 0,
                "width": 0.005
            }                       
        }
    }    
}