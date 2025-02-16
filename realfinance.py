import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import yfinance as yf
from streamlit_option_menu import option_menu
import sqlite3
import hashlib

# ============= DATABASE SETUP =============
def init_db():
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()
    
    # Users table (simplified)
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE,
                  email TEXT UNIQUE,
                  password TEXT)''')
    
    # Expenses table
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  date TEXT,
                  amount REAL,
                  category TEXT,
                  description TEXT)''')
    
    # Investment goals table
    c.execute('''CREATE TABLE IF NOT EXISTS goals
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  name TEXT,
                  target_amount REAL,
                  current_amount REAL,
                  target_date TEXT,
                  priority TEXT)''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# ============= CONFIGURATION =============
st.set_page_config(
    page_title="AI Financial Planner",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= COLOR SCHEME =============
COLORS = {
    'primary': '#00704A',     # Starbucks Green
    'secondary': '#27251F',   # Dark Gray
    'accent': '#C6A969',      # Gold
    'background': '#F7F7F7',  # Light Background
    'text_dark': '#1E3932',   # Dark Green Text
    'text_light': '#FFFFFF',  # White Text
    'success': '#006241',     # Dark Green
    'warning': '#CBA258',     # Light Gold
    'error': '#DC3545',       # Red
}

# ============= CUSTOM CSS =============
st.markdown(f"""
    <style>
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
    }}
    
    .footer {{
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #00704A;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }}
    
    .stApp {{
        background-color: {COLORS['background']};
    }}
    
    h1, h2, h3 {{
        color: {COLORS['primary']};
    }}
""", unsafe_allow_html=True)


# ============= SESSION STATE =============
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# ============= AUTHENTICATION =============
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute("SELECT id FROM users WHERE email=? AND password=?", 
              (email, hashed_password))
    result = c.fetchone()
    conn.close()
    if result:
        st.session_state.user_id = result[0]
        st.session_state.authenticated = True
        return True
    return False

def register_user(username, email, password):
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()
    try:
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                 (username, email, hashed_password))
        conn.commit()
        return True, "Registration successful! Please login."
    except sqlite3.IntegrityError:
        return False, "Email or username already exists!"
    finally:
        conn.close()

def auth_page():
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #00704A; margin-bottom: 2rem;'>AI Financial Planner</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if login_user(email, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long!")
                else:
                    success, message = register_user(new_username, new_email, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

# ============= ION =============
def create_navigation():
    return option_menu(
        menu_title=None,
        options=["Dashboard", "Expenses", "Investments", "Analysis", "Settings"],
        icons=["house", "wallet", "graph-up", "clipboard-data", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
    "container": {"padding": "10px!important", "background-color": COLORS['primary']},
    "icon": {"color": COLORS['text_light'], "font-size": "20px"},
    "nav-link": {
        "font-size": "16px",
        "text-align": "center",
        "margin": "5px",
        "padding": "10px 20px",
        "--hover-color": COLORS['accent'],
        "color": COLORS['text_light']
    },
    "nav-link-selected": {"background-color": COLORS['accent']},
}

    )
# ============= DASHBOARD =============
def dashboard():
    st.markdown("<h1 style='text-align: center;'>Financial Dashboard</h1>", unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Monthly Savings",
            value="₹25,000",
            delta="↑ 8%"
        )
    
    with col2:
        st.metric(
            label="Investments",
            value="₹1,50,000",
            delta="↑ 12%"
        )
    
    with col3:
        st.metric(
            label="Expenses",
            value="₹45,000",
            delta="-5%"
        )
    
    with col4:
        st.metric(
            label="Net Worth",
            value="₹5,00,000",
            delta="↑ 15%"
        )
    
    # Market Overview
    st.markdown("### Market Overview")
    try:
        # Fetch popular Indian stocks
        symbols = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'WIPRO.NS']
        market_data = pd.DataFrame()
        
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='1d')
            if not hist.empty:
                market_data.loc[symbol, 'Price'] = hist['Close'].iloc[-1]
                market_data.loc[symbol, 'Change'] = hist['Close'].iloc[-1] - hist['Open'].iloc[-1]
                market_data.loc[symbol, 'Change %'] = ((hist['Close'].iloc[-1] - hist['Open'].iloc[-1]) / hist['Open'].iloc[-1]) * 100
        
        st.dataframe(market_data.style.format({
            'Price': '₹{:,.2f}',
            'Change': '₹{:,.2f}',
            'Change %': '{:,.2f}%'
        }))
        
        # Market Trends Chart
        st.markdown("### Market Trends (Last Month)")
        fig = go.Figure()
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='1mo')
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'],
                                   name=symbol, mode='lines'))
        
        fig.update_layout(
            title='Stock Performance',
            xaxis_title='Date',
            yaxis_title='Price (₹)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error("Unable to fetch market data. Please check your internet connection.")

# ============= EXPENSE TRACKER =============
def expense_tracker():
    st.markdown("<h1 style='text-align: center;'>Smart Expense Tracker</h1>", unsafe_allow_html=True)
    
    # Add New Expense
    with st.expander("Add New Expense", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            expense_date = st.date_input("Date", datetime.now())
            expense_amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
        
        with col2:
            default_categories = ["Needs", "Wants", "Investment", "Bills", "Entertainment", "Health", "Other"]
            expense_category = st.selectbox("Category", default_categories)
            if expense_category == "Other":
                expense_category = st.text_input("Specify Category")
        
        with col3:
            expense_description = st.text_area("Description", height=100)
        
        if st.button("Add Expense"):
            conn = sqlite3.connect('finance_tracker.db')
            c = conn.cursor()
            c.execute("""
                INSERT INTO expenses (user_id, date, amount, category, description)
                VALUES (?, ?, ?, ?, ?)
            """, (st.session_state.user_id, expense_date.strftime("%Y-%m-%d"), 
                  expense_amount, expense_category, expense_description))
            conn.commit()
            conn.close()
            st.success("Expense added successfully!")
    
    # Expense Analysis
    conn = sqlite3.connect('finance_tracker.db')
    df_expenses = pd.read_sql_query("""
        SELECT date, amount, category, description 
        FROM expenses 
        WHERE user_id = ?
    """, conn, params=(st.session_state.user_id,))
    conn.close()
    
    if not df_expenses.empty:
        # Summary Statistics
        st.markdown("### Expense Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_expenses = df_expenses['amount'].sum()
            st.metric("Total Expenses", f"₹{total_expenses:,.2f}")
        
        with col2:
            avg_daily = df_expenses.groupby('date')['amount'].sum().mean()
            st.metric("Average Daily Expense", f"₹{avg_daily:,.2f}")
        
        with col3:
            most_common_category = df_expenses['category'].mode()[0]
            st.metric("Most Common Category", most_common_category)
        
        # Visualizations
        st.markdown("### Expense Analysis")
        
        # Category-wise Pie Chart
        fig = px.pie(df_expenses, values='amount', names='category',
                    title='Expense Distribution by Category')
        st.plotly_chart(fig)
        
        # Daily Expense Trend
        df_expenses['date'] = pd.to_datetime(df_expenses['date'])
        daily_expenses = df_expenses.groupby('date')['amount'].sum().reset_index()
        
        fig = px.line(daily_expenses, x='date', y='amount',
                     title='Daily Expense Trend',
                     labels={'amount': 'Amount (₹)', 'date': 'Date'})
        st.plotly_chart(fig)
        
    
# ============= INVESTMENT PLANNER =============
def investment_planner():
    st.markdown("<h1 style='text-align: center;'>Investment Planner</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Investment Calculator", "Portfolio Allocation", "Goal Tracker"])
    
    with tab1:
        st.markdown("### Investment Calculator")
        calc_type = st.radio("Select Calculator Type", ["SIP", "Lump Sum"])
        
        if calc_type == "SIP":
            monthly_investment = st.number_input("Monthly Investment (₹)", 
                                               min_value=100, value=5000)
            years = st.number_input("Investment Period (Years)", 
                                  min_value=1, max_value=40, value=10)
            expected_return = st.number_input("Expected Annual Return (%)", 
                                            min_value=1.0, max_value=30.0, value=12.0)
            
            # Calculate SIP returns
            monthly_rate = expected_return / (12 * 100)
            months = years * 12
            future_value = monthly_investment * ((pow(1 + monthly_rate, months) - 1) / 
                                               monthly_rate) * (1 + monthly_rate)
            
            total_investment = monthly_investment * months
            total_returns = future_value - total_investment
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Investment", f"₹{total_investment:,.2f}")
            col2.metric("Total Returns", f"₹{total_returns:,.2f}")
            col3.metric("Future Value", f"₹{future_value:,.2f}")
            
        else:  # Lump Sum
            principal = st.number_input("Investment Amount (₹)", 
                                      min_value=1000, value=100000)
            years = st.number_input("Investment Period (Years)", 
                                  min_value=1, max_value=40, value=10)
            expected_return = st.number_input("Expected Annual Return (%)", 
                                            min_value=1.0, max_value=30.0, value=12.0)
            
            # Calculate Lump Sum returns
            future_value = principal * pow(1 + expected_return/100, years)
            total_returns = future_value - principal
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Initial Investment", f"₹{principal:,.2f}")
            col2.metric("Total Returns", f"₹{total_returns:,.2f}")
            col3.metric("Future Value", f"₹{future_value:,.2f}")
        
        # Growth Visualization
        st.markdown("### Investment Growth Projection")
        years_range = np.arange(0, years + 1)
        
        if calc_type == "SIP":
            values = [monthly_investment * 12 * year for year in years_range]
            monthly_rate = expected_return / (12 * 100)
            growth_values = [monthly_investment * ((pow(1 + monthly_rate, year * 12) - 1) / 
                                                 monthly_rate) * (1 + monthly_rate) 
                           for year in years_range]
        else:
            values = [principal] * len(years_range)
            growth_values = [principal * pow(1 + expected_return/100, year) 
                           for year in years_range]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years_range, y=values, 
                               name='Investment Amount', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=years_range, y=growth_values, 
                               name='Growth', line=dict(color='green')))
        
        fig.update_layout(
            title=f'{calc_type} Investment Growth',
            xaxis_title='Years',
            yaxis_title='Amount (₹)',
            height=400
        )
        st.plotly_chart(fig)
    
    with tab2:
        st.markdown("### Portfolio Allocation")
        age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
        risk_profile = st.selectbox("Risk Profile", 
                                  ["Conservative", "Moderate", "Aggressive"])
        
        # Calculate allocations based on age and risk profile
        equity_percent = max(20, min(80, 100 - age))
        
        if risk_profile == "Conservative":
            equity_percent = max(20, equity_percent - 10)
        elif risk_profile == "Aggressive":
            equity_percent = min(80, equity_percent + 10)
        
        debt_percent = 100 - equity_percent
        
        # Equity breakdown
        large_cap = equity_percent * 0.60
        mid_cap = equity_percent * 0.25
        small_cap = equity_percent * 0.15
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Broad Asset Allocation
            fig = go.Figure(data=[go.Pie(
                labels=['Equity', 'Debt'],
                values=[equity_percent, debt_percent],
                hole=.3
            )])
            fig.update_layout(title="Broad Asset Allocation")
            st.plotly_chart(fig)
        
        with col2:
            # Equity Breakdown
            fig = go.Figure(data=[go.Pie(
                labels=['Large Cap', 'Mid Cap', 'Small Cap'],
                values=[large_cap, mid_cap, small_cap],
                hole=.3
            )])
            fig.update_layout(title="Equity Breakdown")
            st.plotly_chart(fig)
        
        st.markdown(f"""
        ### Recommended Allocation
        
        **Broad Asset Allocation:**
        - Equity: {equity_percent:.1f}%
        - Debt: {debt_percent:.1f}%
        
        **Equity Breakdown:**
        - Large Cap: {large_cap:.1f}%
        - Mid Cap: {mid_cap:.1f}%
        - Small Cap: {small_cap:.1f}%
        """)
    
    with tab3:
        st.markdown("### Goal Tracker")
        
        # Add New Goal
        with st.expander("Add New Goal", expanded=True):
            with st.form("new_goal"):
                goal_name = st.text_input("Goal Name")
                goal_amount = st.number_input("Target Amount (₹)", min_value=0)
                goal_date = st.date_input("Target Date")
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                current_amount = st.number_input("Current Amount (₹)", min_value=0)
                
                submitted = st.form_submit_button("Add Goal")
                if submitted:
                    conn = sqlite3.connect('finance_tracker.db')
                    c = conn.cursor()
                    c.execute("""
                        INSERT INTO goals (user_id, name, target_amount, current_amount, 
                                         target_date, priority)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (st.session_state.user_id, goal_name, goal_amount, 
                          current_amount, goal_date.strftime("%Y-%m-%d"), priority))
                    conn.commit()
                    conn.close()
                    st.success("Goal added successfully!")
        
        # Display Goals
        conn = sqlite3.connect('finance_tracker.db')
        df_goals = pd.read_sql_query("""
            SELECT name, target_amount, current_amount, target_date, priority 
            FROM goals 
            WHERE user_id = ?
        """, conn, params=(st.session_state.user_id,))
        conn.close()
        
        if not df_goals.empty:
            st.markdown("### Your Financial Goals")
            
            for _, goal in df_goals.iterrows():
                progress = (goal['current_amount'] / goal['target_amount']) * 100
                
                st.markdown(f"""
                <div style='padding: 1rem; background-color: white; border-radius: 0.5rem; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 1rem 0;'>
                    <h4>{goal['name']} ({goal['priority']} Priority)</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.progress(progress/100)
                    st.markdown(f"Progress: {progress:.1f}%")
                
                with col2:
                    st.markdown(f"""
                    Target: ₹{goal['target_amount']:,.2f}  
                    Current: ₹{goal['current_amount']:,.2f}  
                    Target Date: {goal['target_date']}
                    """)
                
                # Calculate monthly savings needed
                target_date = datetime.strptime(goal['target_date'], "%Y-%m-%d")
                months_remaining = (target_date - datetime.now()).days / 30
                if months_remaining > 0:
                    monthly_needed = (goal['target_amount'] - goal['current_amount']) / months_remaining
                    st.info(f"You need to save ₹{monthly_needed:,.2f} monthly to reach your goal")

# Update the main() function
def main():
    if not st.session_state.authenticated:
        auth_page()
    else:
        selected = create_ion()
        
        if selected == "Dashboard":
            dashboard()
        elif selected == "Expenses":
            expense_tracker()
        elif selected == "Investments":
            investment_planner()
        elif selected == "Analysis":
            st.title("Analysis - Coming in Section 3")
        elif selected == "Settings":
            st.title("Settings - Coming in Section 3")

# ============= MAIN APP =============
def main():
    if not st.session_state.authenticated:
        auth_page()
    else:
        selected = create_ion()
        
        if selected == "Dashboard":
            st.title("Dashboard - Coming in Section 2")
        elif selected == "Expenses":
            st.title("Expenses - Coming in Section 2")
        elif selected == "Investments":
            st.title("Investments - Coming in Section 2")
        elif selected == "Analysis":
            st.title("Analysis - Coming in Section 3")
        elif selected == "Settings":
            st.title("Settings - Coming in Section 3")
# ============= ADVANCED ANALYTICS =============
def advanced_analytics():
    st.markdown("<h1 style='text-align: center;'>Advanced Analytics</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Expense Analysis", "Investment Analysis", "Financial Health"])
    
    with tab1:
        st.markdown("### Expense Pattern Analysis")
        
        # Get expense data
        conn = sqlite3.connect('finance_tracker.db')
        df_expenses = pd.read_sql_query("""
            SELECT date, amount, category 
            FROM expenses 
            WHERE user_id = ?
        """, conn, params=(st.session_state.user_id,))
        conn.close()
        
        if not df_expenses.empty:
            df_expenses['date'] = pd.to_datetime(df_expenses['date'])
            
            # Monthly Trend
            monthly_expenses = df_expenses.groupby(df_expenses['date'].dt.strftime('%Y-%m'))[['amount']].sum()
            
            fig = px.line(monthly_expenses, x=monthly_expenses.index, y='amount',
                         title='Monthly Expense Trend',
                         labels={'amount': 'Amount (₹)', 'date': 'Month'})
            st.plotly_chart(fig)
            
            # Category Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # Category Distribution
                category_expenses = df_expenses.groupby('category')['amount'].sum()
                fig = px.pie(values=category_expenses.values,
                           names=category_expenses.index,
                           title='Expense Distribution by Category')
                st.plotly_chart(fig)
            
            with col2:
                # Weekly Pattern
                df_expenses['weekday'] = df_expenses['date'].dt.day_name()
                weekly_expenses = df_expenses.groupby('weekday')['amount'].mean()
                
                fig = px.bar(x=weekly_expenses.index,
                           y=weekly_expenses.values,
                           title='Average Daily Spending by Weekday',
                           labels={'x': 'Day', 'y': 'Average Amount (₹)'})
                st.plotly_chart(fig)
            
            
           
            # Calculate metrics
            total_monthly = df_expenses.groupby(df_expenses['date'].dt.strftime('%Y-%m'))['amount'].sum()
            avg_monthly = total_monthly.mean()
            std_monthly = total_monthly.std()
            
            # Generate insights
            insights = []
            
            if total_monthly.iloc[-1] > avg_monthly + std_monthly:
                insights.append("📈 Your spending this month is higher than usual.")
            elif total_monthly.iloc[-1] < avg_monthly - std_monthly:
                insights.append("📉 Your spending this month is lower than usual.")
            
            # Category-specific insights
            for category in df_expenses['category'].unique():
                cat_data = df_expenses[df_expenses['category'] == category]
                cat_monthly = cat_data.groupby(cat_data['date'].dt.strftime('%Y-%m'))['amount'].sum()
                
                if len(cat_monthly) > 1 and cat_monthly.iloc[-1] > cat_monthly.iloc[:-1].mean() * 1.2:
                    insights.append(f"⚠️ {category} expenses have increased significantly.")
            
            for insight in insights:
                st.info(insight)
    
    with tab2:
        st.markdown("### Investment Performance Analysis")
        
        # Sample investment data (replace with actual data)
        investment_data = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
            'Equity': np.random.normal(12000, 2000, 12).cumsum(),
            'Debt': np.random.normal(8000, 1000, 12).cumsum(),
            'Gold': np.random.normal(5000, 500, 12).cumsum()
        })
        
        # Portfolio Performance
        fig = px.line(investment_data, x='Date',
                     y=['Equity', 'Debt', 'Gold'],
                     title='Portfolio Performance Over Time')
        st.plotly_chart(fig)
        
        # Asset Allocation
        current_allocation = {
            'Asset': ['Equity', 'Debt', 'Gold'],
            'Amount': [investment_data['Equity'].iloc[-1],
                      investment_data['Debt'].iloc[-1],
                      investment_data['Gold'].iloc[-1]]
        }
        df_allocation = pd.DataFrame(current_allocation)
        
        fig = px.pie(df_allocation, values='Amount', names='Asset',
                    title='Current Asset Allocation')
        st.plotly_chart(fig)
        
        # Performance Metrics
        st.markdown("### Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_value = df_allocation['Amount'].sum()
            st.metric("Total Portfolio Value", f"₹{total_value:,.2f}")
        
        with col2:
            returns = (total_value - investment_data.iloc[0].sum()) / investment_data.iloc[0].sum() * 100
            st.metric("Total Returns", f"{returns:.1f}%")
        
        with col3:
            monthly_return = returns / 12
            st.metric("Average Monthly Return", f"{monthly_return:.1f}%")
    
    with tab3:
        st.markdown("### Financial Health Score")
        
        # Get user inputs
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=0, value=30000)
            emergency_fund = st.number_input("Emergency Fund (₹)", min_value=0, value=100000)
        
        with col2:
            total_investments = st.number_input("Total Investments (₹)", min_value=0, value=200000)
            total_debt = st.number_input("Total Debt (₹)", min_value=0, value=0)
        
        # Calculate ratios
        savings_rate = ((monthly_income - monthly_expenses) / monthly_income) * 100 if monthly_income > 0 else 0
        emergency_fund_months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
        debt_to_income = (total_debt / (monthly_income * 12)) * 100 if monthly_income > 0 else 0
        investment_ratio = (total_investments / (monthly_income * 12)) * 100 if monthly_income > 0 else 0
        
        # Calculate health score
        score = 0
        score += min(25, savings_rate / 2)  # Max 25 points for savings
        score += min(25, emergency_fund_months * 12.5)  # Max 25 points for emergency fund
        score += min(25, 25 * (1 - debt_to_income/100))  # Max 25 points for low debt
        score += min(25, investment_ratio / 4)  # Max 25 points for investments
        
        # Display score gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Financial Health Score"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': COLORS['primary']},
                'steps': [
                    {'range': [0, 33], 'color': "lightgray"},
                    {'range': [33, 66], 'color': "gray"},
                    {'range': [66, 100], 'color': COLORS['accent']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        st.plotly_chart(fig)
        
        # Analysis and Recommendations
        st.markdown("### Financial Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Strengths")
            if savings_rate >= 20:
                st.success(f"Strong savings rate: {savings_rate:.1f}%")
            if emergency_fund_months >= 6:
                st.success(f"Adequate emergency fund: {emergency_fund_months:.1f} months")
            if debt_to_income < 30:
                st.success(f"Healthy debt levels: {debt_to_income:.1f}%")
            if investment_ratio >= 50:
                st.success(f"Good investment ratio: {investment_ratio:.1f}%")
        
        with col2:
            st.markdown("#### Areas for Improvement")
            if savings_rate < 20:
                st.warning(f"Work on increasing savings rate: {savings_rate:.1f}%")
            if emergency_fund_months < 6:
                st.warning(f"Build emergency fund: Currently {emergency_fund_months:.1f} months")
            if debt_to_income >= 30:
                st.warning(f"High debt-to-income ratio: {debt_to_income:.1f}%")
            if investment_ratio < 50:
                st.warning(f"Increase investments: Currently {investment_ratio:.1f}%")
        
        # Recommendations
        st.markdown("### Personalized Recommendations")
        recommendations = []
        
        if savings_rate < 20:
            recommendations.append("• Create a budget to increase your savings rate to at least 20%")
        if emergency_fund_months < 6:
            recommendations.append(f"• Build emergency fund by saving ₹{(6*monthly_expenses - emergency_fund):,.2f} more")
        if debt_to_income >= 30:
            recommendations.append("• Focus on debt reduction before increasing investments")
        if investment_ratio < 50:
            recommendations.append("• Consider increasing your investment allocation")
        
        for rec in recommendations:
            st.markdown(rec)

# ============= SETTINGS PAGE =============
def settings_page():
    st.markdown("<h1 style='text-align: center;'>Settings</h1>", unsafe_allow_html=True)
    
    # Profile Settings
    st.markdown("### Profile Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get user info
        conn = sqlite3.connect('finance_tracker.db')
        c = conn.cursor()
        c.execute("SELECT username, email FROM users WHERE id = ?", 
                 (st.session_state.user_id,))
        user_info = c.fetchone()
        conn.close()
        
        if user_info:
            username, email = user_info
            st.text_input("Username", value=username, disabled=True)
            st.text_input("Email", value=email, disabled=True)
    
    with col2:
        # Theme Settings
        st.markdown("### Theme Settings")
        dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
    
    # Notification Settings
    st.markdown("### Notification Settings")
    st.checkbox("Email Alerts for Unusual Expenses", value=True)
    st.checkbox("Monthly Report", value=True)
    st.checkbox("Investment Alerts", value=True)
    
    # Data Management
    st.markdown("### Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Data"):
            # Get user's data
            conn = sqlite3.connect('finance_tracker.db')
            df_expenses = pd.read_sql_query("""
                SELECT date, amount, category, description 
                FROM expenses 
                WHERE user_id = ?
            """, conn, params=(st.session_state.user_id,))
            
            # Convert to CSV
            csv = df_expenses.to_csv(index=False)
            
            # Create download button
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="my_financial_data.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Delete Account"):
            st.warning("⚠️ This will permanently delete your account and all associated data!")
            if st.button("Confirm Delete"):
                conn = sqlite3.connect('finance_tracker.db')
                c = conn.cursor()
                # Delete user's data
                c.execute("DELETE FROM expenses WHERE user_id = ?", 
                         (st.session_state.user_id,))
                c.execute("DELETE FROM goals WHERE user_id = ?", 
                         (st.session_state.user_id,))
                c.execute("DELETE FROM users WHERE id = ?", 
                         (st.session_state.user_id,))
                conn.commit()
                conn.close()
                
                # Clear session state
                st.session_state.clear()
                st.success("Account deleted successfully!")
                st.rerun()

# Update the main() function
def main():
    if not st.session_state.authenticated:
        auth_page()
    else:
        selected = create_navigation()
        
        if selected == "Dashboard":
            dashboard()
        elif selected == "Expenses":
            expense_tracker()
        elif selected == "Investments":
            investment_planner()
        elif selected == "Analysis":
            advanced_analytics()
        elif selected == "Settings":
            settings_page()
            
        # Add footer here
        st.markdown("""
            <div class='footer'>
                Developed by Muhammed Adnan | Contact: kladnan321@gmail.com
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
