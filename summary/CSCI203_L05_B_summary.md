# Quadtrees - Complexity

## Time Complexity
- **Find**: O(log N)
- **Insert**: O(log N)
- **Search**: O(log N)

## Space Complexity
- **Space Requirement**: O(k log N)
  - Where `k` is the count of points in the space, and the space is of dimension NxM, where N >= M.

---

# Quadtrees Overview

## Definition
- Quadtrees are a data structure used primarily for partitioning a 2D space into smaller regions.

## Structure
- Each internal node has exactly four children, making it a 4-way tree.
  
  ![Quadtrees Structure](https://example.com/quadtree_structure.png)  <!-- Placeholder for a diagram -->

## Leaf Nodes
- The data associated with a leaf node represents "interesting" information relevant to the region it covers.

---

# Applications of Quadtrees

## Computer Graphics
- Used in rendering scenes, mesh generation, and collision detection in 2D.

## Computer Vision
- Employed in image representation, processing, and segmentation.

## Geographic Information Systems (GIS)
- Useful in mapping applications like Google Maps and Google Earth.

## Other Applications
- Human-Computer interface design, virtual reality, and visualizations of complex functions.

---

# Fast Searching Techniques

## Problem Statement
- Given a set of data (e.g., name and telephone number), how can we efficiently find the number associated with a given name?

## Data Structure Options
- **Linear List**: O(n) time complexity, requires checking each entry.
- **Binary Search Tree (BST)**: O(log n) on average, but O(n) in the worst case without balancing.
- **Balanced Trees**: Better performance than standard BSTs.

## Constant Time Search
- Using a dictionary implemented with a hash table can provide O(1) search time. 

### Dictionary Operations
- **Insert**: `D[key] = value`
- **Delete**: `delete(D[key])`
- **Search**: `value = D[key]`, returns nil if not found.

---

# Quadtrees - Operations

## Construction
1. Divide the current 2D space into four regions.
2. If a region contains one or more points:
   - Create a child node storing the region.
3. If a region does not contain points:
   - Do not create a child.
4. Recursively perform steps 1-3 for each child.

## Types of Nodes
- **Point Node**: Represents a point, always a leaf node.
- **Empty Node**: Represents a region without points.
- **Region Node**: Internal node representing a region, always has four children.

---

# Common Types of Quadtrees

## Point and Point-Region Quadtrees
- Similar to region quadtrees but store a list of points in a leaf rather than values for the entire area.

---

# Implementation of Quadtrees

## PR Quadtrees - Insertion
1. Start with the root node as the current node.
2. If the point is outside the boundary of the current node, stop insertion with an error.
3. Determine the appropriate child node to store the point.
4. If the child node is empty, replace it with a point node.
5. If the child node is a point, replace it with a region node and insert the point recursively.
6. If the child is a region node, set it as the current node and continue the insertion.

## PR Quadtrees - Search
1. Start with the root node as the current node.
2. If the point is outside the boundary, stop the search with an error.
3. Determine the appropriate child node to search.
4. If the child node is empty, return FALSE.
5. If the child node is a point and matches, return TRUE; otherwise, return FALSE.
6. If the child is a region node, set it as the current node and continue searching.

---

# Implementation of Direct Access Tables

## Overview
- A direct access table is an array where the index is the key and the content is the value.
  
### Operations
- **Search**: `T[key]`
- **Insert**: `T[key] = value`
- **Delete**: `T[key] = nil`
- All operations run in O(1) time.

## Limitations
- Requires keys to be non-negative integers and can waste space when the set of keys stored is small.

---

# Hashing for Efficient Key Management

## Problems with Direct Access Tables
1. **Large Universe of Keys**: Keys must be integers, which can lead to large arrays.
2. **Space Waste**: Large potential key space with few actual entries is inefficient.

## Solutions
- **Hashing**: Maps a large universe of keys down to a manageable size using a hash function.

### Hash Function
- A function `h(key)` that ensures 0 < h(key) < m for all valid keys, where `m` is the size of the hash table.

---

# References
1. J. Trinh, *Partitioning 2D Spaces: An Introduction to Quadtrees*, 2020.
2. A. Levitin, *Introduction to the Design and Analysis of Algorithms*, 3rd Ed., Pearson 2011.
3. T. H. Cormen, *Introduction to Algorithms*, 3rd Ed., MIT Press 2009.