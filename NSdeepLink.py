#!/usr/bin/env python3
import argparse
import subprocess
import os
import re
import requests
import xml.etree.ElementTree as ET
from tabulate import tabulate
from colorama import Fore
import zipfile
import plistlib


def banner():
    print(f"""{Fore.YELLOW}
            ⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀
            ⠸⣿⣿⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣿⣿⡏
            ⠀⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⢠⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⠁
            ⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⣀⠀⢀⣴⡟⠀⠀⠀⠀⢠⣟⠛⠛⠛⠛⠛⠛⣣⡀⠀⠀⠀⠀⠹⣷⡀⠀⢀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀
            ⠀⠀⠉⠛⠛⠛⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⣰⣿⣿⣦⠀⠀⠀⠀⣰⣿⣿⣄⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠛⠛⠛⠉⠁⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠻⠿⣿⣿⡀⠀⠀⣴⣿⣿⣿⣿⣷⡀⠀⣼⣿⣿⣿⣿⣦⠀⠀⠀⣿⣿⡿⠿⠛⠛⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣤⣤⣤⣤⣶⣿⣿⡇⠀⠼⠿⠿⠿⠿⠿⠿⠷⠾⠿⠿⠿⠿⠿⠿⠷⠀⢰⣿⣿⣷⣦⣤⣤⣤⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
            ⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⢁⣹⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⢠⣆⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⡀⠉⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠘⣿⣿⠿⠟⠛⠉⠁⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⢀⣾⣿⣆⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠉⠛⠻⠿⣿⣿⠇⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⡿⠋⣸⣿⣿⣿⣿⡿⠃⢀⣾⣿⣿⣿⡄⠀⠿⣿⣿⣿⣿⣯⠈⢿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⠋⠀⢠⣿⣿⣿⡏⠀⠀⢀⣼⣿⣿⣿⣿⣷⡀⠀⠀⠘⣿⣿⣿⡆⠀⠙⢿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⠟⠁⠀⠀⣾⣿⣿⣿⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⡿⠂⠀⠀⢿⣿⣿⣿⡀⠀⠀⠙⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠁⠀⠀⠀⣸⣿⣿⣿⡇⠀⢠⣤⡀⠉⢻⣿⣿⣿⠋⠀⣠⣄⠀⠘⣿⣿⣿⣧⠀⠀⠀⠈⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠀⢠⣿⣿⠃⠀⢸⣿⣿⣿⠀⠈⢿⣿⣇⠀⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠃⠀⠀⢸⣿⣿⣿⠂⠀⠈⢻⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⣿⡿⠿⠿⠿⣿⣿⡆⠀⠀⠈⢿⣿⠃⠀⠀⠰⣿⣿⠿⠿⠿⢿⣿⣿⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢧⡀⠀⠀⠘⠉⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠈⠛⠀⠀⠀⣠⠟⠁{Fore.GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

                 .⣿⣿                            .⣿⣿                  .⣿⣿     
                 .⣿⣿                            .⣿⣿       .         .⣿⣿     
                 .⣿⣿   .⣿⣿      .⣿⣿    .⣿⣿.⣿⣿  .:⣿⣿      .⣿⣿⣿⣿⣿⣿  .⣿⣿  .⣿⣿
             .⣿⣿ .⣿⣿ .⣿⣿  .⣿⣿ .⣿⣿  .⣿⣿ .⣿⣿  .⣿⣿ .⣿⣿      .⣿⣿ .⣿⣿  .⣿⣿.⣿⣿ .⣿⣿ 
            .⣿   .⣿⣿.⣿⣿⣿⣿⣿.⣿⣿.⣿⣿⣿⣿⣿.⣿⣿.:⣿⣿   .⣿⣿.⣿⣿      .⣿⣿ .⣿⣿  .⣿⣿.:.⣿⣿   
            .⣿   .⣿⣿.⣿⣿       .⣿⣿      .⣿⣿ .⣿⣿ .:⣿⣿      .⣿⣿ .⣿⣿  .⣿⣿.⣿⣿ .⣿⣿ 
     Not So .⣿⣿ .⣿⣿   .⣿⣿⣿⣿     .⣿⣿⣿⣿  .⣿⣿.⣿⣿   ⣠⣿⣿⣿⣿⣿⣿⣿⣿.⣿⣿.:⣿⣿  ⣠⣿⣿.⣿⣿  .⣿⣿
                                       .⣿⣿.⣿⣿                                  


                                     By S1rN3tZ⠀⠀⠀⠀⠀⠀⠀
        {Fore.RESET}""")

