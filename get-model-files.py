# tpaviot@gmail.com

import argparse
import hashlib
import os
import subprocess

import requests
from bs4 import BeautifulSoup, SoupStrainer


def runcmd(cmd, verbose=False):
    print(f"{cmd}")
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)


def sha256sum(file):
    """compute sha256 sum, function from
    https://github.com/ggerganov/llama.cpp/blob/master/scripts/verify-checksum-models.py
    """
    block_size = 16 * 1024 * 1024  # 16 MB block size
    b = bytearray(block_size)
    file_hash = hashlib.sha256()
    mv = memoryview(b)
    with open(file, "rb", buffering=0) as f:
        while True:
            n = f.readinto(mv)
            if not n:
                break
            file_hash.update(mv[:n])

    return file_hash.hexdigest()


def download(model_path):
    base_url = f"https://huggingface.co/{model_path}"
    page = requests.get(f"{base_url}/tree/main", timeout=5)

    # get pytorch files and tokenizer.model paths
    pytorch_model_bins = []
    tokenizer_dot_model = None
    file_sha256_map = {}

    for link in BeautifulSoup(
        page.text, parse_only=SoupStrainer("a"), features="html.parser"
    ):
        if link.has_attr("href"):  # it's a link
            if "pytorch_model" in link.text and ".bin." not in link.text:
                # TODO: use a regex
                part_1 = link.text.split("pytorch_model")[1]
                part_2 = part_1.split(".bin")[0]
                pytorch_model_bins.append(f"pytorch_model{part_2}.bin")
            if "tokenizer.model" in link.text:
                tokenizer_dot_model = link.text.strip()

    # download each .bin file
    for pytorch_model_bin in pytorch_model_bins:
        runcmd(f"wget -P ./model {base_url}/resolve/main/{pytorch_model_bin}")
        if not os.path.isfile(f"./model/{pytorch_model_bin}"):
            raise IOError(f"{pytorch_model_bin} download error.")

    # and download the tokenizer.model
    runcmd(f"wget -P ./model {base_url}/resolve/main/{tokenizer_dot_model}")
    if not os.path.isfile(f"./model/{tokenizer_dot_model}"):
        raise IOError(f"{tokenizer_dot_model} download error.")

    # get the expected checksums as well
    for pytorch_model_bin in pytorch_model_bins:
        page = requests.get(f"{base_url}/blob/main/{pytorch_model_bin}", timeout=5)
        if "SHA256" not in page.text:
            raise AssertionError(f"No SHA256 found for file {pytorch_model_bin}")
        expected_checksum = (
            page.text.split("SHA256:</strong>")[1].split("</li>")[0].strip()
        )
        file_sha256_map[f"./model/{pytorch_model_bin}"] = expected_checksum
    page = requests.get(f"{base_url}/blob/main/{tokenizer_dot_model}", timeout=5)
    if "SHA256" not in page.text:
        raise AssertionError(f"No SHA256 found for file {tokenizer_dot_model}")
    expected_checksum = page.text.split("SHA256:</strong>")[1].split("</li>")[0].strip()
    file_sha256_map[f"./model/{tokenizer_dot_model}"] = expected_checksum

    return file_sha256_map


if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()  # description='Example argument parser')
    parser.add_argument("--model_path", "-m", required = True, help="HuggingFace model path")
    args = parser.parse_args()
    model_path = args.model_path
    # download files
    checksum_dict = download(model_path)
    # check sha256 sum for each file
    print("Check sha256 sums ...", end="")
    for file_path, expected_sha256_sum in checksum_dict.items():
        computed_sha256_sum = sha256sum(file_path)
        if computed_sha256_sum != expected_sha256_sum:
            raise AssertionError(f"sha256 checksum error for {file_path}")
    print("done.")
