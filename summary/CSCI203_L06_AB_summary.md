# CSCI203 - Algorithms and Data Structures: Hashing

## Introduction to Hashing
- **Definition**: Hashing is a technique used to uniquely identify a specific object from a group of similar objects. It involves mapping data of arbitrary size to fixed-size values (hash values).
- **Purpose**: Efficient data retrieval, storage, and management.

## Hash Table
- **Structure**: A hash table is a data structure that implements an associative array abstract data type, a structure that can map keys to values.
- **Components**:
  - **Array**: Large array called a hash table.
  - **Hash Function**: A function that maps keys to positions in the hash table.
  - **Load Factor**: Ratio of the number of items (n) to the number of slots (m) in the hash table, \( \alpha = \frac{n}{m} \).

## Hash Function
- **Definition**: A hash function maps keys to positions in the hash table.
- **Characteristics**:
  - **Easy to Calculate**: Should be computationally inexpensive.
  - **Use All of the Key**: Should consider all parts of the key.
  - **Uniform Distribution**: Should spread the keys uniformly across the hash table.

### Common Hash Functions
1. **Division Method**: 
   \[
   h(k) = k \mod m
   \]
   - Good if m is a prime number.
  
2. **Multiplication Method**: 
   \[
   h(k) = \lfloor m(kA \mod 1) \rfloor
   \]
   - Where \( A \) is a constant in the range (0, 1).

3. **Universal Hashing**: 
   \[
   h(k) = ((ak + b) \mod p) \mod m
   \]
   - Where \( p \) is a prime number larger than the size of the key set.

## Collision Handling
- **Definition**: A collision occurs when two different keys hash to the same index in the hash table.
- **Strategies to Handle Collisions**:
  1. **Chaining**: Each slot in the hash table contains a linked list of entries that hash to the same index.
  2. **Open Addressing**: When a collision occurs, the algorithm seeks the next available slot using a probing sequence.

### Chaining
- **Advantages**:
  - Easy and quick insertions and deletions.
  - Allows for more records than the hash table size.
  - Naturally resizable.
- **Disadvantages**:
  - Uses more space due to linked lists.
  - More complex to implement.

#### Example of Chaining
```pseudo
module InsertChaining(item):
    posHash = hash(key of item)
    insert(hashTable[posHash], item)
```

### Open Addressing
- **Definition**: A technique where each key is stored directly in the hash table, and on collision, the algorithm probes for the next available slot.
- **Types of Probing**:
  1. **Linear Probing**: 
     \[
     p(k, i) = (h(k) + i) \mod m
     \]
  2. **Quadratic Probing**:
     \[
     p(k, i) = (h(k) + c_1i + c_2i^2) \mod m
     \]
  3. **Double Hashing**:
     \[
     p(k, i) = (h_1(k) + i \cdot h_2(k)) \mod m
     \]

## Performance Analysis
- **Load Factor**: 
  - Ideally, maintain \( \alpha < 0.5 \) for optimal performance.
  - Average cost of operations is \( O(1 + \frac{n}{m}) \).

- **Amortized Cost**: 
  - Operations on a dynamically growing hash table can be amortized to \( O(1) \).

## Resizing the Hash Table
- **When to Resize**:
  - If \( n \) exceeds \( m \) or falls below a certain threshold (e.g., \( n < \frac{m}{4} \)).
- **Process**:
  1. Create a new array of size \( m' \).
  2. Rehash all existing keys to the new table.
  
## Summary
- **Chaining vs. Open Addressing**:
  - **Chaining**: Simpler to implement, handles more collisions but uses more memory.
  - **Open Addressing**: More memory efficient, faster under certain conditions, but slightly more complex to implement.

## References
- Levitin, A. (2011). *Introduction to the Design and Analysis of Algorithms*.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms*.

These notes provide a structured overview of hashing, hash tables, and the associated concepts discussed in the CSCI203 lecture on Algorithms and Data Structures.