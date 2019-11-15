from wordcloud import WordCloud

words = open('again.txt', encoding='utf-8').read()  # 打开歌词文件，获取到歌词
wordcloud = WordCloud(width=1000,  # 图片的宽度
                      height=860,  # 高度
                      margin=2,  # 边距
                      background_color='black',  # 指定背景颜色
                      font_path='simsun.ttf'  # 指定字体文件，要有这个字体文件，自己随便想用什么字体，就下载一个，然后指定路径就ok了
                      )
wordcloud.generate(words)  # 分词
wordcloud.to_file('again.jpg')  # 保存到图片
