# llama.cpp-azure

[![Azure Build Status](https://dev.azure.com/tpaviot/llama.cpp-azure/_apis/build/status/tpaviot.llama.cpp-azure?branchName=main)](https://dev.azure.com/tpaviot/llama.cpp-azure/_build?definitionId=13)

Use azure to build, test and run [llama.cpp](https://github.com/ggerganov/llama.cpp). This is an ongoing work towards continuous integration for llama.cpp.

**About:**

- Build llama.cpp using Blas
- Download pytorch*.bin and tokenize.model
- Test Export model to ggml F16
- Test Q4_0 quantization
- Test inference of Q4_0 quantized model
- Test perplexity computation on a small subset of wikitext-2
