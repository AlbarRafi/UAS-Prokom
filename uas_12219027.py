import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def menu1() :
	st.write("### Oil Production")
	countries = st.selectbox("Choose countries", list(data_countries))
	data = df.loc[countries]
	fig,ax = plt.subplots(facecolor = '#303340')
	ax.plot(data['tahun'],data['produksi'])
	ax.set_facecolor('#303340')
	plt.grid(color = 'black', ls = '--')
	plt.xlabel('Year')
	plt.ylabel('Production (STB)')
	st.pyplot(fig)

def menu2() :
	st.write("### Oil Production Data per year")
	prod = st.number_input("Year",min_value =  df['tahun'].min(), max_value = df['tahun'].max(), value = df['tahun'].min())
	ranked_data = df[df['tahun'] == prod].sort_values(by = 'produksi', ascending = False).drop(['tahun'], axis = 1)

	#Kode negara
	code = [df_code[df_code['name'] == i].index[0] for i in ranked_data.index]
	ranked_data['kode_negara'] = code

	#Re-arrange
	produksi = ranked_data['produksi']
	ranked_data.drop(['produksi'], axis = 1, inplace = True)
	ranked_data['produksi'] = produksi

	rank1 = st.number_input("Top",min_value = 3, max_value = 50, value = 3)
	st.write(ranked_data.iloc[:rank1])

	#Plotting
	fig1,ax1 = plt.subplots(facecolor = '#303340')
	x = ranked_data.iloc[:rank1]['kode_negara']
	y = ranked_data.iloc[:rank1]['produksi']
	ax1.bar(x,y)
	ax1.set_facecolor('#303340')
	plt.grid(color = 'black', ls = '--', axis = 'y')
	plt.xlabel('Countries')
	plt.ylabel('Production (STB)')
	plt.tight_layout()
	st.pyplot(fig1)

def menu3() :
	st.write("### Cumulative Oil Production Data")
	rank2 = st.number_input("Top",min_value = 3, max_value = len(dc), value = 3)

	code = [df_code[df_code['name'] == i].index[0] for i in dc.index]
	dc['kode_negara'] = code

	rc = dc.copy()
	pdr = rc["Produksi"]
	rc.drop(["Produksi"], axis = 1, inplace = True)
	rc["Produksi"] = pdr

	st.write(rc.iloc[:rank2])
	fig2, ax2 = plt.subplots(facecolor='#303340')
	x = rc.iloc[:rank2]["kode_negara"]
	y = rc.iloc[:rank2]['Produksi']
	ax2.bar(x, y)
	ax2.set_facecolor('#303340')
	plt.grid(color='black', ls='--', axis='y')
	plt.xlabel('Countries')
	plt.ylabel('Cumulative Production (STB)')
	plt.tight_layout()
	st.pyplot(fig2)

def menu4() :
	st.write("### General Information")
	year = st.number_input("Select year",min_value =  df['tahun'].min(), max_value = df['tahun'].max(), value = df['tahun'].min())
	maximum = df.loc[df['tahun'] == year]['produksi'].max()
	minimum = df.loc[(df['tahun'] == year) & (df['produksi'] > 0)]['produksi'].min()
	data_zeros = df[(df['tahun'] == year) & (df['produksi'] == 0)]
	data_max = df[(df['produksi'] == maximum) & (df['tahun'] == year)]
	data_min = df[(df['produksi'] == minimum) & (df['tahun'] == year)]
	
	#Combine data
	all_data = pd.concat([data_zeros,data_min,data_max])

	#Kode negara
	code = [df_code[df_code['name'] == i].index[0] for i in all_data.index]
	all_data['kode_negara'] = code

	#Region
	region = [df_code[df_code['name'] == i]['region'][0] for i in all_data.index]
	all_data['region'] = region

	#Sub-region
	subregion = [df_code[df_code['name'] == i]['sub-region'][0] for i in all_data.index]
	all_data['sub-region'] = subregion

	#Hapus kolom tahun dan pindah kolom produksi
	produksi = list(all_data['produksi'])
	all_data.drop(['tahun','produksi'],axis = 1,inplace = True)
	all_data['produksi'] = produksi

	#Produksi kumulatif
	cum = [dc.loc[i][0] for i in all_data.index]
	all_data['produksi kumulatif'] = cum

	st.write("Maximum Production",all_data[all_data['produksi'] == maximum])
	st.write("Minimum Production",all_data[all_data['produksi'] == minimum])
	st.write("Zero Production",all_data[all_data['produksi'] == 0])


df = pd.read_csv("produksi_minyak_mentah.csv")
df_code = pd.read_json("kode_negara_lengkap.json")

#Data kode negara
df.set_index('kode_negara',inplace = True)
rdata_code = np.array(df.index)


#Kamus kode negara
df_code.set_index('alpha-3',inplace = True)
book_code = np.array(df_code.index)

#Data negara (mentah)
rdata_countries = np.array([df_code.loc[i]['name'] for i in rdata_code if i in book_code])
data_countries = np.unique(rdata_countries)

#Menghilangkan kode yang tidak ada pada kamus
for i in np.unique(rdata_code) : 
	if i not in book_code : 
		df.drop(i,inplace = True)

df.set_index(rdata_countries,inplace = True)

#Data kumulatif
cumulative_book = []
for i in data_countries : cumulative_book+=[[i,df.loc[i]['produksi'].sum()]]	
dc = pd.DataFrame(cumulative_book, columns = ['Name', 'Produksi'], index = data_countries).drop(['Name'],axis = 1).sort_values(by = 'Produksi', ascending = False)
menu1()
menu2()
menu3()
menu4()
