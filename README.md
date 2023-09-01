# llama.cpp-azure

[![Azure Build Status](https://dev.azure.com/tpaviot/llama.cpp-azure/_apis/build/status/tpaviot.llama.cpp-azure?branchName=main)](https://dev.azure.com/tpaviot/llama.cpp-azure/_build?definitionId=13)

Use azure to build, test and run [llama.cpp](https://github.com/ggerganov/llama.cpp) master branch.

**About:**

- Build llama.cpp using Blas
- Download openlm-research/open_llama_3b_v2 hf model
- Test Export model to ggml F16
- Test q5_k_ quantization
- Download CodeLlama-7B-Python-GGUF-q4_k_m from hf/TheBloke
- Test inference of Q4_k_m quantized model
- Compute perplexity a small subset of wikitext-2
