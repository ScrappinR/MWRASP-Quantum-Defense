const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function convertHtmlToPdf(htmlFile, pdfFile) {
    let browser;
    try {
        console.log(`Converting ${htmlFile} to ${pdfFile}...`);
        
        browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        const page = await browser.newPage();
        
        // Load the HTML file
        const htmlPath = path.resolve(htmlFile);
        await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
        
        // Wait for any SVG content to load
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Generate PDF
        const pdfBuffer = await page.pdf({
            path: pdfFile,
            format: 'A4',
            landscape: true,
            printBackground: true,
            margin: {
                top: '10mm',
                right: '10mm',
                bottom: '10mm',
                left: '10mm'
            }
        });
        
        console.log(`✓ Successfully created ${pdfFile}`);
        return true;
        
    } catch (error) {
        console.error(`✗ Error converting ${htmlFile}:`, error.message);
        return false;
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

async function main() {
    const baseDir = 'C:\\Users\\User\\MWRASP-Quantum-Defense\\FILED_PROVISIONAL_PATENTS\\STRATEGIC_MOAT_PATENTS\\10_Temporal_Cryptographic_Key_Lifecycle';
    
    process.chdir(baseDir);
    
    const conversions = [
        ['FIGURE_1_SYSTEM_ARCHITECTURE.html', 'FIGURE_1_SYSTEM_ARCHITECTURE.pdf'],
        ['FIGURE_2_KEY_LIFECYCLE_PROCESS.html', 'FIGURE_2_KEY_LIFECYCLE_PROCESS.pdf'],
        ['FIGURE_3_TEMPORAL_SECURITY_CONTROLS.html', 'FIGURE_3_TEMPORAL_SECURITY_CONTROLS.pdf']
    ];
    
    console.log('Patent 10 SVG to PDF Converter (Node.js + Puppeteer)');
    console.log('='.repeat(60));
    
    let successCount = 0;
    const totalCount = conversions.length;
    
    for (const [htmlFile, pdfFile] of conversions) {
        if (!fs.existsSync(htmlFile)) {
            console.error(`✗ HTML file not found: ${htmlFile}`);
            continue;
        }
        
        if (await convertHtmlToPdf(htmlFile, pdfFile)) {
            successCount++;
        }
    }
    
    console.log('='.repeat(60));
    console.log(`Conversion Results: ${successCount}/${totalCount} successful`);
    
    if (successCount === totalCount) {
        console.log('✓ All SVG files successfully converted to PDF!');
        process.exit(0);
    } else {
        console.log(`✗ ${totalCount - successCount} conversions failed`);
        process.exit(1);
    }
}

main().catch(console.error);