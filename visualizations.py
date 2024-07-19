import plotly.graph_objects as go

# Define a color palette
COLOR_PALETTE = {
    'blue': '#1f77b4',
    'orange': '#ff7f0e',
    'green': '#2ca02c',
    'red': '#d62728',
    'purple': '#9467bd',
    'brown': '#8c564b',
    'pink': '#e377c2',
    'gray': '#7f7f7f',
    'olive': '#bcbd22',
    'cyan': '#17becf'
}

def create_comparison_chart(total_original_value, total_new_value_folio):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Without Folio', 'With Folio'], 
                         y=[total_original_value, total_original_value + total_new_value_folio],
                         name='Sales Value',
                         marker_color=[COLOR_PALETTE['blue'], COLOR_PALETTE['green']]))
    fig.update_layout(
        title='Sales Value Comparison',
        yaxis_title='Sales Value ($)',
        bargap=0.4,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    return fig

def create_sensitivity_chart(variable, values, labels):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, 
        y=values, 
        name='ROI',
        marker_color=COLOR_PALETTE['orange']
    ))
    fig.update_layout(
        title=f'ROI Sensitivity to {variable}',
        xaxis_title=variable,
        yaxis_title='ROI (%)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    return fig