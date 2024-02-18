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

# Function to detect outliers using Z-score
def detect_outliers_z_score(data, threshold=3):
    z_score_yield = (data['Yield'] - data['Yield'].mean()) / data['Yield'].std()
    z_score_quality = (data['Quality'] - data['Quality'].mean()) / data['Quality'].std()

    outliers_yield = data[abs(z_score_yield) > threshold]
    outliers_quality = data[abs(z_score_quality) > threshold]

    return outliers_yield, outliers_quality

# Function to process the uploaded file
def process_file(uploaded_file, detect_outliers=True):
    # Read Excel file
    data = pd.read_excel(uploaded_file, sheet_name='planting_data')

    # Detect outliers if specified
    if detect_outliers:
        outliers_yield, outliers_quality = detect_outliers_z_score(data)
        data = data[~data.index.isin(outliers_yield.index) & ~data.index.isin(outliers_quality.index)]

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
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Display descriptive statistics for Yield and Quality
    st.subheader("Descriptive Statistics:")
    yield_stats = data['Yield'].describe()
    quality_stats = data['Quality'].describe()
    st.write("Descriptive Statistics for Yield:")
    st.write(yield_stats)
    st.write("Descriptive Statistics for Quality:")
    st.write(quality_stats)

    # Pie chart for Distribution of Hybrid
    plt.figure(figsize=(10, 6))
    hybrid_counts = data['Hybrid'].value_counts()
    plt.pie(hybrid_counts, labels=hybrid_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Hybrid')
    st.pyplot()

    # Create subplots for additional analysis
    fig, axes = plt.subplots(3, 2, figsize=(18, 12))

    # Line chart for Yield over Planting Week
    sns.lineplot(x='Planting Week', y='Yield', data=data, ax=axes[0, 0])
    axes[0, 0].set_title('Yield over Planting Week')
    axes[0, 0].set_xlabel('Planting Week')
    axes[0, 0].set_ylabel('Yield')

    # Line chart for Quality over Planting Week
    sns.lineplot(x='Planting Week', y='Quality', data=data, ax=axes[0, 1])
    axes[0, 1].set_title('Quality over Planting Week')
    axes[0, 1].set_xlabel('Planting Week')
    axes[0, 1].set_ylabel('Quality')

    # Segregating the data by hybrid
    hybrid_1 = data[data['Hybrid'] == 1]
    hybrid_2 = data[data['Hybrid'] == 2]

    # Line chart for Yield over Planting Week Hybrid 1
    sns.lineplot(x='Planting Week', y='Yield', data=hybrid_1, ax=axes[1, 0])
    axes[1, 0].set_title('Yield over Planting Week Hybrid 1')
    axes[1, 0].set_xlabel('Planting Week')
    axes[1, 0].set_ylabel('Yield')

    # Line chart for Quality over Planting Week Hybrid 1
    sns.lineplot(x='Planting Week', y='Quality', data=hybrid_1, ax=axes[1, 1])
    axes[1, 1].set_title('Quality over Planting Week Hybrid 1')
    axes[1, 1].set_xlabel('Planting Week')
    axes[1, 1].set_ylabel('Quality')

    # Line chart for Yield over Planting Week Hybrid 2
    sns.lineplot(x='Planting Week', y='Yield', data=hybrid_2, ax=axes[2, 0])
    axes[2, 0].set_title('Yield over Planting Week Hybrid 2')
    axes[2, 0].set_xlabel('Planting Week')
    axes[2, 0].set_ylabel('Yield')

    # Line chart for Quality over Planting Week Hybrid 2
    sns.lineplot(x='Planting Week', y='Quality', data=hybrid_2, ax=axes[2, 1])
    axes[2, 1].set_title('Quality over Planting Week Hybrid 2')
    axes[2, 1].set_xlabel('Planting Week')
    axes[2, 1].set_ylabel('Quality')

    plt.tight_layout()
    st.pyplot(fig)

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
    st.title("Yield and Quality Data Analysis")
    st.write("Upload your Excel file below:")

    # File upload
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Process file with outliers
        st.subheader("With Outliers")
        process_file(uploaded_file, detect_outliers=True)

        # Process file without outliers
        st.subheader("Without Outliers")
        process_file(uploaded_file, detect_outliers=False)

if __name__ == "__main__":
    main()
