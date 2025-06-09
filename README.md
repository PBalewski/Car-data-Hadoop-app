
# Car Data Analysis Web App

This project is a web-based application for analyzing car data using Flask, Apache Spark, and HDFS. It allows users to interactively explore a dataset of cars, filter results based on specific criteria, and get a recommendation for the best car based on fuel efficiency (MPG).

---

## Features

- Interactive car listing with filter options (e.g., brand, price range)
- Paginated and sortable table view
- Automatic recommendation of the most fuel-efficient car
- Data processing with Apache Spark
- By default (however optional) integration with HDFS for data storage
- Clean UI with HTML/CSS templates
- Dockerized for easy deployment

---

## Getting Started (with Docker)

### Prerequisites

- Docker installed on your machine

### Run the app

1. Clone the repository:

```bash
git clone https://github.com/PBalewski/Car-data-Hadoop-app
cd Car-data-Hadoop-app
```

2. Start hdfs (Hadoop must be installed):

```bash
start-dfs.sh
start-yarn.sh
```

3. Build and run the Docker container:

```bash
docker build -t car-data-app .
docker run -p 5000:5000 car-data-app
```

4. Open your browser and go to:

```
http://localhost:5000
```

---

## Project Structure

```
Car-data-Hadoop-app/
├── car_app.py               # Main Flask application
├── CarsData.csv             # Dataset
├── CarsData_analysis.ipynb  # Jupyter Notebook for data exploration
├── templates/               # HTML templates
├── static/                  # CSS files
├── hdfs/                    # HDFS directory (if used)
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md                # Project description
```

---

## Manual Setup (without Docker)

If you'd rather run the app directly:

### Prerequisites

- Python 3.6
- Apache Spark
- Flask
- pandas, pyspark, matplotlib

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the app

```bash
python car_app.py
```

Then go to `http://localhost:5000` in your browser.

---

## Dataset

The included dataset (`CarsData.csv`) contains information such as:

- Model: The model of the car.
- Year: The manufacturing year of the car.
- Price: The price of the car.
- Transmission: The type of transmission used in the car.
- Mileage: The mileage of the car.
- FuelType: The type of fuel used by the car.
- Tax: The tax rate applicable to the car.
- MPG: The miles per gallon efficiency of the car.
- EngineSize: The size of the car's engine.
- Manufacturer: The manufacturer of the car.

---

## License

This project is open-source and available under the [MIT License](LICENSE).
