import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from io import BytesIO
import base64

def Plot(sDates1, sCloses, tickerSymbol, tCases):
    fig, ax1= plt.subplots(figsize=(9, 4.5))
    color = 'tab:blue'
    ax1.set_title('Stock: ' + tickerSymbol, fontsize= 16, color='b')
    ax1.set_xlabel('date', fontsize=14, color='b')
    ax1.set_ylabel('price', fontsize=14, color='b')
    ax1.plot(sDates1, sCloses, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    i=0
    for label in ax1.xaxis.get_ticklabels()[::1]:
        if (i%6 != 0):
            label.set_visible(False)
        i= i+1
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('confirmed cases', fontsize=14, color='r')
    ax2.plot(sDates1, tCases, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    j = 0
    for label in ax2.xaxis.get_ticklabels()[::1]:
        if (i%4 != 0):
            label.set_visible(False)
        j = j+1

    ax2.tick_params(axis='x', which='major', labelsize=10)
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches = 0.1)
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url