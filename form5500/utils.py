import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    return graph

def get_plot(x1, y1, x2, y2, x3, y3):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,10))
    plot1 = plt.subplot2grid((2, 2), (0, 0))
    plot2 = plt.subplot2grid((2, 2), (0, 1))
    plot3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

    plot1.barh(x1, y1)
    plot1.set_title("Top 10 States by Plan count")
    plot1.set_xlabel("Count")
    for index, value in enumerate(y1):
        plot1.text(value, index, '{:,}'.format(value))
    plot2.barh(x2, y2)
    plot2.set_title("Top 10 States by Plan Asset")
    plot2.set_xticklabels(['0B','1,000B','2,000B','3,000B','4,000B','5,000B'])
    plot2.set_xlabel("Total Plan Asset ($)")
    for index, value in enumerate(y2):
        plot2.text(value, index, '${:,}'.format(round(value/1000000000,2))+"B")
    plot3.bar(x3, y3)
    plot3.set_title("Industry by Plan Asset")    
    for index, value in enumerate(y3):
        plot3.text(index-0.5, value, '{:,}'.format(round(value/1000000000,1))+"B", fontsize=6)
    #plot3.rc('axes', labelsize=8)
    plot3.tick_params(axis='x', labelrotation=90, labelsize=6)
    plot3.set_yticklabels(['0B','2,000B','4,000B','6,000B','8,000B','10,000B','12,000B'])
    plot3.set_ylabel("Total Plan Asset ($)")
    
    plt.tight_layout()
    graph = get_graph()
    return graph