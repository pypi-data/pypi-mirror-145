import matplotlib.pyplot as plt
import seaborn as sns

def cc_plot(params):
    '''
    Accepts dictionaries, pd.Series, np.array() as inputs
    Example 1:
    >>>cc_plot({'SMA': [30, 30.5, 40], 'EMA': [40, 67, 87]})

    Example 2:
    >>>cc_plot(np.array([30, 30.5, 40]))

    '''
    try:
        if str(type(params)) == "<class 'dict'>":
            arr = ['b', 'g', 'y', 'r', 'm', 'k', 'w', 'c']

            plt.figure(figsize=(15, 6))
            i = 0

            try:
                for key in params.keys():
                    params[f'{key}'].plot(color=arr[i])
                    i += 1
            except:
                for key in params.keys():
                    plt.plot(params[f'{key}'], color=arr[i])
                    i += 1

            plt.ylabel('Values', fontsize=14)
            plt.xlabel('Time/Days', fontsize=14)
            plt.xticks(rotation=60)
            plt.legend(params.keys())

        elif str(type(params)) == "<class 'pandas.core.series.Series'>":
            arr = ['b', 'g', 'y', 'r', 'm', 'k', 'w', 'c']

            plt.figure(figsize=(15, 6))

            params.plot()

            plt.xticks(rotation=60)
            plt.ylabel('Values', fontsize=14)
            plt.xlabel('Time/Days', fontsize=14)

        elif str(type(params)) == "<class 'numpy.ndarray'>":
            plt.figure(figsize=(15, 6))

            plt.plot(params)

            plt.xticks(rotation=60)
            plt.ylabel('Values', fontsize=14)
            plt.xlabel('Time/Days', fontsize=14)

    except Exception as e:
        print(e)
