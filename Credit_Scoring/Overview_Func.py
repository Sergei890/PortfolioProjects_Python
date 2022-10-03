#!/usr/bin/env python
# coding: utf-8

# In[1]:


def overview(d_):
    
#----------------------------------------------------------------------------------------------------

    from pandas.api.types import is_numeric_dtype
    from pandas.api.types import is_string_dtype

    class bcolors:
        OKBLUE = '\033[94m'
        HEADER = '\033[95m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        WARNING = '\033[93m'
        Green = '\033[92m'
        ENDC = '\033[0m'
        RED = '\033[91m'
        
    special = '''[@_!#$%&*()^<>?/\|}{~:+"'`;]''' # Define special characters 

#----------------------------------------------------------------------------------------------------
    
    for col in d_:

        print("-------------------------------------")

        print(bcolors.OKBLUE + bcolors.BOLD + col.upper() + bcolors.ENDC, f"({d_[col].dtypes})", "\n")
    
# Statistics
        if is_numeric_dtype(d_[col]) == True:
            print("", 
                  bcolors.BOLD + "Max:" + bcolors.ENDC, d_[col].max(), 
                  bcolors.BOLD + "Min:" + bcolors.ENDC, d_[col].min(), "\n",
                  bcolors.BOLD + "Mean:" + bcolors.ENDC, round(d_[col].mean(),2), 
                  bcolors.BOLD + "Median:" + bcolors.ENDC, round(d_[col].median(),2),
                  bcolors.BOLD + "Std:" + bcolors.ENDC, round(d_[col].std(),2))
        
        if d_[col].mode().nunique() < 2:
            print("",bcolors.BOLD + "Mode:" + bcolors.ENDC, d_[col].mode().to_string(index=False))
        else:
            print("",bcolors.BOLD + "More than 2 Modes!" + bcolors.ENDC)
    
        print("            - - - - - - -            ")

# Uniques
        print(bcolors.BOLD + "", d_[col].nunique(), "Unique values" + bcolors.ENDC)
    
        if d_[col].nunique() < 10:
            print(round(d_[col].value_counts(normalize=True)*100,2).to_string(index=True))
    
        print(bcolors.BOLD + "", 
              d_[col].astype(str).apply(len).nunique(), "Unique value's length (in characters)" + bcolors.ENDC)
        
        if d_[col].astype(str).apply(len).nunique() < 10:
            if d_[col].dtypes == 'float64':
                print(round(d_[col].astype(str).str.replace(".0$", "").str.replace(".", "").
                            apply(len).value_counts(normalize=True)*100,2).to_string(index=True))
            else:
                print(round(d_[col].astype(str).apply(len).value_counts(normalize=True)*100,2).to_string(index=True))
        
        print("            - - - - - - -            ")

# Zeros, NaNs, Duplicates
        if ((d_[col] == 0).sum()/d_.shape[0] * 100) > 0:
            print(bcolors.RED + bcolors.BOLD + "", 
                  round(((d_[col] == 0).sum()/d_.shape[0] * 100),3), "% of Zero values" + bcolors.ENDC)   

        if (d_[col].isnull().sum()/d_.shape[0] * 100) > 0:
            print(bcolors.RED + bcolors.BOLD + "", 
                  round(d_[col].isnull().sum()/d_.shape[0] * 100,3), "% of NaN values" + bcolors.ENDC)
    
        print(bcolors.Green + "", 
              round((((d_[col] != 0) & (d_[col].notnull())).sum()/d_.shape[0] * 100),3), 
              "% of Non-NaN and Non-Zero values" + bcolors.ENDC, "\n")
    
        if d_[col].duplicated().any() == True:    
            print(bcolors.RED + "", "Contains Duplicates values!" + bcolors.ENDC)

        print("            - - - - - - -            ")

# Characters
        if d_[col].astype(str).str.count(special).sum() > 0:
            print(bcolors.RED + bcolors.BOLD + "", "Contains special characters!" + bcolors.ENDC)

        if d_[col].astype(str).str.contains('[" "]').sum() > 0:
            print(bcolors.RED + bcolors.BOLD + "", "Contains empty spaces!" + bcolors.ENDC)
        
        print("","Only values with letters:",
              round(((((d_[col].astype(str).str.isalpha()) & 
                       (d_[col].astype(str).str.lower().str.contains('([^nan])'))).sum()) / d_.shape[0]) * 100,2), "%")
    
        print("","Only values with numbers:",
              round((d_[col].astype(str).str.replace(".", "").str.replace("-", "")
                     .str.isnumeric().sum() / d_.shape[0]) * 100,2), "%")
        
        print("","Only values with letters and numbers:",
              round(((((d_[col].astype(str).str.contains('[a-zA-Z]')) & 
                    (d_[col].astype(str).str.contains('[0-9]'))).sum()) / d_.shape[0]) * 100,2), "%")
            
        print("-------------------------------------")
    
        print()


# In[2]:


def plot_density_overview(plot_variable):
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex = True, figsize = (15, 12))
    
    sns.kdeplot(plot_variable, shade=True, ax = ax1)
    ax1.set_xlabel('')
    ax1.set_ylabel('Occurrences', fontsize = 12)

    
    sns.boxplot(plot_variable, ax = ax2)
    ax2.set_ylabel('')
    ax2.set_xlabel('')
    
    x_ECDF = np.sort(plot_variable)
    y_ECDF = np.arange(1, len(x_ECDF)+1) / len(x_ECDF)
    ax3.plot(x_ECDF, y_ECDF, marker='.', linestyle='none', color = "gray", alpha = 0.7)
    ax3.set_xlabel('Values', fontsize = 12)
    ax3.set_ylabel('ECDF', fontsize = 12)
    ax3.margins(0.02)
    
    percentiles = np.array([25, 50, 75, 99])
    ptiles_vers = np.percentile(plot_variable, percentiles)
    ax3.plot(ptiles_vers, percentiles/100, marker='o', color='red', linestyle='none', alpha = 0.5)
    
    plt.subplots_adjust(hspace = 0.3)
    fig.suptitle(f"Distribution of {plot_variable.to_frame().columns[0]}", y = 0.92, fontsize = 15)
    
    plt.show()


