import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from xhtml2pdf import pisa
from io import BytesIO
import re
import random
from utils.helpers import (
    calculate_transportation_emissions,
    calculate_electricity_emissions,
    calculate_diet_emissions
)
from app.main import CarbonAIEngine

def clean_for_pdf(text):
    """Helper tool to completely sanitize string structures for PDF processing."""
    return re.sub(r'[^\x00-\x7F]+', '', str(text))

def generate_professional_pdf(total, transport, energy, diet, score, badge, vehicle, distance, electricity, diet_name, action_items):
    """
    Generates a high-end, presentation-grade PDF document via a pure-Python HTML template engine.
    """
    badge_colors = {
        "Eco Warrior": "#2f855a",
        "Moderate Impact": "#dd6b20",
        "High Carbon Footprint": "#c53030"
    }
    accent_color = badge_colors.get(badge, "#2b6cb0")

    html_content = f"""
    <html>
    <head>
        <style>
            @page {{ size: a4; margin: 20mm 15mm; }}
            body {{ font-family: Helvetica, Arial, sans-serif; color: #2d3748; font-size: 11pt; line-height: 1.5; }}
            .header-container {{ background-color: #1a365d; color: #ffffff; padding: 20px; text-align: center; margin-bottom: 25px; }}
            .header-container h1 {{ margin: 0; font-size: 22pt; font-weight: bold; }}
            .header-container p {{ margin: 5px 0 0 0; font-size: 10pt; color: #e2e8f0; }}
            .badge-box {{ background-color: #f7fafc; padding: 15px; margin-bottom: 25px; border-left: 5px solid {accent_color}; }}
            .badge-title {{ font-size: 9pt; font-weight: bold; color: #718096; }}
            .badge-value {{ font-size: 16pt; font-weight: bold; color: {accent_color}; margin: 4px 0; }}
            table {{ width: 100%; margin-bottom: 30px; }}
            th {{ background-color: #2b6cb0; color: #ffffff; font-weight: bold; text-align: left; padding: 8px; }}
            td {{ padding: 8px; border-bottom: 1px solid #cbd5e0; }}
            .section-title {{ font-size: 13pt; font-weight: bold; color: #1a365d; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; }}
            .checklist-container {{ padding: 10px; background-color: #ffffff; }}
            .checklist-item {{ margin-bottom: 8px; font-size: 11pt; }}
        </style>
    </head>
    <body>
        <div class="header-container">
            <h1>EcoTrack AI -- Environmental Audit Record</h1>
            <p>United Nations SDG 13: Climate Action Compliance Report</p>
        </div>
        <div class="badge-box">
            <div class="badge-title">EVALUATED CARBON OUTPUT EFFICIENCY RANK</div>
            <div class="badge-value">{badge} (Score: {score}/100)</div>
            <p style="margin: 5px 0 0 0; font-size: 10pt;">
                Combined Daily Footprint: <strong>{total:.2f} kg CO2e</strong> | Projected Annual Accumulation: <strong>{(total * 365 / 1000):.2f} Tons/Year</strong>
            </p>
        </div>
        <div class="section-title">Emission Apportionment Audit</div>
        <table>
            <thead>
                <tr><th>Emission Sector</th><th>User Input Parameters</th><th>Daily Output Value</th></tr>
            </thead>
            <tbody>
                <tr><td><strong>Transportation Commutes</strong></td><td>{vehicle} ({distance} km/day)</td><td>{transport:.2f} kg CO2e</td></tr>
                <tr><td><strong>Household Power Grid Utilities</strong></td><td>{electricity} kWh / Month allocation</td><td>{energy:.2f} kg CO2e</td></tr>
                <tr><td><strong>Dietary & Nutritional Habits</strong></td><td>{diet_name} profile</td><td>{diet:.2f} kg CO2e</td></tr>
            </tbody>
        </table>
        <div class="section-title">Your Personalized Action Plan (Easy Goals For This Week)</div>
        <div class="checklist-container">
            <div class="checklist-item">[ ] <strong>Goal 1:</strong> {action_items[0]}</div>
            <div class="checklist-item">[ ] <strong>Goal 2:</strong> {action_items[1]}</div>
            <div class="checklist-item">[ ] <strong>Goal 3:</strong> {action_items[2]}</div>
        </div>
    </body>
    </html>
    """
    
    pdf_buffer = BytesIO()
    pisa.CreatePDF(BytesIO(html_content.encode("utf-8")), dest=pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

def run_app():
    # Centered clean responsive layout
    st.set_page_config(
        page_title="EcoTrack AI: Advanced SDG 13 Portal", 
        page_icon="🌱",
        layout="centered", 
        initial_sidebar_state="expanded"
    )
    
    if "calculated" not in st.session_state:
        st.session_state.calculated = False
    if "ai_response" not in st.session_state:
        st.session_state.ai_response = ""
        
    # Standard environmental coaching guidelines for sidebar injection
    climate_tips = [
        "Unplug chargers when devices are fully charged to avoid phantom power drainage.",
        "Transitioning to a plant-forward lunch just twice a week slashes your dietary emissions by 30%.",
        "Keeping tires properly inflated optimizes fuel efficiency and cuts transport carbon output.",
        "A standard cold-water laundry wash cycle saves up to 75% of the machine's total energy draw.",
        "LED bulb installations conserve roughly 80% more energy than traditional filament lighting."
    ]
    if "current_tip" not in st.session_state:
        st.session_state.current_tip = random.choice(climate_tips)

    ai_engine = CarbonAIEngine()

    # --- 🇺🇳 SIDEBAR COMPONENT (RESTORED & EXPANDED) ---
    with st.sidebar:
        st.markdown("## 🇺🇳 UN SDG 13 Framework")
        st.info("Goal 13: Climate Action mandates taking urgent action to combat change by reducing greenhouse gas outputs.")
        
        st.markdown("---")
        st.markdown("### 🎯 Core Target Benchmarks")
        st.caption("Key focus areas of the SDG 13 infrastructure tracking framework:")
        st.markdown("""
        * **Target 13.1:** Strengthen resilience and adaptive capacity to climate-related hazards.
        * **Target 13.2:** Integrate climate change measures into policies and strategic planning.
        * **Target 13.3:** Improve human institutional capacity on climate mitigation and impact reduction.
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Everyday Climate Tip")
        st.warning(st.session_state.current_tip)
        if st.button("🔄 Roll New Tip", use_container_width=True):
            st.session_state.current_tip = random.choice(climate_tips)
            st.rerun()
            
        st.markdown("---")
        st.markdown("### 🔒 System Compliance")
        st.caption("Evaluation logic uses normalized emission factors aligned with global greenhouse gas accounting protocols.")

    # --- MAIN UI BANNER ---
    st.markdown("""
    <div style="background-color: #1a365d; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 24px; font-family: sans-serif;">🌱 EcoTrack AI Portal</h1>
        <p style="color: #e2e8f0; margin: 5px 0 0 0; font-size: 13px; font-family: sans-serif;">
            Production platform measuring carbon outputs in alignment with UN SDG 13.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌎 Global Climate Baseline Reference")
    st.metric("Target Global Average", "2.0 Metric Tons / Year", "Per Capita Goal", delta_color="inverse")
    st.metric("Current Global Average", "4.7 Metric Tons / Year", "Current Baseline", delta_color="inverse")
    
    st.markdown("---")

    # --- INPUT PANELS ---
    st.subheader("📋 Input Parameter Controls")
    with st.expander("🚗 Transportation Profile", expanded=True):
        vehicle = st.selectbox("Primary Mode of Transport:", ["Petrol Car", "Diesel Car", "Electric Vehicle", "Motorcycle", "Bus/Train", "Walking/Bicycle"])
        distance = st.number_input("Daily Travel Distance (in km):", min_value=0.0, value=15.0, step=1.0)
    
    with st.expander("⚡ Household Electricity", expanded=True):
        electricity = st.number_input("Monthly Electricity Consumption (kWh):", min_value=0.0, value=250.0, step=10.0)
        daily_kwh = electricity / 30.0

    with st.expander("🍽️ Dietary Habits", expanded=True):
        diet = st.selectbox("Select Diet Profile:", ["Heavy Meat Eater", "Average Meat Eater", "Pescatarian (Fish)", "Vegetarian", "Vegan"])

    st.write("")
    calculate_btn = st.button("🚀 Process Footprint & Query AI Coach", type="primary", use_container_width=True)

    if calculate_btn:
        st.session_state.transport_co2 = calculate_transportation_emissions(distance, vehicle)
        st.session_state.energy_co2 = calculate_electricity_emissions(daily_kwh)
        st.session_state.diet_co2 = calculate_diet_emissions(diet, days=1)
        st.session_state.total_co2 = st.session_state.transport_co2 + st.session_state.energy_co2 + st.session_state.diet_co2
        st.session_state.annual_metric_tons = (st.session_state.total_co2 * 365 / 1000)
        
        base_score = 100 - int(st.session_state.annual_metric_tons * 8)
        st.session_state.green_score = max(5, min(100, base_score))
        
        if st.session_state.green_score >= 80:
            st.session_state.badge = "Eco Warrior"
            st.session_state.badge_color = "green"
        elif st.session_state.green_score >= 50:
            st.session_state.badge = "Moderate Impact"
            st.session_state.badge_color = "orange"
        else:
            st.session_state.badge = "High Carbon Footprint"
            st.session_state.badge_color = "red"

        st.session_state.calculated = True
        
        inputs_context = {
            "vehicle": vehicle, "distance": distance, "electricity": electricity, "diet": diet,
            "green_score": st.session_state.green_score, "badge": st.session_state.badge
        }
        
        with st.spinner("Gemini Core Engine computing clean recommendations..."):
            st.session_state.ai_response = ai_engine.generate_sustainability_plan(
                st.session_state.transport_co2, st.session_state.energy_co2, st.session_state.diet_co2, st.session_state.total_co2, inputs_context
            )
            st.session_state.cached_bullets = ai_engine.extract_action_items(st.session_state.ai_response)

    # --- REPORT PANELS ---
    if st.session_state.calculated:
        st.markdown("---")
        st.subheader("📊 Analytical Carbon Report")
        
        st.metric(label="Your Daily Footprint", value=f"{st.session_state.total_co2:.2f} kg CO2e")
        st.metric(label="Annual Projection Equivalent", value=f"{st.session_state.annual_metric_tons:.2f} Tons", delta=f"{st.session_state.annual_metric_tons - 2.0:+.2f} Tons vs Target Baseline", delta_color="inverse")

        st.markdown(f"""
        <div style="background-color: #f7fafc; padding: 12px; border-radius: 6px; border-left: 5px solid {st.session_state.badge_color}; margin: 15px 0;">
            <span style="font-size: 13px; color: #4a5568; font-weight: bold; text-transform: uppercase;">Current Sustainability Rank:</span><br>
            <span style="font-size: 20px; font-weight: bold; color: {st.session_state.badge_color};">{st.session_state.badge}</span>
            <p style="margin: 3px 0 0 0; font-size: 12px; color: #718096;">Your efficiency rating is <strong>{st.session_state.green_score}/100</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

        labels = ['Transportation', 'Electricity', 'Diet']
        values = [st.session_state.transport_co2, st.session_state.energy_co2, st.session_state.diet_co2]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=['#f56565','#4299e1','#48bb78']))])
        fig.update_layout(title_text="Carbon Emission Breakdown", margin=dict(t=40, b=0, l=0, r=0), height=240)
        st.plotly_chart(fig, use_container_width=True)

        # --- EXPORT CENTER ---
        st.markdown("### 💾 Requirement Export Center")
        export_format = st.selectbox("Choose file format:", ["Excel Spreadsheet (.csv)", "Official Executive Document (.pdf)"])
        actions_list = st.session_state.get("cached_bullets", ["Tweak food habits.", "Unplug unused devices.", "Combine vehicle commutes."])
        
        if export_format == "Excel Spreadsheet (.csv)":
            csv_data = (
                f"CATEGORY,USER_INPUT,DAILY_KG_CO2e\n"
                f"Transit,{vehicle} ({distance} km),{st.session_state.transport_co2:.2f}\n"
                f"Energy,{electricity} kWh/Month,{st.session_state.energy_co2:.2f}\n"
                f"Diet,{diet},{st.session_state.diet_co2:.2f}\n"
                f"TOTAL_METRICS,,{st.session_state.total_co2:.2f}\n"
                f"GREEN_SCORE,,{st.session_state.green_score}\n"
                f"RANK,,{clean_for_pdf(st.session_state.badge)}\n"
                f"AI_RECOMMENDATION_1,,{clean_for_pdf(actions_list[0])}\n"
                f"AI_RECOMMENDATION_2,,{clean_for_pdf(actions_list[1])}\n"
                f"AI_RECOMMENDATION_3,,{clean_for_pdf(actions_list[2])}"
            )
            st.download_button(label="📊 Download Excel CSV Spreadsheet", data=csv_data, file_name="EcoTrack_Carbon_Audit.csv", mime="text/csv", use_container_width=True)
            
        elif export_format == "Official Executive Document (.pdf)":
            pdf_data = generate_professional_pdf(
                st.session_state.total_co2, st.session_state.transport_co2, st.session_state.energy_co2, st.session_state.diet_co2,
                st.session_state.green_score, st.session_state.badge, vehicle, distance, electricity, diet, actions_list
            )
            st.download_button(label="📄 Download Professional Audit PDF", data=pdf_data, file_name="EcoTrack_Sustainability_Audit.pdf", mime="application/pdf", use_container_width=True)

        st.write("---")
        st.subheader("🤖 AI Sustainability Coach Insights")
        st.info(st.session_state.ai_response)
            
        st.write("---")
        st.subheader("🤝 Take Action for SDG 13")
        with st.form("pledge_form", clear_on_submit=False):
            pledge_checked = st.checkbox("I pledge to actively lower my carbon footprint!")
            submit_pledge = st.form_submit_button("Lock In My Climate Pledge", use_container_width=True)
            if submit_pledge and pledge_checked:
                st.balloons()
                st.success("Thank you for committing to active Climate Action!")
    else:
        st.write("")
        st.warning("⚠️ Input your parameters above and click 'Process Footprint' to compile data.")

    # --- 🛠️ 🌐 CHATBASE SCRIPT & STYLING OVERRIDES ---
    chatbase_script_raw = """
    <script>
    (function(){
        if(!window.chatbase || window.chatbase("getState")!=="initialized"){
            window.chatbase=(...arguments)=>{
                if(!window.chatbase.q){window.chatbase.q=[]}
                window.chatbase.q.push(arguments)
            };
            window.chatbase=new Proxy(window.chatbase,{
                get(target,prop){
                    if(prop==="q"){return target.q}
                    return(...args)=>target(prop,...args)
                }
            })
        }
        const onLoad = function(){
            const script = window.parent.document.createElement("script");
            script.src = "https://www.chatbase.co/embed.min.js";
            script.id = "t4t9dZSKPg1w3N46f4akA";
            script.domain = "www.chatbase.co";
            script.defer = true;
            window.parent.document.body.appendChild(script);
        };
        if(window.parent.document.readyState==="complete"){
            onLoad();
        }else{
            window.parent.addEventListener("load",onLoad);
        }
    })();
    </script>
    """
    components.html(chatbase_script_raw, height=0, width=0)
    
    st.markdown(
        """
        <style>
        /* Hide the default Streamlit repository indicators, fork options, and header bands */
        #MainMenu, header, .stAppDeployButton, [data-testid="stHeader"] {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* Clear out the hosting footer blocks completely */
        footer {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* Protect component iframe bounding areas from masking page elements */
        iframe[title="streamlit.components.v1.html"] {
            position: fixed !important;
            bottom: 0px !important;
            right: 0px !important;
            width: 0px !important;
            height: 0px !important;
            border: none !important;
            z-index: -1 !important;
            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    run_app()