def run_adb_command(cmd, serial=None):
    base_cmd = ["adb"]
    if serial:
        base_cmd += ["-s", serial]
    base_cmd += cmd
    return subprocess.check_output(base_cmd, stderr=subprocess.DEVNULL).decode("utf-8")


def parse_dumpsys(package, serial=None):
    """
    Function to parse the result of the command adb shell dumsys package <package> and extract deeplinks information.
    Then create a table with these data.
    """
    output = run_adb_command(["shell", "dumpsys", "package", package], serial)

    deeplinks = []
    current_scheme = None
    current_authority = None
    current_path = None
    current_port = None
    current_pattern = None
    auto_verify = False

    for line in output.splitlines():
        line = line.strip()

        # Matching Schemes
        scheme_match = re.match(r'Scheme: "([^"]+)"', line)
        if scheme_match:
            current_scheme = scheme_match.group(1)
            current_authority = None
            current_path = None
            current_port = None
            current_pattern = None
            auto_verify = False
            continue

        # DMatching Hosts
        authority_match = re.match(r'Authority: "([^"]+)"', line)
        if authority_match:
            current_authority = authority_match.group(1)
            continue

        # Matching Path Prefix
        path_match = re.match(r'Path: "PatternMatcher\{PREFIX: (.+)\}"', line)
        if path_match:
            current_path = path_match.group(1)
            continue

        # Matching Ports
        port_match = re.match(r'Port: "([^"]+)"', line)
        if port_match:
            current_port = port_match.group(1)
            continue

        # Matching Patterns
        pattern_match = re.match(r'Pattern: "([^"]+)"', line)
        if pattern_match:
            current_pattern = pattern_match.group(1)
            continue

        # Checking the auto verify status
        if "AutoVerify=true" in line:
            auto_verify = True
            continue

        # Crafting complete deeplinks based on the extracted data
        if current_scheme and current_authority:
            path = current_path if current_path else ""
            deeplink = f"{current_scheme}://{current_authority}"
            if current_port:
                deeplink += f":{current_port}"
            if current_path:
                deeplink += f"{current_path}"
            if current_pattern:
                deeplink += f"#{current_pattern}"

            deeplinks.append([
                deeplink,
                current_scheme,
                current_authority,
                current_port if current_port else "",
                current_path if current_path else "",
                current_pattern if current_pattern else "",
                "✅" if auto_verify else "❌"
            ])
            # Reset to prevent duplicates
            current_authority = None
            current_path = None
            current_port = None
            current_pattern = None
            auto_verify = False

    return deeplinks


def print_table(deeplinks):
    """
    Function for table formatting
    """
    if not deeplinks:
        print(Fore.RED + "[!] " + Fore.RESET + "No Deeplink Found")
        return
    headers = ["Deeplink", "Scheme", "Authority", "Port", "Path", "Pattern", "AutoVerify"]
    print("\n" + Fore.CYAN + "[*] " + Fore.RESET + "Searching Deeplinks" +"\n")
    print(tabulate(deeplinks, headers=headers, tablefmt="grid"))


