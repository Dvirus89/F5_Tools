
#!/bin/bash
license_pool_path="/var/tmp/license_pool.txt"  # Replace with the actual path to your file

# Read the last line of the file and store it in a variable
last_line=$(tail -n 1 "$file_path")

# Remove the last line from the file
sed -i '$d' "$file_path"

echo "Fixing management default route"
tmsh modify sys management-route default { gateway 10.1.1.1 }

echo "Activating license key: $last_line"
SOAPLicenseClient --basekey $last_line