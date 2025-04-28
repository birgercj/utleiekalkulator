import streamlit as st
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Utleiekalkulator", page_icon="🏡")

# App-tittel
st.title("🏡 Utleie Lønnsomhetskalkulator med 10-års simulering")

st.header("Legg inn informasjon om eiendommen")

# Input-felter
case_name = st.text_input("Navn på case", placeholder="F.eks. 'Leilighet St. Hanshaugen'")

purchase_price = st.number_input("Kjøpesum (kr) inkl dok", min_value=0, step=100000, value=4000000)
equity_percentage = st.number_input("Egenkapital (%)", min_value=0.0, max_value=100.0, value=20.0, step=5.0)
equity = purchase_price * (equity_percentage / 100)

interest_rate = st.number_input("Rente på lån (%)", min_value=0.0, value=5.0, step=0.1)
loan_years = st.number_input("Lånetid (år)", min_value=1, value=25, step=1)
monthly_rent = st.number_input("Månedlige leieinntekter (kr)", min_value=0)

st.subheader("Kostnader per måned")
maintenance = st.number_input("Vedlikehold (kr)", min_value=0, value=0, step=100)
electricity = st.number_input("Strøm (kr)", min_value=0, value=0, step=100)
municipal_fees = st.number_input("Kommunale avgifter (kr)", min_value=0, value=0, step=100)
property_tax = st.number_input("Eiendomsskatt (kr)", min_value=0, value=0, step=100)
internet = st.number_input("Internett (kr)", min_value=0, value=0, step=100)
insurance = st.number_input("Forsikring (kr)", min_value=0, value=0, step=100)

st.subheader("Risiko og simulering")
months = st.number_input("Antall måneder med leieinntekter", min_value=0, value=10, step=1, max_value=12)

# Simulering parametre
st.subheader("Parametre for 10 års simulering")
rent_growth_rate = st.number_input("Leieinntektsvekst per år (%)", value=2.0, step=0.5) / 100
interest_change_per_year = st.number_input("Renteendring per år (%)", value=0.0, step=0.1) / 100
cost_inflation_rate = st.number_input("Kostnadsvekst per år (%)", value=2.0, step=0.5) / 100
property_value_growth = st.number_input("Boligverdi vekst per år (%)", value=3.0, step=0.5) / 100

# Beregn-knapp
if st.button("Beregn lønnsomhet og vis simulering"):

    loan_amount = purchase_price - equity
    monthly_interest_rate = interest_rate / 100 / 12
    number_of_payments = loan_years * 12

    if loan_amount > 0 and monthly_interest_rate > 0:
        loan_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    else:
        loan_payment = 0

    total_monthly_expenses = maintenance + electricity + municipal_fees + property_tax + internet + insurance

    # Beregninger for nåværende år
    monthly_net_rent = monthly_rent - total_monthly_expenses
    monthly_cash_flow = monthly_net_rent - loan_payment

    annual_rent = monthly_rent * months
    annual_expenses = total_monthly_expenses * 12
    annual_loan_payment = loan_payment * 12
    annual_net_rent = monthly_net_rent * months
    annual_cash_flow = annual_rent - (annual_expenses + annual_loan_payment)

    # Yield og Cash on Cash
    brutto_yield = (annual_rent / purchase_price) * 100 if purchase_price > 0 else 0
    netto_yield = (annual_net_rent / purchase_price) * 100 if purchase_price > 0 else 0
    cash_on_cash = (annual_cash_flow / equity) * 100 if equity > 0 else 0

    if case_name == "":
        case_name = "ditt case"

    # Resultatvisning - Nåværende år
    st.header(f"📋 Resultater for {case_name} (nåværende økonomi)")

    st.subheader("Finansiering")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Kjøpesum", f"{purchase_price:,.0f} kr")
    with col2:
        st.metric("Egenkapital", f"{equity:,.0f} kr")
    with col3:
        st.metric("Lånebeløp", f"{loan_amount:,.0f} kr")

    st.subheader("Inntekter og utgifter")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Månedlige leieinntekter", f"{monthly_rent:,.0f} kr")
    with col2:
        st.metric(f"Årlige leieinntekter ({months} mnd)", f"{annual_rent:,.0f} kr")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Månedlige utgifter", f"{total_monthly_expenses:,.0f} kr")
    with col2:
        st.metric("Årlige utgifter", f"{annual_expenses:,.0f} kr")

    st.subheader("Resultater")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Månedlig netto leieinntekt", f"{monthly_net_rent:,.0f} kr")
    with col2:
        st.metric("Årlig netto leieinntekt", f"{annual_net_rent:,.0f} kr")
    st.subheader("Finansieringskostnader")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Lånebeløp pr måned m/avdrag", f"{loan_payment:,.0f} kr")
    with col2:
        st.metric("Årlig lånekostnad", f"{annual_loan_payment:,.0f} kr")
    st.subheader("Kontantstrøm")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Månedlig kontantstrøm", f"{monthly_cash_flow:,.0f} kr")
    with col2:
        st.metric("Årlig kontantstrøm", f"{annual_cash_flow:,.0f} kr")

    st.subheader("Nøkkeltall")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Brutto Yield", f"{brutto_yield:.2f} %")
    with col2:
        st.metric("Netto Yield", f"{netto_yield:.2f} %")
    with col3:
        st.metric("Cash-on-Cash Return", f"{cash_on_cash:.2f} %")

    # --- Simulering 10 år ---
    st.header(f"📈 10-års simulering for {case_name}")

    years = []
    rents = []
    expenses = []
    cash_flows = []
    property_values = []

    # Startverdier
    current_rent = monthly_rent
    current_expenses = total_monthly_expenses
    current_interest_rate = interest_rate
    current_loan_payment = loan_payment
    current_property_value = purchase_price

    for year in range(11):  # År 0 til 10
        annual_rent = current_rent * months
        annual_expenses = current_expenses * 12
        annual_loan_payment = current_loan_payment * 12
        annual_cash_flow = annual_rent - (annual_expenses + annual_loan_payment)

        years.append(year + datetime.datetime.now().year)      
        rents.append(annual_rent)
        expenses.append(annual_expenses + annual_loan_payment)
        cash_flows.append(annual_cash_flow)
        property_values.append(current_property_value)

        # Oppdater for neste år
        current_rent *= (1 + rent_growth_rate)
        current_expenses *= (1 + cost_inflation_rate)
        current_property_value *= (1 + property_value_growth)
        current_interest_rate += interest_change_per_year

        if loan_amount > 0:
            monthly_interest_rate_new = current_interest_rate / 100 / 12
            current_loan_payment = loan_amount * (monthly_interest_rate_new * (1 + monthly_interest_rate_new) ** number_of_payments) / ((1 + monthly_interest_rate_new) ** number_of_payments - 1)

    # --- Plotly graf ---
    st.subheader("Utvikling av inntekter, kostnader, kontantstrøm og boligverdi")

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=years, y=rents, mode='lines+markers', name='Årlig leieinntekt'))
    fig.add_trace(go.Scatter(x=years, y=expenses, mode='lines+markers', name='Årlige kostnader (inkl. lån)'))
    fig.add_trace(go.Scatter(x=years, y=cash_flows, mode='lines+markers', name='Årlig kontantstrøm'))
    fig.add_trace(go.Scatter(x=years, y=property_values, mode='lines+markers', name='Boligverdi', yaxis="y2"))

    fig.update_layout(
        title="Utvikling av inntekter, kostnader, kontantstrøm og boligverdi",
        xaxis_title="År",
        yaxis_title="Beløp (kr)",
        yaxis2=dict(
            title="Boligverdi (kr)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
