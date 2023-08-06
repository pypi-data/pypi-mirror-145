# Public data food analysis 



## Install

`pip install public_data_food_analysis_3`

## For data analysis on the Columbia study

```python
import public_data_food_analysis_3.columbia as pdfac
import pandas as pd
```

```python
df = pdfac.make_table(pdfac.read_logging_data('data/col_test_data')\
                      , pd.read_excel('data/col_test_data/toy_data_17May2021.xlsx'))
```

    Participant yrt1999 didn't log any food items in the following day(s):
    2021-05-18
    Participant yrt2000 didn't log any food items in the following day(s):
    2021-05-12
    2021-05-13
    2021-05-14


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>mCC_ID</th>
      <th>Participant_Study_ID</th>
      <th>Study Phase</th>
      <th>Intervention group (TRE or HABIT)</th>
      <th>Start_Day</th>
      <th>End_day</th>
      <th>Eating_Window_Start</th>
      <th>Eating_Window_End</th>
      <th>phase_duration</th>
      <th>caloric_entries</th>
      <th>...</th>
      <th>logging_day_counts</th>
      <th>%_logging_day_counts</th>
      <th>good_logging_days</th>
      <th>%_good_logging_days</th>
      <th>good_window_days</th>
      <th>%_good_window_days</th>
      <th>outside_window_days</th>
      <th>%_outside_window_days</th>
      <th>adherent_days</th>
      <th>%_adherent_days</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>yrt1999</td>
      <td>2</td>
      <td>S-REM</td>
      <td>TRE</td>
      <td>2021-05-12</td>
      <td>2021-05-14</td>
      <td>00:00:00</td>
      <td>23:59:00</td>
      <td>3 days</td>
      <td>7</td>
      <td>...</td>
      <td>3</td>
      <td>1.00</td>
      <td>2.0</td>
      <td>0.666667</td>
      <td>3</td>
      <td>1.00</td>
      <td>0</td>
      <td>0.0</td>
      <td>2</td>
      <td>0.666667</td>
    </tr>
    <tr>
      <th>1</th>
      <td>yrt1999</td>
      <td>2</td>
      <td>T3-INT</td>
      <td>TRE</td>
      <td>2021-05-15</td>
      <td>2021-05-18</td>
      <td>08:00:00</td>
      <td>18:00:00</td>
      <td>4 days</td>
      <td>8</td>
      <td>...</td>
      <td>3</td>
      <td>0.75</td>
      <td>2.0</td>
      <td>0.500000</td>
      <td>1</td>
      <td>0.25</td>
      <td>2</td>
      <td>0.5</td>
      <td>1</td>
      <td>0.250000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>yrt2000</td>
      <td>3</td>
      <td>T3-INT</td>
      <td>TRE</td>
      <td>2021-05-12</td>
      <td>2021-05-14</td>
      <td>08:00:00</td>
      <td>16:00:00</td>
      <td>3 days</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0.00</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.0</td>
      <td>0</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 26 columns</p>
</div>



```python
df.iloc[0]
```




    mCC_ID                                           yrt1999
    Participant_Study_ID                                   2
    Study Phase                                        S-REM
    Intervention group (TRE or HABIT)                    TRE
    Start_Day                            2021-05-12 00:00:00
    End_day                              2021-05-14 00:00:00
    Eating_Window_Start                             00:00:00
    Eating_Window_End                               23:59:00
    phase_duration                           3 days 00:00:00
    caloric_entries                                        7
    mean_daily_eating_window                           13.75
    std_daily_eating_window                        11.986972
    earliest_entry                                       4.5
    2.5%                                              4.5375
    97.5%                                            27.5625
    duration mid 95%                                  23.025
    logging_day_counts                                     3
    %_logging_day_counts                                 1.0
    good_logging_days                                    2.0
    %_good_logging_days                             0.666667
    good_window_days                                       3
    %_good_window_days                                   1.0
    outside_window_days                                    0
    %_outside_window_days                                0.0
    adherent_days                                          2
    %_adherent_days                                 0.666667
    Name: 0, dtype: object



```python
df.iloc[1]
```




    mCC_ID                                           yrt1999
    Participant_Study_ID                                   2
    Study Phase                                       T3-INT
    Intervention group (TRE or HABIT)                    TRE
    Start_Day                            2021-05-15 00:00:00
    End_day                              2021-05-18 00:00:00
    Eating_Window_Start                             08:00:00
    Eating_Window_End                               18:00:00
    phase_duration                           4 days 00:00:00
    caloric_entries                                        8
    mean_daily_eating_window                        8.666667
    std_daily_eating_window                         8.504901
    earliest_entry                                       7.5
    2.5%                                                 7.7
    97.5%                                               23.9
    duration mid 95%                                    16.2
    logging_day_counts                                     3
    %_logging_day_counts                                0.75
    good_logging_days                                    2.0
    %_good_logging_days                                  0.5
    good_window_days                                       1
    %_good_window_days                                  0.25
    outside_window_days                                    2
    %_outside_window_days                                0.5
    adherent_days                                          1
    %_adherent_days                                     0.25
    Name: 1, dtype: object


