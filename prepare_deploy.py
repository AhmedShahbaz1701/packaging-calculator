import os
import shutil

def prepare_deploy():
    public_dir = 'public'
    pages_src = 'pages'
    index_src = 'index.html'
    scanner_src = 'scanner.html' # New file
    sitemap_src = 'sitemap.xml'
    robots_src = 'robots.txt'
    
    # 1. Clean/Create 'public' directory
    if os.path.exists(public_dir):
        print(f"Cleaning existing '{public_dir}' directory...")
        shutil.rmtree(public_dir)
    
    os.makedirs(public_dir)
    print(f"Created '{public_dir}' directory.")

    # 2. Copy files
    files_to_copy = [index_src, scanner_src, sitemap_src, robots_src, '404.html']
    
    for file_src in files_to_copy:
        if os.path.exists(file_src):
            shutil.copy2(file_src, public_dir)
            print(f"Copied '{file_src}' to '{public_dir}/'.")
        else:
            print(f"Warning: '{file_src}' not found! (Did you run build scripts?)")

    # 3. Copy pages folder
    if os.path.exists(pages_src):
        dest_pages = os.path.join(public_dir, 'pages')
        shutil.copytree(pages_src, dest_pages)
        print(f"Copied '{pages_src}' folder to '{dest_pages}'.")
    else:
        print(f"Warning: '{pages_src}' folder not found!")
        
    # 4. Success Message
    print("-" * 40)
    print("🚀 Ready to deploy! Drag the 'public' folder to Netlify/Cloudflare.")
    print("-" * 40)

if __name__ == "__main__":
    prepare_deploy()