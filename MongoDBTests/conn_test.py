import pymongo
print ("Starting the test...")

my_uri = "mongodb+srv://mvpuser:superuser@cluster0.xznyzq7.mongodb.net/?appName=Cluster0"

print ("Got the address ready")

try:
  client = pymongo.MongoClient(my_uri)
  print("Door opened! Connected.")
  client.admin.command('ping')
  print("Said hello-it's listening")
  client.close()
  print("All done-hung up")
except:
  print("Oops, door locked. Error happened!")