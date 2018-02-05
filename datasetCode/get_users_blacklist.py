import matplotlib.pyplot as plt
import plotly.plotly as py
from load_jsons import *
import collections

createBlacklist = True

data = load("../../../hd/datasets/instaEmotions/json/")
print "Number of jsons: " + str(len(data))

posts_TH = 50  # Will discard users having more than 100 publications, they are probably spam

# Plot num of publications of top  users
users = {}
for k, v in data.iteritems():
    if v['owner']['id'] not in users:
        users[v['owner']['id']] = 1
    else:
        users[v['owner']['id']] = users[v['owner']['id']] + 1

print "Number of users: " + str(len(users))
print "User with max publications has:  " + str(max(users.values()))

topX = 5000
user_publis_sorted = users.values()
user_publis_sorted.sort(reverse=True)
x = range(topX)
width = 1/1.5
plt.bar(x, user_publis_sorted[0:topX], width, color="blue")
plt.title("Num of posts of top authors")
plt.show()
print "Done"

if createBlacklist:
    # Create a blacklist of users: That will be users having more than X publications (100)
    print "Creating users black list"
    users_blacklist = open("../../../hd/datasets/instaEmotions/users_blacklist" + str(posts_TH) + ".txt","w")
    blacklisted = 0
    for user, num in users.iteritems():
        if num > posts_TH:
            blacklisted += 1
            users_blacklist.write(str(user) + '\n')
    print "Num of blacklisted users: " + str(blacklisted)


print "Done"

