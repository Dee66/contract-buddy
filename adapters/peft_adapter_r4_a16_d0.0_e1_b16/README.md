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
- source_sentence: 'This class provides a generic function for comparing any two tuples.

    Each instance records a list of tuple-indices (from most significant

    to least significant), and sort direction (ascending or descending) for

    each tuple-index.  The compare functions can then be used as the function

    argument to the system sort() function when a list of tuples need to be

    sorted in the instances order.'
  sentences:
  - "Type variable tuple. A specialized form of type variable that enables\nvariadic\
    \ generics.\n\nThe preferred way to construct a type variable tuple is via the\n\
    dedicated syntax for generic functions, classes, and type aliases,\nwhere a single\
    \ '*' indicates a type variable tuple::\n\n    def move_first_element_to_last[T,\
    \ *Ts](tup: tuple[T, *Ts]) -> tuple[*Ts, T]:\n        return (*tup[1:], tup[0])\n\
    \nType variables tuples can have default values:\n\n    type AliasWithDefault[*Ts\
    \ = (str, int)] = tuple[*Ts]\n\nFor compatibility with Python 3.11 and earlier,\
    \ TypeVarTuple objects\ncan also be created as follows::\n\n    Ts = TypeVarTuple('Ts')\
    \  # Can be given any name\n    DefaultTs = TypeVarTuple('Ts', default=(str, int))\n\
    \nJust as a TypeVar (type variable) is a placeholder for a single type,\na TypeVarTuple\
    \ is a placeholder for an *arbitrary* number of types. For\nexample, if we define\
    \ a generic class using a TypeVarTuple::\n\n    class C[*Ts]: ...\n\nThen we can\
    \ parameterize that class with an arbitrary number of type\narguments::\n\n  \
    \  C[int]       # Fine\n    C[int, str]  # Also fine\n    C[()]        # Even\
    \ this is fine\n\nFor more details, see PEP 646.\n\nNote that only TypeVarTuples\
    \ defined in the global scope can be\npickled."
  - 'Return an instance of the FileInput class, which can be iterated.


    The parameters are passed to the constructor of the FileInput class.

    The returned instance, in addition to being an iterator,

    keeps global state for the functions of this module,.'
  - "Loads or creates a SentenceTransformer model that can be used to map sentences\
    \ / text to embeddings.\n\nArgs:\n    model_name_or_path (str, optional): If it\
    \ is a filepath on disc, it loads the model from that path. If it is not a path,\n\
    \        it first tries to download a pre-trained SentenceTransformer model. If\
    \ that fails, tries to construct a model\n        from the Hugging Face Hub with\
    \ that name.\n    modules (Iterable[nn.Module], optional): A list of torch Modules\
    \ that should be called sequentially, can be used to create custom\n        SentenceTransformer\
    \ models from scratch.\n    device (str, optional): Device (like \"cuda\", \"\
    cpu\", \"mps\", \"npu\") that should be used for computation. If None, checks\
    \ if a GPU\n        can be used.\n    prompts (Dict[str, str], optional): A dictionary\
    \ with prompts for the model. The key is the prompt name, the value is the prompt\
    \ text.\n        The prompt text will be prepended before any text to encode.\
    \ For example:\n        `{\"query\": \"query: \", \"passage\": \"passage: \"}`\
    \ or `{\"clustering\": \"Identify the main category based on the\n        titles\
    \ in \"}`.\n    default_prompt_name (str, optional): The name of the prompt that\
    \ should be used by default. If not set,\n        no prompt will be applied.\n\
    \    similarity_fn_name (str or SimilarityFunction, optional): The name of the\
    \ similarity function to use. Valid options are \"cosine\", \"dot\",\n       \
    \ \"euclidean\", and \"manhattan\". If not set, it is automatically set to \"\
    cosine\" if `similarity` or\n        `similarity_pairwise` are called while `model.similarity_fn_name`\
    \ is still `None`.\n    cache_folder (str, optional): Path to store models. Can\
    \ also be set by the SENTENCE_TRANSFORMERS_HOME environment variable.\n    trust_remote_code\
    \ (bool, optional): Whether or not to allow for custom models defined on the Hub\
    \ in their own modeling files.\n        This option should only be set to True\
    \ for repositories you trust and in which you have read the code, as it\n    \
    \    will execute code present on the Hub on your local machine.\n    revision\
    \ (str, optional): The specific model version to use. It can be a branch name,\
    \ a tag name, or a commit id,\n        for a stored model on Hugging Face.\n \
    \   local_files_only (bool, optional): Whether or not to only look at local files\
    \ (i.e., do not try to download the model).\n    token (bool or str, optional):\
    \ Hugging Face authentication token to download private models.\n    use_auth_token\
    \ (bool or str, optional): Deprecated argument. Please use `token` instead.\n\
    \    truncate_dim (int, optional): The dimension to truncate sentence embeddings\
    \ to. `None` does no truncation. Truncation is\n        only applicable during\
    \ inference when :meth:`SentenceTransformer.encode` is called.\n    model_kwargs\
    \ (Dict[str, Any], optional): Additional model configuration parameters to be\
    \ passed to the Hugging Face Transformers model.\n        Particularly useful\
    \ options are:\n\n        - ``torch_dtype``: Override the default `torch.dtype`\
    \ and load the model under a specific `dtype`.\n          The different options\
    \ are:\n\n                1. ``torch.float16``, ``torch.bfloat16`` or ``torch.float``:\
    \ load in a specified\n                ``dtype``, ignoring the model's ``config.torch_dtype``\
    \ if one exists. If not specified - the model will\n                get loaded\
    \ in ``torch.float`` (fp32).\n\n                2. ``\"auto\"`` - A ``torch_dtype``\
    \ entry in the ``config.json`` file of the model will be\n                attempted\
    \ to be used. If this entry isn't found then next check the ``dtype`` of the first\
    \ weight in\n                the checkpoint that's of a floating point type and\
    \ use that as ``dtype``. This will load the model\n                using the ``dtype``\
    \ it was saved in at the end of the training. It can't be used as an indicator\
    \ of how\n                the model was trained. Since it could be trained in\
    \ one of half precision dtypes, but saved in fp32.\n        - ``attn_implementation``:\
    \ The attention implementation to use in the model (if relevant). Can be any of\n\
    \          `\"eager\"` (manual implementation of the attention), `\"sdpa\"` (using\
    \ `F.scaled_dot_product_attention\n          <https://pytorch.org/docs/master/generated/torch.nn.functional.scaled_dot_product_attention.html>`_),\n\
    \          or `\"flash_attention_2\"` (using `Dao-AILab/flash-attention <https://github.com/Dao-AILab/flash-attention>`_).\n\
    \          By default, if available, SDPA will be used for torch>=2.1.1. The default\
    \ is otherwise the manual `\"eager\"`\n          implementation.\n        - ``provider``:\
    \ If backend is \"onnx\", this is the provider to use for inference, for example\
    \ \"CPUExecutionProvider\",\n          \"CUDAExecutionProvider\", etc. See https://onnxruntime.ai/docs/execution-providers/\
    \ for all ONNX execution providers.\n        - ``file_name``: If backend is \"\
    onnx\" or \"openvino\", this is the file name to load, useful for loading optimized\n\
    \          or quantized ONNX or OpenVINO models.\n        - ``export``: If backend\
    \ is \"onnx\" or \"openvino\", then this is a boolean flag specifying whether\
    \ this model should\n          be exported to the backend. If not specified, the\
    \ model will be exported only if the model repository or directory\n         \
    \ does not already contain an exported model.\n\n        See the `PreTrainedModel.from_pretrained\n\
    \        <https://huggingface.co/docs/transformers/en/main_classes/model#transformers.PreTrainedModel.from_pretrained>`_\n\
    \        documentation for more details.\n    tokenizer_kwargs (Dict[str, Any],\
    \ optional): Additional tokenizer configuration parameters to be passed to the\
    \ Hugging Face Transformers tokenizer.\n        See the `AutoTokenizer.from_pretrained\n\
    \        <https://huggingface.co/docs/transformers/en/model_doc/auto#transformers.AutoTokenizer.from_pretrained>`_\n\
    \        documentation for more details.\n    config_kwargs (Dict[str, Any], optional):\
    \ Additional model configuration parameters to be passed to the Hugging Face Transformers\
    \ config.\n        See the `AutoConfig.from_pretrained\n        <https://huggingface.co/docs/transformers/en/model_doc/auto#transformers.AutoConfig.from_pretrained>`_\n\
    \        documentation for more details.\n    model_card_data (:class:`~sentence_transformers.model_card.SentenceTransformerModelCardData`,\
    \ optional): A model\n        card data object that contains information about\
    \ the model. This is used to generate a model card when saving\n        the model.\
    \ If not set, a default model card data object is created.\n    backend (str):\
    \ The backend to use for inference. Can be one of \"torch\" (default), \"onnx\"\
    , or \"openvino\".\n        See https://sbert.net/docs/sentence_transformer/usage/efficiency.html\
    \ for benchmarking information\n        on the different backends.\n\nExample:\n\
    \    ::\n\n        from sentence_transformers import SentenceTransformer\n\n \
    \       # Load a pre-trained SentenceTransformer model\n        model = SentenceTransformer('all-mpnet-base-v2')\n\
    \n        # Encode some texts\n        sentences = [\n            \"The weather\
    \ is lovely today.\",\n            \"It's so sunny outside!\",\n            \"\
    He drove to the stadium.\",\n        ]\n        embeddings = model.encode(sentences)\n\
    \        print(embeddings.shape)\n        # (3, 768)\n\n        # Get the similarity\
    \ scores between all sentences\n        similarities = model.similarity(embeddings,\
    \ embeddings)\n        print(similarities)\n        # tensor([[1.0000, 0.6817,\
    \ 0.0492],\n        #         [0.6817, 1.0000, 0.0421],\n        #         [0.0492,\
    \ 0.0421, 1.0000]])"
