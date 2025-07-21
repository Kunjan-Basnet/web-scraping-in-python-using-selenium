import pandas as pd
# dict={
#     'id':[1,2,3,2,1,3],
#     'name':['ram','sam','hari','sita','gita','gopal']
# }

# df=pd.DataFrame(dict)
# df.to_csv("friends.csv",index=False)

reading=pd.read_csv("friends.csv")
print(reading)
duplicate=reading['id'].value_counts()
dup=duplicate[duplicate>1]
print(dup)
sum_of_all=(dup-1).sum()
print(sum_of_all)
print(reading[reading['id']==2])