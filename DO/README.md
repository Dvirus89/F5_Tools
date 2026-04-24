# Declarative Onboarding Scripts

These scripts automate the installation of F5 Declarative Onboarding (DO) and apply a base configuration to BIG-IP devices.

## Usage

You can run these scripts directly from the repository using the following commands:

### BIG-IP 1
```bash
curl -s https://raw.githubusercontent.com/Dvirus89/F5_Tools/main/DO/do-bigip1.sh | bash
```

### BIG-IP 2
```bash
curl -s https://raw.githubusercontent.com/Dvirus89/F5_Tools/main/DO/do-bigip2.sh | bash
```

## Description
Each script performs the following actions:
1. Downloads and installs the Declarative Onboarding RPM.
2. Prompts the user for a license key.
3. Generates a `do.json` file with the license key and device-specific configuration.
4. Submits the declaration to the BIG-IP.
