import numpy as np
from pyspark.sql.functions import isnan, isnull
from pyspark.sql.types import BooleanType, StringType, DateType

def getMissingValues(dataframe):
  count = dataframe.count()
  columns = dataframe.columns
  nan_count = []
  # we can't check for nan in a boolean type column
  for column in columns:
    if dataframe.schema[column].dataType == BooleanType():
      nan_count.append(0)
    elif dataframe.schema[column].dataType == StringType():
      nan_count.append(0)
    elif dataframe.schema[column].dataType == DateType():
      nan_count.append(0)
    else:
      nan_count.append(dataframe.where(isnan(column)).count())
  null_count = [dataframe.where(isnull(column)).count() for column in columns]
  return([count, columns, nan_count, null_count])

def missingTable(stats):
  count, columns, nan_count, null_count = stats
  count = str(count)
  nan_count = [str(element) for element in nan_count]
  null_count = [str(element) for element in null_count]
  max_init = np.max([len(str(count)), 10])
  line1 = "+" + max_init*"-" + "+"
  line2 = "|" + (max_init-len(count))*" " + count + "|"
  line3 = "|" + (max_init-9)*" " + "nan count|"
  line4 = "|" + (max_init-10)*" " + "null count|"
  for i in range(len(columns)):
    max_column = np.max([len(columns[i]),\
                        len(nan_count[i]),\
                        len(null_count[i])])
    line1 += max_column*"-" + "+"
    line2 += (max_column - len(columns[i]))*" " + columns[i] + "|"
    line3 += (max_column - len(nan_count[i]))*" " + nan_count[i] + "|"
    line4 += (max_column - len(null_count[i]))*" " + null_count[i] + "|"
  lines = f"{line1}\n{line2}\n{line1}\n{line3}\n{line4}\n{line1}"
  print(lines)


