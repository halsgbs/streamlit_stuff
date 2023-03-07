import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title='FC search engine', page_icon=':tada')
full_table = pd.read_excel('master_data.xlsx')
checks_table = pd.read_excel('Results.xlsx')





def search_for_custkey(seqq):
    df = pd.read_excel('master_data.xlsx')
    search_results = df[df['CustomerKey'] == int(seqq)]
    return search_results

def search_for_custlabel(seqq):
    df = pd.read_excel('master_data.xlsx')
    search_results = df[df['CustomerLabel'] == int(seqq)]
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
    options = ["Home", "Search for account - Customer Key", "Search for account - Customer label", "Legal Checks", "Data results"],
    icons=['house', 'search', 'layers' ,'list','bar-chart-fill'],
    menu_icon='cast',
    default_index=0,
    orientation='Horizontal')

# if 'customer_key' not in st.session_state:
#     st.session_state['customer_key'] = 0

# if 'search_button' not in st.session_state:
#     st.session_state['search_button'] = False
# st.write(st.session_state)

# Create sidebar with options
#options = ["Home", "Search for account - customer Key", "Search for account - customer label", "data results"]
#ßselected = st.sidebar.selectbox("Select an option", options)
# Display output based on selected option
# if selected_option == 'Home':
#     # st.write(""" 
#     # Please see sidebar for options :) 
#     # """)
lottie_arrow = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_mc9dp5xs.json')
lottie_welcome = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_onhsipvc.json')

if selected_option == 'Home':
    st_lottie(lottie_welcome)

if selected_option == "Search for account - customer Key":
        # st.write(""" 
        # # Financial Crime Search Engine
        # """)        
        st.header('Search for Customer Information')
        st.write('##')
        with st.form(key='my_form'):
            customer_key = st.text_input("Enter customer key:")
            search_button = st.form_submit_button(label="Search")
  
        if search_button:
            st.header('Results')
            st.write('###')
            with st.spinner('getting your results...'):
                results = search_for_custkey(customer_key)
                st.write(results)

elif selected_option == "Search for account - customer label":

        # st.write(""" 
        # # Financial Crime Search Engine
        # """)
        st.header('Search for Customer Information')
        with st.form(key='my_form2'):
            cust_label = st.text_input('Enter Customer Label: ')
            search_button = st.form_submit_button(label='Search')

        if search_button:
            st.header('Results')
            st.write('###')
            with st.spinner('getting your results...'):
                results = search_for_custlabel(cust_label)
                st.write(results)
elif selected_option == 'data results':
    st.write(""" ## Full Dataset """)
    st.write(full_table)

elif selected_option == 'Legal Checks':
    st.write(""" 
    ## Check if Customer passed all checks here:

    """)
    with st.form(key='my_form'):
        customer_key = st.text_input("Enter customer key:")
        search_button = st.form_submit_button(label="Search")
    
    if search_button:
        #st.header()
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
