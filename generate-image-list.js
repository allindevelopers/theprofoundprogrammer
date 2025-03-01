#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Directory containing the images
const imagesDir = path.join(__dirname, 'downloaded_images');
// Output file path
const outputFile = path.join(__dirname, 'image-list.js');

// Function to generate the image list
function generateImageList() {
  try {
    // Check if the directory exists
    if (!fs.existsSync(imagesDir)) {
      console.error(`Directory not found: ${imagesDir}`);
      process.exit(1);
    }

    // Read all files in the directory
    const files = fs.readdirSync(imagesDir);
    
    // Filter for JPEG files
    const jpegFiles = files.filter(file => 
      file.toLowerCase().endsWith('.jpg') || 
      file.toLowerCase().endsWith('.jpeg')
    );

    // Create the image list
    const imageList = jpegFiles.map(jpegFile => {
      // Get the base name without extension
      const baseName = path.parse(jpegFile).name;
      
      // Check if corresponding .txt file exists
      const txtFile = `${baseName}.txt`;
      const txtPath = path.join(imagesDir, txtFile);
      
      // Only include entries where both JPEG and TXT files exist
      if (fs.existsSync(txtPath)) {
        return {
          image: `downloaded_images/${jpegFile}`,
          description: `downloaded_images/${txtFile}`
        };
      }
      return null;
    }).filter(item => item !== null);

    // Create the JavaScript content
    const jsContent = `const imageList = ${JSON.stringify(imageList, null, 2)};\n`;

    // Write the JavaScript file
    fs.writeFileSync(outputFile, jsContent);
    
    console.log(`Successfully generated ${outputFile} with ${imageList.length} images`);
  } catch (error) {
    console.error('Error generating image list:', error);
    process.exit(1);
  }
}

// Run the function
generateImageList();

