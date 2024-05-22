# Statis AI

Statis AI is a tool for performing Python statistical analysis on data that can be uploaded in CSV or Excel format. By leveraging Arctic, a language model capable of generating code, Statis AI automates the process of analyzing data and visualizing results. You can set this application to run the generated code on your data either on cloud compute (AWS/Azure) or locally.

This project is a submission for the [Arctic Streamlit Hackathon](https://arctic-streamlit-hackathon.devpost.com/?ref_feature=challenge&ref_medium=your-open-hackathons&ref_content=Recently+ended). It showcases Arctic's capabilities in enterprise applications, **such as writing code and SQL queries**, as highlighted in [Snowflake's blog post](https://www.snowflake.com/blog/arctic-open-efficient-foundation-language-models-snowflake/).

## Setup Locally

### Step 1: Set Up a Virtual Environment

To create and activate a virtual environment, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to your project directory.
3. Run the following commands:

```sh
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Step 2: Install the Requirements

With the virtual environment activated, install the necessary packages by running:

```sh
pip install -r requirements.txt
```

### Step 3: Set Up Replicate API Token

To access Arctic, you need to set up your Replicate API token. Follow these steps:

1. Obtain your API token from [Replicate's API Tokens page](https://replicate.com/account/api-tokens).
2. Export the token in your terminal or command prompt:

```sh
export REPLICATE_API_TOKEN=<paste-your-token-here>
```

### Step 4: Run the Application

With everything set up, you can run the Streamlit application using:

```sh
streamlit run app.py
```

### Features of Statis AI

- Upload CSV or Excel files to analyze data.
- Input queries in natural language to specify the analysis or visualization you need.
- Arctic generates Python code based on your input and data structure.
- Executes the generated code, displays the results (plots and dataframes) and provides a summary.

We hope you find Statis AI useful for your data analysis needs! If you have any questions or run into any issues, feel free to reach out.
