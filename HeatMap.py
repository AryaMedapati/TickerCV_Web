import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def HeatMap(score, tickerSymbol, cmap, bestScore, bestTs):
    print("score, tickerSYmbol, cmap, bestscore, bestTs")
    print(score)
    print(tickerSymbol)
    print(cmap)
    print(bestScore)
    print(bestTs)
    fig, ax3 = plt.subplots(figsize=(13, 1.3))
    fig.subplots_adjust(bottom=0.5)


    if score < 0:
        score = 0 - score
        final = tickerSymbol + " Negative " + str(round(score, 2))
    else:
        final = tickerSymbol + " " + str(round(score, 2))

    # cmap = matplotlib.cm.cool
    # labels = ('Dreadful', 'Poor', 'Mediocre', 'Good', 'Excellent', 'Phenomenal')
    norm = matplotlib.colors.Normalize(vmin=0 ,vmax=100)
    trans = ax3.get_yaxis_transform()

    print("score and bestScore")
    print(score)
    print(bestScore)

    if tickerSymbol != bestTs:
        ax3.annotate(final, xy=(score/100,-0.3),
                        xytext=(score/100, -1.23), xycoords=trans, textcoords='axes fraction', color='tab:blue',
        arrowprops=dict(color='tab:blue', arrowstyle='->'),
        horizontalalignment='center', verticalalignment='baseline',)

    #color='tab:blue', shrink=0.0, width=0.5, headwidth=3.5, headlength=3.5
    #color='green', shrink=0.0, width=0.5, headwidth=3.5, headlength=3.5


    if bestScore < 0:
        bestScore = 0 - bestScore
        final2 = "Best: " + bestTs + " Negative " + str(round(bestScore, 2))
    else:
        final2 = "Best: " + bestTs + " " + str(round(bestScore, 2))

    ax3.annotate(final2, xy=(bestScore/100,-0.3),
                        xytext=(bestScore/100, -0.98), xycoords=trans, textcoords='axes fraction', color='green',
    arrowprops=dict(color='green', arrowstyle='->'),
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
