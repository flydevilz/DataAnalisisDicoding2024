import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

df = pd.read_csv('dataset/full.csv')
# add date col for year filter
df['year'] = pd.to_datetime(df['order_delivered_customer_date'], format='%Y-%m-%d').dt.year

# sidebar
st.sidebar.header("Filter:")

year = st.sidebar.multiselect(
    "Select year:",
    options= df['year'].unique(),
    default= df['year'].unique()
    )

note = st.sidebar.multiselect(
    "Select category:",
    options= df['note'].unique(),
    default= df['note'].unique()
    )

payment_type = st.sidebar.multiselect(
    "Select payment type:",
    options=df['payment_type'].unique(),
    default=df['payment_type'].unique()
)

df1 = df.query(
    "(year == @year) and (note == @note) and (payment_type == @payment_type)"
)

# mainpage
st.title(":bar_chart: Delivered Order Summary")
st.markdown("##")

# kpi order
total_transaction = int(df1['payment_value'].sum())
average_rating = round(df1['review_score'].mean(), 1)
average_transaction = round(df1['payment_value'].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Transaction:")
    st.subheader(f"US ${total_transaction:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} :star:")
with right_column:
    st.subheader("Average Transaction:")
    st.subheader(f"US ${average_transaction}")

st.markdown("---")

# visualization
note_groupby = df1.groupby('note')['review_score'].agg('mean').reset_index().rename(columns={'review_score': 'mean_review_score'})
fig_note= px.bar(note_groupby, x='note', y='mean_review_score', title='Delivery Rating Mean', labels={'mean_review_score': 'Review Score', 'note':'Delivery Time'})
st.plotly_chart(fig_note)

paytype_counts = df1['payment_type'].value_counts().reset_index()
fig_paycount = px.bar(paytype_counts, x='payment_type', y='count', title='User Payment Count', labels={'payment_type': 'Payment Type', 'count': 'Count'})
st.plotly_chart(fig_paycount)

mean_transaction = df1.groupby('payment_type')['payment_value'].agg('mean').reset_index()
fig_trans = px.bar(mean_transaction, x='payment_type', y='payment_value', title='Mean Transaction From Every Payment Type', labels={'payment_type': 'Payment Type', 'payment_value': 'Transaction (in $)'})
st.plotly_chart(fig_trans)