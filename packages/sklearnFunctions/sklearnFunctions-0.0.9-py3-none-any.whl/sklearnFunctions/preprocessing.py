import pandas as pd
import numpy as np

class outliers:
    def outliers_removal(self,data):
        """
            Parameters
            ----------
            Note : The Values of the DataFrame must be numeric values

            data : DataFrame input
                DESCRIPTION. This function will remove the outliers present in our DataFrame

            The Outlier removal is based on the formula

            IQR = 75th percentile - 25th percentile

            lower limit = 25th percentile - 1.5(IQR)

            upper limit = 75th percentile + 1.5(IQR)
    
            The Values that falls below lower limit and above upper limit are called outliers

            Returns
            -------
            DataFrame
                Return the DataFrame with outliers removed.
            """

        outliers={}

        for k, v in data.items():

            q1 = v.quantile(0.25)
            q3 = v.quantile(0.75)

            iqr = q3 - q1

            lower= q1 - 1.5 * iqr
            upper= q3 + 1.5 * iqr

            outliers[k]={"lower":lower,"upper":upper}

            # Removing outlier data from DataFrame

            data=data[data[k] >= outliers[k]["lower"]]
            data=data[data[k] <= outliers[k]["upper"]]

            # return Outlier removed DataFrame
            
        return data


    def is_present(self,data):
        """
            Parameters
            ----------
            data : DataFrame input
                DESCRIPTION. This function will return the percentage of outliers present in column.
    
            Returns
            -------
            DataFrame
                Return the pecentage of outliers present in each column.
        """
        outlier_percentage={"column_Name":[],"outlier_Percentage":[]}

        for col, val in data.items():
            q1 = val.quantile(0.25)
            q3 = val.quantile(0.75)
            irq = q3 - q1
            v_col = val[(val <= q1 - 1.5 * irq) | (val >= q3 + 1.5 * irq)]
            perc = np.shape(v_col)[0] * 100.0 / np.shape(data)[0]
            outlier_percentage["column_Name"].append(col)
            outlier_percentage["outlier_Percentage"].append(perc)

        return pd.DataFrame(outlier_percentage)