# Streamlit Web Application README

## Overview

This repository contains a Streamlit web application that displays company data based on a `buildingID` provided via URL query parameters. The app fetches data from a Google BigQuery dataset and visualizes it on a webpage, including links to external resources for more detailed company information. Secrets are managed by streamlit. 

## Features

- **Display Company Information:** Lists head offices and establishment units associated with a specific building.
- **Google Maps Integration:** Embeds a Google Maps view of the building's location.
- **External Links:** Provides links to OpenTheBox and Bizzy for additional company details.
- **Caching:** Utilizes Streamlit's caching to optimize performance by storing query results for 10 minutes.


## Deployment

To update the application:

1. Push to this repo
2. Streamlit cloud updates the app


## Acknowledgments

This project was developed using [Streamlit](https://streamlit.io).

---

For further assistance, please contact the project maintainer or open an issue in the repository.
