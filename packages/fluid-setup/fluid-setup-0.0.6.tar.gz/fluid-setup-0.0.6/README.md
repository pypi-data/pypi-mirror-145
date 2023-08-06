[![](https://res.cloudinary.com/fluid-attacks/image/upload/q_auto,f_auto/v1619036532/airs/logo-fluid-attacks-dark_x1fpui.webp)](https://fluidattacks.com/)

# Fluid Attacks Environment Setup

## Run setup

```bash
curl -sL https://raw.githubusercontent.com/afgalvan/fluid-setup/main/installer.sh | bash -s
```

Edit setup.yml and add your credentials here:

```yaml
aws:
  setup: true
  iam: 0000000
  application: https://amazon_aws_url
  organization: organization.okta.com
  credentials:
    role: dev
    email: example@mail.com
    password: password
```

Run the setup

```bash
fluid-setup
```
