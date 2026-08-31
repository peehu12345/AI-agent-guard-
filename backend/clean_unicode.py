import os

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace Rupee symbol with Rs.
        if 'Rs. ' in content:
            new_content = content.replace('Rs. ', 'Rs. ')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Cleaned: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    root_dir = r"c:\Users\91969\Desktop\AGENTGUARD\backend"
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            if name.endswith('.py'):
                clean_file(os.path.join(dirpath, name))

if __name__ == '__main__':
    main()
