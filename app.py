import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import datetime
from bs4 import BeautifulSoup
import requests
url ="https://dps.psx.com.pk/screener"
headers = {'User-Agent': 'Mozilla/5.0'}
r=requests.get(url)
Soup=BeautifulSoup(r.text,'html.parser')
table = Soup.find('table')
rows = table.find_all('tr')
data=[]
headers = [header.text.strip() for header in rows[0].find_all('th')]
for row in rows[1:]:  # Skip the header
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]#ele is variable for element in <td>
    if cols:  # If row is not empty
        data.append(cols)
df = pd.DataFrame(data, columns=['SYMBOL', 'SECTOR', 'LISTED IN','MARKET CAP.','PRICE','CHANGE(%)','1-YEAR CH.(%)*','PE RATIO(TTM)','DIVIDEND YEILD(%)','FREE FLOAT','30D VOLUMNE AVG.'])
st.title("Psx Investment Tracker:W.r.t Share Price and Currency Value")
#st.dataframe(df)
st.write("Select Share and enter purchase price against it")
Col=df["SYMBOL"]#.tolist()
Share=st.selectbox("Select",Col)
df1=df[df["SYMBOL"]==Share]
#st.write(df1)
Share_price=float(df1['PRICE'])
Qty=st.number_input("Enter no of share Purchase",min_value=1)
Price=st.number_input("Enter purchase price of each share",min_value=.01)
Date=st.date_input("Enter date of Purchase",value=datetime.date(2015,4,27))
#st.write(type(Date))
Output=Qty*Price
C_Output=Qty*Share_price
df2=pd.read_csv(r"Dollar_rate.csv")
#st.dataframe(df2)
df2['Date']=pd.to_datetime(df2['Date']).dt.date
df2_rate=df2[df2['Date']==Date]
st.write(f"Conversion Rate:1$=Rs.,{float(df2_rate['Price']):,.2f}")
st.subheader("Purchase Value")
Dol=(df2_rate['Price'])
inv_d=(Output/Dol)
st.markdown(f"Your total investment in **{Share}** was **Rs.{float(Output):,.2f}**which was equivalent to **{float(inv_d):,.2f} dollars**")
st.subheader("Return on Investment")
Date_R=st.date_input("Enter date on which Return_Investment is to be check",value=datetime.date(2025,4,25))
df3_r_rate=df2[df2['Date']==Date_R]
Dol_r=(df3_r_rate['Price'])
inv_r=(C_Output/Dol_r)

st.markdown(f"Your investment in **{Share}** as per current rate you investment is equal to **Rs.{float(C_Output):,.2f}** i.e **{float(inv_r):,.2f} dollars**") # and equivalen to {inv_Dollar}now")
if float(inv_r)<float(inv_d):
    st.markdown("**You are in loss**")
else:st.markdown("**You are in Profit**" )
#st.bar_chart(Dol,Dol_r)
fig,ax=plt.subplots(figsize=(10,6))
ax.scatter(Date,float(inv_d),color="Green")
ax.scatter(Date_R,float(inv_r),color="blue")
ax.plot([Date,Date_R],[float(inv_d),float(inv_r)],linestyle='--',color="Black")
ax.set_xlabel("Date")
ax.set_ylabel("Value in $")
st.pyplot(fig)  



  