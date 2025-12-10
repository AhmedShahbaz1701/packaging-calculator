import os

def build_index():
    pages_dir = 'pages'
    output_file = 'index.html'
    
    # 1. Scan for files
    if not os.path.exists(pages_dir):
        print(f"Error: Directory '{pages_dir}' not found.")
        return

    files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]
    files.sort()

    # 2. Generate Card HTML
    cards_html = ""
    
    for filename in files:
        # specific cleanup for the naming convention used in previous step
        # e.g. "fedex-small-box-weight-csrd.html" -> "FedEx Small Box"
        clean_name = filename.replace('.html', '')
        clean_name = clean_name.replace('-weight-csrd', '') # Cleanup the SEO suffix if present
        clean_name = clean_name.replace('-', ' ').title()
        
        # Specific fix for acronyms if needed (optional polish)
        clean_name = clean_name.replace('Usps', 'USPS').replace('Fedex', 'FedEx').replace('Dhl', 'DHL')
        clean_name = clean_name.replace('14 5', '14.5')

        card = f"""
        <div class="card-item bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 border border-slate-200 overflow-hidden flex flex-col">
            <div class="p-5 flex-grow">
                <div class="flex justify-between items-start mb-3">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                        Verified Data
                    </span>
                    <svg class="h-5 w-5 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                </div>
                <h3 class="text-lg font-semibold text-slate-900 mb-2 leading-tight">{clean_name}</h3>
                <p class="text-sm text-slate-500">Instant packaging weight calculation for CSRD compliance.</p>
            </div>
            <div class="bg-slate-50 px-5 py-3 border-t border-slate-100">
                <a href="/{pages_dir}/{filename}" class="block w-full text-center text-sm font-semibold text-emerald-700 hover:text-emerald-800 transition-colors">
                    View Data &rarr;
                </a>
            </div>
        </div>
        """
        cards_html += card

    # 3. Generate Full HTML
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Packaging Data | CSRD Directory</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📦</text></svg>">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        slate: {{
                            850: '#1e293b',
                        }}
                    }}
                }}
            }}
        }}
    </script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans min-h-screen">

    <!-- Hero Section -->
    <header class="bg-slate-850 text-white border-b border-slate-700 relative overflow-hidden">
        <!-- Top Nav -->
        <div class="absolute top-0 right-0 p-4 flex space-x-3 z-10">
             <a href="/scanner.html" class="inline-flex items-center px-3 py-1.5 bg-emerald-600 text-white hover:bg-emerald-700 transition-colors rounded-md shadow-sm">
                ✨ AI Invoice Scanner
                <span class="ml-2 inline-flex items-center rounded-full bg-yellow-400 px-2 py-0.5 text-xs font-medium text-yellow-900">New</span>
            </a>
             <a href="https://forms.gle/9tN5joJShbtxsqLQ7" target="_blank" rel="noopener noreferrer" class="inline-flex items-center px-3 py-1.5 border border-slate-600 text-sm font-medium rounded-md text-slate-200 bg-slate-800 hover:bg-slate-700 transition-colors shadow-sm hover:text-white">
                ➕ Add Missing Box
            </a>
        </div>

        <div class="max-w-5xl mx-auto px-4 py-16 md:py-24 text-center relative z-0">
            <div class="inline-block mb-4 px-3 py-1 rounded-full bg-slate-700 border border-slate-600 text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                Official Directory
            </div>
            <h1 class="text-4xl md:text-6xl font-bold tracking-tight mb-6">Ship to Germany & France without the Fines.</h1>
            <p class="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto mb-10">
                Free tools to calculate packaging taxes (LUCID/CITEO) and generate compliance reports.
            </p>
            
            <!-- Search Bar -->
            <div class="max-w-lg mx-auto relative mb-12">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-slate-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                    </svg>
                </div>
                <input type="text" id="searchInput" 
                    class="block w-full pl-10 pr-3 py-4 border border-transparent rounded-lg leading-5 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:bg-slate-600 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 sm:text-sm transition-all shadow-xl" 
                    placeholder="Search standard box sizes (e.g., 'FedEx', 'Cube', 'Poly')...">
            </div>
        </div>
    </header>

    <!-- Action Grid (Above Fold) -->
    <section class="max-w-5xl mx-auto px-4 -mt-10 relative z-10 mb-16">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
                        <!-- Card A: Data -->
            
                        <a href="#directory" class="bg-white p-6 rounded-xl shadow-lg border border-slate-200 hover:shadow-xl transition-all group flex flex-col items-center text-center">
            
                            <h3 class="text-lg font-bold text-slate-900 mb-2">I need Data</h3>
            
                            <p class="text-sm text-slate-500 mb-4 flex-grow">Browse 80+ verified box weights for your report.</p>
            
                            <div class="w-12 h-12 bg-slate-100 rounded-lg flex items-center justify-center group-hover:bg-slate-200 transition-colors">
            
                                <span class="text-2xl">🧮</span>
            
                            </div>
            
                        </a>
            
            
            
                        <!-- Card B: Invoice (Highlighted) -->
            
                        <a href="/scanner.html" class="bg-white p-6 rounded-xl shadow-lg border-2 border-emerald-500 hover:shadow-emerald-200 transition-all group relative overflow-hidden flex flex-col items-center text-center">
            
                            <div class="absolute top-0 right-0 bg-emerald-500 text-white text-[10px] font-bold px-2 py-1 rounded-bl-lg">NEW</div>
            
                            <h3 class="text-lg font-bold text-slate-900 mb-2">I have an Invoice</h3>
            
                            <p class="text-sm text-slate-500 mb-4 flex-grow">Upload a PDF invoice to extract line items automatically.</p>
            
                            <div class="w-12 h-12 bg-emerald-50 rounded-lg flex items-center justify-center group-hover:bg-emerald-100 transition-colors">
            
                                <span class="text-2xl">📸</span>
            
                            </div>
            
                        </a>
            
            
            
                        <!-- Card C: Guide -->
            
                        <a href="/lucid-guide.html" class="bg-white p-6 rounded-xl shadow-lg border border-slate-200 hover:shadow-xl transition-all group flex flex-col items-center text-center">
            
                            <h3 class="text-lg font-bold text-slate-900 mb-2">I'm Confused</h3>
            
                            <p class="text-sm text-slate-500 mb-4 flex-grow">Step-by-step registration guide for LUCID.</p>
            
                            <div class="w-12 h-12 bg-slate-100 rounded-lg flex items-center justify-center group-hover:bg-slate-200 transition-colors">
            
                                <span class="text-2xl">📖</span>
            
                            </div>
            
                        </a>

        </div>
    </section>

    <!-- Directory Section -->
    <section id="directory" class="max-w-5xl mx-auto px-4 py-10 pt-0">
        
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-slate-800">Packaging Database</h2>
            <span class="text-sm text-slate-500" id="count">{len(files)} Records Found</span>
        </div>

        <!-- Grid -->
        <div id="gridContainer" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {cards_html}
        </div>
        
        <!-- No Results State (Hidden by default) -->
        <div id="noResults" class="hidden py-12 text-center">
            <p class="text-slate-400 text-lg">No packaging formats found matching your search.</p>
        </div>

    </section>

    <!-- Footer -->
    <footer class="bg-slate-50 border-t border-slate-200 mt-12 py-8">
        <div class="max-w-5xl mx-auto px-4 text-center text-slate-500 text-sm">
            <p>&copy; 2025 Open Packaging Data Project. All rights reserved.</p>
            <p class="mt-2">Data provided for estimation purposes only. Not for legal trade use.</p>
            <div class="mt-4 flex justify-center gap-4">
                <a href="https://github.com/1701as/packaging-calculator" class="hover:text-slate-700 underline transition-colors">Open Source Code</a>
                <span>•</span>
                <a href="mailto:admin@tare.fyi" class="hover:text-slate-700 underline transition-colors">Feedback</a>
            </div>
        </div>
    </footer>

    <!-- Search Logic -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const searchInput = document.getElementById('searchInput');
            const gridContainer = document.getElementById('gridContainer');
            const cards = document.querySelectorAll('.card-item');
            const noResults = document.getElementById('noResults');
            const countLabel = document.getElementById('count');
            
            searchInput.addEventListener('input', (e) => {{
                const searchTerm = e.target.value.toLowerCase();
                let visibleCount = 0;

                cards.forEach(card => {{
                    const title = card.querySelector('h3').innerText.toLowerCase();
                    if (title.includes(searchTerm)) {{
                        card.style.display = ''; // Reset to default (flex/block)
                        visibleCount++;
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});

                // Update Counter
                countLabel.innerText = visibleCount + ' Records Found';

                // Show/Hide No Results
                if (visibleCount === 0) {{
                    gridContainer.classList.add('hidden');
                    noResults.classList.remove('hidden');
                }} else {{
                    gridContainer.classList.remove('hidden');
                    noResults.classList.add('hidden');
                }}
            }});
        }});
    </script>

</body>
</html>
    """

    # 4. Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
        print(f"Successfully generated {output_file} with {len(files)} entries.")

if __name__ == "__main__":
    build_index()