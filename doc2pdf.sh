#!/bin/bash

# Create combined documentation PDF
cd /Users/yemikudaisi/frappe-bench/apps/bank_integration

# Create a temporary combined markdown file
cat > combined_docs.md << 'EOF'
# Bank Integration - Complete Documentation

EOF

# Add README content
echo "## Main README" >> combined_docs.md
echo "" >> combined_docs.md
cat README.md >> combined_docs.md
echo "" >> combined_docs.md
echo "\\newpage" >> combined_docs.md
echo "" >> combined_docs.md

# Add all documentation files in order
for file in doc/01-overview.md doc/02-configuration.md doc/03-scheduled-sync-workflow.md doc/04-manual-sync-workflow.md doc/05-authentication.md doc/06-data-mapping.md doc/07-error-handling.md doc/08-common-sync-process.md doc/transaction_mapping.md; do
    if [ -f "$file" ]; then
        echo "Adding $file to combined documentation..."
        echo "## $(basename "$file" .md | tr '-' ' ' | tr '_' ' ' | sed 's/\b\(.\)/\u\1/g')" >> combined_docs.md
        echo "" >> combined_docs.md
        cat "$file" >> combined_docs.md
        echo "" >> combined_docs.md
        echo "\\newpage" >> combined_docs.md
        echo "" >> combined_docs.md
    fi
done

# Convert to PDF with nice formatting
pandoc combined_docs.md -o bank_integration_complete_docs.pdf \
    --pdf-engine=wkhtmltopdf \
    --toc \
    --toc-depth=3 \
    --variable geometry:margin=1in \
    --variable fontsize=11pt \
    --variable colorlinks=true \
    --variable linkcolor=blue \
    --variable urlcolor=blue \
    --variable toccolor=black \
    --metadata title="Bank Integration - Complete Documentation" \
    --metadata author="Akhilam Inc" \
    --metadata date="$(date +'%B %d, %Y')"

# Clean up temporary file
rm combined_docs.md

echo "PDF created: bank_integration_complete_docs.pdf"
