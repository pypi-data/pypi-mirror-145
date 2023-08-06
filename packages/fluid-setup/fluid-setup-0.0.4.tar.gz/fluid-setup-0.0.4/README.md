[![](https://res.cloudinary.com/fluid-attacks/image/upload/q_auto,f_auto/v1619036532/airs/logo-fluid-attacks-dark_x1fpui.webp)](https://fluidattacks.com/)

# Fluid Attacks Environment Setup

## Requirements

- git
- python
- Nix
- make

## Install makes

```
nix profile install github:fluidattacks/makes/22.04
```

## Run setup

```bash
pip install fluid-setup
fluid-setup

# or

git clone https://github.com/afgalvan/fluid-setup
cd fluid-setup
make setup
```
