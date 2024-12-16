from burp import IBurpExtender, IMessageEditorTabFactory, IMessageEditorTab
from java.io import PrintWriter
from javax.swing import (
    JPanel, JLabel, JTextField, JButton, BoxLayout, BorderFactory, SwingConstants
)
from java.awt import GridBagLayout, GridBagConstraints, Insets, Color

class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Find and Replace")
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)

        # Register the message editor tab factory
        callbacks.registerMessageEditorTabFactory(self)
        self._stdout.println("Find and Replace extension loaded.")

    # Factory method to create a custom message editor tab
    def createNewInstance(self, controller, editable):
        return FindAndReplaceTab(self, controller, editable)




class FindAndReplaceTab(IMessageEditorTab):
    def __init__(self, extender, controller, editable):
        self._extender = extender
        self._helpers = extender._helpers
        self._controller = controller
        self._editable = editable

        # Main panel
        self._panel = JPanel()
        self._panel.setLayout(GridBagLayout())
        self._panel.setBorder(BorderFactory.createLineBorder(Color(0, 120, 215), 2))

        # Constraints for layout
        gbc = GridBagConstraints()
        gbc.insets = Insets(5, 5, 5, 5)
        gbc.fill = GridBagConstraints.HORIZONTAL

        # Title label
        gbc.gridx = 0
        gbc.gridy = 0
        gbc.gridwidth = 2
        title_label = JLabel("Find and Replace Utility", SwingConstants.CENTER)
        title_label.setForeground(Color(50, 50, 50))
        title_label.setBorder(BorderFactory.createMatteBorder(0, 0, 2, 0, Color(200, 200, 200)))
        self._panel.add(title_label, gbc)

        # Find input
        gbc.gridy += 1
        gbc.gridwidth = 1
        self._panel.add(JLabel("Find:"), gbc)

        gbc.gridx = 1
        self._find_field = JTextField(20)
        self._panel.add(self._find_field, gbc)

        # Replace input
        gbc.gridx = 0
        gbc.gridy += 1
        self._panel.add(JLabel("Replace:"), gbc)

        gbc.gridx = 1
        self._replace_field = JTextField(20)
        self._panel.add(self._replace_field, gbc)

        # Buttons panel
        gbc.gridx = 0
        gbc.gridy += 1
        gbc.gridwidth = 2
        buttons_panel = JPanel()
        buttons_panel.setLayout(BoxLayout(buttons_panel, BoxLayout.X_AXIS))
        buttons_panel.setBorder(BorderFactory.createEmptyBorder(10, 0, 0, 0))

        self._apply_button = JButton("Apply Changes", actionPerformed=self.apply_changes)
        self._reset_button = JButton("Reset", actionPerformed=self.reset_fields)

        buttons_panel.add(self._apply_button)
        buttons_panel.add(self._reset_button)
        self._panel.add(buttons_panel, gbc)

        # Storage for the message data
        self._original_message = None
        self._modified_message = None

    def getUiComponent(self):
        return self._panel

    def isEnabled(self, content, isRequest):
        return True

    def getTabCaption(self):
        return "Find & Replace"

    def setMessage(self, content, isRequest):
        if content:
            self._original_message = content
            self._modified_message = content
        else:
            self._original_message = None
            self._modified_message = None

    def getMessage(self):
        return self._modified_message

    def isModified(self):
        return self._original_message != self._modified_message

    def getSelectedData(self):
        return None

    def apply_changes(self, event):
        if self._original_message:
            find_str = self._find_field.getText()
            replace_str = self._replace_field.getText()

            request_info = self._helpers.analyzeRequest(self._original_message)
            headers = request_info.getHeaders()
            body = self._original_message[request_info.getBodyOffset():].tostring()

            # Perform find-and-replace
            modified_body = body.replace(find_str, replace_str)

            # Rebuild the message
            self._modified_message = self._helpers.buildHttpMessage(headers, modified_body)
            self._extender._stdout.println("Applied: '{find}' -> '{replace}'".format(find=find_str, replace=replace_str))

    def reset_fields(self, event):
        self._find_field.setText("")
        self._replace_field.setText("")
        self._extender._stdout.println("Fields reset.")

