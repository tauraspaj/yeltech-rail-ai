# Yeltech Rail Temperature Prediction Using ML
Web application to deploy and monitor ML models developed to forecast rail temperature.

## Getting Started
### Init conda environment
```sh
conda create -n yeltech-env python=3.10
```

### Installation

1. ```sh
   pip install -r front_end/requirements.txt
   ```

2. ```sh
   docker build -t "yeltech-ai" -f back_end/Dockerfile .
   ```

3. ```sh
   docker run -it -p 8296:8296 yeltech-ai
   ```

4. ```sh
   streamlit run main.py
