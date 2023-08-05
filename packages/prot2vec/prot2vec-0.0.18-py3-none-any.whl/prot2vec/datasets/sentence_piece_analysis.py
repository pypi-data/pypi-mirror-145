import numpy as np
from copy import deepcopy


def vectorize_seq(seq, max_len, tokenizer):
    inputs = tokenizer.encode_plus(
        seq,
        add_special_tokens=True,
        max_length=max_len,
        padding="max_length",
        truncation=True,
    )
    input_ids = inputs["input_ids"]
    return input_ids


def vectorize_batch(batch, mask_position, max_len, tokenizer):
    tokens_in = []
    domain_linker = list()

    for (t_in,), dom_lin in batch:
        t_in = vectorize_seq(t_in, max_len, tokenizer)

        tokens_in.append(t_in)
        domain_linker.append(dom_lin)

    tokens_in = np.array(tokens_in, dtype=np.int32)
    mask = np.zeros(tokens_in.shape)

    tokens_masked = deepcopy(tokens_in)

    masked_indexes = [[mask_position] for _ in range(tokens_in.shape[0])]
    masked_coord_y = np.concatenate(masked_indexes)
    masked_coord_x = np.repeat(np.arange(tokens_in.shape[0]), 1)

    tokens_masked[masked_coord_x, masked_coord_y] = tokenizer.mask_token_id

    mask[masked_coord_x, masked_coord_y] = 1

    return tokens_masked, tokens_in, mask, domain_linker
