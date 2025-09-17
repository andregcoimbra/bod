# Software for building subjective-objective composite indicators using Benefit-of-the-Doubt: So-called S-CI-BoD
## Description
The software is an interactive software for building composite indicators using BoD method and uncertainty analysis. The application is built with Streamlit and allows users to import data, configure parameters, and obtain results visually and intuitively.

## How to Use
1. **Requirements**
* Python 3.8+
* Libraries: streamlit, pandas, plotly, openpyxl, sklearn, scipy
* Data file in Excel format (.xlsx)
2. **Running the Application**
  
    In the terminal, run:
  
    ```$ streamlit run ci/app.py ```

3. **Step-by-Step**

   **a) Upload Data**
    * In the sidebar, click Select Excel file and upload your .xlsx file.
    * The software will display a preview of your data.
  
   **b) Select Columns**
    * Choose the numeric columns to be used for calculating composite indicators in Select columns.
    * Optionally, select a control variable for data normalization in Select the control variable.
    * Optionally, select a label column to identify rows in Select label column.
  
   **c) Parameter Setup**
    * In the setup bounds, you can define minimum and maximum values for each selected column, if needed. By default, values are set between 0 and 1.

   **d) Calculation**
    * Click Calculate to process the data.
    * The results will be displayed according to the configured bounds.
  
   **e) Results**
    * Available views and actions:
        * Table with composite indicators and weights.
        * Scatter plot and histogram of the results.
        * Minimum and maximum values of the composite indicator.
        * Button to download results as an Excel file.

## Notes
   * The input file must have a maximum of 300 rows (extra rows will be discarded).
   * If there are missing values, the software will inform which columns are affected and stop processing.
   * Minimum and maximum values for BoD must be between 0 and 1.

## Support
   For questions or suggestions, contact the developer.
