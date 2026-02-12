Attach to existing chrome session by starting it with open port on 9222. This allows you to attach to instagram, grok, and pinterest accounts with NO API KEY. 
Of course, this is only for infrequent posts, e.g. once per day. Also this requires constant internet connection, I am running on a dedicated server.

Background images and music clips (extracting the catchiest parts based on byoutube heatmap) can be downloaded with backgrounds.py and heatmap.py.
Backgrounds.py extract images from pinterest, and requires giving in a suitable search url.
Heatmaps.py takes in a JSON.
I used each to extract about a hundred of each and then randomise selectin during video generation

The VidBot simply generates videos consisting of fading text and a fading background for simple video generation.
I query grok to generate text in a JSON file which suits my use case of creating quote videos.
