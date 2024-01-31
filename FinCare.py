import streamlit as st

def calculate_loan_payments(loan_amount, interest_rate, months):
    monthly_interest_rate = interest_rate / 100 / 12
    if months > 0:
        loan_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -months)
    
        total_payment = loan_payment * months
        interest_paid = total_payment - loan_amount

        return loan_payment, total_payment, interest_paid
    return 0, 0, 0

# Streamlit UI
st.set_page_config(page_title="FinCare", page_icon="FinCare-removebg.png", layout="wide")
col1, col2 = st.columns([0.5,2])
with col2:
    st.image("FinCare_banner_cropped.png", width = 700)
st.divider()


col1, col2 = st.columns(2, gap="large")
# Input fields with sliders
with col1:
    account = st.number_input("Account savings: ")
    income = st.number_input("Monthly Income:", value=1500)
    rent = st.number_input("Monthly Rent/ Housing Cost:", value=1000)
with col2:
    utilities = st.slider("Monthly Utilities:", min_value=0, max_value=1000, value=200)
    taxes = st.slider("Taxes due:", min_value=0, max_value=5000, value=100)
    other = st.slider("Other Monthly Expenses:", min_value=0, max_value=5000, value=100)
upcoming = st.number_input("Upcoming single time payments: ")
st.divider()

# Loan input fields
st.header("Loan/Mortgage Details")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Loan 1")
    loan_amount1 = st.number_input("Loan/Mortgage Amount:")
    interest_rate1 = st.number_input("Interest Rate (%):")
    loan_duration1 = st.number_input("Loan Duration (Months):")

with col2:
    st.subheader("Loan 2")
    loan_amount2 = st.number_input("Other Loan/Mortgage Amount:")
    interest_rate2 = st.number_input("Other Interest Rate (%):")
    loan_duration2 = st.number_input("Other Loan Duration (Months):")
    
st.divider()

# Calculate future loan payments
loan_payment1, total_payment1, interest_paid1 = calculate_loan_payments(loan_amount1, interest_rate1, loan_duration1)
loan_payment2, total_payment2, interest_paid2 = calculate_loan_payments(loan_amount2, interest_rate2, loan_duration2)

# Calculate financial status
total_expenses = rent + utilities + taxes + loan_payment1 + loan_payment2 + other
savings = income - total_expenses



col1, col2, col3 = st.columns(3, gap="large")
# Display results
risk = False
with col1:
    st.subheader("Financial Status:")
    # Predict when they will run out of money
    if savings < 0:
        risk = True
        months_until_empty = int((account - upcoming )/ abs(savings))
        st.warning(f"Monthly losses: ${savings:.2f}")
        st.warning(f"You are losing money. You will run out of savings in approximately {months_until_empty} months.")
    else:
        st.success(f"Monthly savings: ${savings:.2f}")
        st.success("You are saving money. Good job!")

with col2:
    with st.container():
        st.subheader("Loan Repayment Details:")
        st.write(f"Total Monthly Loan Payment: ${(loan_payment1 + loan_payment2):.2f}")
        st.write(f"Total Payment over {max(loan_duration1,loan_duration2)} months: ${(total_payment1 + total_payment2):.2f}")
        st.write(f"Total Interest Paid: ${(interest_paid1 + interest_paid2):.2f}")

with col3:
    st.subheader("Cost Burden:")
    if income>0:
        if (rent + utilities + loan_payment1 + loan_payment2) / income > 0.5:
            st.error("You are severely cost-burdened.")
        elif (rent + utilities + loan_payment1 + loan_payment2) / income > 0.3:
            st.warning("You are cost-burdened.")
        else:
            st.success("You are not cost-burdened.")
st.divider()

if risk:
    st.subheader("Get Housing Help:")
    col1, col2 = st.columns(2)
    with col1:
        st.write("##### [HUD Exchange](https://www.hudexchange.info/housing-and-homeless-assistance/)")
        st.image("hudLogo.png")
    with col2:
        st.write("##### [Strategies to End Homelessness](https://www.strategiestoendhomelessness.org/get-help/)")
        st.image("STEH_Logo.png")
    st.divider()
# Additional information
st.markdown(
    """
    ### Tips:
    - **Cost-Burdened**: You spend over 30% of your income on housing needs.
    - **Severely Cost-Burdened**: You spend over 50% of your income on housing needs.
    - **Monthly Savings**: The amount of money left after deducting rent and other costs from your income.
    - **Loan Details**: Input the loan amount, interest rate, and duration to calculate future loan payments.
    - **Negative Savings**: Indicates you are losing money, and the app predicts when you might run out of savings.
    """
)