def parse_apk(apk_path):
    """
    Function to decompile the APK and parse the AndroidManifest.xml file to extract the deeplink information
    """
    deeplinks = []  # Store deeplinks
    try:
        print(f"{Fore.CYAN}[*]{Fore.RESET} Decompiling the APK\n")
        # Run apktool to decode the APK
        subprocess.run(['apktool', 'd', apk_path, '-o', 'decoded_apk'])

        # Path to the decoded manifest
        decoded_manifest_path = 'decoded_apk/AndroidManifest.xml'
        strings_file_path = 'decoded_apk/res/values/strings.xml'

        # Step 1: Parse strings.xml to create a mapping of string references
        string_map = parse_strings(strings_file_path)

        # Step 2: Parse the AndroidManifest.xml
        tree = ET.parse(decoded_manifest_path)
        root = tree.getroot()

        # Extract data like android:scheme, android:host, etc.
        namespaces = {'android': 'http://schemas.android.com/apk/res/android'}
        extracted_data = []

        for intent_filter in root.findall('.//intent-filter'):
            scheme = None
            host = None
            path_prefix = None
            port = None
            pattern = None
            auto_verify = False

            # Extract scheme
            scheme_elem = intent_filter.find('.//data[@android:scheme]', namespaces)
            if scheme_elem is not None:
                scheme = scheme_elem.attrib.get('{http://schemas.android.com/apk/res/android}scheme')

            # Extract host (authority)
            host_elem = intent_filter.find('.//data[@android:host]', namespaces)
            if host_elem is not None:
                host = host_elem.attrib.get('{http://schemas.android.com/apk/res/android}host')

            # Extract path prefix
            path_prefix_elem = intent_filter.find('.//data[@android:pathPrefix]', namespaces)
            if path_prefix_elem is not None:
                path_prefix = path_prefix_elem.attrib.get('{http://schemas.android.com/apk/res/android}pathPrefix')

            # Extract port
            port_elem = intent_filter.find('.//data[@android:port]', namespaces)
            if port_elem is not None:
                port = port_elem.attrib.get('{http://schemas.android.com/apk/res/android}port')

            # Extract pattern
            pattern_elem = intent_filter.find('.//data[@android:pattern]', namespaces)
            if pattern_elem is not None:
                pattern = pattern_elem.attrib.get('{http://schemas.android.com/apk/res/android}pattern')

            # Check if autoVerify attribute is present
            auto_verify_elem = intent_filter.attrib.get('{http://schemas.android.com/apk/res/android}autoVerify', 'false')
            if auto_verify_elem == 'true':
                auto_verify = True

            # Replace references like @string/APKTOOL_DUMMYVAL_0xxxxxx in scheme, host, and path_prefix
            if scheme:
                scheme = replace_string_reference(scheme, string_map)
            if host:
                host = replace_string_reference(host, string_map)
            if path_prefix:
                path_prefix = replace_string_reference(path_prefix, string_map)
            if port:
                port = replace_string_reference(port, string_map)
            if pattern:
                pattern = replace_string_reference(pattern, string_map)

            # Crafting the complete deeplinks thanks to the extracted values
            if scheme and host:
                path = path_prefix if path_prefix else ""
                deeplink = f"{scheme}://{host}"
                if port:
                    deeplink += f":{port}"
                if path:
                    deeplink += f"{path}"
                if pattern:
                    deeplink += f"#{pattern}"
                
                deeplinks.append([
                    deeplink,  # The full deeplink
                    scheme,    # The scheme (e.g., http)
                    host,      # The host (e.g., example.com)
                    port if port else "",  # Port
                    path_prefix if path_prefix else "",  # Path prefix
                    pattern if pattern else "",  # Pattern
                    "✅" if auto_verify else "❌"  # AutoVerify status
                ])

        # Clean up the decoded APK folder
        subprocess.run(['rm', '-r', "decoded_apk"])

    except Exception as e:
        print(f"{Fore.RED}[!]{Fore.RESET} Error Analyzing APK : {e}")

    return deeplinks


def parse_ipa(ipa_path, verify=False):
    """
    Parse an IPA file to extract URL schemes and Universal Links (Associated Domains)
    """
    deeplinks = []
    associated_domains = []

    try:
        with zipfile.ZipFile(ipa_path, 'r') as ipa:
            # Find the .app folder inside Payload
            app_folder = [f for f in ipa.namelist() if f.startswith("Payload/") and f.endswith(".app/")]
            if not app_folder:
                print(f"[!] No .app folder found in {ipa_path}")
                return []
            app_folder = app_folder[0]

            # parse Info.plist info
            plist_path = app_folder + "Info.plist"
            with ipa.open(plist_path) as f:
                plist_data = plistlib.load(f)

            # Custom URL schemes
            for url_type in plist_data.get("CFBundleURLTypes", []):
                schemes = url_type.get("CFBundleURLSchemes", [])
                for scheme in schemes:
                    deeplinks.append([f"{scheme}://", scheme, "", "", "", "", "N/A"])

            # Extract info from Mach-O binary
            app_name = app_folder.rstrip("/").split("/")[-1].replace(".app", "")
            macho_path = app_folder + app_name
            with ipa.open(macho_path) as f:
                binary_data = f.read()
                matches = re.findall(rb'applinks:([^\x00\s]+)', binary_data)
                for m in matches:
                    host = m.decode('utf-8', errors='ignore')
                    clean_host = clean_string(host)
                    if host not in associated_domains:
                        associated_domains.append(clean_host)
                        deeplinks.append([f"https://{clean_host}", "https", clean_host, "", "", "", "N/A"])

            # Optional AASA verification
            if verify and associated_domains:
                results = verify_aasa(associated_domains)
                print_verify_table(results)

    except Exception as e:
        print(f"[!] Error parsing IPA: {e}")

    return deeplinks


