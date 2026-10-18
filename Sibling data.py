import pandas as pd 
#create Dataframe with sample data
data={
    'Name':['Susan','Grace','John','Morgan'],
    'Gender':['Female','Female','Male','Male'],
    'Age':[40,38,36,20],
    'Height':['Medium','Medium','Medium','Tall']
}
Siblings=pd.DataFrame(data)
print(Siblings)
