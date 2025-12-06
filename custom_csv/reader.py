"""CustomCsvReader: A CSV reader implementation using iterator protocol."""


class CustomCsvReader:
    """CSV reader that implements the iterator protocol.
    
    Reads CSV files character-by-character and yields rows as lists of strings.
    Handles quoted fields, escaped quotes, and newlines within fields.
    """
    
    def __init__(self, file_path, delimiter=',', quotechar='"'):
        """Initialize the CSV reader.
        
        Args:
            file_path (str): Path to the CSV file to read.
            delimiter (str): Field delimiter character (default: ',').
            quotechar (str): Quote character for escaping (default: '"').
        """
        self.file_path = file_path
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.file = None
    
    def __iter__(self):
        """Return the iterator object itself."""
        self.file = open(self.file_path, 'r', encoding='utf-8')
        self.inside_quotes = False
        self.current_row = []
        self.current_field = []
        return self
    
    def __next__(self):
        """Parse and return the next row from the CSV file."""
        while True:
            char = self.file.read(1)
            
            if not char:  # End of file
                if self.current_field or self.current_row:
                    self.current_row.append(''.join(self.current_field))
                    result = self.current_row
                    self.current_row = []
                    self.current_field = []
                    self.file.close()
                    return result
                else:
                    self.file.close()
                    raise StopIteration
            
            # Handle quote character
            if char == self.quotechar:
                if self.inside_quotes:
                    # Look ahead for next character
                    next_char = self.file.read(1)
                    if not next_char:  # End of file
                        self.inside_quotes = False
                    elif next_char == self.quotechar:
                        # Escaped quote - add one quote to field
                        self.current_field.append(self.quotechar)
                    else:
                        # End of quoted field
                        self.inside_quotes = False
                        if next_char == self.delimiter:
                            self.current_row.append(''.join(self.current_field))
                            self.current_field = []
                        elif next_char in ('\n', '\r'):
                            self.current_row.append(''.join(self.current_field))
                            self.current_field = []
                            if next_char == '\r':
                                peek = self.file.read(1)
                                if peek != '\n' and peek:
                                    self.file.seek(self.file.tell() - 1)
                            return self.current_row
                        else:
                            self.current_field.append(next_char)
                else:
                    # Start of quoted field
                    if len(self.current_field) == 0:
                        self.inside_quotes = True
                    else:
                        self.current_field.append(char)
            
            # Handle delimiter
            elif char == self.delimiter and not self.inside_quotes:
                self.current_row.append(''.join(self.current_field))
                self.current_field = []
            
            # Handle newline
            elif char in ('\n', '\r') and not self.inside_quotes:
                self.current_row.append(''.join(self.current_field))
                self.current_field = []
                if char == '\r':
                    next_char = self.file.read(1)
                    if next_char != '\n' and next_char:
                        self.file.seek(self.file.tell() - 1)
                if self.current_row and self.current_row != ['']:
                    return self.current_row
                self.current_row = []
            
            # Regular character
            else:
                self.current_field.append(char)
