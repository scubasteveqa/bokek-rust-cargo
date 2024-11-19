from bokeh.layouts import column
from bokeh.models import Button, PreText, TextInput
from bokeh.plotting import curdoc
import rust_bokeh

# Initialize Bokeh widgets
command_input = TextInput(title="Enter Command", placeholder="e.g., echo Hello from Rust!")
output_display = PreText(text="Output will appear here", width=600, height=300)
run_button = Button(label="Run Command", button_type="success")

# Function to execute the Rust command
def run_command():
    command = command_input.value.strip()
    if not command:
        output_display.text = "Please enter a valid command."
        return

    try:
        output = rust_bokeh.run_command(command)
        output_display.text = f"Command: {command}\n\nOutput:\n{output}"
    except Exception as e:
        output_display.text = f"Error: {str(e)}"

# Set up the button click callback
run_button.on_click(run_command)

# Layout and add to document
layout = column(command_input, run_button, output_display)
curdoc().add_root(layout)
curdoc().title = "Bokeh App with Rust Integration"
