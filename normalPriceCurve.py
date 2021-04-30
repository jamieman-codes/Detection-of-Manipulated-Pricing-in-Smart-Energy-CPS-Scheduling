import pandas
from scipy.optimize import linprog
import matplotlib.pyplot as plt

input = pandas.read_csv('COMP3217CW2Input.csv')

#Split input into users
user1 = input.iloc[0:10]
user2 = input.iloc[10:20]
user3 = input.iloc[20:30]
user4 = input.iloc[30:40]
user5 = input.iloc[40:50]
users = [user1,user2,user3,user4,user5]
userVars = []

pricing = [4.246522377, 3.640027796, 3.480502639, 3.245460995, 3.162915992, 3.597667495, 3.905355954, 4.078340246, 5.374797426, 4.944699124, 5.438100083, 3.909231366, 6.200666726, 4.482141894, 5.410801558, 6.149170969, 5.8837687, 6.329263208, 6.469511152, 5.58349762, 5.558922379, 5.255354797, 5.568480613, 5.441475567]

#Compute how many varibles will be needed to calculate the soultion for each user
for user in users:
    totalVars = 0
    for index, task in user.iterrows():
        for x in range(task["Ready Time"], task["Deadline"] + 1):
            totalVars += 1
    userVars.append(totalVars)

total = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0}
for userPos in range(0, len(users)):
    c = [] #coefficients of the linear objective function to be minimized.
    a = [] #The equality constraint matrix.
    b = [] #The equality constraint vector
    bounds = [] #Array of bounds
    hours = [] #Maps to result array
    a_index = 0
    for index, task in users[userPos].iterrows(): #Loop over each users task
        a_row = []
        for i in range(0, a_index):
            a_row.append(0)
        for x in range(task["Ready Time"], task["Deadline"] + 1):
            c.append(pricing[x]) #Get price
            a_index += 1
            a_row.append(1)
            bounds.append((0,1))
            hours.append(x)
        for i in range(a_index, userVars[userPos]):
            a_row.append(0)
        a.append(a_row)
        b.append(task["Energy Demand"])

    #Work out minimisation for user        
    res = linprog(c, A_eq=a, b_eq=b, bounds=bounds)
    print("User " +str(userPos + 1) + " total energy used: ", res.fun)
    resX  = res.x
    #Add to total
    for x in range(0, len(hours)):
        total[hours[x]] += resX[x]

#Plot
plt.plot(total.keys(), total.values())
plt.title("Scheduling Soultions for Normal Pricing curve")
plt.xlabel("Time")
plt.ylabel("Energy Used")
plt.grid(True)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
plt.show()
