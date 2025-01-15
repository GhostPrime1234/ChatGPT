```markdown
# Lecture Notes: String Searching and Sorting Algorithms

## String Search

### Definition
- **String Searching**: The process of finding a specific substring (s) within a larger text (t).
  
### Applications
- **Real-life Applications**:
  - `grep`: Command line utility for searching plain-text data sets.
  - Text editors: Finding text within documents.
  - Genome matching: Searching for patterns in DNA sequences.
  - Search engines: Finding relevant results for queries.

### Linear Search
- **Example**:
  - Text (t): “harry happened to have a hard hand”.
  - Substring (s): “hara”.
- **Process**:
  - Start at each position in t and compare with s.
  - Complexity: O(|s| x |t|).
  
### Karp-Rabin String Search Algorithm
- **Hashing Approach**:
  - Calculate the hash for s and each substring of t.
  - Use a rolling hash to compute the hash for the next substring in constant time.
  
- **Algorithm**:
  ```python
  hash_s = hash(s)
  hash_t = hash(t[0..length(s)-1])
  for i in range(0, length(t) - length(s)):
      if hash_s == hash_t:
          # brute-force compare
      hash_t = roll(hash_t, t[i], t[i + length(s)])
  ```

## Lower Bound for Comparison Sort

### Comparison Sort
- **Definition**: Sorting algorithms that only use comparisons between elements to determine order.
- **Examples**: Insertion sort, merge sort, heap sort.

### Decision Tree Model
- **Concept**: A decision tree represents the comparisons made by a sorting algorithm.
- **Properties**:
  - Each internal node represents a comparison.
  - Leaf nodes represent possible permutations of the input.
  
### Theorem
- **Worst-Case Lower Bound**: All comparison sorts require at least O(n log n) comparisons.
  
### Proof of Lower Bound
- A decision tree for n elements has n! leaves.
- The height of the tree, which corresponds to the worst-case time complexity, is O(n log n).

## Sorting in Linear Time

### Bucket Sorting
- **Concept**: Divides the input into several "buckets" and sorts each bucket individually.
  
- **Algorithm**:
  ```python
  def bucket_sort(A):
      n = len(A)
      B = [[] for _ in range(n)]
      for value in A:
          index = int(n * value)  # Assuming values are in [0, 1)
          B[index].append(value)
      for bucket in B:
          insertion_sort(bucket)
      return [item for bucket in B for item in bucket]
  ```

### Radix Sorting
- **Concept**: Sorts numbers digit by digit, starting from the least significant digit to the most significant digit.
  
- **Algorithm**:
  ```python
  def radix_sort(A, d):
      for i in range(d):
          stable_sort(A, i)  # Stable sort based on the i-th digit
  ```

### Complexity
- **Bucket Sort**: O(n) on average if the input is uniformly distributed.
- **Radix Sort**: O(d(n + k)), where d is the number of digits and k is the range of the input values.

### Efficiency
- Both sorting algorithms achieve linear time complexity under certain conditions, making them preferable in specific scenarios compared to traditional comparison-based sorts.

## Conclusion
- Understanding string searching and sorting algorithms is fundamental in algorithm design and analysis.
- The choice of algorithm can significantly affect performance based on the characteristics of the input data and the specific requirements of the task at hand.
```