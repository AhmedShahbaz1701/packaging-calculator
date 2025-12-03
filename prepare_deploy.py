import os
import shutil

def prepare_deploy():
    public_dir = 'public'
    pages_src = 'pages'
    index_src = 'index.html'
    sitemap_src = 'sitemap.xml'
    
    # 1. Clean/Create 'public' directory
    if os.path.exists(public_dir):
        print(f"Cleaning existing '{public_dir}' directory...")
        shutil.rmtree(public_dir)
    
    os.makedirs(public_dir)
    print(f"Created '{public_dir}' directory.")

    # 2. Copy index.html
    if os.path.exists(index_src):
        shutil.copy2(index_src, public_dir)
        print(f"Copied '{index_src}' to '{public_dir}/'.")
    else:
        print(f"Warning: '{index_src}' not found!")

    # 3. Copy pages folder
    if os.path.exists(pages_src):
        dest_pages = os.path.join(public_dir, 'pages')
        shutil.copytree(pages_src, dest_pages)
        print(f"Copied '{pages_src}' folder to '{dest_pages}'.")
    else:
        print(f"Warning: '{pages_src}' folder not found!")

    # 4. Copy sitemap.xml
    if os.path.exists(sitemap_src):
        shutil.copy2(sitemap_src, public_dir)
        print(f"Copied '{sitemap_src}' to '{public_dir}/'.")
    else:
        print(f"Warning: '{sitemap_src}' not found! (Did you run generate.py?)")
        
    # 5. Success Message
    print("-" * 40)
    print("🚀 Ready to deploy! Drag the 'public' folder to Netlify/Cloudflare.")
    print("-" * 40)

if __name__ == "__main__":
    prepare_deploy()