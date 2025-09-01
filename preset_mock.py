#!/usr/bin/env python3

from nicegui import ui

# Global variables to store current settings
line_settings = {
    'weight': 2,
    'color': '#000000',
    'dash': 'solid'
}

font_settings = {
    'family': 'Arial',
    'size': 16
}

# Available options
DASH_TYPES = {
    'solid': '',
    'dashed': '5,5',
    'dotted': '2,3',
    'dash-dot': '5,5,2,5',
    'long-dash': '10,5'
}

FONT_FAMILIES = [
    'Arial', 'Times New Roman', 'Courier New', 'Helvetica',
    'Georgia', 'Verdana', 'Comic Sans MS', 'Impact'
]


def get_css_dash_style(dash_type):
    """Convert our dash type to CSS border style"""
    dash_map = {
        'solid': 'solid',
        'dashed': 'dashed',
        'dotted': 'dotted',
        'dash-dot': 'dashed',
        'long-dash': 'dashed'
    }
    return dash_map.get(dash_type, 'solid')


# Create the UI
@ui.page('/')
def main_page():
    ui.label('Font and Line Picker Demo').classes('text-2xl font-bold mb-4')

    with ui.row().classes('w-full gap-8'):
        # Line picker section
        with ui.column():
            ui.label('Line Properties').classes('text-xl font-semibold mb-3')

            # Line weight slider
            with ui.row().classes('items-center gap-4 mb-3'):
                ui.label('Weight:')
                weight_slider = ui.slider(min=1, max=20, value=line_settings['weight'])
                weight_label = ui.label(f"{line_settings['weight']}px")

            # Line color picker
            with ui.row().classes('items-center gap-4 mb-3'):
                ui.label('Color:')
                color_picker = ui.color_input(value=line_settings['color'])

            # Dash type selector
            with ui.row().classes('items-center gap-4 mb-3'):
                ui.label('Style:')
                dash_select = ui.select(
                    options=list(DASH_TYPES.keys()),
                    value=line_settings['dash']
                )

            # Line preview
            ui.label('Preview:').classes('font-semibold mt-4 mb-2')
            line_preview = ui.html('')

        # Font picker section
        with ui.column().classes('flex-1'):
            ui.label('Font Properties').classes('text-xl font-semibold mb-3')

            # Font family selector
            with ui.row().classes('items-center gap-4 mb-3'):
                ui.label('Family:').classes('w-16')
                font_select = ui.select(
                    options=FONT_FAMILIES,
                    value=font_settings['family']
                ).classes('flex-1')

            # Font size slider
            with ui.row().classes('items-center gap-4 mb-3'):
                ui.label('Size:').classes('w-16')
                size_slider = ui.slider(
                    min=8, max=48, value=font_settings['size']
                )
                size_label = ui.label(f"{font_settings['size']}px").classes('w-12')

            # Font preview
            ui.label('Preview:').classes('font-semibold mt-4 mb-2')
            font_preview = ui.html(
                '<div style="padding: 20px; border: 1px solid #ccc; background: white; min-height: 60px; display: flex; align-items: center; font-family: Arial; font-size: 16px;">The quick brown fox jumps over the lazy dog. 1234567890</div>')

    # Combined preview section
    ui.separator().classes('my-8')
    ui.label('Combined Preview').classes('text-xl font-semibold mb-3')

    with ui.card().classes('w-full p-4'):
        combined_preview = ui.html(
            '<div style="font-family: Arial; font-size: 16px; color: #000000; border-bottom: 2px solid #000000; padding-bottom: 10px;">Sample text with custom styling</div>')

    # Settings display
    ui.separator().classes('my-8')
    ui.label('Current Settings').classes('text-xl font-semibold mb-3')

    with ui.card().classes('w-full p-4'):
        line_settings_label = ui.label(
            f"Line: {line_settings['weight']}px {line_settings['dash']} {line_settings['color']}")
        font_settings_label = ui.label(f"Font: {font_settings['family']}, {font_settings['size']}px")

    def update_line_preview():
        """Update the line preview SVG"""
        dash_pattern = DASH_TYPES[line_settings['dash']]
        dash_attr = f'stroke-dasharray="{dash_pattern}"' if dash_pattern else ''

        svg_content = f'''<svg width="300" height="60" style="border: 1px solid #ccc; background: white;">
            <line x1="20" y1="30" x2="280" y2="30" 
                  stroke="{line_settings['color']}" 
                  stroke-width="{line_settings['weight']}"
                  {dash_attr} />
        </svg>'''
        line_preview.content = svg_content

    def update_font_preview():
        """Update the font preview"""
        font_preview.content = f'''<div style="padding: 20px; border: 1px solid #ccc; background: white; min-height: 60px; display: flex; align-items: center; font-family: {font_settings['family']}; font-size: {font_settings['size']}px;">The quick brown fox jumps over the lazy dog. 1234567890</div>'''

    def update_combined_preview():
        """Update the combined preview"""
        combined_preview.content = f'''<div style="font-family: {font_settings['family']}; font-size: {font_settings['size']}px; color: {line_settings['color']}; border-bottom: {line_settings['weight']}px {get_css_dash_style(line_settings['dash'])} {line_settings['color']}; padding-bottom: 10px;">Sample text with custom styling</div>'''

    def update_settings_labels():
        """Update the settings display"""
        line_settings_label.text = f"Line: {line_settings['weight']}px {line_settings['dash']} {line_settings['color']}"
        font_settings_label.text = f"Font: {font_settings['family']}, {font_settings['size']}px"

    def update_all():
        """Update all previews and labels"""
        update_line_preview()
        update_font_preview()
        update_combined_preview()
        update_settings_labels()
        weight_label.text = f"{line_settings['weight']}px"
        size_label.text = f"{font_settings['size']}px"

    # Event handlers
    def on_weight_change():
        line_settings['weight'] = int(weight_slider.value)
        update_all()

    def on_color_change():
        line_settings['color'] = color_picker.value
        update_all()

    def on_dash_change():
        line_settings['dash'] = dash_select.value
        update_all()

    def on_font_change():
        font_settings['family'] = font_select.value
        update_all()

    def on_size_change():
        font_settings['size'] = int(size_slider.value)
        update_all()

    # Connect event handlers
    weight_slider.on_value_change(on_weight_change)
    color_picker.on_value_change(on_color_change)
    dash_select.on_value_change(on_dash_change)
    font_select.on_value_change(on_font_change)
    size_slider.on_value_change(on_size_change)

    # Initial update
    update_all()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Font and Line Picker Demo', port=8080, show=True)