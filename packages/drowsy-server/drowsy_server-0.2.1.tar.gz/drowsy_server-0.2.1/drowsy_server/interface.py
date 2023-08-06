import dearpygui.dearpygui as dpg

from drowsy_server import version


def save_callback():
    print("Save Clicked")


def show_interface():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()
    with dpg.window(label=f"Drowsy Server {version}"):
        dpg.add_text("Hello world")
        dpg.add_button(label="Save", callback=save_callback)
        dpg.add_input_text(label="string")
        dpg.add_slider_float(label="float")
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
