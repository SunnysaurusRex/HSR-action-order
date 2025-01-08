import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#pandas read xcel file
c1 = pd.read_excel('HSR_speed1.xlsx',
					   sheet_name = 0,
					   index_col = None
					   )
sheet2 = pd.read_excel('HSR_speed1.xlsx',
					   sheet_name = 1,
					   index_col = None
					   )
sheet3 = pd.read_excel('HSR_speed1.xlsx',
					   sheet_name = 2,
					   index_col = None
					   )
sheet4 = pd.read_excel('HSR_speed1.xlsx',
					   sheet_name = 3,
					   index_col = None
					   )
print(sheet2.index) #column names
test_name = sheet2['extra_spd']
print('x',test_name)
test_array = sheet3['extra_spd']
print(c1['name'][0])

N = 7
#reformat dataframe columns into arrays size N
def reform(array, n):
	array = array.to_numpy()
	array[np.isnan(array)] = 0 #isnan is useful for finding bad data in arrays / if isnan True: change nan to 0
	array = np.concatenate([array, np.zeros(n - array.size)])
	return array

print(reform(test_array, N))



class character:
	def __init__(self, name, base_speed, extra_speed, N, percent_speed, flat_speed, action_forward):
		self.name = name
		self.b_spd = base_speed 
		self.e_spd = extra_speed
		self.n = N
		self.p_spd = percent_speed
		self.f_spd = flat_speed
		self.af = action_forward
		#self.p_spd = np.array(percent_speed, dtype=object)
		#self.f_spd = np.array(flat_speed, dtype=object)
		#self.af = np.array(action_forward, dtype=object)
		self.AV = np.empty(self.n)
		self.AV[0] = (10000/((self.b_spd*(1+(self.p_spd[0]/100)))+(self.e_spd+self.f_spd[0])))*((100-self.af[0])/100)
		for i in range(1, self.n):
			x =(10000/((self.b_spd*(1+(self.p_spd[i]/100)))+(self.e_spd+self.f_spd[i])))*((100-self.af[i])/100)
			self.AV[i] = x + self.AV[i-1]
	

	def print(self):
		print(f'{self.name} {self.b_spd} {self.f_spd} {self.p_spd}\n {self.AV}kekw')

	def print_AV(self): print(f'{self.AV}')

	def AV(self):
		self.AV[0] = (10000/((self.b_spd*(1+(self.p_spd[0]/100)))+(self.e_spd+self.f_spd[0])))*((100-self.af[0])/100)
		for i in range(1, self.n):
			x =(10000/((self.b_spd*(1+(self.p_spd[i]/100)))+(self.e_spd+self.f_spd[i])))*((100-self.af[i])/100)
			self.AV[i] = x + self.AV[i-1]
		return self.AV

	def AVsort(self):
		string = np.char.array([self.name]*self.n)
		for i in range(self.n):
			self.AV[i] = np.round(self.AV[i], 2)
		#self.AVsort = self.AV.astype(str)
		#create_name_AV = np.vstack(([[self.name]*self.n], [self.AV]))
		#print(create_name_AV, 'a')
		#AV_df = pd.Series(self.AV)	
		AV_df = pd.DataFrame({
				'Name': [self.name]*self.n,
				'action_value': self.AV
			})
		#print(AV, 'pandas')
		#self.AVsort = np.vstack((string, self.AVsort)).T
		return AV_df


#Jade_percent_speed= np.concatenate( ([10]*2, np.zeros(5)) )
#Jade_flat_speed = np.zeros(7)
#Jade_action_forward = [50, 0, 0, 0, 0, 0, 0]
#Jade = character('Jade', 103, 4, 7, Jade_percent_speed, Jade_flat_speed, Jade_action_forward)
print('b', c1['base_spd'][0])
Jade = character(c1['name'][0],
				 c1['base_spd'][0],
				 c1['extra_spd'][0], 7,
				 reform(c1['percent_spd'], N),
				 reform(c1['flat_spd'], N),
				 reform(c1['action_forward'], N)
				 
				 )

Jade.print_AV()
#print('Jade AV:', Jade.AV())

Yukong_percent_speed = np.concatenate( ([10]*2, np.zeros(7)) )
Yukong_flat_speed = np.zeros(9)
Yukong_action_forward = np.zeros(9)
Yukong = character('----Yukong', 107, 30.1, 9, Yukong_percent_speed, Yukong_flat_speed, Yukong_action_forward)

Serval_percent_speed = [10, 24] + [14]*6
Serval_flat_speed = [0] + [30]*6
Serval_action_forward = np.zeros(7)
Serval = character('Serval', 104, 7.2, 7,Serval_percent_speed, Serval_flat_speed, Serval_action_forward)


Gallagher_percent_speed = np.concatenate( ([10]*2, np.zeros(5)) )
Gallagher_flat_speed = np.zeros(7)
Gallagher_action_forward = np.zeros(7)
Gallagher = character('Gallagher', 98, 42, 7, Gallagher_percent_speed, Gallagher_flat_speed, Gallagher_action_forward)

print('xd')

x = pd.concat([Jade.AVsort(), Yukong.AVsort(), Serval.AVsort(), Gallagher.AVsort()])
y = pd.DataFrame(x)
#y.columns = ['action_value']
y.set_index('action_value', inplace=True)
y = y.sort_values(by=['action_value'])
y = y.reset_index()
y = y[['Name', 'action_value']]
#print('x',y)
aa = Jade.AV

#z = pd.DataFrame(np.transpose([string, aa]))

#AVskip = y['action_value'][0]

#y = y - AVskip
#index = y[(y.action_value == 0)].index
#y = y.drop(index)

#print('__\n\n',y)

row_count = y.shape[0]

print('a',y.index)
print('\n first action\n', y)

"""
while True:
	if y.empty: 
		print('\nlast action')
		break
	else:
		input('\npress key')
		print('accepted key')
		currentAV = y['action_value'].iloc[0]  # get integer location of integer=0
		#currentAV = y.index[0]
		#print(currentAV)
		y['action_value'] = y['action_value'] - currentAV
		print('\n current acting character\n', y)
		input('\nnext turn order')
		#index = y[(y.action_value == 0)].index
		y = y.drop(0)
		y = y.reset_index(drop=True)

"""


