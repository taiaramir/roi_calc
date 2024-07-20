import streamlit as st
from calculations import calculate_roi
from visualizations import create_comparison_chart, create_sensitivity_chart
from plans import PLANS
from streamlit import session_state as state


st.set_page_config(page_title="Folio ROI Calculator", layout="wide")

# Add this custom CSS
st.markdown("""
<style>
.metric-container {
    margin-bottom: 20px;
}
.metric-label {
    font-size: 16px;
    color: #888;
    margin-bottom: 0;
}
.metric-value {
    font-size: 24px;
    font-weight: 300;  /* This makes the font light weight */
    color: #4CAF50;
    margin-top: 0;
}
</style>
""", unsafe_allow_html=True)


def main():
    # Plan selection
    selected_plan = st.sidebar.selectbox('Select Plan:', options=list(PLANS.keys()), key='plan_select')
    plan_data = PLANS[selected_plan]

    # Sidebar inputs
    st.sidebar.header('Input Parameters')
    sales_people = st.sidebar.number_input('Number of Sales People:', min_value=1, value=plan_data['sales_people'], key='sales_people')
    closed_pitch_value = st.sidebar.number_input('Closed Pitch Value ($):', min_value=0, value=plan_data['closed_pitch_value'], key='closed_pitch_value')
    weekly_pitches = st.sidebar.number_input('Weekly Pitches Per Person:', min_value=0, value=10, key='weekly_pitches')
    close_rate = st.sidebar.number_input('Close Rate (%):', min_value=0.0, max_value=100.0, value=plan_data['close_rate'], key='close_rate')
    additional_weekly_pitches = st.sidebar.number_input('Additional Weekly Pitches Per Person With Folio:', min_value=0, value=3, key='additional_weekly_pitches')
    folio_annual_fee = st.sidebar.number_input('Folio Annual Fee ($):', min_value=0, value=plan_data['folio_annual_fee'], key='folio_annual_fee')
    months = st.sidebar.selectbox('Time Period (Months):', options=[3, 6, 12], index=2, key='months')

    if st.sidebar.button('Calculate ROI', key='calculate_button') or 'results' not in state:
        state.results = calculate_roi(sales_people, closed_pitch_value, weekly_pitches, close_rate, additional_weekly_pitches, folio_annual_fee, months)
        state.params = {
            'sales_people': sales_people,
            'closed_pitch_value': closed_pitch_value,
            'weekly_pitches': weekly_pitches,
            'close_rate': close_rate,
            'additional_weekly_pitches': additional_weekly_pitches,
            'folio_annual_fee': folio_annual_fee,
            'months': months
        }

    if 'results' in state:
        display_results(state.results)
        display_visualizations(state.results)
        display_sensitivity_analysis(state.params)

    display_assumptions()

def display_results(results):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class='metric-container'>
                <p class='metric-label'>Total Original Value</p>
                <p class='metric-value'>${int(results['total_original_value']):,}</p>
            </div>
            <div class='metric-container'>
                <p class='metric-label'>Total New Value with Folio</p>
                <p class='metric-value'>${int(results['total_new_value_folio']):,}</p>
            </div>
            <div class='metric-container'>
                <p class='metric-label'>Net Gain from Folio</p>
                <p class='metric-value'>${int(results['net_gain']):,}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-container'>
                <p class='metric-label'>ROI for Folio</p>
                <p class='metric-value'>{int(results['roi'])}%</p>
            </div>
            <div class='metric-container'>
                <p class='metric-label'>Folio pays for itself</p>
                <p class='metric-value'>{results['pay_for_itself']:.1f} times over</p>
            </div>
            <div class='metric-container'>
                <p class='metric-label'>Additional Closed Deals</p>
                <p class='metric-value'>{int(results['total_new_value_folio'] / results['closed_pitch_value'])}</p>
            </div>
        """, unsafe_allow_html=True)

def display_visualizations(results):
    fig = create_comparison_chart(results['total_original_value'], results['total_new_value_folio'])
    st.plotly_chart(fig)

def display_sensitivity_analysis(params):
    st.header('Sensitivity Analysis')
    sensitivity_variable = st.selectbox('Select variable for sensitivity analysis:', 
                                        ['Additional Weekly Pitches', 'Close Rate', 'Closed Pitch Value'],
                                        key='sensitivity_select')
    
    if sensitivity_variable == 'Additional Weekly Pitches':
        values = [calculate_roi(**{**params, 'additional_weekly_pitches': i})['roi'] for i in range(1, 6)]
        labels = list(range(1, 6))
        x_title = 'Additional Weekly Pitches'
    elif sensitivity_variable == 'Close Rate':
        values = [calculate_roi(**{**params, 'close_rate': i})['roi'] for i in range(5, 26, 5)]
        labels = [f"{i}%" for i in range(5, 26, 5)]
        x_title = 'Close Rate'
    else:  # Closed Pitch Value
        values = [calculate_roi(**{**params, 'closed_pitch_value': i})['roi'] for i in range(10000, 50001, 10000)]
        labels = [f"${i:,}" for i in range(10000, 50001, 10000)]
        x_title = 'Closed Pitch Value'

    fig = create_sensitivity_chart(x_title, values, labels)
    st.plotly_chart(fig)

def display_assumptions():
    st.sidebar.markdown("""
    ## Assumptions
    - Consistent performance throughout the selected time period
    - Linear relationship between additional pitches and closed deals
    - No seasonal variations in sales performance
    """)

if __name__ == "__main__":
    main()