import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64



def HeatMap(score, tickerSymbol, cmap, bestScore, bestTs, vmin, vmax):

    debug = 0;

    if debug == 1:
        print("score, tickerSYmbol, cmap, bestscore, bestTs")
        print(score)
        print(tickerSymbol)
        print(cmap)
        print(bestScore)
        print(bestTs)
    fig, ax3 = plt.subplots(figsize=(10, 1.3))


    final = tickerSymbol + " " + str(round(score, 2))

    # cmap = matplotlib.cm.cool
    # labels = ('Dreadful', 'Poor', 'Mediocre', 'Good', 'Excellent', 'Phenomenal')
    norm = matplotlib.colors.Normalize(vmin=vmin ,vmax=vmax)
    matplotlib.colorbar.ColorbarBase(ax3, cmap=cmap, norm=norm, orientation='horizontal')
    #ax3.set_xlabel('Correlation', fontsize=14, color='b')

    fig.subplots_adjust(bottom=0.45)

    if debug == 1:
        print("score and bestScore")
        print(score)
        print(bestScore)

    down = vmin -1.25 * (vmax-vmin)

    if tickerSymbol != bestTs:
        ax3.annotate(final, xy=(score, vmin),
                    xytext=(score, down), xycoords='data', textcoords='data', color='tab:blue',
        arrowprops=dict(color='tab:blue', arrowstyle='->'),
        horizontalalignment='center', verticalalignment='baseline',)


    #color='tab:blue', shrink=0.0, width=0.5, headwidth=3.5, headlength=3.5
    #color='green', shrink=0.0, width=0.5, headwidth=3.5, headlength=3.5



    final2 = "Best: " + bestTs + " " + str(round(bestScore, 2))

    ax3.annotate(final2, xy=(bestScore,vmin),
                        xytext=(bestScore, vmin-(vmax-vmin)), xycoords='data', textcoords='data', color='green',
    arrowprops=dict(color='green', arrowstyle='->'),
    horizontalalignment='center', verticalalignment='baseline',)

    #cb1.ax.set_xticklabels(labels)
    img1 = BytesIO()
    plt.savefig(img1, format='png', bbox_inches='tight', pad_inches = 0.1)
    plt.close()
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode('utf8')
    return plot_url1