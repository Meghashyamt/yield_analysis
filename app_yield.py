import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to find the best location and week for each hybrid
def best_location_week(hybrid_data):
    # Filtering data for Quality above 85%
    filtered_data = hybrid_data[hybrid_data['Quality'] > 85]

    # Grouping by Location and Planting Week and calculating mean Yield and Quality
    grouped_data = filtered_data.groupby(['Location', 'Planting Week']).agg({'Yield': 'mean', 'Quality': 'mean'}).reset_index()

    # Finding the combination with the highest yield
    best_combination = grouped_data[grouped_data['Yield'] == grouped_data['Yield'].max()]
    return best_combination

# Function to process the uploaded file
def process_file(uploaded_file):
    # Read Excel file
    data = pd.read_excel(uploaded_file, sheet_name='planting_data')

    # Set seaborn style
    sns.set(style="whitegrid")

    # Creating a set of plots 
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))

    # Plot 1: Yield distribution
    sns.histplot(data['Yield'], bins=30, kde=True, ax=axes[0, 0])
    axes[0, 0].set_title('Distribution of Yield')

    # Plot 2: Quality distribution
    sns.histplot(data['Quality'], bins=30, kde=True, ax=axes[0, 1])
    axes[0, 1].set_title('Distribution of Quality')

    # Plot 3: Yield vs Planting Week
    sns.boxplot(x='Planting Week', y='Yield', data=data, ax=axes[1, 0])
    axes[1, 0].set_title('Yield vs Planting Week')

    # Plot 4: Quality vs Planting Week
    sns.boxplot(x='Planting Week', y='Quality', data=data, ax=axes[1, 1])
    axes[1, 1].set_title('Quality vs Planting Week')

    plt.tight_layout()
    st.pyplot(fig)

    # Create subplots for additional analysis
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Pie chart for Distribution of Hybrid
    hybrid_counts = data['Hybrid'].value_counts()
    axes[0].pie(hybrid_counts, labels=hybrid_counts.index, autopct='%1.1f%%', startangle=140)
    axes[0].set_title('Distribution of Hybrid')

    # Line chart for Yield over Planting Week
    sns.lineplot(x='Planting Week', y='Yield', data=data, ax=axes[1])
    axes[1].set_title('Yield over Planting Week')
    axes[1].set_xlabel('Planting Week')
    axes[1].set_ylabel('Yield')

    # Line chart for Quality over Planting Week
    sns.lineplot(x='Planting Week', y='Quality', data=data, ax=axes[2])
    axes[2].set_title('Quality over Planting Week')
    axes[2].set_xlabel('Planting Week')
    axes[2].set_ylabel('Quality')

    plt.tight_layout()
    st.pyplot(fig)

    # Segregating the data by hybrid
    hybrid_1 = data[data['Hybrid'] == 1]
    hybrid_2 = data[data['Hybrid'] == 2]

    # Analyzing for each hybrid
    best_combination_hybrid_1 = best_location_week(hybrid_1)
    best_combination_hybrid_2 = best_location_week(hybrid_2)

    # Identifying weeks to avoid for Quality < 85%
    weeks_to_avoid = data[data['Quality'] < 85]['Planting Week'].unique()
    weeks_to_avoid_hybrid_1 = hybrid_1[hybrid_1['Quality'] < 85]['Planting Week'].unique()
    weeks_to_avoid_hybrid_2 = hybrid_2[hybrid_2['Quality'] < 85]['Planting Week'].unique()

    # Displaying results
    st.subheader("Best Combination for Hybrid 1:")
    st.dataframe(best_combination_hybrid_1)
    
    st.subheader("Best Combination for Hybrid 2:")
    st.dataframe(best_combination_hybrid_2)
    
    st.subheader("Weeks to Avoid (Overall):")
    st.write(weeks_to_avoid)
    
    st.subheader("Weeks to Avoid for Hybrid 1:")
    st.write(weeks_to_avoid_hybrid_1)
    
    st.subheader("Weeks to Avoid for Hybrid 2:")
    st.write(weeks_to_avoid_hybrid_2)

# Streamlit app
def main():
    st.title("Planting Data Analysis")
    st.write("Upload your Excel file below:")

    # File upload
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        process_file(uploaded_file)

if __name__ == "__main__":
    main()
