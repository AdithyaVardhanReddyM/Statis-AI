import streamlit as st
import pandas as pd
import replicate
import subprocess
import os
from PIL import Image

# Function to stream generated code directly from Replicate
def stream_data(input_data):
    code_events = []
    text_part = ""
    code_part = ""
    for event in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input=input_data
    ):
        code_events.append(event.data)

    # Join all events into a single string
    formatted_text = "".join(code_events)
    print(formatted_text)
    print(code_events)
    # Find the index of the code block
    start_idx = formatted_text.find("```python")
    end_idx = formatted_text.find("```", start_idx + 1)

    # Extract text and code parts
    if start_idx != -1 and end_idx != -1:
        text_part = formatted_text[:start_idx]
        code_part = formatted_text[start_idx + len("```python"):end_idx]


    # Display text part
    st.markdown(text_part)

    # Display code part if it exists and save to file
    if code_part:
        st.code(code_part, language='python')
        code_part += """
import matplotlib.pyplot as plt
import pandas as pd

# Save plots
for i in plt.get_fignums():
    plt.figure(i)
    plt.savefig(f'output_plot_{i}.png')

# Save DataFrame output to CSV
if 'df_output' in locals():
    df_output.to_csv('output_data.csv', index=False)
"""
        with open("generated_code.py", "w") as code_file:
            code_file.write(code_part)
        return code_part

# Function to execute the generated code locally
def execute_code_locally(data_file):
    try:
        # Command to run the generated code with the data file
        result = subprocess.run(['python3', 'generated_code.py', data_file], capture_output=True, text=True)

        if result.returncode == 0:
            st.success("Code executed successfully. 🎉")
            # display_outputs()
        else:
            st.error("Error executing code.")
            st.text(result.stderr)
    except Exception as e:
        st.error(f"Exception occurred: {e}")

# Function to display the outputs
def display_outputs():
    # Display saved plots
    plot_files = [f for f in os.listdir() if f.startswith('output_plot_') and f.endswith('.png')]
    if plot_files:
        st.subheader("📊 Plots")
        for plot_file in plot_files:
            st.image(Image.open(plot_file), caption=plot_file)

    # Display saved DataFrame output
    if os.path.exists('output_data.csv'):
        df_output = pd.read_csv('output_data.csv')
        st.subheader("📄 Results")
        st.write(df_output)


def summary_output(prompt):
    summ = []
    with open('generated_code.py', 'r') as file:
        python_code = file.read()
    with open('output_data.csv', 'r') as file:
        result_data = file.read()
    input_data = {
        "prompt": f"Generate a Summary (no code), consider the following: a code {python_code} was run as result of prompt: {prompt} and result df is: {result_data}, summary can based on insights of results, explain results and why this code is ran",
        "temperature": temperature,
    }
    for event1 in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input=input_data
    ):
        summ.append(event1.data)

    summary = "".join(summ)
    st.markdown(summary)
    


# Streamlit app layout
st.set_page_config(page_title="Statis AI: Data Analyzer", layout="wide")

# Sidebar
with st.sidebar:
    st.title("Statis AI: Data Analyzer")
    st.markdown("### Upload your file and adjust settings:")
    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'])
    temperature = st.slider("Model Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

# Popup for file upload
if not uploaded_file:
    st.info("Please upload a CSV or Excel file to get started. 📂")

if uploaded_file:
    # Save the uploaded file to disk
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read data into a DataFrame
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("### 📈 Data Preview:")
    st.write(df.head())

    query = st.text_input("💬  Visualize and Get Insights from your Data with a Query (e.g., 'Plot Graphs.. ,Find Metrics..'):")

    if query:
        if st.button('Go'):
            columns = df.columns.tolist()
            # Prepare input for the Replicate model
            prompt = f"Generate a Python code (only in ```python (code goes here..) ``` format) (do not give or mention any sample data in code. I have my own data with name : {uploaded_file.name} ) for the following data analysis task: {query}\n\nColumns:\n{columns}\n\n Other than the plots the output of the code should be in dataframe format (even if its a table or a single value), named 'df_output',Python code cannot be empty, always include legends in plots"

            input_data = {
                "prompt": prompt,
                "temperature": temperature,
            }

            st.markdown("### 📝 Generated Code:")
            code = stream_data(input_data)

            if code:
                # if st.button("Execute Code"):
                st.markdown("### 🚀 Execution Status:")
                execute_code_locally(file_path)

                st.markdown("### 📉 Analysis:")
                display_outputs()

                st.markdown("### ✏️ Summary:")
                summary_output(prompt)
                