def parse_strings(strings_file_path):
    """
    Parse strings.xml to build a mapping of string references (e.g., @string/foo) to actual string values.
    """
    string_map = {}
    try:
        tree = ET.parse(strings_file_path)
        root = tree.getroot()

        # Loop through all string elements in the XML and create a mapping
        for string_elem in root.findall('string'):
            name = string_elem.attrib.get('name')
            if name:
                value = string_elem.text
                string_map[f"@string/{name}"] = value

    except Exception as e:
        print(f"{Fore.RED}[!]{Fore.RESET} Error parsing strings : {e}")

    return string_map

def clean_string(value):
    if not value:
        return value
    # Remove trailing whitespace and stray XML tags
    value = value.strip()
    value = re.sub(r'</?string>', '', value)  # remove <string> or </string>
    return value


def replace_string_reference(value, string_map):
    """
    Replace all @string/ references in a value with the corresponding string from the string_map.
    """
    # Find all occurrences of @string/<name>
    references = re.findall(r'@string/(\w+)', value)

    for ref in references:
        ref_key = f"@string/{ref}"
        if ref_key in string_map:
            # Replace @string/reference with the actual value
            value = value.replace(ref_key, string_map[ref_key])

    return value


def verify_assetlinks(hosts, package):
    """
    Function to Verify Assets Links by requesting the /.well-known/assetlinks.json on each domain
    """
    results = []
    for host in hosts:
        url = f"https://{host}/.well-known/assetlinks.json"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                try:
                    data = r.json()
                    parsed = []
                    match = False
                    for entry in data:
                        # Extracting the interesting values in the response
                        target = entry.get("target", {})
                        pkg = target.get("package_name")
                        certs = target.get("sha256_cert_fingerprints", [])
                        if pkg and certs:
                            parsed.append([host, pkg, "\n".join(certs)])
                            if pkg == package:
                                match = True
                    # Add to the table
                    for row in parsed:
                        row.append("OK" if match else "NOK")
                        results.append(row)

                except json.JSONDecodeError:
                    results.append([host, "-", "-", "Invalid JSON"])
            else:
                results.append([host, "-", "-", f"HTTP {r.status_code}"])
        except Exception as e:
            results.append([host, "-", "-", f"Erreur: {e}"])
    return results


def verify_aasa(hosts, bundle_id):
    """
    Verify Apple App Site Association (AASA) files for Universal Links
    """
    results = []
    headers = {"Accept": "application/json"}

    for host in hosts:
        url = f"https://{host}/.well-known/apple-app-site-association"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                try:
                    data = r.json()
                    paths = []
                    applinks = data.get("applinks", {})
                    details = applinks.get("details", [])
                    match = False
                    for detail in details:
                        app_id = detail.get("appID")
                        if app_id and bundle_id in app_id:
                            match = True
                        paths.append(",".join(detail.get("paths", [])))
                    results.append([host, bundle_id, "\n".join(paths), "OK" if match else "NOK"])
                except Exception:
                    results.append([host, bundle_id, "-", "Invalid JSON"])
            else:
                results.append([host, bundle_id, "-", f"HTTP {r.status_code}"])
        except Exception as e:
            results.append([host, bundle_id, "-", f"Error: {e}"])

    return results


def print_verify_table(results):
    if not results:
        print(Fore.RED + "[!] " + Fore.RESET + "No host to verify")
        return
    headers = ["Host", "Package", "Fingerprints", "Status"]
    print("\n" + Fore.CYAN + "[*] " + Fore.RESET + "Verifying deeplinks" +"\n")
    print(tabulate(results, headers=headers, tablefmt="grid"))


def launch_deeplink(deeplink, serial=None):
    """
    Function to launch a specific deeplink using adb shell am start -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d <deeplink>
    """
    try:
        run_adb_command(["shell", "am", "start", "-a", "android.intent.action.VIEW", "-c", "android.intent.category.BROWSABLE", "-d", deeplink], serial)
        print(f"{Fore.CYAN}[*] {Fore.RESET}Deeplink launched : {deeplink}")
    except Exception as e:
        print(f"{Fore.RED}[!] {Fore.RESET}An error occured during deepling lauch {deeplink}: {e}")

