# Chatbot5
This is a simple RAG implementation with hugging face model/transformers context. 
In the scope of this project, we implemented a cost effective way for a RAG model to optimize the accuracy of the QA replies, reduce the rate of hallucination, which is a weakness of large language models in specific task QA. 
Check out this report for more information:
https://drive.google.com/file/d/1G5Paf2Fl4IlD3l0kbEaP7VGXJhoV_Nv4/view?usp=drive_link

# Running tutorials
## First, you need to put the icons to a folder in the same directory with the name "icon".

# For Windows
## Step 1:
```shell
python -m venv env 
```

## Step 2:
```shell
!pip install -r requirements.txt
```

## Step 3:
```shell
streamlit run app.py
```

# FOR MAC USING CONDA
### Note: You should install Xcode before (because you need to have Xcode installed on your system in order to proceed with the installation or compilation of certain software packages or libraries.)
## Step 1: 
``` terminal
conda create --name chatbot  python=3.10
```

## Step 2
``` terminal
conda activate chatbot 
```

## Step 3:
``` terminal
pip install sentence-transformers==2.2.1 install -r requirementsformac.txt
```

## Step 4:
``` shell
streamlit run app.py
```