# In[3]:


def plot_hist_bins_overview(plot_variable):
    
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats
    
    custom_bins = np.linspace(0, plot_variable.max(), 15)
    
    plt.figure(figsize=(15, 8), dpi=80)
    
    ax1 = plt.subplot(1,1,1)
    ax1.hist(plot_variable, bins = custom_bins[:], edgecolor="black")
    ax1.set_xlabel('Bins boundaries', rotation=0, labelpad=4, loc='right')
    ax1.set_xticks(custom_bins[:])
    
    # Set scond x-axis
    ax2 = ax1.twiny()
    
    # Decide the ticklabel position in the new x-axis,
    # then convert them to the position in the old x-axis
    
    newlabel = np.linspace(0, plot_variable.max(), 15)[list(range(1,14,1))]
    
    hmm = [f'{round(stats.percentileofscore(plot_variable,newlabel[0]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[1]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[2]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[3]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[4]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[5]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[6]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[7]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[8]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[9]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[10]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[11]),1)} %',
           f'{round(stats.percentileofscore(plot_variable,newlabel[12]),1)} %',           
          ]
    
    ax2.set_xticks(newlabel)
    ax2.set_xticklabels(hmm)
    
    ax2.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
    ax2.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
    
    ax2.spines['bottom'].set_position(('outward', 36))
    ax2.set_xlabel('Cumulatitative percentage of data', rotation=0, labelpad=7, loc = "left")
    ax2.set_xlim(ax1.get_xlim())
    
    ax1.set_title(f"Distribution of '{plot_variable.to_frame().columns[0]}' values (bins)", y = 1.01, x = 0.5, fontsize = 18)
    
    plt.show()

