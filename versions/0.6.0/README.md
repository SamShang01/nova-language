# Nova Programming Language - Version 0.6.0

Nova is a modern, high-performance programming language designed for simplicity and efficiency.

## Features

- Clean, Python-like syntax
- Strong type system
- Virtual machine with JIT compilation
- Standard library with basic modules
- Version management system

## What's New in 0.6.0

### Major Features
- **Anonymous data structures** (struct, union, enum)
- **Improved parser** for complex expressions
- **Support for `name:value` syntax** for keyword arguments
- **Enhanced member access parsing**

### Bug Fixes
- Parser error when handling complex expressions in struct methods
- Class system parameter count checking
- Minor bug fixes in virtual machine

### Improvements
- Optimized parser performance
- Improved error messages
- Enhanced semantic analysis for type checking

## Example: Anonymous Struct

```nova
// Define an anonymous struct
let point = struct {
    x: int;
    y: int;
};

// Create an instance
let p = point(x=1, y=2);

// Access members
print(p.x, p.y);
```

## Installation

```bash
# From source
python setup.py install

# Using script.py
python script.py install --version=0.6.0
```

## Usage

```bash
# Run Nova REPL
nova

# Run Nova script
nova script.nova
```

## Documentation

For more information, please refer to the official documentation.