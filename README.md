# llama.cpp-azure

[![Azure Build Status](https://dev.azure.com/tpaviot/llama.cpp-azure/_apis/build/status/tpaviot.llama.cpp-azure?branchName=main)](https://dev.azure.com/tpaviot/llama.cpp-azure/_build?definitionId=13)

Use azure to build, test and run [llama.cpp](https://github.com/ggerganov/llama.cpp) over common LLama based HuggingFace models.

This is an ongoing work towards continuous integration of llama.cpp and/or quantized models.

**About:**

- Build llama.cpp using Blas
- Download pytorch*.bin and tokenize.model
- Export model to ggml F16
- Quantize model using Q4_0
- Test inference of quantized model
- Test perplexity computation on a small subset of wikitext-2
- Q4_0 model available for download as an azure artifact
- 3 models currently tested: [open_llama_7b_v2](https://huggingface.co/openlm-research/open_llama_7b_v2), [Vicuna-7b](https://huggingface.co/lmsys/vicuna-7b-v1.3) and [vigogne-7b-instruct](https://huggingface.co/bofenghuang/vigogne-7b-instruct)

**Known limitations/issues:**

- restricted to 7B models max (13B models consume too much storage)
