# CNC AI Quotation Generator

A professional CNC machining cost estimation platform that automatically generates quotations from CAD files. This application processes DXF files, extracts geometry information, calculates machining costs, and generates professional PDF quotations.

## 🚀 Features

### Core Functionality
- **DXF File Processing**: Upload and parse DXF files with precision
- **Geometry Extraction**: Automatically extract lines, arcs, circles, and polylines
- **Material Database**: Support for 6 common materials (steel, aluminum, plastic, wood, brass, copper)
- **Smart Cost Calculation**: AI-powered cost and time estimation
- **PDF Generation**: Professional quotation documents with company branding

### Technical Features
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Real-time Processing**: Instant quotation generation
- **Responsive UI**: Modern, mobile-friendly interface
- **File Validation**: Secure file upload with size and format restrictions
- **Error Handling**: Comprehensive error handling and user feedback

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd CAD
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
CAD/
├── app.py                 # Main Flask application
├── cad_processor.py      # DXF file processing and geometry extraction
├── cost_calculator.py    # Cost and time calculation logic
├── pdf_generator.py      # PDF quotation generation
├── templates/
│   └── index.html        # Main web interface
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── uploads/              # Temporary file upload directory
└── temp_pdfs/            # Generated PDF storage
```

## 🔧 Configuration

### Material Properties
The application includes predefined material properties in `cost_calculator.py`:

- **Feed Rates**: Material-specific cutting speeds (mm/min)
- **Material Costs**: Per-cubic-cm pricing
- **Machine Rates**: Hourly labor costs per material
- **Setup Times**: Standard setup and tool change times

### Company Information
Customize company details in `pdf_generator.py`:
- Company name and address
- Contact information
- Website and branding

## 📊 How It Works

### 1. File Upload
- User uploads a DXF file through the web interface
- File is validated for format and size (max 16MB)

### 2. Geometry Processing
- DXF file is parsed using the `ezdxf` library
- Geometry entities are extracted and measured:
  - Lines: Distance between start and end points
  - Arcs: Arc length based on radius and angle
  - Circles: Circumference calculation
  - Polylines: Sum of segment lengths

### 3. Cost Calculation
- **Cutting Time**: Based on total length and material-specific feed rate
- **Material Cost**: Calculated from cutting area and material density
- **Labor Cost**: Based on machining time and hourly rates
- **Total Cost**: Sum of all cost components

### 4. PDF Generation
- Professional quotation document with:
  - Company header and branding
  - Project details and specifications
  - Cost breakdown table
  - Terms and conditions

## 🎯 Usage

### Basic Workflow
1. **Upload DXF File**: Drag and drop or click to browse
2. **Select Material**: Choose from available material types
3. **Set Thickness**: Enter material thickness in millimeters
4. **Generate Quotation**: Click to process and calculate costs
5. **Download PDF**: Get your professional quotation document

### Supported File Formats
- **DXF**: AutoCAD Drawing Exchange Format
- **Maximum Size**: 16MB
- **Entity Types**: Lines, Arcs, Circles, Polylines

### Material Options
- **Steel**: High-strength, precision machining
- **Aluminum**: Lightweight, fast cutting
- **Plastic**: Versatile, cost-effective
- **Wood**: Natural material, easy machining
- **Brass**: Corrosion-resistant, decorative
- **Copper**: Excellent conductivity, soft material

## 🔍 Technical Details

### DXF Processing
- Uses `ezdxf` library for robust DXF parsing
- Supports multiple entity types and complex geometries
- Handles coordinate transformations and units

### Cost Algorithms
- **Feed Rate Calculation**: Material-specific cutting speeds
- **Time Estimation**: Includes setup, cutting, and tool change times
- **Cost Factors**: Material, labor, and overhead calculations

### PDF Generation
- Built with `ReportLab` for professional output
- Customizable templates and styling
- Automatic table generation and formatting

## 🚨 Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Corrupted DXF files
- Missing geometry data
- Calculation errors
- File size limitations

## 🔒 Security Features

- File type validation
- Size restrictions
- Secure file handling
- Temporary file cleanup
- Input sanitization

## 🧪 Testing

### Sample DXF Files
To test the application, you can use:
- Simple geometric shapes (rectangles, circles)
- Complex mechanical parts
- Multi-layer drawings
- Various entity combinations

### Validation
- Test with different material types
- Verify cost calculations
- Check PDF output quality
- Test error scenarios

## 🚀 Future Enhancements

### Planned Features
- **Advanced Nesting**: Optimize part placement on sheets
- **Toolpath Optimization**: Intelligent cutting path generation
- **Material Database**: Expand material properties
- **3D Support**: Handle 3D CAD files
- **API Integration**: RESTful API for external systems

### Performance Improvements
- **Caching**: Cache processed geometry data
- **Async Processing**: Background job processing
- **Database**: Persistent storage for quotations
- **Cloud Storage**: Secure file storage solutions

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include error handling
- Write unit tests for new features

## 📞 Support

### Common Issues
- **File Upload Errors**: Check file format and size
- **Calculation Issues**: Verify material and thickness inputs
- **PDF Generation**: Ensure ReportLab is properly installed

### Getting Help
- Check the error messages in the application
- Review the console output for debugging information
- Verify all dependencies are installed correctly

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **ezdxf**: DXF file processing library
- **ReportLab**: PDF generation capabilities
- **Flask**: Web framework
- **Bootstrap**: UI components and styling

---

**Built with ❤️ for the CNC manufacturing community**

*Precision CNC Solutions - Making manufacturing smarter, one quotation at a time.*
