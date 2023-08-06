# Databricks-Assets-NRM

This is the main repository for all databricks assets. 

## Folder Structure

The following is a visual representation of the folder structure of the repository.

    .
    ├── main                    # Legacy NRM files to be retired after test period
    ├── sample_code             # To be removed
    ├── sources                 # List of all the data sources used in Databricks
    │   ├── Argus               # Examples of some data sources
    │   │   ├── ...-bronze.py   # formerly named raw data extration
    │   │   ├── ...-silver.py   # data transformation notebooks
    │   │   ├── ...-gold.py     # finalized data notebooks
    │   │   └── ...             # Any other files like tests or variations of notebooks
    │   ├── BankOfCanada        
    │   ├── Calendar            
    │   └── ...                 # More data sources
    ├── tests                   # Test files
    ├── utils                   # Helper files
    │   ├── operations          # Helper functions for specific data sources
    │   └── ...                 # Additional helper files for 


