---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:100
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-MiniLM-L6-v2
widget:
- source_sentence: '>>> import io

    >>> read_floatnl(io.BytesIO(b"-1.25\n6"))

    -1.25'
  sentences:
  - A string substitution required a setting which was not available.
  - 'zipimporter(archivepath) -> zipimporter object


    Create a new zipimporter instance. ''archivepath'' must be a path to

    a zipfile, or to a specific path inside a zipfile. For example, it can be

    ''/tmp/myimport.zip'', or ''/tmp/myimport.zip/mydirectory'', if mydirectory is
    a

    valid directory inside the archive.


    ''ZipImportError is raised if ''archivepath'' doesn''t point to a valid Zip

    archive.


    The ''archive'' attribute of zipimporter objects contains the name of the

    zipfile targeted.'
  - '>>> import io

    >>> read_string4(io.BytesIO(b"\x00\x00\x00\x00abc"))

    ''''

    >>> read_string4(io.BytesIO(b"\x03\x00\x00\x00abcdef"))

    ''abc''

    >>> read_string4(io.BytesIO(b"\x00\x00\x00\x03abcdef"))

    Traceback (most recent call last):

    ...

    ValueError: expected 50331648 bytes in a string4, but only 6 remain'
- source_sentence: 'Register the core Python file extensions.


    defPyIcon -- The default icon to use for .py files, in ''fname,offset'' format.

    defPycIcon -- The default icon to use for .pyc files, in ''fname,offset'' format.

    runCommand -- The command line to use for running .py files'
  sentences:
  - 'StreamReaderWriter instances allow wrapping streams which

    work in both read and write modes.


    The design is such that one can use the factory functions

    returned by the codec.lookup() function to construct the

    instance.'
  - "Abstract base class that provides __repr__.\n\nThe __repr__ method returns a\
    \ string in the format::\n    ClassName(attr=name, attr=name, ...)\nThe attributes\
    \ are determined either by a class-level attribute,\n'_kwarg_names', or by inspecting\
    \ the instance __dict__."
  - '>>> import io

    >>> read_long4(io.BytesIO(b"\x02\x00\x00\x00\xff\x00"))

    255

    >>> read_long4(io.BytesIO(b"\x02\x00\x00\x00\xff\x7f"))

    32767

    >>> read_long4(io.BytesIO(b"\x02\x00\x00\x00\x00\xff"))

    -256

    >>> read_long4(io.BytesIO(b"\x02\x00\x00\x00\x00\x80"))

    -32768

    >>> read_long1(io.BytesIO(b"\x00\x00\x00\x00"))

    0'
- source_sentence: 'In case filepath is a symlink, follow it until a

    real file is reached.'
  sentences:
  - 'Instances of this class behave much like the built-in compile

    function, but if one is used to compile text containing a future

    statement, it "remembers" and compiles all subsequent program texts

    with the statement in force.'
  - 'int([x]) -> integer

    int(x, base=10) -> integer


    Convert a number or string to an integer, or return 0 if no arguments

    are given.  If x is a number, return x.__int__().  For floating-point

    numbers, this truncates towards zero.


    If x is not a number or if base is given, then x must be a string,

    bytes, or bytearray instance representing an integer literal in the

    given base.  The literal can be preceded by ''+'' or ''-'' and be surrounded

    by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

    Base 0 means to interpret the base from the string as an integer literal.

    >>> int(''0b100'', base=0)

    4'
  - A private marker - used in Parameter & Signature.
- source_sentence: Quote a single character.
  sentences:
  - 'Raised when a registry operation with the archiving

    and unpacking registries fails'
  - "Statically assert that a line of code is unreachable.\n\nExample::\n\n    def\
    \ int_or_str(arg: int | str) -> None:\n        match arg:\n            case int():\n\
    \                print(\"It's an int\")\n            case str():\n           \
    \     print(\"It's a str\")\n            case _:\n                assert_never(arg)\n\
    \nIf a type checker finds that a call to assert_never() is\nreachable, it will\
    \ emit an error.\n\nAt runtime, this throws an exception when called."
  - Quote a single character.
- source_sentence: String that doesn't quote its repr.
  sentences:
  - "ASN.1 object identifier lookup\n    "
  - "Represent an address as 4 packed bytes in network (big-endian) order.\n\nArgs:\n\
    \    address: An integer representation of an IPv4 IP address.\n\nReturns:\n \
    \   The integer address packed as 4 bytes in network (big-endian) order.\n\nRaises:\n\
    \    ValueError: If the integer is negative or too large to be an\n      IPv4\
    \ IP address."
  - Clear the cache entirely.
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/all-MiniLM-L6-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <!-- at revision c9745ed1d9f207416be6d2e6f8de32d1f16199bf -->
- **Maximum Sequence Length:** 256 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/UKPLab/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'max_seq_length': 256, 'do_lower_case': False}) with Transformer model: PeftModelForFeatureExtraction 
  (1): Pooling({'word_embedding_dimension': 384, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
  (2): Normalize()
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    "String that doesn't quote its repr.",
    'Clear the cache entirely.',
    'Represent an address as 4 packed bytes in network (big-endian) order.\n\nArgs:\n    address: An integer representation of an IPv4 IP address.\n\nReturns:\n    The integer address packed as 4 bytes in network (big-endian) order.\n\nRaises:\n    ValueError: If the integer is negative or too large to be an\n      IPv4 IP address.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities.shape)
# [3, 3]
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 100 training samples
* Columns: <code>sentence_0</code> and <code>sentence_1</code>
* Approximate statistics based on the first 100 samples:
  |         | sentence_0                                                                         | sentence_1                                                                         |
  |:--------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
  | type    | string                                                                             | string                                                                             |
  | details | <ul><li>min: 5 tokens</li><li>mean: 62.12 tokens</li><li>max: 256 tokens</li></ul> | <ul><li>min: 6 tokens</li><li>mean: 80.42 tokens</li><li>max: 256 tokens</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
  |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>Compress a block of data.<br><br>Refer to LZMACompressor's docstring for a description of the<br>optional arguments *format*, *check*, *preset* and *filters*.<br><br>For incremental compression, use an LZMACompressor instead.</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | <code>AsyncFunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns, string? type_comment, type_param* type_params)</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
  | <code>Guess the type of a file based on its URL.<br><br>Return value is a tuple (type, encoding) where type is None if the<br>type can't be guessed (no or unknown suffix) or a string of the<br>form type/subtype, usable for a MIME Content-type header; and<br>encoding is None for no encoding or the name of the program used<br>to encode (e.g. compress or gzip).  The mappings are table<br>driven.  Encoding suffixes are case sensitive; type suffixes are<br>first tried case sensitive, then case insensitive.<br><br>The suffixes .tgz, .taz and .tz (case sensitive!) are all mapped<br>to ".tar.gz".  (This is table-driven too, using the dictionary<br>suffix_map).<br><br>Optional `strict' argument when false adds a bunch of commonly found, but<br>non-standard types.</code> | <code>zipimporter(archivepath) -> zipimporter object<br><br>Create a new zipimporter instance. 'archivepath' must be a path to<br>a zipfile, or to a specific path inside a zipfile. For example, it can be<br>'/tmp/myimport.zip', or '/tmp/myimport.zip/mydirectory', if mydirectory is a<br>valid directory inside the archive.<br><br>'ZipImportError is raised if 'archivepath' doesn't point to a valid Zip<br>archive.<br><br>The 'archive' attribute of zipimporter objects contains the name of the<br>zipfile targeted.</code>                                                                                                                                                                                                                                                                                                                                                                                                                                      |
  | <code>Text wrapping and filling.</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | <code>Get type arguments with all substitutions performed. For unions,<br>basic simplifications used by Union constructor are performed.<br>On versions prior to 3.7 if `evaluate` is False (default),<br>report result as nested tuple, this matches<br>the internal representation of types. If `evaluate` is True<br>(or if Python version is 3.7 or greater), then all<br>type parameters are applied (this could be time and memory expensive).<br>Examples::<br><br>    get_args(int) == ()<br>    get_args(Union[int, Union[T, int], str][int]) == (int, str)<br>    get_args(Union[int, Tuple[T, int]][str]) == (int, (Tuple, str, int))<br><br>    get_args(Union[int, Tuple[T, int]][str], evaluate=True) ==                  (int, Tuple[str, int])<br>    get_args(Dict[int, Tuple[T, T]][Optional[int]], evaluate=True) ==                  (int, Tuple[Optional[int], Optional[int]])<br>    get_args(Callable[[], T][int], evaluate=True) == ([], int,)</code> |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim"
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `num_train_epochs`: 1
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `overwrite_output_dir`: False
- `do_predict`: False
- `eval_strategy`: no
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `per_gpu_train_batch_size`: None
- `per_gpu_eval_batch_size`: None
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 1
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: {}
- `warmup_ratio`: 0.0
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `save_safetensors`: True
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `no_cuda`: False
- `use_cpu`: False
- `use_mps_device`: False
- `seed`: 42
- `data_seed`: None
- `jit_mode_eval`: False
- `use_ipex`: False
- `bf16`: False
- `fp16`: False
- `fp16_opt_level`: O1
- `half_precision_backend`: auto
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: 0
- `ddp_backend`: None
- `tpu_num_cores`: None
- `tpu_metrics_debug`: False
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `past_index`: -1
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_min_num_params`: 0
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `fsdp_transformer_layer_cls_to_wrap`: None
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch
- `optim_args`: None
- `adafactor`: False
- `group_by_length`: False
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `use_legacy_prediction_loop`: False
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_inputs_for_metrics`: False
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `fp16_backend`: auto
- `push_to_hub_model_id`: None
- `push_to_hub_organization`: None
- `mp_parameters`: 
- `auto_find_batch_size`: False
- `full_determinism`: False
- `torchdynamo`: None
- `ray_scope`: last
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_tokens_per_second`: False
- `include_num_input_tokens_seen`: False
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: False
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin

</details>

### Framework Versions
- Python: 3.13.3
- Sentence Transformers: 4.1.0
- Transformers: 4.52.4
- PyTorch: 2.7.1+cpu
- Accelerate: 1.7.0
- Datasets: 3.6.0
- Tokenizers: 0.21.1

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{henderson2017efficient,
    title={Efficient Natural Language Response Suggestion for Smart Reply},
    author={Matthew Henderson and Rami Al-Rfou and Brian Strope and Yun-hsuan Sung and Laszlo Lukacs and Ruiqi Guo and Sanjiv Kumar and Balint Miklos and Ray Kurzweil},
    year={2017},
    eprint={1705.00652},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->