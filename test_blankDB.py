# ihandler
from src.handler.ihandler import handler

# iparser
from src.parser.iparser import tokenizer, pair_maker, pair_sort

# iengine
from src.engine.iengine import engine

while not handler.exit_signal:
    handler.get_input()
    bool_value, output_analyzer = handler.get_output()
    if not bool_value:
        break
    print("acceptable:", bool_value)
    print("analyzer:", output_analyzer)
    tokenizer.input_syntax_list(output_analyzer)
    output_tokenizer = tokenizer.tokenize()
    print("tokenizer:", output_tokenizer)
    precedence_list = []
    for i, e in enumerate(output_tokenizer):
        output_pparser = pair_maker(e)
        ordered_output_pparser = pair_sort(output_pparser)
        precedence_list.append(ordered_output_pparser)
        print("Precedence Parser:", i, ordered_output_pparser)
    [precedence_list] = precedence_list
    print("precedence list:", precedence_list)
    engine_process = engine(precedence_list=precedence_list)
    print("mapped_list:", engine_process._mapped_list)
    print("memory:", engine_process._memory)
    result = engine_process.result()
    print("result:", result)


# table name: dummy
# id | a
# ----|------
# 0  | helloworld
# 1  |


# try these queries:
# select id from dummy
# select a from dummy
