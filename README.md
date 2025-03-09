## Terminal CMDs

#### Create Virtual Environment and Activate using Anaconda (recommended )

- **Note:** Anaconda must be installed

```
conda create -p venv python==3.12
conda activate venv/

```

#### Create Virtual Environment and Activate using Python

```
python -m venv [folder_name]
[folder_name]\Scripts\activate

```

#### Install ipykernel for .ipynb to run

```
pip install ipykernel
```

#### List Installed Packages:

```
pip list
```

#### Download all packages inside the requirements.txt:

```
pip install -r requirements.txt
```

#### Running Streamlit on webbrowser localhost

```
streamlit run yourscript.py
```
