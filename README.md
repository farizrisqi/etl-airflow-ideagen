# Project Showcase: Playwright Web Scraping, Dual-Stream ETL & Automation Pipeline

## 📌 Project Description
This project is an end-to-end solution for data extraction, processing, and automation. Focusing heavily on **Big Data, ETL ,and  Data Engineering**, this pipeline is designed to automatically retrieve data from internal systems, process it through a Dual-Stream ETL pipeline, and distribute it for both administrative automation (RPA), text-based Artificial Intelligence processing (NLP) and other internal team purposes

## 🏗️ Architecture & Workflow
This system breaks down complex data processing into four main integrated stages:

### 1. Data Ingestion (Playwright Web Scraping)
* **Authentication & Scraping:** The system automatically authenticates into the Company Database using **Playwright** to extract operational data.
* **Data Extraction & Routing:** The extracted raw data is then intelligently routed to the appropriate processing streams.

### 2. Data Engineering: Dual-Stream ETL Pipeline
The core of this data processing utilizes a dual-stream architecture to handle different datasets efficiently using **Pandas**:

* **Ops Report Stream:** * Extracts and cleans Ops Data.
    * Updates the Reporter/Crew DB.
    * Generates the Accountability Context for downstream evaluation.
* **Assigned Report Stream:**
    * Extracts and cleans Assigned Data.
    * Performs complex data segmentation.
    * Extracts identifiers (Report Number) and compiles the complete payload.
    * Updates the Report Database and generates Defect Data Output.

### 3. Review & Integration
Both data streams converge at the **Review Report Closure** stage, where the data is evaluated and validated against the company's CRM Policy. 

### 4. Machine Learning & Automation Pipeline (Staging)
The cleaned, processed, and reviewed data is finally distributed into two continuous portfolios:
* **Staging for RPA:** Triggers the Ongoing RPA Portfolio to handle administrative task automation (*Trigger Admin Automation*).
* **Staging for AI:** Feeds the Defect Data into **Machine Learning** models to perform an *NLP Risk Assessment*, providing automated risk-level insights based on the text of the reports.

## 🛠️ Core Tech Stack
* **Web Scraping & Automation:** Playwright
* **Data Engineering (ETL):** Python (Pandas)
* **Machine Learning:** NLP (Natural Language Processing)