- source_sentence: 'Common operations on Posix pathnames.


    Instead of importing this module directly, import os and refer to

    this module as os.path.  The "os.path" name is an alias for this

    module on Posix systems; on other systems (e.g. Windows),

    os.path provides the same operations in a manner specific to that

    platform, and is an alias to another module (e.g. ntpath).


    Some of this can actually be useful on non-Posix systems too, e.g.

    for manipulation of the pathname component of URLs.'
  sentences:
  - 'Set or return backgroundcolor of the TurtleScreen.


    Arguments (if given): a color string or three numbers

    in the range 0..colormode or a 3-tuple of such numbers.


    Example:

    >>> bgcolor("orange")

    >>> bgcolor()

    ''orange''

    >>> bgcolor(0.5,0,0.5)

    >>> bgcolor()

    ''#800080'''
  - A base class for ExitStack and AsyncExitStack.
  - A string substitution required a setting which was not available.
- source_sentence: DecimalTuple(sign, digits, exponent)
  sentences:
  - 'Tests if the type is a :class:`typing.ForwardRef`. Examples::


    u = Union["Milk", Way]

    args = get_args(u)

    is_forward_ref(args[0]) == True

    is_forward_ref(args[1]) == False'
  - 'Open a file in read only mode using the encoding detected by

    detect_encoding().'
  - Prints multi-column formatting for year calendars
