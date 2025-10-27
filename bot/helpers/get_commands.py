"""Helper to get all commands from the commands directory."""

from pathlib import Path
import importlib.util


def get_commands(directory):
    """
    Get all command modules from a directory.
    
    Args:
        directory: Path to the commands directory
        
    Returns:
        dict: Dictionary with 'commands' and 'files' lists
    """
    commands = []
    files = []
    
    try:
        directory_path = Path(directory)
        
        # Iterate over all Python files
        for file_path in directory_path.rglob('*.py'):
            if file_path.name.startswith('__'):
                continue
                
            try:
                # Load the module
                spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if it has the required attributes
                if hasattr(module, 'data') and hasattr(module, 'execute'):
                    commands.append(module.data)
                    files.append(module)
                else:
                    print(
                        f'[discord] the command at {file_path} is missing '
                        'a required "data" or "execute" property'
                    )
                    
            except Exception as e:
                print(f'[discord] error loading {file_path}: {e}')
        
        return {'commands': commands, 'files': files}
        
    except Exception as ex:
        print(f'[discord] error occurred processing command files: {ex}')
        return {'commands': [], 'files': []}
