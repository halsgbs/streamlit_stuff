
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie
#from PIL import Image
import PIL

st.set_page_config(page_title='FC search engine', page_icon=':tada')


def customer_status(customer_key):
    df = pd.read_excel('tracker.xlsx')
    df.set_index('CustomerKey', inplace=True)
    if int(customer_key) in df.index:
        row = df.loc[int(customer_key)]
        withdrawals = row['Withdrawals']
        refund_attempt =row['Refund_Attempt']
        moneydest = row['Money_Destination']
        investigation = row['Investigation']
        frozen = row['Frozen']
        facility_limit = row['Facility_Limit']
        outstanding_balance = row['Outstanding_balance']


        result = {'Outstanding Balance': outstanding_balance,
        'Withdrawals': withdrawals,
        'Refund Attempt': refund_attempt,
        'Money Destination': moneydest,
        'Investigation': investigation,
        'Frozen': frozen,
        'Facility Limit': facility_limit
        }
        return result
    else:
        return None 




def get_customer_data(customer_key):
    # Check if customer key is in the index
    df = pd.read_excel('master_data.xlsx')
    df.set_index('CustomerKey', inplace=True)
    if int(customer_key) in df.index:
        # Get the row for the customer key
        
        # Get the email address and phone number column values
        row = df.loc[int(customer_key)]
        first_name = row['FirstName']
        last_name = row['LastName']
        email_address = row['EmailAddress']
        phone_number = row['Phone']
        address = row['AddressLine1']
        birth_date = row['BirthDate']
        marital_status = row['MaritalStatus']
        gender = row['Gender']
        yearlyincome = row['YearlyIncome']
        total_kids = row['TotalChildren']
        education = row['Education']
        occupation = row['Occupation']
        cars_owned = row['NumberCarsOwned']

        # Create a dictionary with 'emailaddress' and 'phonenumber' as the keys and their respective column values as the values
        result = {'First Name': first_name, 
        'Last Name': last_name, 
        'Email': email_address, 
        'Phone number': phone_number,
        'Address': address,
        'Birth Date': birth_date,
        'Marital Status': marital_status,
        'Gender': gender,
        'Yearly Income': yearlyincome,
        'Number of Kids': total_kids,
        'Education': education,
        'Occupation': occupation,
        'Cars owned': cars_owned
        }
        return result
    else:
        return None

def search_for_custkey(seqq):
    df = pd.read_excel('master_data.xlsx')
    search_res = df[df['CustomerKey'] == int(seqq)]
    search_results = df[search_res]
    return search_results

def search_for_custlabel(seqq):
    df = pd.read_excel('master_data.xlsx')
    search_res = df[df['CustomerLabel'] == int(seqq)]
    search_results = df[search_res]
    return search_results

def all_checks_passed(seqq):
    df = pd.read_excel('Results.xlsx')
    search_results = df.loc[df['CustomerKey'] == int(seqq)]
    all_checks = search_results['all_clear'].values[0]
    first_name = search_results['FirstName'].values[0]
    last_name = search_results['LastName'].values[0]
    name_of_cust = first_name + ' ' + last_name
    if all_checks == 'Yes':
        end_message = f'{name_of_cust} has passed all the checks.'
        return end_message
    else:
        end_message = f'{name_of_cust} did NOT pass all the checks.'
        return end_message



def which_checks(seqq):
    df = pd.read_excel('Results_without_allclear.xlsx')
    search_results = df.loc[df['CustomerKey'] == int(seqq)]
    empty_list = []
    for column in df.columns:
        if search_results[column].values == 'No':
            empty_list.append(column)
    return empty_list 


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



selected_option = option_menu(menu_title= 'Financial Crime Search Engine',
    options = ["Home", "Customer Info", "Account Tracker", "Legal Checks", "Dashboard"],
    icons=['house', 'search' ,'list', 'easel'],
    menu_icon='cast',
    default_index=0,
    orientation='Horizontal')


lottie_arrow = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_mc9dp5xs.json')
lottie_welcome = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_onhsipvc.json')

if selected_option == 'Home':
    st_lottie(lottie_welcome)

if selected_option == "Customer Info":
     
        st.header('Search for Customer Information')
        st.write('##')
        with st.form(key='my_form'):
            customer_key = st.text_input("Enter customer key:")
            search_button = st.form_submit_button(label="Search")
  
        if search_button:
            st.header('Results')
            st.write('###')
            with st.spinner('getting your results...'):
                results = get_customer_data(customer_key)
                #st.write(results)
                for key,value in results.items():
                    st.write(f'{key}: {value}')

elif selected_option == 'Account Tracker':
    st.header('Search for Account Information')
    st.write('##')
    with st.form(key='my_form'):
        customer_key = st.text_input("Enter customer key:")
        search_button = st.form_submit_button(label="Search")
  
    if search_button:
        st.header('Results')
        st.write('###')
        options = st.selectbox('Info', ('Customer Info', 'Account Info'))
        if options == 'Customer Info':
            with st.spinner('getting your results...'):
                results = get_customer_data(customer_key)
            #st.write(results)
                for key,value in results.items():
                    st.write(f'{key}: {value}')
        if options == 'Account Info':
            with st.spinner('getting your results...'):
                results = customer_status(customer_key)
            #st.write(results)
                for key,value in results.items():
                    st.write(f'{key}: {value}')

elif selected_option == 'Legal Checks':
    st.write(""" 
    ## Check if Customer passed all checks here:

    """)
    with st.form(key='my_form'):
        customer_key = st.text_input("Enter customer key:")
        search_button = st.form_submit_button(label="Search")
    
    if search_button:

        st.write('###')

        with st.spinner('getting your results...'):
            results = all_checks_passed(customer_key)
            results2 = which_checks(customer_key)
            st.write('<h3>' + results + '</h3>', unsafe_allow_html=True)
            if 'did NOT' in results:
                col1,col2 = st.columns([1,3])
                with col1:
                    st.write('###')
                    st_lottie(lottie_arrow, height=90)
                st.write("""

                ### Failed checks are:

                """)
                for item in results2:
                    st.write(item)

elif selected_option == 'Dashboard':
    st.image(PIL.Image.open('page1.png'), use_column_width=True)
    st.image(PIL.Image.open('page2.png'), use_column_width=True)
    st.image(PIL.Image.open('page3.png'), use_column_width=True)
    st.image(PIL.Image.open('page4.png'), use_column_width=True)
    st.image(PIL.Image.open('Picture1.png'), use_column_width=True)   