- source_sentence: String that doesn't quote its repr.
  sentences:
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
  - Clear the cache entirely.
  - "Exception raised when an error occurs while attempting to\ncompile the file.\n\
    \nTo raise this exception, use\n\n    raise PyCompileError(exc_type,exc_value,file[,msg])\n\
    \nwhere\n\n    exc_type:   exception type to be used in error message\n      \
    \          type name can be accesses as class variable\n                'exc_type_name'\n\
    \n    exc_value:  exception value to be used in error message\n              \
    \  can be accesses as class variable 'exc_value'\n\n    file:       name of file\
    \ being compiled to be used in error message\n                can be accesses\
    \ as class variable 'file'\n\n    msg:        string message to be written as\
    \ error message\n                If no value is given, a default exception message\
    \ will be\n                given, consistent with 'standard' py_compile output.\n\
    \                message (or default) can be accesses as class variable\n    \
    \            'msg'"
- source_sentence: 'The `winxpgui` module is obsolete and has been completely replaced
    by `win32gui` and `win32console.GetConsoleWindow`. Use those instead. '
  sentences:
  - 'Extract the raw traceback from the current stack frame.


    The return value has the same format as for extract_tb().  The

    optional ''f'' and ''limit'' arguments have the same meaning as for

    print_stack().  Each item in the list is a quadruple (filename,

    line number, function name, text), and the entries are in order

    from oldest to newest stack frame.'
  - 'FileInput([files[, inplace[, backup]]], *, mode=None, openhook=None)


    Class FileInput is the implementation of the module; its methods

    filename(), lineno(), fileline(), isfirstline(), isstdin(), fileno(),

    nextfile() and close() correspond to the functions of the same name

    in the module.

    In addition it has a readline() method which returns the next

    input line, and a __getitem__() method which implements the

    sequence behavior. The sequence must be accessed in strictly

    sequential order; random access and readline() cannot be mixed.'
  - "Abstract base class for the individual library controllers\n\nA library controller\
    \ must expose the following class attributes:\n    - user_api : str\n        Usually\
    \ the name of the library or generic specification the library\n        implements,\
    \ e.g. \"blas\" is a specification with different implementations.\n    - internal_api\
    \ : str\n        Usually the name of the library or concrete implementation of\
    \ some\n        specification, e.g. \"openblas\" is an implementation of the \"\
    blas\"\n        specification.\n    - filename_prefixes : tuple\n        Possible\
    \ prefixes of the shared library's filename that allow to\n        identify the\
    \ library. e.g. \"libopenblas\" for libopenblas.so.\n\nand implement the following\
    \ methods: `get_num_threads`, `set_num_threads` and\n`get_version`.\n\nThreadpoolctl\
    \ loops through all the loaded shared libraries and tries to match\nthe filename\
    \ of each library with the `filename_prefixes`. If a match is found, a\ncontroller\
    \ is instantiated and a handler to the library is stored in the `dynlib`\nattribute\
    \ as a `ctypes.CDLL` object. It can be used to access the necessary symbols\n\
    of the shared library to implement the above methods.\n\nThe following information\
    \ will be exposed in the info dictionary:\n  - user_api : standardized API, if\
    \ any, or a copy of internal_api.\n  - internal_api : implementation-specific\
    \ API.\n  - num_threads : the current thread limit.\n  - prefix : prefix of the\
    \ shared library's filename.\n  - filepath : path to the loaded shared library.\n\
    \  - version : version of the library (if available).\n\nIn addition, each library\
    \ controller may expose internal API specific entries. They\nmust be set as attributes\
    \ in the `set_additional_attributes` method."
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
    'The `winxpgui` module is obsolete and has been completely replaced by `win32gui` and `win32console.GetConsoleWindow`. Use those instead. ',
    'Abstract base class for the individual library controllers\n\nA library controller must expose the following class attributes:\n    - user_api : str\n        Usually the name of the library or generic specification the library\n        implements, e.g. "blas" is a specification with different implementations.\n    - internal_api : str\n        Usually the name of the library or concrete implementation of some\n        specification, e.g. "openblas" is an implementation of the "blas"\n        specification.\n    - filename_prefixes : tuple\n        Possible prefixes of the shared library\'s filename that allow to\n        identify the library. e.g. "libopenblas" for libopenblas.so.\n\nand implement the following methods: `get_num_threads`, `set_num_threads` and\n`get_version`.\n\nThreadpoolctl loops through all the loaded shared libraries and tries to match\nthe filename of each library with the `filename_prefixes`. If a match is found, a\ncontroller is instantiated and a handler to the library is stored in the `dynlib`\nattribute as a `ctypes.CDLL` object. It can be used to access the necessary symbols\nof the shared library to implement the above methods.\n\nThe following information will be exposed in the info dictionary:\n  - user_api : standardized API, if any, or a copy of internal_api.\n  - internal_api : implementation-specific API.\n  - num_threads : the current thread limit.\n  - prefix : prefix of the shared library\'s filename.\n  - filepath : path to the loaded shared library.\n  - version : version of the library (if available).\n\nIn addition, each library controller may expose internal API specific entries. They\nmust be set as attributes in the `set_additional_attributes` method.',
    'FileInput([files[, inplace[, backup]]], *, mode=None, openhook=None)\n\nClass FileInput is the implementation of the module; its methods\nfilename(), lineno(), fileline(), isfirstline(), isstdin(), fileno(),\nnextfile() and close() correspond to the functions of the same name\nin the module.\nIn addition it has a readline() method which returns the next\ninput line, and a __getitem__() method which implements the\nsequence behavior. The sequence must be accessed in strictly\nsequential order; random access and readline() cannot be mixed.',
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
  | sentence_0                                                                                                                                                                                                                                     | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
  |:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>Will be raised in TurtleScreen.update, if _RUNNING becomes False.<br><br>This stops execution of a turtle graphics script.<br>Main purpose: use in the Demo-Viewer turtle.Demo.py.</code>                                                | <code>Connect to *address* and return the socket object.<br><br>Convenience function.  Connect to *address* (a 2-tuple ``(host,<br>port)``) and return the socket object.  Passing the optional<br>*timeout* parameter will set the timeout on the socket instance<br>before attempting to connect.  If no *timeout* is supplied, the<br>global default timeout setting returned by :func:`getdefaulttimeout`<br>is used.  If *source_address* is set it must be a tuple of (host, port)<br>for the socket to bind as a source address before making the connection.<br>A host of '' or port 0 tells the OS to use the default. When a connection<br>cannot be created, raises the last error if *all_errors* is False,<br>and an ExceptionGroup of all errors if *all_errors* is True.</code> |
  | <code>AsyncFunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns, string? type_comment, type_param* type_params)</code>                                                                                 | <code>Return the number of Thread objects currently alive.<br><br>This function is deprecated, use active_count() instead.</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
  | <code>Compress a block of data.<br><br>Refer to LZMACompressor's docstring for a description of the<br>optional arguments *format*, *check*, *preset* and *filters*.<br><br>For incremental compression, use an LZMACompressor instead.</code> | <code>AsyncFunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns, string? type_comment, type_param* type_params)</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
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