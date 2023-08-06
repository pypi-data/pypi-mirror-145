def write_brat_format_file(
    target_dir = "",
    file_name = "",
    entities = [],
    relations = [],
    ):

    with open(
        "{}/{}.ann".format(target_dir,file_name),
        "w",encoding="utf-8") as f:
        for entity in entities:
            f.write("{}\t{} {} {}\t{}\n".format(entity["entity_id"],entity["type"],entity["start"],entity["end"],entity["text"]))
        
        for r_id,rel in enumerate(relations):
            f.write("R{}\t{} Arg1:{} Arg2:{}\n".format(r_id,rel["rel_type"],rel["arg_1"],rel["arg_2"]))