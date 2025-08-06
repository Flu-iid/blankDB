# Introduction

experimental DBMS for academic purposes with slight interest in microkernel architecture written in python.

This project will have a simple storage engine, query parser, transaction manager and a indexing system and other parts specified in [Structure](#structure).

# Structure

```
[Handler] ---> [Parser]
    ^                 \
     \                 \
      \                 \
       \                 \
        \                 v
        [View]<---------[Engine] <----> [Indexing]

```

```mermaid
graph LR
    U[User] --> H[Handler]
    H -->|Query| P[Parser]
    P -->|Execution List| E[Engine]
    E -->|Raw Data| V[View]
    V -->|Formatted Result| H
    H --> U

    subgraph Parser Internals
        P --> A[Analyzer]
        P --> T[Tokenizer]
        P --> PP[Precedence Parser]
    end

    subgraph Storage
        E --> T1[Table1.txt]
        E --> T2[Table2.txt]
    end
```

As it can be seen a cyclical structure which move around [Handler](#handler) which handles user requests
and [Engine] that writes and reads data onto storage.

# Handler

Handler is the part that is responsible for receiving, processing, and responding to user requests. and presenting responses and results accoring to structures of view module.

# Parser

[parser.md](./src/parser/parser.md)

# Engine

# View
