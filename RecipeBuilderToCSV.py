import streamlit as st
import pandas as pd
import io

def main():
    # Function to create a new ingredient entry
    def create_new_ingredient_entry():
        return {"ingredient": "", "unit": "tablespoons", "quantity": 0.0, "link": ""}

    # Initialize session state
    if 'recipes' not in st.session_state:
        st.session_state.recipes = []
    if 'ingredient_entries' not in st.session_state:
        st.session_state.ingredient_entries = [create_new_ingredient_entry()]

    # Custom header and alignment style
    alignment_style = """
    <style>
    .header-font {
        font-size: 1em; /* 50% of the base font size */
    }
    .column {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .stTextInput, .stSelectbox, .stNumberInput, .stButton {
        width: 100%;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """

    st.markdown(alignment_style, unsafe_allow_html=True)

    # Button to add new ingredient entry
    if st.button("Add New Ingredient"):
        st.session_state.ingredient_entries.append(create_new_ingredient_entry())

    # Dynamic ingredient entry fields
    for i, entry in enumerate(st.session_state.ingredient_entries):
        col1, col2, col2_1, col3 = st.columns(4)
        with col1:
            entry["ingredient"] = st.text_input("Enter an ingredient", key=f"ingredient_{i}")
        with col2:
            entry["unit"] = st.selectbox("Units Of Food", ["tablespoons", "teaspoons", "grams", "ounces"], key=f"unit_{i}")
        with col2_1:
            entry["quantity"] = st.number_input("Quantity", min_value=0.0, format="%.3f", step=0.001, key=f"quantity_{i}")
        with col3:
            entry["link"] = st.text_input("Enter a link", key=f"link_{i}")

    # Column for save button
    col4 = st.empty()  # Placeholder for save button

    # Save recipe functionality
    if col4.button("Save Recipe"):
        for entry in st.session_state.ingredient_entries:
            if entry["ingredient"]:
                formatted_quantity = f"{entry['quantity']:.3f}"
                recipe_entry = (entry["ingredient"], f"{formatted_quantity} {entry['unit']}", entry["link"])
                st.session_state.recipes.append(recipe_entry)
        st.session_state.ingredient_entries = [create_new_ingredient_entry()]
        st.success("Recipe saved!")

    # Display saved data in a structured format
    st.header("Saved Recipes")
    for recipe in st.session_state.recipes:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(recipe[0])  # Ingredient
        with col2:
            st.write(recipe[1])  # Quantity and Unit
        with col3:
            # Display link only if it exists
            if recipe[2]:
                st.markdown(f"[{recipe[0]} Link]({recipe[2]})", unsafe_allow_html=True)
            else:
                st.write("No Link Provided")

    # Function to convert recipes to a CSV file
    def convert_to_csv(recipes):
        df = pd.DataFrame(recipes, columns=['Ingredient', 'Quantity', 'Link'])
        return df.to_csv(index=False).encode('utf-8')

    # Download button for recipes CSV
    if st.session_state.recipes:
        csv = convert_to_csv(st.session_state.recipes)
        st.download_button(
            label="Download Recipes as CSV",
            data=csv,
            file_name='recipes.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
