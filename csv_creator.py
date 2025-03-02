import pandas as pd

# Define the data for the CSV

data = {
    "Question": [
        "What are iterators?",
        "What are the six building blocks of STL?",
        "What are random access and sequential access?",

    ],
    "Answer": [
       "Iterators provide a standard/unified way to access elements in containers, regardless of the underlying data structure.",
       "Containers, iterators, algorithms, functors, adapters, allocators.",
       "Random Access: Allows direct access to any element in a data structure, enabling fast retrieval (e.g., arrays, hash tables). Sequential Access: Requires accessing elements in a linear order, one by one, which can be slower (e.g., linked lists, sequential file reading)."
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to a CSV file
df.to_csv('c++_lvalue_rvalue_and_lambda_notes.csv', index=False)
