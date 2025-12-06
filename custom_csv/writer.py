"""CustomCsvWriter: A CSV writer implementation."""


class CustomCsvWriter:
    """CSV writer that writes data to CSV format.
    
    Automatically quotes fields containing special characters and escapes
    internal quotes by doubling them.
    """
    
    def __init__(self, file_path, delimiter=',', quotechar='"', line_terminator='\n'):
        """Initialize the CSV writer.
        
        Args:
            file_path (str): Path to the CSV file to write.
            delimiter (str): Field delimiter character (default: ',').
            quotechar (str): Quote character for escaping (default: '"').
            line_terminator (str): Line terminator (default: '\n').
        """
        self.file_path = file_path
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.line_terminator = line_terminator
    
    def _needs_quoting(self, field):
        """Determine if a field needs to be quoted.
        
        A field needs quoting if it contains:
        - The delimiter character
        - The quote character
        - Newline characters (\n or \r)
        
        Args:
            field (str): The field to check.
        
        Returns:
            bool: True if field needs quoting, False otherwise.
        """
        return (self.delimiter in field or 
                self.quotechar in field or 
                '\n' in field or 
                '\r' in field)
    
    def _escape_field(self, field):
        """Escape and optionally quote a field.
        
        Args:
            field (str): The field to escape.
        
        Returns:
            str: The escaped field, quoted if necessary.
        """
        # Convert to string if not already
        field = str(field)
        
        # Escape internal quotes by doubling them
        if self.quotechar in field:
            field = field.replace(self.quotechar, self.quotechar + self.quotechar)
        
        # Quote the field if necessary
        if self._needs_quoting(field):
            field = self.quotechar + field + self.quotechar
        
        return field
    
    def writerow(self, row):
        """Write a single row to the CSV file.
        
        Args:
            row (list): A list of values representing a row.
        """
        with open(self.file_path, 'a', encoding='utf-8', newline='') as f:
            escaped_fields = [self._escape_field(field) for field in row]
            line = self.delimiter.join(escaped_fields) + self.line_terminator
            f.write(line)
    
    def writerows(self, rows):
        """Write multiple rows to the CSV file.
        
        Args:
            rows (list): A list of rows, where each row is a list of values.
        """
        with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
            for row in rows:
                escaped_fields = [self._escape_field(field) for field in row]
                line = self.delimiter.join(escaped_fields) + self.line_terminator
                f.write(line)
