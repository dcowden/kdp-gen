"""
NiceGUI v2 app: custom graph-paper generator with PDF preview.
Left column: options, Right column: preview fills remaining space.
Persistent iframe using ui.html to avoid freezing browser.
"""

from __future__ import annotations
import json, os, tempfile, time
from copy import deepcopy
from typing import Any, Dict, Tuple
from nicegui import ui, app as asgi_app
from notebook import make_notebook_page
import config as cfg

# ------------------ Presets ------------------ #
PRESETS = {
    name: deepcopy(getattr(cfg, name))
    for name in dir(cfg)
    if name.startswith('GRID_OPTIONS_') and isinstance(getattr(cfg, name), dict)
}
if not PRESETS:
    raise RuntimeError('No presets found in config.py')

working_config = deepcopy(next(iter(PRESETS.values())))
selected_preset_name = next(iter(PRESETS))
preview_path = None

# ------------------ Helpers ------------------ #
def is_number(x): return isinstance(x, (int,float)) and not isinstance(x,bool)
def parse_tuple(text:str) -> Tuple[float,...]:
    s=text.strip().replace('(', '').replace(')', '').replace('[','').replace(']','').replace('x',',').replace('X',',')
    return tuple(float(p.strip()) for p in s.split(',') if p.strip())
def tuple_to_str(t): return ', '.join(str(x) for x in t)
def deep_set(d,path,value):
    cur=d
    for key in path[:-1]: cur=cur[key]
    cur[path[-1]]=value

# ------------------ Form Builder ------------------ #
def build_field(key,value,path):
    with ui.row().classes('items-center gap-2'):
        ui.label(key).classes('font-medium min-w-[7rem]')
        if isinstance(value,bool):
            ui.switch(value=value,on_change=lambda e: deep_set(working_config,path,bool(e.value)))
        elif is_number(value):
            ui.number(value=value, step=(1 if isinstance(value,int) else 0.01), on_change=lambda e: deep_set(working_config,path,float(e.value)))
        elif isinstance(value,(tuple,list)) and value and all(isinstance(x,(int,float)) for x in value):
            ui.input(value=tuple_to_str(tuple(value)), on_change=lambda e: deep_set(working_config,path,tuple(parse_tuple(e.value))))
        elif isinstance(value,str):
            ui.input(value=value,on_change=lambda e: deep_set(working_config,path,e.value))
        elif isinstance(value,dict):
            with ui.expansion(key):
                for k,v in value.items():
                    build_field(k,v,(*path,k))
        else:
            ui.textarea(value=json.dumps(value), on_change=lambda e: deep_set(working_config,path,json.loads(e.value)))

def build_form(container):
    container.clear()
    with container:
        with ui.card().classes('p-4'):
            ui.label('Units').classes('text-sm font-semibold')
            unit_select = ui.toggle(options={'in':'Imperial (in)','mm':'Metric (mm)'},
                                    value=working_config.get('unit','in'))
            unit_select.on('change', lambda e: working_config.update({'unit':e.value}))
        for k,v in working_config.items():
            if k != 'unit': build_field(k,v,(k,))

# ------------------ PDF Preview ------------------ #
@asgi_app.get('/preview')
async def preview_pdf():
    from fastapi.responses import FileResponse
    if preview_path and os.path.exists(preview_path):
        return FileResponse(preview_path, media_type='application/pdf')
    return {'error':'No preview available'}

def refresh_preview(path):
    global preview_path
    preview_path = path
    iframe.content = f'<iframe src="/preview?ts={int(time.time()*1000)}" style="width:100%;height:100%;border:0;"></iframe>'

def generate_pdf(download=True):
    cfg_copy = deepcopy(working_config)
    ps = cfg_copy.get('pageSize')
    if isinstance(ps,str) and any(c in ps for c in ',xX()[]'):
        try: cfg_copy['pageSize'] = tuple(parse_tuple(ps))
        except: pass
    filename = filename_input.value or 'graph_paper.pdf'
    if not filename.lower().endswith('.pdf'): filename += '.pdf'
    tmp_path = tempfile.NamedTemporaryFile(delete=False,suffix='.pdf').name
    try:
        make_notebook_page(cfg_copy,tmp_path)
        if download:
            ui.download(tmp_path, filename=filename)
            ui.notify('PDF generated!',type='positive')
        else:
            refresh_preview(tmp_path)
            ui.notify('Preview updated',type='info')
    except Exception as e:
        ui.notify(f'Generation failed: {e}', type='negative')
        if os.path.exists(tmp_path): os.remove(tmp_path)

# ------------------ UI Layout ------------------ #
ui.page_title('Custom Graph Paper')

with ui.header().classes('bg-white/80 backdrop-blur border-b border-gray-200'):
    ui.label('Graph Paper Generator').classes('text-lg md:text-2xl font-semibold py-2 px-3')

# Main container: full viewport minus header
with ui.row().style('height: calc(100vh - 64px); gap: 12px;').classes('w-full'):

    # Left column: options
    with ui.column().style('flex: 0 0 400px;') as left_col:
        with ui.card().classes('w-full p-4'):
            ui.label('Preset & Overrides').classes('text-base md:text-lg font-semibold')
            with ui.row().classes('items-center gap-3 w-full'):
                preset_select = ui.select(options=sorted(PRESETS.keys()), value=selected_preset_name).props('outlined dense')
                filename_input = ui.input(value='graph_paper.pdf').props('outlined').classes('grow')
            form_container = ui.column().classes('w-full gap-2')
            build_form(form_container)
        with ui.card().classes('w-full p-4'):
            ui.label('Actions').classes('text-base md:text-lg font-semibold')
            with ui.row().classes('gap-2'):
                generate_btn = ui.button('Download PDF', icon='download')
                preview_btn = ui.button('Preview PDF', icon='visibility')

    # Right column: preview
    with ui.column().style('flex: 1 1 auto;height:100%;') as right_col:
        #iframe = ui.iframe('/preview')
        iframe = ui.html('<iframe src="/preview" style="border:0;"></iframe>').classes('w-full h-full')

# ------------------ Event Handlers ------------------ #
generate_btn.on('click', lambda: generate_pdf(download=True))
preview_btn.on('click', lambda: generate_pdf(download=False))
preset_select.on('change', lambda e: (working_config.update(deepcopy(PRESETS[e.value])), build_form(form_container)))

# ------------------ Run App ------------------ #
app = asgi_app
if __name__ in {"__main__","__mp_main__"}:
    ui.run(host='127.0.0.1', port=5000, title='Graph Paper Generator')
