# Document Graph
A HashTree with keys for nodes comprised of a label and value. Each label defines a subtree representing a document section. Each value defines a strict order of where each item is in relation to another within the section. Nodes within the tree can reference any other node to relate information, or to override traversal. Default traversal will iterate through the tree using in-order traversal.

## Purpose
- Document sections are grouped together, so relationships are local.
- Document sections can be returned together, so relationships can be structured.
- Document sections know the next section, as sections are ordered.
- Section elements can be any data, including empty, but not null.
- Section elements are ordered.
- Section elements can be sections (a subsection), and the document is a singular section at the root.
- Section elements can be a reference to another section's elements, this reference can be traversed to, and this reference can be labeled.
- Traversal is expected to be in-order by section and element, and will ignore traversing to references by default.
- Traversal can break order using references and loop if allowed.
- Traversal can be conditional, and conditional elements can be skipped.
- Conditions are functions-as-elements that are referenced by elements, and only return true or false.
- Functions are skipped if not referenced.
- Functions can return a reference label, and this can be navigated to.

## Theory
### Legend
* n = number of Sections
* k = size of Section

### Fetch
Section, worst case: O(1)<br>
Element, worst case: O(1)<br>
By reference, worst case: O(1)

### Insert
Section: worst case: O(logn)<br>
Element: worst case: O(logk)<br>
New reference, worst case: O(1)

### Delete
Section: worst case: O(k + logn)<br>
Element: worst case: O(logk)<br>
Old reference, worst case: O(1)

### Explaination
This data structure uses a HashMap and a BinaryTree to organize this data wtih nodes that support traversal. The HashMap is used for all operations that are not traversal. The binary tree exists for traversal and is always balanced.
The cost of balancing this tree results in a slower worst case for element insertion and deletion, as the tree must rebalance itself. Fetches are fast as it can use section labels and then element indexes for specific items.
This performance is only from fetching the data, and not from any search performed on the data within it. Deleting a section is expensive as it requires iterating through each element and deleting any reference involving it, then rebalancing the tree.
References exist in a separate HashMap, as these are primarily used for conditions or traversal. This extra overhead is to ensure in-order traversal are not slowed down by these condition references. Since these reference do not cause rebalancing, modifications to them can be done in a fixed time. Lastly, values are default labels for elements, as elements are just sections without a label. These values are intergers, usually from 0 to a prime in a non-sequential increasing order. When an insertion occurs, a value is derrived using the previous and following values in a way to fit that element between two other elements. So, to avoid lengthy insertions from this process re-indexing will be required after reaching a threashold to create "space" between elements. An array will contain a reference to this number, so the "second" element will reference that number. Elements are not stored in an array as they can be sections and sections move in groups, as well as to not overcomplicate this any further.

### Summary
- Section labels, element ids, and element-to-element references are stored in both HashMap and BinaryTree
- Reads are fast using a HashMap
- Inserts are slower due to BinaryTree balancing and occassionally element id re-indexing
- Deletes are slow due to BinaryTree balancing and removing references.
