import re
import os

def process_file(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The exact target string to replace in the Hero Section
    target_img_url = "https://lh3.googleusercontent.com/aida-public/AB6AXuC_etCCBIOQkxmhjXkJUx4oKQCYMQXylv0dT5-3HdXSfrP-wDs4UKepGA0bTT19cPIPRi1nG2HBYzLXRzOYW1SxDCWQxRu5uYE1mxcddZ5b8nlKwxiMHj-c-KYX4-3zFwUa0KswsgBFuhOxiOXC0aPiAoivh3zWXgIs4_MZqncIqBTfNByOCFvlZIYIyTo-iWlTqFlk3K7fkcgZi8BaNE4WijT_Zi4NPzafGapPsfkaIlRTzbuV8XdGx17Yfe0bLukJvQ"
    
    # We find the <img> tag that contains this URL
    pattern = re.compile(r'<img class="w-full h-full object-cover"[^>]*src="' + re.escape(target_img_url) + r'">')
    
    new_logo_block = """<!-- Logo Centerpiece -->
<div class="absolute inset-0 flex items-center justify-center bg-surface-base p-space-xl">
  <div class="absolute inset-0 bg-gradient-to-tr from-primary/5 via-surface-base to-surface-container-low"></div>
  <img class="relative z-10 w-full max-w-[200px] sm:max-w-[260px] object-contain drop-shadow-[0_10px_20px_rgba(212,175,55,0.15)]" alt="Logo DepilaMachos" src="https://lh3.googleusercontent.com/aida/AEtjO1UJhzTLwJ634-E0KVv2zzx1P9-xjRXf8q27iJlV4h0JaxZkBDt128SlF7TPbP-V9hOURmkjL1o6XLRjN2i1EDTufpdreGUXjEXQxOi6UsVExhkvpUVW9Hy9QW5Qd8_nygXnI1ZF2f9m2zztATWHO_n8szi4QPqH3tG6L9kCn472IFSn4U9ba3QZfY8JFKYH477BX-0Hkj5WdhDnTw2AT19kSD6vg8aBsxSqeswQrZ_hug0ZRmYJjPhOjA">
</div>"""

    content = pattern.sub(new_logo_block, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Safely updated hero image in {filepath}")

process_file('index.html')
process_file('en/index.html')
