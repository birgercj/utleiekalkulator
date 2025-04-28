import streamlit as st

st.set_page_config(page_title="Utleiekalkulator", page_icon="🏡")

# App tittel
st.title("🏡 Utleie Lønnsomhetskalkulator")

st.header("Legg inn informasjon om eiendommen")

# Input felt
case_name = st.text_input("Navn på case", placeholder="F.eks. 'Leilighet St. Hanshaugen'")

purchase_price = st.number_input("Kjøpesum (kr) inkl dok", min_value=0, step=100000, value=4000000)

equity_percentage = st.number_input("Egenkapital (%)", min_value=0.0, max_value=100.0, value=20.0, step=5.0)
equity = purchase_price * (equity_percentage / 100)

interest_rate = st.number_input("Rente på lån (%)", min_value=0.0, value=5.0, step=0.1, help="Rente for AS er ofte 1 til 1,5% høyere enn for privatpersoner.")
loan_years = st.number_input("Lånetid (år)", min_value=1, value=25, help="Lånetid for AS er ofte maks 20 år.", step=1)

monthly_rent = st.number_input("Månedlige leieinntekter (kr)", min_value=0)

st.subheader("Kostnader per måned")
maintenance = st.number_input("Vedlikehold (kr)", min_value=0, value=0, step=100)
electricity = st.number_input("Strøm (kr)", min_value=0, value=0, step=100)
municipal_fees = st.number_input("Kommunale avgifter (kr)", min_value=0, value=0, step=100)
property_tax = st.number_input("Eiendomsskatt (kr)", min_value=0, value=0, step=100)
internet = st.number_input("Internett (kr)", min_value=0, value=0, step=100)
insurance = st.number_input("Forsikring (kr)", min_value=0, value=0, step=100)

st.subheader("Risiko")
months = st.number_input("Antall måneder med leieinntekter", min_value=0, value=10, step=1, max_value=12,
                         help="Noen banker godtar kun 10 måneder med leieinntekter som inntekt. Dette er for å være konservativ.")

# Når brukeren klikker "Beregn"
if st.button("Beregn lønnsomhet"):

    # Beregninger
    loan_amount = purchase_price - equity
    monthly_interest_rate = interest_rate / 100 / 12
    number_of_payments = loan_years * 12

    # Annuitetslån månedlig betaling
    if loan_amount > 0 and monthly_interest_rate > 0:
        loan_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    else:
        loan_payment = 0

    total_monthly_expenses = maintenance + electricity + municipal_fees + property_tax + internet + insurance

    # Netto leieinntekt
    monthly_net_rent = monthly_rent - total_monthly_expenses

    # Månedlig kontantstrøm
    monthly_cash_flow = monthly_net_rent - loan_payment

    # Årlig beregninger
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

    # Resultatvisning
    st.header(f"Resultater for {case_name}")

    st.subheader("Finansiering")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Kjøpesum", f"{purchase_price:,.0f} kr")
    with col2:
        st.metric("Egenkapital", f"{equity:,.0f} kr")
    with col3:
        st.metric("Lånebeløp", f"{loan_amount:,.0f} kr")

    st.subheader("Inntekter")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Månedlige leieinntekter", f"{monthly_rent:,.0f} kr")
    with col2:
        st.metric(f"Årlige leieinntekter ({months} mnd)", f"{annual_rent:,.0f} kr")

    st.subheader("Utgifter")
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
        
