def calculate_roi(sales_people, closed_pitch_value, weekly_pitches, close_rate, additional_weekly_pitches, folio_annual_fee, months):
    # Calculate pitches
    monthly_pitches = weekly_pitches * 4
    period_pitches = monthly_pitches * months
    
    # Calculate closed pitches
    total_closed_pitches_per_person = period_pitches * (close_rate / 100)
    total_closed_pitches_company = total_closed_pitches_per_person * sales_people
    
    # Calculate additional pitches with Folio
    additional_monthly_pitches = additional_weekly_pitches * 4
    additional_period_pitches = additional_monthly_pitches * months
    additional_won_pitches_per_person = additional_period_pitches * (close_rate / 100)
    additional_won_pitches_company = additional_won_pitches_per_person * sales_people
    
    # Calculate values
    total_original_value = total_closed_pitches_company * closed_pitch_value
    total_new_value_folio = additional_won_pitches_company * closed_pitch_value
    
    # Calculate ROI
    folio_period_fee = folio_annual_fee * (months / 12)
    net_gain = total_new_value_folio - folio_period_fee
    roi = (net_gain / folio_period_fee) * 100
    pay_for_itself = net_gain / folio_period_fee
    
    return {
        'total_original_value': total_original_value,
        'total_new_value_folio': total_new_value_folio,
        'net_gain': net_gain,
        'roi': roi,
        'pay_for_itself': pay_for_itself,
        'closed_pitch_value': closed_pitch_value
    }