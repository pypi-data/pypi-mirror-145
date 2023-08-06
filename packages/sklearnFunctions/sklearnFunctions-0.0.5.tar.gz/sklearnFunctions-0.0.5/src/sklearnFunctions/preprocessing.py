import pandas as pd

class outliers:
    def outliers_removal(self,data):
        """
            Parameters
            ----------
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

            data=data[data['y'] >= outliers[k]["lower"]]
            data=data[data['y'] <= outliers[k]["upper"]]

            # return Outlier removed DataFrame
            
        return data