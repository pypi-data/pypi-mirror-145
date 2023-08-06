# Unseal - Mechanistic Interpretability for Transformers

<!-- include logo image -->
<img src="https://github.com/TomFrederik/unseal/blob/main/docs/images/logo.png?raw=true" width="400">

## Prerequisites

Unseal requires python 3.6+.


## Installation

For its visualizations interfaces, Unseal uses [this fork](https://github.com/TomFrederik/pysvelte) of the PySvelte library, which can be installed via pip:

```sh
git clone git@github.com:TomFrederik/PySvelte.git
cd PySvelte
pip install -e .
```

In order to run PySvelte, you will also need to install ``npm`` via your package manager.
The hooking functionality of Unseal should still work without PySvelte, but we can't give any guarantees

Install Unseal via pip

```sh
pip install unseal
```

## Usage

We refer to our documentation for tutorials and usage guides:

[Documentation](https://unseal.readthedocs.io/en/latest/)


## Notebooks

Here are some notebooks that also showcase Unseal's functionalities.

<a href="https://colab.research.google.com/drive/1Y1y2GnDT-Uzvyp8pUWWXt8lEfHWxje3b?usp=sharing">
    <img src="https://github.com/TomFrederik/unseal/blob/main/docs/images/notebook_images/inspectgpt2_card.png?raw=true">
</a>

<a href="https://colab.research.google.com/drive/1ljCPvbr7VPEIlbZQvrUceLSDsdeo3oRH?usp=sharing">
    <img src="https://github.com/TomFrederik/unseal/blob/main/docs/images/notebook_images/trace_info_flow_card.png?raw=true">
</a>