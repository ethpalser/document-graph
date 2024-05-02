# Document Graph
A TreeMap with keys for nodes comprised of a label and value. Each label defines a subtree representing a document section. Each value defines a strict order of where each item is in relation to another within the section. Nodes within the tree can reference any other node to relate information, or to override traversal. Default traversal will iterate through the tree using in-order traversal.

## Purpose
- Document sections are grouped together, so relationships are local.
- Document sections can be returned together, so relationships can be structured.
- Document sections know the next section, as sections are ordered.
- Section elements can be any data, including empty, but not null.
- Section elements are ordered.
- Section elements can be sections (a subsection), and the document is a singular section at the root.
- Section elements can be a reference to another section's elements, this reference can be traversed to, and this reference can be labeled.
- Traversal is expected to be in-order by section and element, and will ignore traversing to references by default.
- Traversal can break order using a reference and even loop if allowed.
- Traversal can be conditional, and conditional elements can be skipped.
- Conditions are functions-as-elements that are referenced by elements, and only return true or false.
- Functions are skipped if not referenced.
- Functions can return a reference label, and this can be navigated to.
- Functions can mutate data, but only built-in functions.

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
References exist in a separate HashMap, as these are primarily used for conditions or traversal. This extra overhead is to ensure in-order traversal are not slowed down by these condition references. Since these reference do not cause rebalancing, modifications to them can be done in a fixed time. Lastly, values are default labels for elements, as elements are just sections without a label. These values are unique hash ids. An array will contain a reference to this id, so the "second" element will reference that id. Elements are not stored in an array as they can be sections and sections move in groups, as well as to not overcomplicate this any further.

### Summary
- Section labels, element ids, and element-to-element references are stored in both HashMap and BinaryTree
- Reads are fast using a HashMap
- Inserts are slower due to BinaryTree balancing
- Deletes are slow due to BinaryTree balancing and removing references
- Ideal use is to process a document into this data structure once, and then only traverse and fetch.

## Considerations
### Lazy File Reading
What if this data structure stored references to start and end bytes of a document? This data structure could retain a reference to that file and only read from those sections when necessary. The only problem is the overhead for starting and stopping the i/o channel, and error handling. Also, what if the file is too large to store in memory? It may not be possible to divide the document into pieces for this data structure. This data structure could be setup to store that data, along with references. Whenever data becomes unimportant it can be removed from this structure. A cache could exist between this and the file and fetch potentially important data whenever i/o is performed.<br>
Although this is a consideration, if file access is frequent it would be better to use a more lightweight data structure, as it is unlikely you need to perform extensive fetching and traversal. If traversal is important but the content is being inserted and/or removed dynamically during traversal, then another data structure would be useful to manage multiple documents graphs and have the frequently changed areas be treated as their own document. If the document is actually all word file content across a directory, that content does not change, and that content needs to be aggregated and traversed, then a lazy approach with this structure would be effective.

### Redundancy
What if this data structure has data within it become corrupted? The process of generating this structure is expensive, so needing to redo this operation will impact performance. If traversal is not needed then any other in-memory database would be better. Otherwise, a system could use this structure with redundancy.

### Encryption
What if this data is being traversed through by multiple streams, but access is only allowed for one of them? This may be a case for conditions, but that could cause tremendous bloat if a condition needs to be created for every element. It could be possible to encrypt the data before it is added, and only users with a key to decrypt it can do anything useful with it. This effectively makes this data structure a block-chain. What if viruses, hacks and any other unwanted reader tried reading the memory used by this data structure? If the programming language does nothing then we can assume that it can read that data. Built-in encryption will help with security once it is stored inside the data structure, but nothing as the document is being processed. This structure could be setup with an encrypted stream that data can be fed into, in chunks.

### Constraints
While the intent is not to make another in-memory database, there may be situations when an insertion is required that must meet some constraint. What if the data must be a certain type, or that data must be a certain value? Without constraints a function would only limit *access* to an element, but with constraints insertion can be limited. A type constraint would be another function stored under a special constraint section that is referenced by that element or section. A value constraint is similar, but matching on values. Type constraints could be provided, as there is a finite amount of primitive types, and anything else can be checked by providing that class. Other constraints could be supported, but the developer would have to construct that function.  Value contraints with encrpytion included would only be able to support value matching, as it would check encrypted values instead of decrypting the data. Also, hypoethetically if you wanted to create a section as a "database" with subsections as "tables" and further subsections with "fields" with elements of any value, then please use an SQL or NoSQL database, as this would be better supported there.

## Concerns
### Malicous Use of Functions
Conditions, callback functions that return true or false, and routers, callback functions that return a label and possibly an id, are intended as I plan on using this structure with this level of control for traversal. However, these functions can be defined however the developer wants. This means that the function can use anything available to it at runtime. For example, the function is a closure containing an object that creates a backdoor, and whenever this function is used that backdoor exposes the data. This could potentially bypass encrpytion. It could even identify certain records if it reverses the encryption, and then mutate it. To avoid this, a structure may be enforced to severely limit how these callback functions are built.

### Injection Attacks
This is about escaping data, such as a string, and injecting code. This depends on the programming language and structures underneath. If the tools used to setup and use this data structure are already not preventing injection this must be prevented.

### Infinite Loops
Loops are already expected, but what if it is a reference that references another reference that then refrences the first? If the traversal function went as deep as the refrence would go, this would never end. This structure could be setup to only traverse once in a reference, and any attempt by a developer to go as deep as the reference would go is at their own risk. Cycle-safety is undesireable, as it adds a large cost to insertion for what is a developer error.
