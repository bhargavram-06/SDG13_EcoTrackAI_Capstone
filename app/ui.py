import streamlit as st
import plotly.graph_objects as go
from utils.helpers import (
    calculate_transportation_emissions,
    calculate_electricity_emissions,
    calculate_diet_emissions
)
from app.main import CarbonAIEngine

def run_app():
    # Page configurations
    st.set_page_config(
        page_title="SDG 13: Climate Action Portal", 
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize Session State memory keys so data stays persistent
    if "calculated" not in st.session_state:
        st.session_state.calculated = False
    if "ai_response" not in st.session_state:
        st.session_state.ai_response = ""

    # Left Interactive Sidebar
    with st.sidebar:
        st.markdown("## 🇺🇳 UN SDG 13 Framework")
        st.image("https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?auto=format&fit=crop&w=300&q=80", caption="Protect Our Environment")
        st.info("""
        **Goal 13: Climate Action** mandates taking urgent action to combat climate change and its impacts by reducing global greenhouse gas outputs.
        """)
        st.markdown("---")
        st.markdown("### 📊 System Status")
        st.success("● Core Math Engine: Online")
        st.success("● Local AI Advisor: Ready")

    # High-Impact Educational Hero Banner
    st.markdown("""
    <div style="background-color: #e53e3e; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
        <h1 style="color: white; margin: 0; font-size: 28px; font-family: sans-serif;">🌱 EcoTrack AI — Climate Action Portal</h1>
        <p style="color: #fee2e2; margin: 5px 0 0 0; font-size: 16px; font-family: sans-serif;">
            Empowering individuals to measure, understand, and mitigate their carbon footprints in alignment with United Nations SDG 13.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Global Context Reference Metrics
    st.markdown("### 🌎 Global Climate Baseline Reference")
    col_ref1, col_ref2, col_ref3 = st.columns(3)
    col_ref1.metric("Target Global Average", "2.0 Metric Tons / Year", "Per Capita Goal", delta_color="inverse")
    col_ref2.metric("Current US Average", "16.0 Metric Tons / Year", "High Impact Vector", delta_color="inverse")
    col_ref3.metric("Current Global Average", "4.7 Metric Tons / Year", "Current Baseline", delta_color="inverse")
    
    st.markdown("---")

    ai_engine = CarbonAIEngine()

    # Layout Split
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("📋 Enter Daily Parameters")
        
        with st.expander("🚗 Transportation Profile", expanded=True):
            vehicle = st.selectbox(
                "Primary Mode of Transport:",
                ["Petrol Car", "Diesel Car", "Electric Vehicle", "Motorcycle", "Bus/Train", "Walking/Bicycle"]
            )
            distance = st.number_input("Daily Travel Distance (in kilometers):", min_value=0.0, value=15.0, step=1.0)
        
        with st.expander("⚡ Household Electricity", expanded=True):
            electricity = st.number_input("Monthly Electricity Consumption (in kWh):", min_value=0.0, value=250.0, step=10.0)
            daily_kwh = electricity / 30.0

        with st.expander("🍽️ Dietary Habits", expanded=True):
            diet = st.selectbox(
                "Select Diet Profile:",
                ["Heavy Meat Eater", "Average Meat Eater", "Pescatarian (Fish)", "Vegetarian", "Vegan"]
            )

        st.write("")
        calculate_btn = st.button("🚀 Process Footprint & Query AI Coach", type="primary", use_container_width=True)

    # Core Logic Controller using Session State Memory
    if calculate_btn:
        st.session_state.transport_co2 = calculate_transportation_emissions(distance, vehicle)
        st.session_state.energy_co2 = calculate_electricity_emissions(daily_kwh)
        st.session_state.diet_co2 = calculate_diet_emissions(diet, days=1)
        st.session_state.total_co2 = st.session_state.transport_co2 + st.session_state.energy_co2 + st.session_state.diet_co2
        st.session_state.annual_metric_tons = (st.session_state.total_co2 * 365 / 1000)
        st.session_state.calculated = True
        
        inputs_context = {"vehicle": vehicle, "distance": distance, "electricity": electricity, "diet": diet}
        with st.spinner("AI Engine generating optimization directives... Please hold."):
            st.session_state.ai_response = ai_engine.generate_sustainability_plan(
                st.session_state.transport_co2, st.session_state.energy_co2, st.session_state.diet_co2, st.session_state.total_co2, inputs_context
            )

    with col2:
        st.subheader("📊 Analytical Carbon Report")
        
        if st.session_state.calculated:
            # Metrics cards
            m1, m2 = st.columns(2)
            m1.metric(label="Your Daily Footprint", value=f"{st.session_state.total_co2:.2f} kg CO2e")
            
            target_diff = st.session_state.annual_metric_tons - 2.0
            if target_diff > 0:
                m2.metric(label="Annual Projection Equivalent", value=f"{st.session_state.annual_metric_tons:.2f} Tons", delta=f"+{target_diff:.2f} Tons Over Target Goal", delta_color="inverse")
            else:
                m2.metric(label="Annual Projection Equivalent", value=f"{st.session_state.annual_metric_tons:.2f} Tons", delta=f"{target_diff:.2f} Tons Under Target Goal", delta_color="normal")

            # Chart Engine
            labels = ['Transportation', 'Electricity (Daily Allocation)', 'Dietary Footprint']
            values = [st.session_state.transport_co2, st.session_state.energy_co2, st.session_state.diet_co2]
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=['#f56565','#4299e1','#48bb78']))])
            fig.update_layout(title_text="Carbon Emission Apportionment Breakdown", margin=dict(t=40, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig, use_container_width=True)

            # Export Results Center
            st.write("---")
            st.markdown("### 💾 Export Results Center")
            export_format = st.selectbox(
                "Choose file format based on your requirements:",
                ["Excel Spreadsheet (.csv)", "Formal Document (.txt)", "Printable Certificate (.html / .pdf via browser)"]
            )
            
            if export_format == "Excel Spreadsheet (.csv)":
                csv_data = (
                    "===========================================================\n"
                    "ECOTRACK AI SUSTAINABILITY AUDIT LOG,,,\n"
                    "UN SUSTAINABLE DEVELOPMENT GOAL 13 - CLIMATE ACTION,,,\n"
                    "===========================================================\n\n"
                    "EMISSION CATEGORY,USER INPUT DATA,DAILY EMISSIONS (KG CO2E),ANNUAL EQUIVALENT (METRIC TONS)\n"
                    f"Transportation Vector,{vehicle} ({distance} km),{st.session_state.transport_co2:.2f},{(st.session_state.transport_co2 * 365 / 1000):.2f}\n"
                    f"Household Energy Vector,{electricity} kWh/Month,{st.session_state.energy_co2:.2f},{(st.session_state.energy_co2 * 365 / 1000):.2f}\n"
                    f"Dietary Footprint Lifestyle,{diet},{st.session_state.diet_co2:.2f},{(st.session_state.diet_co2 * 365 / 1000):.2f}\n"
                    "-----------------------------------------------------------\n"
                    f"TOTAL METRICS RECKONING,Combined Streams,{st.session_state.total_co2:.2f},{st.session_state.annual_metric_tons:.2f}\n"
                    f"TARGET GOAL VARIANCE,UN Baseline Target (2.0 Tons),,{target_diff:+.2f} Tons Variance\n"
                )
                st.download_button(
                    label="📊 Download Clean Excel CSV Spreadsheet", data=csv_data, file_name="EcoTrack_Carbon_Audit.csv", mime="text/csv", use_container_width=True
                )
                
            elif export_format == "Formal Document (.txt)":
                txt_data = (
                    f"=========================================================\n"
                    f"        ECOTRACK AI - ENVIRONMENTAL SUSTAINABILITY REPORT \n"
                    f"        UN SUSTAINABLE DEVELOPMENT GOAL 13: CLIMATE ACTION \n"
                    f"=========================================================\n\n"
                    f"• Calculated Daily Carbon Footprint : {st.session_state.total_co2:.2f} kg CO2e\n"
                    f"• Projected Annual Accumulation     : {st.session_state.annual_metric_tons:.2f} Metric Tons / Year\n"
                    f"• Target Allocation Discrepancy    : {target_diff:+.2f} Metric Tons vs UN Goal Base\n\n"
                    f"USER PROPERTY RESOURCE MAP:\n"
                    f"---------------------------------------------------------\n"
                    f"1. Transit Vehicle Mode : {vehicle}\n"
                    f"2. Daily Commute Range  : {distance} Kilometers\n"
                    f"3. Monthly Power Draw   : {electricity} kWh\n"
                    f"4. Nutritional Profile  : {diet}\n\n"
                    f"Report compiled successfully via local math vector arrays.\n"
                    f"========================================================="
                )
                st.download_button(
                    label="📄 Download Structural TXT Document", data=txt_data, file_name="EcoTrack_Carbon_Report.txt", mime="text/plain", use_container_width=True
                )
                
            elif export_format == "Printable Certificate (.html / .pdf via browser)":
                html_data = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>EcoTrack AI Sustainability Report</title>
                    <style>
                        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; padding: 40px; color: #2d3748; background-color: #ffffff; }}
                        .cert-border {{ border: 4px double #2b6cb0; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                        .banner {{ background: linear-gradient(135deg, #e53e3e, #c53030); color: white; padding: 25px; border-radius: 6px; text-align: center; margin-bottom: 30px; }}
                        .banner h1 {{ margin: 0; font-size: 26px; text-transform: uppercase; letter-spacing: 1px; }}
                        .banner p {{ margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; }}
                        .main-metric {{ background-color: #f7fafc; border: 1px solid #e2e8f0; border-left: 6px solid #2b6cb0; padding: 20px; border-radius: 4px; margin-bottom: 25px; }}
                        .main-metric h2 {{ margin: 0; font-size: 16px; text-transform: uppercase; color: #4a5568; }}
                        .main-metric .val {{ font-size: 32px; font-weight: bold; color: #2b6cb0; margin-top: 5px; }}
                        table {{ width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 14px; }}
                        th {{ background-color: #2b6cb0; color: white; font-weight: 600; text-align: left; padding: 12px; }}
                        td {{ padding: 12px; border: 1px solid #e2e8f0; }}
                        tr:nth-child(even) {{ background-color: #fafdff; }}
                        .footer {{ text-align: center; margin-top: 40px; font-size: 11px; color: #a0aec0; border-top: 1px solid #e2e8f0; padding-top: 15px; }}
                    </style>
                </head>
                <body>
                    <div class="cert-border">
                        <div class="banner">
                            <h1>🌱 EcoTrack AI — Sustainability Audit Certificate</h1>
                            <p>Official Assessment Supporting UN Sustainable Development Goal 13: Climate Action</p>
                        </div>
                        
                        <div class="main-metric">
                            <h2>Calculated Operational Performance Profile</h2>
                            <div class="val">{st.session_state.total_co2:.2f} kg CO2e / Day</div>
                            <p style="margin: 5px 0 0 0; font-size: 14px; color: #718096;">Annual Projected Trendline Tracking at: <strong>{st.session_state.annual_metric_tons:.2f} Metric Tons / Year</strong></p>
                        </div>
                        
                        <h3>Granular Apportionment Summary Breakdown</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Emission Sector Category</th>
                                    <th>Your Profile Configuration Inputs</th>
                                    <th>Daily Impact Assessment</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Transportation System</strong></td>
                                    <td>{vehicle} ({distance} km/day)</td>
                                    <td>{st.session_state.transport_co2:.2f} kg CO2e</td>
                                </tr>
                                <tr>
                                    <td><strong>Household Electrical Power</strong></td>
                                    <td>{electricity} kWh / Month Allocation</td>
                                    <td>{st.session_state.energy_co2:.2f} kg CO2e</td>
                                </tr>
                                <tr>
                                    <td><strong>Nutritional Dietary Framework</strong></td>
                                    <td>{diet} Lifestyle</td>
                                    <td>{st.session_state.diet_co2:.2f} kg CO2e</td>
                                </tr>
                            </tbody>
                        </table>
                        
                        <div class="footer">
                            Report compiled via local computational validation arrays inside the EcoTrack Artificial Intelligence framework.<br>
                            <strong>Directions to print PDF:</strong> Open this downloaded file in any browser, press <strong>Ctrl + P</strong> (or Cmd + P), and select 'Save as PDF'.
                        </div>
                    </div>
                </body>
                </html>
                """
                st.download_button(
                    label="🌐 Download High-Design Printable Certificate File", data=html_data, file_name="EcoTrack_Sustainability_Certificate.html", mime="text/html", use_container_width=True
                )

            # AI Insights Module Display
            st.write("---")
            st.subheader("🤖 AI Sustainability Coach Insights")
            st.info(st.session_state.ai_response)
                
            # Interactive Climate Pledge Component
            st.markdown("---")
            st.subheader("🤝 Take Action for SDG 13")
            
            # Use a unique form structure to capture the pledge click independently
            with st.form("pledge_form", clear_on_submit=False):
                pledge_checked = st.checkbox("I pledge to actively lower my carbon footprint by making resource-conscious choices!")
                submit_pledge = st.form_submit_button("Lock In My Climate Pledge", use_container_width=True)
                
                if submit_pledge and pledge_checked:
                    st.balloons()  # Balloons only fire on explicit form click now!
                    st.success("Thank you for committing to active Climate Action! Your milestone has been logged.")
                elif submit_pledge and not pledge_checked:
                    st.warning("Please check the checkbox first to commit to your climate pledge action plan.")
        else:
            st.warning("⚠️ Input your parameters in the left pane and click 'Process Footprint' to compile data streams and trigger AI insight analysis.")

if __name__ == "__main__":
    run_app()