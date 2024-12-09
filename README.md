# **End-to-End Machine Learning Pipeline for Personalized Recommendations in Databricks**

## **Overview**

This project implements a comprehensive end-to-end machine learning pipeline in Databricks to deliver personalized product recommendations for an e-commerce platform. The pipeline integrates structured and unstructured data, enabling enhanced insights and predictions to optimize customer engagement and product recommendations.

**Problem Statement**: E-commerce platforms often struggle to provide highly personalized product recommendations that improve customer engagement and retention. Understanding customer behavior through interactions, reviews, and transaction data can reveal insights into preferences, purchase intent, and satisfaction. This project aims to build an end-to-end recommendation system on Databricks, leveraging both structured interaction data and unstructured review data to deliver more relevant product suggestions, enhancing customer experience and boosting conversion rates.

**Objective**: The primary goal is to create a robust data engineering pipeline that collects, processes, analyzes, and models customer engagement with products. This will enable e-commerce businesses to:
- Identify customer engagement levels based on actions such as viewing, adding to cart, and purchasing.
- Deliver personalized product recommendations that align with customer preferences and enhance engagement.
- Predict future customer interactions, ultimately supporting data-driven decision-making for targeted marketing and inventory management.

---

## **Datasets**

### **1. Cosmetic Store Website Data**
- **Description**: Primary dataset containing user interaction logs such as event types (view, add-to-cart, etc.), timestamps, product IDs, and session details.
- **Purpose**: Provides the foundational structured data for user interactions.

### **2. Cosmetics and Beauty Products Reviews**
- **Description**: Dataset of textual reviews, product ratings, and other metadata (e.g., brand names, review titles).
- **Purpose**: Enhances the pipeline with unstructured data for sentiment analysis and insights into customer opinions.

### **3. Product Mapping Data**
- **Description**: A mapping file connecting product IDs between the primary interaction data and review data.
- **Purpose**: Ensures seamless integration of structured and unstructured datasets.

---

## **Data Clarity**

**Response Variable (Y)**: Customer engagement level 
- Class 0: Low Engagement (View)
- Class 1: Medium Engagement (Add-to-Cart)
- Class 2: Disengagement (Remove from Cart)
- Class 3: High Engagement (Purchase)

**Predictor Variables (X)**
- Structured Data: session-based interaction data (user_session, event_type), product attributes (category_code, brand, price), and time-based patterns (event_time).
- Unstructured Data: Textual information from product descriptions and customer reviews in the Sephora dataset. This data will be used to capture customer sentiment, product characteristics, and preferences, enhancing the model’s understanding of product relevance.

---

## **Technologies Used**

- **Databricks**: Unified analytics platform for scalable data processing.
- **Apache Spark**: Distributed computing for data transformation and analysis.
- **Python/PySpark**: Core programming language.
- **SQL**: To query and analyze structured data.
- **NLP Libraries**:
  - **SpaCy**: Text preprocessing, stemming, and lemmatization.
  - **Transformers (GPT)**: Tokenization and embedding generation for unstructured data.
- **Delta Lake**: Storage for transactional reliability and scalability.
- **MLflow (Stretch Goal)**: To track model metrics, manage versioning, and facilitate reproducibility.
- **Unity Catalog (Stretch Goal)**: For Data Governance.
- **AWS S3**: Cloud storage for raw datasets.
- **Visualization Tools**:
  - Matplotlib
  - Seaborn
  - Power BI Dashboard or Tableau: For data visualization and reporting.

---

## **Pipeline Workflow**

### **1. Data Cleaning**
- Standardizes column names across datasets.
- Removes invalid or missing data.
- Cleans textual data by removing stopwords and special characters.

### **2. Feature Engineering**
- **Structured Features**:
  - Customer engagement levels (view, add-to-cart, purchase, etc.).
  - Product popularity, session diversity, and user recency/frequency.
- **Unstructured Features**:
  - Sentiment analysis using pre-trained models.
  - Lemmatization and stemming for textual reviews.

### **3. Data Transformation**
- Scaling and normalization of numerical columns.
- Tokenization and embedding extraction from textual data using GPT models.

### **4. Exploratory Data Analysis (EDA)**
- Visualizes data distributions (e.g., product prices, ratings).
- Analyzes correlations between variables.
- Examines sentiment trends and engagement levels.

### **5. Delta Table Management**
- Converts cleaned and transformed datasets into Delta tables.
- Ensures schema consistency and reliable storage.

### **6. Coming Soon (Future Scope)**
- Build and evaluate recommendation models.
- Implement personalized email campaigns based on engagement levels.
- Introduce reranking using LLMs for improved recommendation quality.

---

## **Sponsor**

This project is proudly sponsored by **Royal Cyber**, a trusted global leader in IT consultancy and enterprise solutions. The sponsorship enables the exploration of advanced machine learning solutions for real-world e-commerce challenges.

---

## Getting Started

This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.

Prerequisites

In order to run this project and leverage all of the intended features, the repository must be housed in a databricks workspace. In order to set up the folders properly, you must follow the following instructions:

1. [Configure your databricks/git credentials.](https://docs.databricks.com/en/repos/repos-setup.html)
2. [Create a git folder inside a databricks workspace using the repo URL.](https://docs.databricks.com/en/repos/git-operations-with-repos.html)

---

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

---

## **License**

This project is licensed under the MIT License.

---

## **Contributors**

- Zainab Sunny - zainab786@uchicago.edu
- Kate Pferdner - kpferdner@uchicago.edu
- Wonjae Lee - wonjael@uchicago.edu
- Zihan Chen - zihanc@uchicago.edu
