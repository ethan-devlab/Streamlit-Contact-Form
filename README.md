# Streamlit-Contact-Form
A Contact Form written Streamlit

## Set up your secrets.toml file
Make sure you build the **secrets.toml** in `.streamlit/`, the path be looks like `.streamlit/secrets.toml`<br>

Then follow the structure below:<br>
```
[General]
available_date = "yyyy-mm-dd"

[Email]
email = "your email"
password = "your email password token"
bcc = "email you want to bcc"
```
## Run
After finishing setting up secrets.toml, run the program with `streamlit run main.py`
