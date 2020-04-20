import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def HeatMap(score, tickerSymbol, cmap, bestScore, bestTs):
    fig, ax3 = plt.subplots(figsize=(13, 1.3))
    fig.subplots_adjust(bottom=0.5)
    if score < 0:
        nscore = 0 - score
    elif score > 0:
        nscore = score
    else:
        nscore = 0
    # cmap = matplotlib.cm.cool
    # labels = ('Dreadful', 'Poor', 'Mediocre', 'Good', 'Excellent', 'Phenomenal')
    norm = matplotlib.colors.Normalize(vmin=0 ,vmax=100)
    trans = ax3.get_yaxis_transform()
    if score < 0:
        final = tickerSymbol + " Negative " + str(round(nscore, 2))
    else:
        final = tickerSymbol + " " + str(round(nscore, 2))
    ax3.annotate(final, xy=(nscore/100,-0.3),
                        xytext=(nscore/100, -1.22), xycoords=trans, textcoords='axes fraction', color='tab:blue',
    arrowprops=dict(color='tab:blue', shrink=0.0, width=0.5, headwidth=3.5, headlength=3.5),
    horizontalalignment='center', verticalalignment='baseline',)


    final2 = "Best: " + bestTs + " " + str(round(bestScore, 2))
    ax3.annotate(final2, xy=(bestScore/100,-0.4),
                        xytext=(bestScore/100, -1.0), xycoords=trans, textcoords='axes fraction', color='green',
    arrowprops=dict(color='green', shrink=0.0, width=0.5, headwidth=3.5, headlength=3.5),
    horizontalalignment='center', verticalalignment='baseline',)
    ax3.set_xlabel('Correlation', fontsize=14, color='b')
    matplotlib.colorbar.ColorbarBase(ax3, cmap=cmap, norm=norm, orientation='horizontal')
    #cb1.ax.set_xticklabels(labels)
    img1 = BytesIO()
    plt.savefig(img1, format='png')
    plt.close()
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode('utf8')
    return plot_url1
