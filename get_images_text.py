import flickr_api
from flickr_api.api import flickr
import os
import glob

data_path = "../../datasets/EmotionDataset/agg"
out_path = "../../datasets/EmotionDataset/txt/"

flickr_api.set_keys(api_key = '0a4ef63db8d41381ec68ad218cac019f', api_secret = 'd367ebc499917aae')
# a = flickr_api.auth.AuthHandler()
# perms = "read"
# url = a.get_authorization_url(perms)
# print url
# a.set_verifier("de2cefb149ba1e0d")
# flickr_api.set_auth_handler(a)
# a.save("aux.txt")
flickr_api.set_auth_handler("auth.txt")

errors = 0
done = 0
for file_name in glob.glob(data_path + "/*.csv"):
    print file_name
    with open(file_name, 'r') as file:
        for line in file:
            done += 1
            try:
                data = line.split(',')
                out_name = data[1].split('/')[-1]

                if not os.path.exists(out_path + data[0]):
                    os.makedirs(out_path + data[0])

                out_name = out_path + data[0] + '/' + out_name.replace('jpg','txt')

                im_id = data[1].split('/')[4].split('_')[0]
                xml = flickr.photos.getInfo(photo_id=im_id)
                try:
                    title = xml.split('<title>')[1].split('</title>')[0]
                except:
                    print "Wrong title"
                    errors +=1
                    print "Errors: " + str(errors) + " out of " + str(done)
                    title = ""
                try:
                    description = xml.split('<description>')[1].split('</description>')[0]
                except:
                    print "Wrong description"
                    errors +=1
                    print "Errors: " + str(errors) + " out of " + str(done)
                    description = ""
                try:
                    tags = ""
                    num_tags = len(xml.split('</tag>')) - 1
                    for i in range(0,num_tags):
                        tag = xml.split('</tag>')[i].split('>')[-1]
                        tags += tag + " "
                except:
                    print "Wrong tags"
                    errors +=1
                    print "Errors: " + str(errors) + " out of " + str(done)
                    tags = ""

                text = title + "\n" + description + "\n" + tags

                with open(out_name,'w') as f:
                    f.write(text)

            except:
                print "Failed to download metdata for: " + str(data[1])
                errors += 1
                print "Errors: " + str(errors) + " out of " + str(done)
                continue

print "Done"
print "Errors: " + str(errors) + " out of " + str(done)
