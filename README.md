# Burp Suite Find and Replace Extension

This Burp Suite extension provides a simple "Find and Replace" utility for modifying HTTP request and response content directly within Burp Suite's message editor. It allows users to specify a string to find and a string to replace it with, making it easier to perform quick modifications to HTTP messages.

## Features

- **Find and Replace**: Allows you to search for a specific string and replace it with another in HTTP request and response bodies.
- **GUI Integration**: Integrates directly into the Burp Suite message editor with a custom tab.
- **Easy to Use**: Simple interface with a "Find" input, "Replace" input, and buttons for applying changes or resetting fields.

## Installation

1. Download the `Find and Replace` extension `.jar` file or save the Python script.
2. Open Burp Suite.
3. Go to the **Extender** tab in Burp Suite.
4. Click on the **Extensions** sub-tab.
5. Click **Add** and choose **Python** as the extension type.
6. Select the `.py` file and click **Open**.

## Usage

Once the extension is loaded, follow these steps to use it:

1. Open the **Proxy** or **Repeater** tab in Burp Suite and select an HTTP message.
2. Click the **Find & Replace** tab in the message editor.
3. Enter the string you want to **find** in the "Find" field.
4. Enter the string you want to **replace** in the "Replace" field.
5. Click **Apply Changes** to modify the message.
6. Click **Reset** to clear the input fields.

### Example:

- **Find**: `user123`
- **Replace**: `admin456`

Clicking **Apply Changes** will replace all occurrences of `user123` with `admin456` in the HTTP message body.

## Code Overview

### BurpExtender Class

The `BurpExtender` class implements the `IBurpExtender` and `IMessageEditorTabFactory` interfaces. It registers the extension within Burp Suite and creates a new instance of the `FindAndReplaceTab`.

- **registerExtenderCallbacks**: Initializes the extension and registers the message editor tab.
- **createNewInstance**: Creates a new instance of the `FindAndReplaceTab`.

### FindAndReplaceTab Class

The `FindAndReplaceTab` class defines the user interface for the "Find and Replace" utility.

- **UI Components**:
  - Title label ("Find and Replace Utility")
  - Input fields for "Find" and "Replace" strings
  - Buttons to **Apply Changes** or **Reset**
- **Methods**:
  - `getUiComponent`: Returns the main panel with all UI components.
  - `setMessage`: Sets the current HTTP message to be modified.
  - `getMessage`: Returns the modified message.
  - `apply_changes`: Performs the find-and-replace operation on the HTTP message body.
  - `reset_fields`: Resets the input fields for find and replace.

## Requirements

- Burp Suite (Community or Professional)
- Python 2.7 or later (for Burp Suite Python extensions)

## License

This extension is released under the MIT License.

## Disclaimer

This extension is provided "as-is" without warranty of any kind. Use it at your own risk.

## Contact

For any issues or feature requests, please open an issue in the repository.

