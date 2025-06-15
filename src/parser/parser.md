# Parser

The parser Ideal structure has 3 parts;

1. Analyzer: which gives [Hanlder](../handler/handler.md) a lead to how to apply rules on syntax like avoid charecters or apply seperators correctly.

2. Tokenizer: translates each part of syntax into correct tokens.

3. parser: puts each token in repsected order and wraps them for engine to execute (ofcourse transaction step most
   be implemented as well but thats for later stages)

## Analyzer

Checks lexicography rules and splits the syntax to elements ready be tokenizer.

we keep analyzer in parser structure since the lex rules are mostly related to how
tokenizer and parser work. so in order to keep them modular, handler has to use whatever the parser's analyzer provides.

Analyzer uses 3 sets to apply these rules.

- **avoid_set**: with `avoid_set` handler can check for restrictions set by rules on syntax
  (ideally `avoid_set` is empty)

- **sep_set**: with `sep_set` handler can check how to seperate syntax into sentences for better
  handling by tokenizer.

- **end_set**: with `end_set` handler can know when to end a sentence.

## Tokenizer

## parser
