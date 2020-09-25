from wordcloud import WordCloud
from matplotlib import pyplot as plt

path2topics = "out.txt"
sample_size = 30
topic = []
prob = []
checker_string = "Topic:"
topicno = 1
with open(path2topics,'r') as f:
    for line in f.readlines():
        if(line.find(checker_string)!=-1):
            topic = []
            prob = []   
        else:
            line = line.replace(" : ",":")
            top_prob = line.split(':')
            prob.append(float(top_prob[1]))
            topic.append(top_prob[0])
            if(len(prob)==sample_size):
                filename = checker_string + str(topicno) + ".png"
                d = {w: f for w, f in zip(topic,prob)}
                wordcloud = WordCloud(background_color='turquoise', colormap='inferno', prefer_horizontal=1)
                wordcloud.generate_from_frequencies(frequencies=d)
                plt.imshow(wordcloud)
                plt.axis('off')
                plt.show()
                plt.savefig(filename)
                topicno += 1



"""d = {w: f for w, f in
     zip(['italian', 'decent', 'groupon', 'strip', 'fork', 'quiet', 'food decent', 'typical', 'disappointed','isn','car','long time','hostess','expexted','priced'],
         [0.020095687,0.016522536,0.013868708,0.01174721,0.011203488,0.009762707,0.008950789,0.008469931,0.008433853,0.008296738, 0.008194167,0.007993372,0.007914658,0.007594712,0.007569114])}
wordcloud = WordCloud(background_color='turquoise', colormap='inferno', prefer_horizontal=1)
wordcloud.generate_from_frequencies(frequencies=d)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
"""