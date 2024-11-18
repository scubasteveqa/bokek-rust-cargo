from bokeh.layouts import column
from bokeh.models import Button, PreText
from bokeh.plotting import curdoc
import pywinpty
import threading
import numpy as np

if not hasattr(np, 'bool8'):
    np.bool8 = np.bool


# Bokeh elements
output_display = PreText(text="Output will appear here", width=500, height=300)
run_command_button = Button(label="Run Command", button_type="success")

def run_command():
    # Function to run a command using pywinpty and display output in the Bokeh app
    output_display.text = "Starting command...\n"

    # Create a pseudo-terminal
    master, slave = pywinpty.PtyProcess.spawn(['cmd.exe', '/k', 'echo Hello, Bokeh with pywinpty!'])

    # Read and update the output in a separate thread
    def update_output():
        while True:
            try:
                output = master.read(1)
                if output:
                    output_display.text += output.decode('utf-8')
                else:
                    break
            except EOFError:
                break

    threading.Thread(target=update_output, daemon=True).start()

# Set up the button click event
run_command_button.on_click(run_command)

# Layout
curdoc().add_root(column(run_command_button, output_display))
curdoc().title = "Bokeh App with pywinpty"
