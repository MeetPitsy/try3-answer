import requests
import os
import json
import streamlit as st
import pandas as pd
import emoji
from deta import Deta 

def home_page():
    st.title(emoji.emojize('Welcome to CPG Brand - Manufacturer Matching App :factory:'))
    # Add an image
    st.image('/Users/seanjenkins/desktop/myproject/try3-answer/Automation2.jpg', caption='At-Home autonomous CPG manufacturing & 3pl fulfillment center', use_column_width=True)
    st.write('This app helps CPG brands find the perfect contract manufacturer.')
    if st.button('Let\'s go!'):
        st.session_state.page += 1

def load_data():
    manufacturers = pd.DataFrame({
        'Name': ['Gar Labs', 'Pitsy Automation', 'Lily\'s', 'Beauty Private Label', 'Federal Packaging', 'Twincraft', 
                 'Coughlin Companies', 'Sinoscan', 'KKT', 'Goodkind Co', 'Botanic Beauty Labs', 
                 'Essential Wholesale', 'Genie Supply', 'Glow Essential Labs'],
        'MOQ': [5000, 0, 10000, 3000, 5000, 15000, 5000, 10000, 5000, 10000, 1000, 1000, 1500, 500],
        'Time': [14, 0.125, 16, 12, 15, 20, 14, 16, 15, 17, 15, 17, 17, 10],
        'Price_per_unit': [2.00, 1.49, 5.50, 4.50, 5.00, 2.50, 4.50, 3.50, 5.00, 3.00, 4.50, 3.49, 4.00, 3.00],
        'Email': ['tom@garlabs.com', 'hello@meetpitsy.com', 'hello@moesgroup.org', 'Sales@bqgmanufacturing.com', 'info@federalpackage.com', 
                  'jackson.berman@twincraft.com', 'info@contactcoghlin.com', 'info@sinoscan.com', 'krupa@kktconsultants.com', 
                  'info@nutracapusa.com', None, None, None, None],
        'Comments': ['Best so far, we have to provide packaging, and transport for shipping...', 
                     None, None, 'Injection molding, customer supplied containers, labeling, screen printing',
                     'Base strategy of library of formulas that are then customized. Small handful of bases ready to be scaled up.',
                     None, None, None, None, None, '10 gallon minimum order of customization formulation but did offer 500-1000 units in filling', 
                     None, 'Timeline for quote day or two - foundation of raw material (1-2 weeks to approving sample manufacturing is 3-4 weeks) Projections and forecast of amount of units to help lead times', None]
    })
    return manufacturers

def post_to_deta(data):
    try:
        # Deta Base uses 'put' method to store data
        response = base.put(data['records'][0]['fields'])
        return response
    except Exception as e:
        st.error(f"An Error occurred: {e}")
        ...

def input_company_info():
    st.title(emoji.emojize('Enter Your Company Information :memo:'))
    company_name = st.text_input('Company Name', placeholder='Enter Company Name')
    product_type = st.text_input('Product Type', placeholder='Enter Product Type')
    segment = st.text_input('Segment', placeholder='Enter Segment')
    annual_units = st.number_input('Annual Units', value=0)
    website_url = st.text_input('Website URL', placeholder='http://')
    revenue_last_year = st.number_input('Revenue in the last 12 months ($)', value=0)
    price_per_unit = st.number_input('Price Per Unit ($)', value=0)
    projected_revenue = st.number_input('Projected Revenue for the next 12 months ($)', value=0)
    ideal_monthly_units = st.number_input('Ideal Monthly Units', value=0)
    monthly_units_sold = st.number_input('Monthly Units Sold', value=0)
    differentiation = st.text_input('Company Differentiation', placeholder='What sets your company apart?')
    monthly_revenue = st.number_input('Average Monthly Revenue ($)', value=0)
    monthly_expense = st.number_input('Average Monthly Expense ($)', value=0)

    if st.button('Submit'):
        data = {
            "records": [
                {
                    "fields": {
                        "Company Name": company_name,
                        "Product Type": product_type,
                        "Segment": segment,
                        "Annual Units": annual_units,
                        "Website URL": website_url,
                        "Revenue Last Year": revenue_last_year,
                        "Price Per Unit": price_per_unit,
                        "Projected Revenue": projected_revenue,
                        "Ideal Monthly Units": ideal_monthly_units,
                        "Monthly Units Sold": monthly_units_sold,
                        "Company Differentiation": differentiation,
                        "Monthly Revenue": monthly_revenue,
                        "Monthly Expense": monthly_expense
                    }
                }
            ]
        }
        response = post_to_deta(data)
        if response:  
            st.success(emoji.emojize('Company Info Saved Successfully! :white_check_mark:'))
            st.session_state.page += 1
        else:
            st.error('Something went wrong. Please try again.')

        # Get your project key from Deta Base dashboard
deta = Deta("b0u5qbektag_2v3XHsha7iGaJ99d5Rrbv3X4StgkGQJ2")  
base = deta.Base("pitsy")

def choose_criteria():
    st.title(emoji.emojize('Choose Your Main Criteria for Manufacturer Selection :mag:'))
    criteria = st.selectbox('Choose your main criteria', ['MOQ', 'Time', 'Price_per_unit'])
    st.session_state.criteria = criteria
    if st.button('Let\'s see the matches!'):
        st.session_state.page += 1

def best_match():
    st.title('Your Best Manufacturer Matches')
    manufacturers = load_data()
    criteria = st.session_state.criteria  # Get the selected criteria from the session state
    # Sort the manufacturers based on the selected criteria
    sorted_manufacturers = manufacturers.sort_values(by=criteria, ascending=True)

    # Fetch top 3 manufacturers
    for i in range(3):
        manufacturer = sorted_manufacturers.iloc[i]
        st.subheader(f'{i+1}. {manufacturer["Name"]}')
        st.write(f"This manufacturer is one of the top choices based on the {criteria} criteria. "
                  f"It has {manufacturer[criteria]} {criteria}.")
        if st.button(f'Contact {manufacturer["Name"]}'):
            mailto = f'mailto:{manufacturer["Email"]}?subject=Inquiry%20from%20CPG%20Brand%20-%20Manufacturer%20Matching%20App&body=Dear%20{manufacturer["Name"]},%0D%0A%0D%0AI%20found%20your%20company%20on%20the%20CPG%20Brand%20-%20Manufacturer%20Matching%20App.%20Could%20you%20please%20provide%20me%20with%20more%20information%20about%20your%20services?%0D%0A%0D%0AThank%20you.'
            st.markdown(f'<a href="{mailto}" target="_blank">Email {manufacturer["Name"]}</a>', unsafe_allow_html=True)

    st.write('These manufacturers have been chosen based on the lowest values of your selected criteria, '
             'which could translate into lower production costs and faster delivery times for your CPG brand.')
    if st.button('Back to Home'):
        st.session_state.page = 0

def manufacturers_list():
    st.title('Manufacturers List')
    manufacturers = load_data()
    st.write(manufacturers)
    if st.button('Back to Home'):
        st.session_state.page = 0

def admin_login():
    st.title('Admin Login')
    pwd = st.text_input("Enter Password", type='password')  # Using 'password' as type hides the input
    if st.button('Login'):
        if pwd == 'admin_password':  # Replace 'admin_password' with the actual password
            st.session_state.page += 1
        else:
            st.error("The password you entered is incorrect.")

PAGES = [home_page, input_company_info, choose_criteria, best_match, admin_login, manufacturers_list]

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 0
    PAGES[st.session_state.page]()

if __name__ == "__main__":
    main()

