import streamlit as st
import pywinpty
import threading

# Function to run a command using pywinpty
def run_command(command):
    output_lines = []

    # Create a pseudo-terminal
    master, slave = pywinpty.PtyProcess.spawn(['cmd.exe', '/k', command])

    # Read output from the pseudo-terminal
    def read_output():
        while True:
            try:
                output = master.read(1)
                if output:
                    output_lines.append(output.decode('utf-8'))
                    st.session_state["output"] = "".join(output_lines)
                else:
                    break
            except EOFError:
                break

    thread = threading.Thread(target=read_output, daemon=True)
    thread.start()
    thread.join()

# Streamlit app layout
st.title("Streamlit App with pywinpty")
st.write("Run commands interactively in a pseudo-terminal!")

# Command input
command = st.text_input("Enter a command to run (e.g., `echo Hello World`):")

# Run the command when the button is clicked
if st.button("Run Command"):
    if command.strip():
        st.session_state["output"] = ""
        run_command(command)
    else:
        st.warning("Please enter a valid command.")

# Display output
if "output" in st.session_state:
    st.text_area("Command Output", st.session_state["output"], height=300)