def search_for_deeplink_handling_in_code(code_directory):
    """
    Search for Intent handling related to deeplinks in both Java and Kotlin code.
    Looks for occurrences of 'getIntent().getData()', 'Intent.getData()', 'getIntent().getAction()', etc.
    Case-insensitive search.
    """
    deeplink_patterns = [
        r'getIntent\(\)\.getData\(\)',    # Java call to get data from the Intent
        r'Intent\.getData\(\)',            # Common Intent method for retrieving data
        r'getIntent\(\)\.getAction\(\)',   # Action of the intent
        r'getIntent\(\)\.getScheme\(\)',   # Scheme part of the URI
        r'getIntent\(\)\.getHost\(\)',     # Host part of the URI
        r'getIntent\(\)\.getPath\(\)',     # Path part of the URI
        r'setData\(\)'                     # Set data for the Intent (handling deeplinks)
        r'intent\.data',                # Kotlin variant (accessing data directly)
        r'intent\.action',              # Kotlin variant (accessing action directly)
        r'intent\.scheme',              # Kotlin variant (accessing scheme directly)
        r'intent\.host',                # Kotlin variant (accessing host directly)
        r'intent\.path',                # Kotlin variant (accessing path directly)
        r'UriMatcher\(',                # URI Matcher usage (e.g., for matching deeplinks in older apps)
        r'Pattern\.compile\(',          # Compiling patterns for URI matching
        r'Pattern\.matches\(',          # Matching a URI with a pattern
        r'Uri\.getHost\(',              # Getting host from URI
        r'Uri\.getPath\(',              # Getting path from URI
        r'Uri\.getScheme\(',            # Getting scheme from URI
        r'Uri\.getQueryParameter\(',    # Extract query parameters from URI
        r'Uri\.getQueryParameterNames\(', # Getting all query parameters
        r'Uri\.getFragment\(',          # Extract fragment from URI
        r'Uri\.getAuthority\(',         # Extract authority from URI
        r'Uri\.parse\(',                # Parsing URI in Java (e.g., `Uri.parse()`)
        r'Intent\.setData\(',           # Setting data for Intent in Java
        r'Intent\.setDataAndType\(',    # Setting data and type for Intent
        r'Intent\.setAction\(',         # Setting action for Intent
        r'getIntent\(\)\.getExtras\(\)', # Retrieve extras from Intent (can include deeplink info)
        r'getIntent\(\)\.getStringExtra\(', # Retrieve string extra from Intent (could be deeplink related)
        r'Intent\.getStringExtra\(',    # Common method for extracting specific data (extra)
        r'@DeepLink\(',                     # DeepLink annotation to map deeplinks to activities
        r'DeepLinkDispatch\.handleDeepLink\(', # Calling `handleDeepLink` to route deeplinks
        r'Branch\.getInstance\(\)\.handleDeepLink\(',     # Handling deep link via Branch SDK
        r'Branch\.getInstance\(\)\.initSession\(',         # Initializing a Branch session (used for deep links)
        r'Branch\.getInstance\(\)\.setRequestMetadata\(',  # Setting metadata before handling deep link
        r'FirebaseDynamicLinks\.getInstance\(\)\.getDynamicLink\(',  # Handling dynamic links with Firebase
        r'FirebaseDynamicLinks\.getInstance\(\)\.createDynamicLink\(',  # Creating dynamic links
        r'FirebaseDynamicLinks\.getInstance\(\)\.setEventListener\(',   # Setting listeners for dynamic links
        r'URLDecoder\.decode\(',              # Decoding a URI (to handle deeplinks with encoded data)
        r'URLEncoder\.encode\(',              # Encoding a URI (to handle deeplinks with encoded data)
        r'NavController\.navigate\(',           # Navigating via the NavController (deep link)
        r'NavDeepLinkBuilder\(',                # Builder for creating deep links with Navigation Component
        r'@Route\(',                           # ARouter annotation for routing
        r'ARouter\.getInstance\(\)\.build\(',   # ARouter deep link handling code
        r'Observable\.just\(',                  # Observable-based approach for deeplink handling
        r'SubscribeOn\(',                       # RxJava’s subscribeOn() method
        r'.subscribe\(',                        # RxJava’s subscribe() method to handle deeplinks
        r'Flowable\.fromCallable\(',             # Flowable used for handling deeplinks
        r'Intent\.parseUri\(',                  # Parsing custom URIs
    ]
    deeplink_references = []

    # Walk through the directory and search for relevant code in all .java and .kt files
    for root, dirs, files in os.walk(code_directory):
        for file in files:
            if file.endswith(".java") or file.endswith(".kt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line_number, line in enumerate(lines, 1):
                            # Case-insensitive search for any of the deeplink patterns in the line
                            if any(re.search(pattern, line, re.IGNORECASE) for pattern in deeplink_patterns):
                                deeplink_references.append({
                                    'file': file_path,
                                    'line_number': line_number,
                                    'line': line.strip()
                                })
                except Exception as e:
                    print(f"[!] Error reading file {file_path}: {e}")

    return deeplink_references

def print_deeplink_references(deeplink_references):
    """
    Function to print the results of the search_for_deeplink_handling_in_code function
    """
    if not deeplink_references:
        print(f"{Fore.RED}[!]{Fore.RESET} No deeplink handling found in the code.")
        return
    
    print(f"\n{Fore.GREEN}[+]{Fore.RESET} Potential Deeplink Handling Found:\n")
    for reference in deeplink_references:
        print(f"[{Fore.GREEN}File{Fore.RESET}] {reference['file']} [{Fore.CYAN}Line {reference['line_number']}{Fore.RESET}] {Fore.RED}{reference['line']}{Fore.RESET}")


def main():
    banner()
    parser = argparse.ArgumentParser(description="App Links Recon Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--adb", action="store_true", help="ADB Analyze")
    group.add_argument("--apk", type=str, help="APK analyze")
    group.add_argument("--ipa", type=str, help="IPA analyze")
    group.add_argument("-l", "--launch", type=str, help="Launch a deeplink")
    group.add_argument("-c", "--code-search", type=str, help="Search for potential deeplink handling in JAVA / Kotlin code")
    
    parser.add_argument("-p", "--package", type=str, help="Package Name (ex: com.example.xyz)")
    parser.add_argument("-s", "--serial", type=str, help="Device/Emulator to use")
    parser.add_argument("-v", "--verify", action="store_true", help="Verify Assets Links")
    parser.add_argument("-o", "--output", type=str, help="Save results in an output file")
    
    args = parser.parse_args()

    deeplinks = []

    if args.adb:
        if not args.package:
            parser.error("--adb require --package")
        deeplinks = parse_dumpsys(args.package, args.serial)

    elif args.apk:
        deeplinks = parse_apk(args.apk)

    elif args.ipa:
        deeplinks = parse_ipa(args.ipa)


    if deeplinks:
        print_table(deeplinks)

    # Extraire les hosts pour vérification
    if args.verify and deeplinks:
        hosts = [d[2] for d in deeplinks if d[2]]  # extraire les hosts uniques
        hosts = list(set(hosts))

        results = []

        if args.ipa:
            results = verify_aasa(hosts, args.package)
        else:
            # Android: vérifier les assetlinks.json
            if args.package:
                results = verify_assetlinks(hosts, args.package)
            else:
                results = verify_assetlinks(hosts, None)

        print_verify_table(results)


    if args.launch:
        launch_deeplink(args.launch, args.serial)

    if args.code_search:
        print(f"{Fore.CYAN}[*]{Fore.RESET} Searching for deeplink handling in code...")
        code_directory = args.code_search
        deeplink_references = search_for_deeplink_handling_in_code(code_directory)
        print_deeplink_references(deeplink_references)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                if deeplinks:
                    headers = ["Deeplink", "Scheme", "Authority", "Port", "Path", "Pattern", "AutoVerify"]
                    f.write("=== Deeplinks Found ===\n")
                    f.write(tabulate(deeplinks, headers=headers, tablefmt="grid"))
                    f.write("\n\n")
                if args.verify and deeplinks:
                    f.write("=== Verification Results ===\n")
                    headers = ["Host", "Package", "Fingerprints", "Status"]
                    f.write(tabulate(results, headers=headers, tablefmt="grid"))
                    f.write("\n\n")
                if args.code_search:
                    f.write("=== Code Search Results ===\n")
                    if deeplink_references:
                        for ref in deeplink_references:
                            f.write(f"[File] {ref['file']} [Line {ref['line_number']}] {ref['line']}\n")
                    else:
                        f.write("No deeplink handling found in the code.\n")
            print(f"\n{Fore.GREEN}[+]{Fore.RESET} Results saved to {args.output}")
        except Exception as e:
            print(f"{Fore.RED}[!]{Fore.RESET} Error saving output file: {e}")


if __name__ == "__main__":
    main()
